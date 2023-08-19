from abc import ABC, abstractmethod
import multiprocessing
import time
import logging
from pathlib import Path
from typing import Tuple

from usaspending_api.common.csv_helpers import count_rows_in_delimited_file
from usaspending_api.common.helpers.sql_helpers import read_sql_file_to_text
from usaspending_api.download.filestreaming.download_generation import (
    EXCEL_ROW_LIMIT,
    split_and_zip_data_files,
    wait_for_process,
    execute_psql,
    generate_export_query_temp_file,
)
from usaspending_api.download.lookups import FILE_FORMATS
from usaspending_api.download.filestreaming.download_generation import generate_export_query_temp_file
from pyspark.sql import SparkSession
from usaspending_api.common.etl.spark import hadoop_copy_merge, load_csv_file
from usaspending_api.common.helpers.spark_helpers import configure_spark_session, get_active_spark_session


class AbstractToCSVStrategy(ABC):
    """A composable class that can be used according to the Strategy software design pattern.
    The Covid-19 "to csv" strategy establishes the interface for a suite of download
    algorithms; which take data from a source and outputs the result set to a csv.
    Implement this abstract class by taking specific algorithms which pull data from a source,
    and outputs to a csv, and bundle them into separate classes called strategies which
    inherit from this base class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_format = "csv"

    @abstractmethod
    def download_to_csv(
        self,
        source_sql: str,
        destination_path: Path,
        destination_file_name: str,
        working_dir_path: Path,
        covid_profile_download_zip_path: Path,
    ) -> Tuple[str, int]:
        """
        Args:
            source_sql: Some string that can be used as the source sql
            destination_path: The absolute destination path of the generated data files as a string
            working_dir_path: The working directory path as a string
            covid_profile_download_zip_path: The path (as a string) to the covid profile download zip file
        """
        pass


class AuroraToCSVStrategy(AbstractToCSVStrategy):
    def __init__(self, logger: logging.Logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logger

    def download_to_csv(
        self, source_sql, destination_path, destination_file_name, working_dir_path, covid_profile_download_zip_path
    ):
        source_sql = Path(source_sql)
        start_time = time.perf_counter()
        self._logger.info(f"Downloading data to {destination_path}")
        temp_data_file_name = destination_path.parent / (destination_path.name + "_temp")
        options = FILE_FORMATS[self.file_format]["options"]
        export_query = r"\COPY ({}) TO STDOUT {}".format(read_sql_file_to_text(source_sql), options)
        try:
            temp_file, temp_file_path = generate_export_query_temp_file(export_query, None, working_dir_path)
            # Create a separate process to run the PSQL command; wait
            psql_process = multiprocessing.Process(
                target=execute_psql, args=(temp_file_path, temp_data_file_name, None)
            )
            psql_process.start()
            wait_for_process(psql_process, start_time, None)

            delim = FILE_FORMATS[self.file_format]["delimiter"]

            # Log how many rows we have
            self._logger.info(f"Counting rows in delimited text file {temp_data_file_name}")
            try:
                count = count_rows_in_delimited_file(filename=temp_data_file_name, has_header=True, delimiter=delim)
                self._logger.info(f"{destination_path} contains {count:,} rows of data")
            except Exception:
                self._logger.exception("Unable to obtain delimited text file line count")

            start_time = time.perf_counter()
            zip_process = multiprocessing.Process(
                target=split_and_zip_data_files,
                args=(
                    str(covid_profile_download_zip_path),
                    temp_data_file_name,
                    str(destination_path),
                    self.file_format,
                    None,
                ),
            )
            zip_process.start()
            wait_for_process(zip_process, start_time, None)
        except Exception as e:
            raise e
        finally:
            Path(temp_file_path).unlink()
        return destination_path, count


class DatabricksToCSVStrategy(AbstractToCSVStrategy):
    def __init__(self, logger: logging.Logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logger

    def download_to_csv(
        self, source_sql, destination_path, destination_file_name, working_dir_path, covid_profile_download_zip_path
    ):
        self.spark = None
        destination_path = f"s3a://dti-usaspending-bulk-download-qat/csv_downloads/{destination_file_name}"
        try:
            extra_conf = {
                # Config for Delta Lake tables and SQL. Need these to keep Dela table metadata in the metastore
                "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
                # See comment below about old date and time values cannot be parsed without these
                "spark.sql.legacy.parquet.datetimeRebaseModeInWrite": "LEGACY",  # for dates at/before 1900
                "spark.sql.legacy.parquet.int96RebaseModeInWrite": "LEGACY",  # for timestamps at/before 1900
                "spark.sql.jsonGenerator.ignoreNullFields": "false",  # keep nulls in our json
            }
            self.spark = get_active_spark_session()
            self.spark_created_by_command = False
            if not self.spark:
                self.spark_created_by_command = True
                self.spark = configure_spark_session(**extra_conf, spark_context=self.spark)  # type: SparkSession
            df = self.spark.sql(source_sql)
            record_count = load_csv_file(self.spark, df, destination_path, logger=self._logger)
            # When combining these later, will prepend the extracted header to each resultant file.
            # The parts therefore must NOT have headers or the headers will show up in the data when combined.
            header = ",".join([_.name for _ in df.schema.fields])
            self._logger.info("Concatenating partitioned output files ...")
            hadoop_copy_merge(
                spark=self.spark,
                parts_dir=destination_path,
                zip_file_path=covid_profile_download_zip_path,
                header=header,
                overwrite=True,
                delete_parts_dir=False,
                rows_per_part=EXCEL_ROW_LIMIT,
                max_rows_per_merged_file=EXCEL_ROW_LIMIT,
                logger=self._logger,
            )
        except Exception:
            self._logger.exception("Exception encountered. See logs")
            raise
        finally:
            if self.spark_created_by_command:
                self.spark.stop()
        return f"{destination_path}.{self.file_format}", record_count
