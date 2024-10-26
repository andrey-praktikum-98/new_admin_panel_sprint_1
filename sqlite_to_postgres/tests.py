import logging
from dataclasses import astuple
from load_sqlite import SQLiteService
from transform_postgres import PostgresService
import settings

logging.basicConfig(level=logging.INFO)


def compare_data(sqlite_conn, pg_conn):
    mapping_table = settings.mapping_table
    success = True
    for table, model in mapping_table.items():
        count_data_sqlite = sqlite_service.get_count_data(sqlite_conn, table)
        count_data_postgres = postgres_service.get_count_data(pg_conn, table)
        try:
            assert count_data_sqlite == count_data_postgres
        except AssertionError:
            logging.error(f"Количество строк не совпадает в таблице: {table}")
            success = False

        data_sqlite = get_data_sqlite(sqlite_conn, table, model)
        data_postgres = get_data_postgres(pg_conn, table, model)

        for sqlite_val, postgres_val in zip(data_sqlite, data_postgres):
            try:
                assert sqlite_val == postgres_val
            except AssertionError:
                logging.error(f"Данные не совпадают: {table}")
                success = False
    if success:
        logging.info("Таблицы совпадают")


def get_data_sqlite(sqlite_conn, table, model):
    sqlite_data = sqlite_service.get_data_from_table(sqlite_conn, table)
    for vals in sqlite_data:
        data_db = [model(**data).cut_date() for data in vals]
        yield reformat_data(data_db)


def get_data_postgres(pg_conn, table, model):
    postges_data = postgres_service.get_data_from_postgres(pg_conn, table)
    for vals in postges_data:
        data_db = [model(**data).post_init() for data in vals]
        yield reformat_data(data_db)


def reformat_data(data_from_db):
    sorted_data = sorted([astuple(item) for item in data_from_db])
    return sorted_data


if __name__ == "__main__":
    sqlite_service = SQLiteService()
    postgres_service = PostgresService()
    with sqlite_service.conn_context(
        settings.SQLITE_DB_PATH
    ) as sqlite_conn, postgres_service.conn_context(
        settings.POSTGRES_DB_DSN
    ) as pg_conn:
        compare_data(sqlite_conn, pg_conn)
