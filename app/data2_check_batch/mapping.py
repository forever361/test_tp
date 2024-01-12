from enum import Enum
import app.data2_check_batch.validator as v

class DbType(Enum):
    BIGINT = 'BIGINT'
    INT = 'INT'
    DECIMAL = 'DECIMAL'
    DOUBLE = 'DOUBLE'
    STRING = 'STRING'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    TIMESTAMP = 'TIMESTAMP'
    BINARY = 'BINARY'

COL_NAME_MAPPING = {'CVC2':'FIELD0',
                        'CVC2_NEW':'FIELD1',
                        'CVC2_PREV':'FIELD2',
                        'CVV':'FIELD3',
                        'CVV_NEW':'FIELD4',
                        'CVV_PREV':'FIELD5'}

DEFULT_ALI_TYPE_MAPPING = {'I1' : DbType('BIGINT'),
                    'I2' : DbType('BIGINT'),
                    'I' : DbType('INT'),
                    'I8' : DbType('BIGINT'),
                    'D' : DbType('DECIMAL'),
                    'N' : DbType('DECIMAL'),
                    'F' : DbType('DOUBLE'),
                    'CF' : DbType('STRING'),
                    'CV' : DbType('STRING'),
                    'DA' : DbType('DATE'),
                    'TZ' : DbType('DATETIME'),
                    'PT' : DbType('DATETIME'),
                    'TS' : DbType('TIMESTAMP'),
                    'SZ' : DbType('TIMESTAMP'),
                    'PM' : DbType('TIMESTAMP'),
                    'PS' : DbType('TIMESTAMP'),
                    'BF' : DbType('BINARY')}

OSS_ALI_TYPE_MAPPING = {'I1' : DbType('STRING'),
                    'I2' : DbType('STRING'),
                    'I' : DbType('STRING'),
                    'I8' : DbType('STRING'),
                    'D' : DbType('DECIMAL'),
                    'N' : DbType('DECIMAL'),
                    'F' : DbType('STRING'),
                    'CF' : DbType('STRING'),
                    'CV' : DbType('STRING'),
                    'DA' : DbType('STRING'),
                    'TZ' : DbType('STRING'),
                    'PT' : DbType('STRING'),
                    'TS' : DbType('STRING'),
                    'SZ' : DbType('STRING'),
                    'PM' : DbType('STRING'),
                    'PS' : DbType('STRING'),
                    'BF' : DbType('STRING')}

class OSS_DDL_TYPE(Enum):
    FIX = "FIX"
    DEFAULT = "DEFAULT"

class FileNature(Enum):
    MASTER = "MASTER"
    TRANSACTION = "TRANSACTION"
    ONE_BATCH = "ONE_BATCH"

VALIDATOR_MAPPING = {"AliValidator":v.AliValidator,
                    #  "TdValidator":v.TdValidator,
                     "OraValidator":v.OraValidator,
                     "PgValidator":v.OraValidator,
                      "FileValidator": v.FileValidator,
                     "AliValidator_batch":v.AliValidator_batch,
                     "FileValidator_batch":v.FileValidator_batch
                     }

class ValidateStatue(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"