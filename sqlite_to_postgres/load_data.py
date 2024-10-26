import sqlite3
from dataclasses import astuple, fields

import psycopg2

from load_sqlite import SQLiteService
from transform_postgres import PostgresService
import settings

import logging

logging.basicConfig(level=logging.INFO)


def load_from_sqlite(sqlite_conn, pg_conn):
    mapping_table = settings.mapping_table
    for table, model in mapping_table.items():
        success = True
        try:
            data_generator = sqlite_service.get_data_from_table(
                sqlite_conn, table)
            for rows in data_generator:
                data_to_insert, column_names_str = reformat_data(model, rows)
                postgres_service.data_to_postgres(
                    pg_conn, table, column_names_str, data_to_insert
                )
        except (sqlite3.Error, psycopg2.DatabaseError) as e:
            logging.error(f"ошибка сбора или выгрузки данных {table}: {e}")
            success = False

        if success:
            logging.info(f"таблица: {table}, 🎉 Данные успешно перенесены!!!")


def reformat_data(model, data):
    try:
        data_from_db = [(model(**row)) for row in data]
        data_to_insert = [astuple(item) for item in data_from_db]
        column_names = [field.name for field in fields(data_from_db[0])]
        column_names_str = ", ".join(column_names)
        return data_to_insert, column_names_str
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    sqlite_service = SQLiteService()
    postgres_service = PostgresService()
    with sqlite_service.conn_context(
        settings.SQLITE_DB_PATH
    ) as sqlite_conn, postgres_service.conn_context(
        settings.POSTGRES_DB_DSN
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
