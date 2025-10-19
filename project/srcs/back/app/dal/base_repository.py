# from app.core.database import DB_instance as Database
from app.core.config import Config
from psycopg2 import sql
from typing import List, Dict, Any, Tuple, Optional

class BaseRepository:
    @classmethod
    def _fetch_one(cls, query: str, params=None):
        with Config.DB_instence.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    @classmethod
    def _execute(cls, query: str, params=None):
        with Config.DB_instence.get_cursor(commit=True) as cursor:
            cursor.execute(query, params)

            keys = [col[0] for col in cursor.description]

            values = cursor.fetchone()
            if not values :
                return None

            return dict(zip(keys, values))

    @classmethod
    def _fetch(cls, query: str, params=None):
        with Config.DB_instence.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    @classmethod
    def _build_insert_query(
        cls,
        *,
        table_name: str,
        columns: List[str],
        data: Dict[str, Any],
    ) -> Tuple[Optional[sql.Composed], Optional[List[Any]]]:

        if not isinstance(data, dict) or set(data.keys()) != set(columns):

            print (data.keys(), set(columns), flush=True)
            print (set(data.keys()) != set(columns), flush=True)
            return None, None
        
        ordered_values = [data[col] for col in columns]
        
        columns_sql = sql.SQL(', ').join(map(sql.Identifier, columns))
        values_sql = sql.SQL(', ').join(sql.Placeholder() * len(columns))
        
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            columns_sql,
            values_sql
        )
        return query, ordered_values

    @classmethod
    def insert(
        cls,
        *,
        table_name: str,
        columns: List[str],
        data: Dict[str, Any],
        returning="id") :
        query, _values = cls._build_insert_query(table_name=table_name, columns=columns, data=data)
        print (query, flush=True)
        if returning :
            query += sql.SQL(" RETURNING {}").format(sql.Identifier(returning))

        with Config.DB_instence.get_cursor(commit=True) as cursor:
            cursor.execute(query, tuple(_values))
            return cursor.fetchone()[0] if returning else None

    @classmethod
    def find_by_id(cls, id, what: str = "*"):
        return cls.find_by_something(id=id, what=what)
        # query = sql.SQL("SELECT * FROM {} WHERE id = %s").format(
        #     sql.Identifier(cls._table_name)
        # )
        # return Config.DB_instence.execute(query, (id,), fetch_one=True)

    @classmethod
    def delete(cls, id):
        query = sql.SQL("DELETE FROM {} WHERE id = %s RETURNING id").format(
            sql.Identifier(cls._table_name)
        )
        with Config.DB_instence.get_cursor(commit=True) as cursor:
            cursor.execute(query, (id,))
            return cursor.fetchone()
    
    
    @classmethod
    def find_by_something(cls, id, something="id", what="*"):
        if what == "*":
            what_sql = sql.SQL(what)
        else:
            what_sql = sql.Identifier(what)

        query = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
            what_sql,
            sql.Identifier(cls._table_name),
            sql.Identifier(something)
        )
        with Config.DB_instence.get_cursor() as cursor:
            cursor.execute(query, (id,))
            return cursor.fetchone()