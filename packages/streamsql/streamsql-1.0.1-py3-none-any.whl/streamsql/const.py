'''
API Paths
'''
DEFAULT_HOST = "https://streamsql.io"
RESOURCE_PATH = '/api/resource'
TRANSFORM_PATH = '/api/transform'
STATUS_PATH = TRANSFORM_PATH + '/status'
INGEST_SINGLE = '/api/send/single'
INGEST_BATCH = '/api/send/batch'
GET_TABLE = '/api/get'
SUBSCRIBE_PATH = '/api/transform/subscribe'

'''
APIKEY Header
'''
APIKEY_HEADER = 'X-StreamSQL-Admin-Key'

'''
Patterns
'''
RE_TABLE_NAME = '^[a-zA-Z0-9]+$'
RE_ALIAS_NAME = RE_TABLE_NAME
RE_RESOURCE_NAME = RE_TABLE_NAME
RE_TRANSFORM_NAME = RE_TABLE_NAME
RE_API_KEY = '([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})|([0-9a-zA-Z]{48})'

'''
TYPES
'''
SQL_TYPES = [
    "STRING",
    "BOOLEAN",
    "BYTE",
    "SHORT",
    "INT",
    "LONG",
    "FLOAT",
    "DOUBLE",
    "ROW",
    "DECIMAL",
    "SQL_DATE",
    "SQL_TIME",
    "SQL_TIMESTAMP"
]

class FieldTypes:
    String = "STRING"
    Bool = "BOOLEAN"
    Byte = "BYTE"
    Short = "SHORT"
    Int = "INT"
    Long = "LONG"
    Float = "FLOAT"
    Double = "DOUBLE"
    Row = "ROW"
    Decimal = "DECIMAL"
    Date = "SQL_DATE"
    Time = "SQL_TIME"
    TimeStamp = "SQL_TIMESTAMP"

'''
Resource Types
'''
STREAM_RESOURCE = 'STREAM_RESOURCE'
LOOKUP_RESOURCE = 'LOOKUP_RESOURCE'

RESOURCE_TYPES = [
    STREAM_RESOURCE,
    LOOKUP_RESOURCE
]

class ResourceTypes:
    Stream = STREAM_RESOURCE
    Lookup = LOOKUP_RESOURCE

'''
Ingestion Formats
'''
JSON = 'JSON'

FORMAT_TYPES = [
    JSON
]
