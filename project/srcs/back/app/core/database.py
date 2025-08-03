from .config import Config
import psycopg2.pool
from flask import g, current_app
from contextlib import contextmanager


class Database:
    pool = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            2, 10,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME
        )
        # app.cli.command('init-db', self.init_db())
        app.before_request(self.before_request)
        app.teardown_appcontext(self.teardown_appcontext)
        with app.app_context():
            if not self.is_db_initialized():
                try:
                    self.init_db()
                except Exception as e:
                    app.logger.warning(f"Auto-init failed: {str(e)}")

    def is_db_initialized(self):
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users'
                )
            """)
            return cursor.fetchone()[0]
        finally:
            self.pool.putconn(conn)


    def before_request(self):
        if not hasattr(g, 'db_conn'):
            g.db_conn = self.pool.getconn()

    def teardown_appcontext(self, exception):
        conn = g.pop('db_conn', None)
        if conn is not None:
            self.pool.putconn(conn) 
    
    def init_db(self):
        conn = self.pool.getconn()
        try:
            with current_app.open_resource('core/schema.sql') as f:
                script = f.read().decode('utf-8')
                cursor = conn.cursor()
                cursor.execute(script)
                conn.commit()
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Database initialization failed: {str(e)}")
            raise
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def get_cursor(self, commit: bool = False) :
        conn = None
        cursor = None
        try:

            if hasattr(g, 'db_conn'):
                conn = g.db_conn
            else:
                conn = self.pool.getconn()
            
            cursor = conn.cursor()
            yield cursor
            
            if commit:
                conn.commit()

        except Exception as e:
            current_app.logger.error(f"Unexpected error: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and not hasattr(g, 'db_conn'):
                self.pool.putconn(conn)

    # @app.cli.command('init-db')
    # def init_db_command(self):
    #     """Initialize the database from schema.sql"""
    #     try:
    #         db.init_db()
    #         click.echo("Database initialized successfully!")
    #     except Exception as e:
    #         click.echo(f"Error initializing database: {str(e)}")
