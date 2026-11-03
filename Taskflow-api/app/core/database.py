"""
Conexión a la base de datos con SQLAlchemy.

- engine:        la conexión (y el pool de conexiones) con la BD.
- SessionLocal:  fábrica de sesiones. Una sesión = una "conversación" con la BD
                 donde se hacen consultas y se confirman (commit) los cambios.
- Base:          clase de la que heredan todos los modelos (declarative).
- get_db():      dependencia de FastAPI que da UNA sesión por petición y la
                 cierra siempre al terminar, aunque haya un error.
"""

from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import DATABASE_URL, DB_TIMEOUT, SQL_ECHO

IS_SQLITE = DATABASE_URL.startswith("sqlite")

# Opciones específicas de SQLite:
# - check_same_thread=False: FastAPI atiende las peticiones en varios hilos y
#   SQLite, por defecto, solo deja usar una conexión en el hilo que la creó.
#   Es seguro porque cada petición usa su propia sesión (get_db).
# - timeout: segundos que se espera si la BD está bloqueada por otra escritura,
#   en lugar de fallar al momento con "database is locked".
connect_args = {"check_same_thread": False, "timeout": DB_TIMEOUT} if IS_SQLITE else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=SQL_ECHO,
    # pool_pre_ping: antes de reutilizar una conexión del pool comprueba que
    # sigue viva (hace un "SELECT 1"). Evita errores cuando el servidor de BD
    # ha cerrado conexiones inactivas. En SQLite apenas cuesta nada y deja el
    # código listo para PostgreSQL/MySQL.
    pool_pre_ping=True,
    # Pooling: SQLAlchemy mantiene un pool de conexiones abiertas y las presta
    # a cada sesión, en vez de abrir y cerrar una conexión en cada petición
    # (que es lento). Con SQLite en archivo usa QueuePool por defecto; con
    # PostgreSQL se ajustaría con pool_size / max_overflow / pool_timeout.
)


if IS_SQLITE:
    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
        """SQLite NO comprueba las claves foráneas salvo que se active en cada conexión."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    # expire_on_commit=False: tras el commit, los objetos conservan sus valores
    # en memoria. Si fuera True (por defecto), al devolver el objeto en la
    # respuesta SQLAlchemy lanzaría otra consulta para recargarlo, o fallaría
    # si la sesión ya está cerrada.
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base declarativa: cada clase que hereda de aquí es una tabla."""


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI: abre una sesión para la petición y la cierra al final.

    Con `yield`, FastAPI ejecuta lo de antes del yield al empezar la petición,
    inyecta la sesión en el endpoint y, cuando termina la respuesta, ejecuta el
    `finally`. Si hay una excepción se hace rollback para no dejar cambios a medias.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Crea las tablas que no existan (de momento sin migraciones)."""
    from app import models  # noqa: F401 - registra los modelos en Base.metadata

    Base.metadata.create_all(bind=engine)
