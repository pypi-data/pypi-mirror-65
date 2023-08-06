from psycopg2.sql import SQL, Identifier, Literal

FIND_PRIMARY_KEY_COLUMNS = SQL("SELECT kcu.ordinal_position column_position, \
                               kcu.column_name column_name FROM \
information_schema.table_constraints tco \
JOIN information_schema.key_column_usage kcu ON kcu.constraint_name =\
tco.constraint_name \
WHERE constraint_type = 'PRIMARY KEY' AND tco.table_name = {table_name} \
ORDER BY column_position;")

FIND_DISTINCT_PRIMARY_KEYS = SQL("SELECT DISTINCT {columns} FROM {table_name};")


COPY_CSV_DATA = SQL("COPY {table_name} \
                    FROM %(resource_path)s \
                    IAM_ROLE %(iam_role)s \
                    FORMAT csv \
                    DELIMITER '|'\
                    REGION %(region)s \
                    GZIP;")

def find_primary_key_column_info(table_name):
    return FIND_PRIMARY_KEY_COLUMNS.format(table_name=Literal(table_name))

def find_distinct_column_permutations(table_name, *columns):
    column_identifiers = map(Identifier, columns)
    column_clause = SQL(', ').join(column_identifiers)
    return FIND_DISTINCT_PRIMARY_KEYS.format(columns=column_clause,
                                             table_name=Identifier(table_name))

def copy_csv_data(table_name):
    return COPY_CSV_DATA.format(table_name=Identifier(table_name))

def _build_equals(column, value):
    return SQL('{column} = {value}').format(column=Identifier(column),
                                            value=Literal(value))

def _condition_builder(columns):
    def build_condition(key):
        conditions = map(_build_equals, columns, key)
        compound_condition = SQL(' AND ').join(conditions)
        return SQL('({})').format(compound_condition)
    return build_condition

def drop_primary_keys_in(table_name, columns, keys):
    if len(columns) == 1:
        return SQL('DELETE FROM {} WHERE {} in \
                   {}').format(Identifier(table_name), Identifier(columns[0]),
                               Literal(tuple(map(lambda k: k[0], keys))))
    clauses = map(_condition_builder(columns), keys)
    compound = SQL(' OR ').join(clauses)
    return SQL('DELETE FROM {} WHERE {}').format(Identifier(table_name), compound)
