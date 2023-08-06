"""Populates model predictions for preprobed h3 hexagons."""

import ast
import csv
import itertools
import logging
import os
import re
import shutil
import time
from subprocess import Popen

import geojson
import pandas as pd
from sqlalchemy.dialects import postgresql

from geospin.utilities.h3 import PolyFiller
from geospin.utilities.misc import fetch_latest_zip_code_areas

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Populator:
    """This is the super class for Populators.

    Populators populate data to a database. The database can be dumped to allow
    distributing it to e.g. the Google cloud.

    :param geospin.utilites.backend.DatabaseBackend db_backend: The population
        will be done using this database backend.
    """

    def __init__(self, db_backend):
        self.db_backend = db_backend

    def dump_db(self, dump_filename):
        """
        Dumps the database into `.sql` file with gcloud compatible format.

        See the google cloud documentation for additional information:
        https://cloud.google.com/sql/docs/postgres/import-export/exporting?hl=de

        :param str dump_filename: Filename of the sql dump.
        """
        command = \
            f"pg_dump " \
            f"--format=plain " \
            f"--no-owner " \
            f"--no-acl " \
            f"{self.db_backend.conn_url} " \
            f"| sed -E " \
            f"'s/(DROP|CREATE|COMMENT ON) EXTENSION/-- \1 EXTENSION/g' " \
            f"> {dump_filename}"
        proc = Popen(command, shell=True)
        proc.wait()


class ZipCodePopulator(Populator):
    """Populates the latest zip code geometries.

    A table named 'zip_codes' will be written to the target database including
    the following columns:
    - 'zip_code' (str): A german zip code
    - 'wkt' (str): Well-Known-Text notation of the zip code area geometry.
    - 'geojson' (str): GeoJSON notation of the zip code area geometry.
    - 'hex_ids' ([str]): Array of hex IDs which intersect with the zip code
        area.

    :param bool reload: If True the zip code information will be fetched
        from file system otherwise from url.
    :param str zip_codes_filename: If reload is 'True', the filename
        specifies the file to load. If reload is 'False' and zip_codes_filename
        is set, this is the output filename.
    """

    def __init__(self, reload_from_file=False, zip_codes_filename=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.reload_from_file = reload_from_file
        self.zip_codes_filename = zip_codes_filename

    def execute(self):
        """Executes the ZipCode population.

        Fetches zip code area information from URL or file system depending on
        'self.reload_from_file'. The result is written to the table 'zip_codes'
        in the Populator database.
        """
        if self.reload_from_file:
            zip_codes_df = self._fetch_zip_codes_from_file()
        else:
            zip_codes_df = self._fetch_zip_codes_from_url()

        zip_codes_df.to_sql(
            'zip_codes',
            self.db_backend.engine,
            if_exists='replace',
            dtype={
                'hex_ids': postgresql.ARRAY(postgresql.TEXT),
                'zip_code': postgresql.TEXT
            },
            index=False
        )
        return zip_codes_df

    def _fetch_zip_codes_from_file(self):
        """ Get the zip codes and its polygons from file.

        For each zip code there will be the following information given:
            wkt (str): The zip code area geometry given as WKT
            geojson (str): A geojson representation of the geometry.
            hex_ids ([str]): A list of all hex_ids within the zip code area.

        :return pandas.DataFrame zip_codes_df: A dataframe containing the
            columns zip_code, wkt, geojson and hex_ids.
        """
        zip_codes_df = pd.read_csv(
            self.zip_codes_filename,
            dtype={'zip_code': object},
            converters={"hex_ids": ast.literal_eval})

        return zip_codes_df

    def _fetch_zip_codes_from_url(self):
        """ Get the zip codes and its polygons from url.

        For each zip code there will be the following information given:
            wkt (str): The zip code area geometry given as WKT
            geojson (str): A geojson representation of the geometry.
            hex_ids ([str]): A list of all hex_ids within the zip code area.
        If `self.zip_codes_filename` is set, the result will be additionally
        written as csv to the file.

        :return pandas.DataFrame zip_codes_df: A dataframe containing the
            columns zip_code, wkt, geojson and hex_ids.
        """
        zip_codes_df = fetch_latest_zip_code_areas()
        zip_codes_df['geojson'] = zip_codes_df['wkt'].apply(
            lambda wkt: str(geojson.Feature(geometry=wkt)))

        zip_codes_df['wkt'] = zip_codes_df['wkt'].apply(
            lambda geom: geom.wkt)

        poly_filler = PolyFiller(resolution=9, add_hex_id_if='intersected')
        zip_codes_df['hex_ids'] = zip_codes_df['wkt'].apply(
            lambda x: poly_filler.fill(x))
        zip_codes_df = pd.DataFrame(zip_codes_df)

        if self.zip_codes_filename is not None:
            zip_codes_df.to_csv(self.zip_codes_filename, index=False)

        return zip_codes_df


class PredictionPopulator(Populator):
    """Populates model predictions.

    A model pickle is loaded from the file system as well as preprobed data from
    the probe database. The model is then applied to each location in the probe
    database. The result is populated in a table named 'predictions' in the
    target database.

    Examples:
    Example for a scikit-learn model:
    >>> model = joblib.load(model_filename)
    >>> prediction_populator = PredictionPopulator(model.predict,
    >>>         db_backend=db_backend,
    >>>         probe_db_backend=probe_db_backend)
    >>> prediction_populator.execute_in_chunks()

    Example for a scikit-learn model predicting probabilities:
    >>> model = joblib.load(model_filename)
    >>> predict_proba = lambda features: model.predict_proba(features)[:, 1]
    >>> prediction_populator = PredictionPopulator(predict_proba,
    >>>         db_backend=db_backend,
    >>>         probe_db_backend=probe_db_backend)
    >>> prediction_populator.execute_in_chunks()

    Example for random numbers:
    >>> import random
    >>> predict_random = lambda features: random.random()
    >>> prediction_populator = PredictionPopulator(predict_random,
    >>>         db_backend=db_backend,
    >>>         probe_db_backend=probe_db_backend)
    >>> prediction_populator.execute_in_chunks()

    :param function predict_function: Function pointer to the predict function.
        This function must accept expect one argument `features`, which will be
        a pandas.DataFrame.
    :param geospin.utilities.backend.DatabaseBackend probe_db_backend: The probe
        features will be fetch from this backend. There needs to be a column
        `hex_id` contained in the
    :param probe_db_table: Table name in the probe database where the
        features are fetched from.
    """

    def __init__(self, predict_function, probe_db_backend,
                 probe_db_table='germany_probed_hexagon_resolution_9',
                 **kwargs):
        super().__init__(**kwargs)
        self.temp_folder = 'temp_populator'
        self.probe_db_table_name = probe_db_table
        self.probe_db_backend = probe_db_backend

        self.predict_function = predict_function

    def _get_column_names(self):
        """Get the column names of the probe database."""
        sql_query = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{self.probe_db_table_name}';
        """

        with self.probe_db_backend.engine.connect() as conn:
            result = conn.execute(sql_query)
        column_names = [row[0] for row in result]

        return column_names

    def _get_prediction_for_chunk(self, chunk, col_names):
        """Apply the model to the chunk."""
        df = pd.DataFrame(chunk, columns=col_names)
        hex_ids = df["hex_id"]
        features = df.drop(["hex_id"], axis=1)

        prediction = self.predict_function(features)

        return pd.Series(index=hex_ids,
                         data=prediction,
                         name='prediction')

    def _get_chunk_filenames(self):
        """Returns the list of chunk filenames found in the temp folder.

        :return list(str) chunk_filenames: List of chunk filenames found.
        """
        filenames = os.listdir(self.temp_folder)
        chunk_filenames = [f for f in filenames if
                           re.search(r'^chunk_\d{4}.csv$', f)]
        return chunk_filenames

    def _to_sql(self):
        """Read all the chunks from file system and write to target database."""
        logger.info('Populate to target database.')
        files = self._get_chunk_filenames()
        files = sorted(files)
        logger.info(f'\t --- Found #{len(files)} chunks. ---')
        # Replace existing predictions table
        replace = True
        start_time = time.time()
        for filename in files:
            predictions = pd.read_csv(os.path.join(self.temp_folder, filename))
            predictions.to_sql(
                'predictions',
                self.db_backend.engine,
                if_exists='replace' if replace else 'append',
                index=False
            )
            replace = False
        duration = (time.time() - start_time)
        logger.info(f"\t --- Populated in {duration} seconds ---")

    @staticmethod
    def _chunk_filename_to_idx(filename):
        """Return the index of a chunk filename.

        :param str filename: Chunk filename with specified format.
        :return int idx: Chunk index.
        """
        groups = re.search(r'^chunk_(\d{4}).csv$', filename)
        if groups:
            return int(groups.group(1))
        else:
            raise ValueError(f'Filename {filename} has wrong format.')

    def _get_sorted_chunk_idxs(self):
        """Check for existing chunks in the temp folder and return the sorted
        found indexes.

        :return list(int): List of chunk indexes.
        """
        filenames = self._get_chunk_filenames()
        idxs = [self._chunk_filename_to_idx(f) for f in filenames]

        return sorted(idxs)

    def _get_last_hex_id(self):
        """Returns the HEX ID of the last row in the last chunk file found.

        :return str: HEX ID of the last row.
        """
        filenames = os.listdir(self.temp_folder)

        last_chunk_filename = os.path.join(self.temp_folder, max(filenames))
        with open(last_chunk_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pass
        return row['hex_id']

    @staticmethod
    def _is_integer_list_continuous_from_zero(list_):
        if not list_:
            return False
        return list_ == list(range(0, max(list_) + 1))

    def _contains_only_chunk_files(self):
        """Checks if the temp folder contains only chunk files.

        :return bool: If True, there are only chunk files.
        """
        found_files = os.listdir(self.temp_folder)
        found_chunk_files = self._get_chunk_filenames()

        return sorted(found_files) == sorted(found_chunk_files)

    def _get_probe_query_statement(self, chunk_size, last_hex_id=False):
        """Returns a SQL query statement.

        Depending on existing chunks there will be a WHERE statement to leave
        already fetched HEX IDs out.

        :param int chunk_size: Size of each chunk in rows.
        :param bool,str last_hex_id: Last found HEX ID in the temporary folder.
        :return str query_statement: Query statement to fetch probed features.
        """
        if last_hex_id:
            query_statement = f"SELECT * " \
                              f"FROM {self.probe_db_table_name} " \
                              f"WHERE hex_id > '{last_hex_id}' " \
                              f"ORDER BY hex_id ASC"
        else:
            query_statement = f'SELECT * ' \
                              f'FROM {self.probe_db_table_name} ' \
                              f'ORDER BY hex_id ASC'

        return query_statement

    def _safe_make_temp_folder(self):
        """Makes a temp folder to store intermediate predictions.

        If there is already a temporary folder, do not overwrite but try
        to resume. The last successfully written HEX ID will be returned.

        :return tuple (last_hex_id, chunk_offset)
            WHERE
            str, bool last_hex_id: False if no temporal folder found,
                otherwise the last HEX ID found.
            int last_chunk_id: -1 if no chunk was found, else the id.
        """
        # Try to create a temp folder
        try:
            # If there is no temp folder yet, create one and start with the
            # first chunk.
            last_hex_id = False
            last_chunk_id = -1
            os.makedirs(self.temp_folder, exist_ok=False)
        except FileExistsError:
            # If the temp folder still exists, the population was interrupted.
            # Check the previous progress and resume the population.
            # Check the integrity of the temporal folder.
            self._check_integrity_of_temp_folder()

            last_chunk_id = max(self._get_sorted_chunk_idxs())
            last_hex_id = self._get_last_hex_id()
            logger.info(f'Found #{last_chunk_id + 1} chunks. Continue with HEX '
                        f'IDs greater than {last_hex_id}.')
        return last_hex_id, last_chunk_id

    def _check_integrity_of_temp_folder(self):
        """Raises an error if the integrity is violated."""
        idxs = self._get_sorted_chunk_idxs()
        if not self._is_integer_list_continuous_from_zero(idxs):
            raise IOError(f'Found temporal folder {self.temp_folder} '
                          f'with missing chunks. Delete the folder '
                          f'manually.')

        if not self._contains_only_chunk_files():
            raise IOError(f'Found temporal folder {self.temp_folder} '
                          f'with unexpected content. Delete the folder '
                          f'manually.')

    def _process_chunk(self, chunk, chunk_idx, column_names):
        """Does the processing of the chunk.

        A prediction will be made of each chunk element, which will then be
        saved to the file system.
        :param list(tuple) chunk: A chunk of probed features.
        :param int chunk_idx: The index of the chunk.
        :param list(str) column_names: The column names of the probe features.
        """
        predictions_df = self._get_prediction_for_chunk(chunk, column_names)
        out_path = os.path.join(self.temp_folder, f'chunk_{chunk_idx:04}.csv')
        predictions_df.to_csv(out_path, header=True)

    def execute_in_chunks(self, chunk_size=10000):
        """Execute the population of prediction to the target database.

        The probed data is processed in chunks of size 'chunk_size'. Preliminary
        results will be cached in the temp folder. If the execution is
        interrupted (e.g. by a network connection interruption), the execution
        will be resumed after restart.
        After a successful procession of all chunks, the results will be written
        to the target database.

        :param int chunk_size: Number of rows which will be evaluated at once.
        """
        # Make a temp folder for the temporal storage of the prediction chunks
        last_hex_id, last_chunk_id = self._safe_make_temp_folder()
        query_statement = self._get_probe_query_statement(chunk_size,
                                                          last_hex_id)
        column_names = self._get_column_names()

        with self.probe_db_backend.engine.connect() as connection:
            logger.info(f'Start streamed query: {query_statement} and predict '
                        f'in chunks.')
            start_time = time.time()

            query_stream = connection.execution_options(
                stream_results=True
            ).execute(query_statement)

            duration = (time.time() - start_time)
            logger.info(f"\t --- Query in {duration} seconds ---")

            start_time = time.time()
            for n, features_chunk in enumerate(self._chunk_iter(
                    chunk_size, query_stream), 1):
                chunk_idx = last_chunk_id + n
                self._process_chunk(features_chunk,
                                    chunk_idx=chunk_idx,
                                    column_names=column_names)

                duration = (time.time() - start_time)
                logger.info(
                    f"\t --- Chunk {chunk_idx} in {duration:.4f} sec ---")
                start_time = time.time()

        self._to_sql()
        logger.info(f'Remove temp folder {self.temp_folder}.')
        shutil.rmtree(self.temp_folder)

    @staticmethod
    def _chunk_iter(n, iterable):
        it = iter(iterable)
        while True:
            chunk = list(itertools.islice(it, n))
            if not chunk:
                return
            yield chunk
