from sqlalchemy import Integer
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement


class unix_timestamp(FunctionElement):
    type = Integer()
    inherit_cache = True


@compiles(unix_timestamp, "postgresql")
def pg_unix_timestamp(element, compiler, **kw):
    return "EXTRACT(EPOCH FROM NOW())::INTEGER"