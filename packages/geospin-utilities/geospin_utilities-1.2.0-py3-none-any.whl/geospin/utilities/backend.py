from urllib.parse import quote_plus as urlquote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DatabaseBackend(object):
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        strargs = ['user', 'password', 'host', 'database']
        for arg in strargs:
            if not isinstance(getattr(self, arg), str):
                raise TypeError("Parameter {} must be string-like.".format(arg))
        try:
            self.port = int(self.port)
        except (ValueError, TypeError):
            # Catch ValueError on inconvertible value
            # Catch TypeError on None
            raise TypeError("Parameter port must be int (or int-convertible).")

        fmt = 'postgres://{user:s}:{password:s}@{host:s}:{port:d}/{database:s}'
        self.conn_url = fmt.format(
            user=urlquote(self.user),
            password=urlquote(self.password),
            host=urlquote(self.host),
            port=self.port,
            database=urlquote(self.database)
        )
        self.engine = create_engine(
            self.conn_url,
            connect_args={
                'connect_timeout': 20,
                'keepalives': 1,
                'keepalives_idle': 20,
                'keepalives_interval': 30,
                'keepalives_count': 10,
            }
        )
        smaker = sessionmaker(bind=self.engine)
        self.session = scoped_session(smaker)

    def __enter__(self):
        return self.session()

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.session.remove()
