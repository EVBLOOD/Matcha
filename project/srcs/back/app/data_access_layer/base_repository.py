from core.database import Database
from psycopg2 import sql
from typing import List, Dict, Any, Tuple, Optional

class BaseRepository:
   
    @classmethod
    def _build_insert_query(
        cls,
        *,
        table_name: str,
        columns: List[str],
        data: Dict[str, Any],
    ) -> Tuple[Optional[sql.Composed], Optional[List[Any]]]:
        if not isinstance(data, dict) or set(data.keys()) != set(columns):
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
        query, _values = cls._build_insert_query(table_name=table_name, column=columns, data=data)
        if returning :
            query += sql.SQL(" RETURNING {}").format(sql.Identifier(returning))
        
        with Database.get_cursor(commit=True) as cursor:
            cursor.execute(query, tuple(_values))
            return cursor.fetchone()[0] if returning else None

    @classmethod
    def find_by_id(cls, id):
        query = sql.SQL("SELECT * FROM {} WHERE id = %s").format(
            sql.Identifier(cls._table_name)
        )
        return Database.execute(query, (id,), fetch_one=True)

    @classmethod
    def delete(cls, id):
        query = sql.SQL("DELETE FROM {} WHERE id = %s").format(
            sql.Identifier(cls._table_name)
        )
        return Database.execute(query, (id,))