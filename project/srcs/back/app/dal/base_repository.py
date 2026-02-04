# from app.core.database import DB_instance as Database
from app.core.config import Config
from psycopg2 import sql
from typing import List, Dict, Any, Tuple, Optional
from contextlib import nullcontext

class BaseRepository:
    @classmethod
    def get_exec_cursor(cls, existing_cursor=None):
        if existing_cursor:
            return nullcontext(existing_cursor)
        return Config.DB_instence.get_cursor()

    @classmethod
    def get_exec_cursor_and_commit(cls, existing_cursor=None):
        if existing_cursor:
            return nullcontext(existing_cursor)
        return Config.DB_instence.get_cursor(commit=True)

    @classmethod
    def _fetch_one(cls, query: str, params=None, injected_cursor = None):
        with cls.get_exec_cursor(injected_cursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    @classmethod
    def _execute(cls, query: str, params=None, injected_cursor = None):
        with cls.get_exec_cursor_and_commit(injected_cursor) as cursor:
            cursor.execute(query, params)

            description = cursor.description
            values = cursor.fetchone()
            
            if not values :
                return None

            keys = [col[0] for col in description]


            return dict(zip(keys, values))

    @classmethod
    def _fetch_all(cls, query: str, params=None, injected_cursor = None):
        with cls.get_exec_cursor(injected_cursor) as cursor:
            cursor.execute(query, params)
            description = cursor.description
            keys = [col[0] for col in description]
            values = cursor.fetchall()
            data = []
            if not values :
                return None
            for value in values :
                data.append(dict(zip(keys, value))) 
                
            return data

    @classmethod
    def _fetch(cls, query: str, params=None, injected_cursor = None):
        with cls.get_exec_cursor(injected_cursor) as cursor:
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
        print(f"Starting ?", flush=True)
        
        if not isinstance(data, dict) or set(data.keys()) != set(columns):
            return None, None
        print(f"Starting ?S", flush=True)
        
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
        returning="id", injected_cursor = None) :
        print(f"table_name: {table_name},columns: {columns}", flush=True)
        query, _values = cls._build_insert_query(table_name=table_name, columns=columns, data=data)
        print(f"query: {query},_values: {_values}", flush=True)

        if returning :
            query += sql.SQL(" RETURNING {}").format(sql.Identifier(returning))

        with cls.get_exec_cursor_and_commit(injected_cursor) as cursor:
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
    def delete(cls, id, injected_cursor = None):
        query = sql.SQL("DELETE FROM {} WHERE id = %s RETURNING id").format(
            sql.Identifier(cls._table_name)
        )
        with cls.get_exec_cursor_and_commit(injected_cursor) as cursor:
            cursor.execute(query, (id,))
            return cursor.fetchone()
    
    
    @classmethod
    def find_by_something(cls, id, something="id", what="*", injected_cursor = None):
        if what == "*":
            what_sql = sql.SQL(what)
        else:
            what_sql = sql.Identifier(what)

        query = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
            what_sql,
            sql.Identifier(cls._table_name),
            sql.Identifier(something)
        )
        with cls.get_exec_cursor(injected_cursor) as cursor:
            cursor.execute(query, (id,))
            return cursor.fetchone()