import psycopg2
import csv
import shutil
import os
import io
import boto3
import gzip
from typing import Iterable, List, Any
from uuid import uuid4
from .queries import *

s3 = boto3.client("s3")

class RedshiftUpload(object):
    def __init__(self, connection_uri: str, s3_bucket: str, region: str):
        self.connection = psycopg2.connect(connection_uri)
        self.s3_bucket = s3_bucket
        self.region = region

    def upload(self, table_name: str, rows: Iterable[List[Any]], replace: bool, iam_role:
               str):
        table = RedshiftTable(self.connection, table_name)
        rows = self.filter_rows(table, rows, replace)
        key = self.upload_rows(table, rows)
        # note: important to delete existing BEFOREHAND
        if replace:
            table.drop_existing(rows)
        self.copy_rows(table, key, iam_role)
        self.connection.commit()

    def filter_rows(self, table, rows, replace):
        rows = table.unique(rows)
        if replace:
            return rows
        return table.non_existing(rows)

    def upload_rows(self, table, rows):
        upload_id = uuid4()
        output = io.StringIO()
        w = csv.writer(output, delimiter='|')
        w.writerows(rows)
        gzipped = gzip.compress(bytes(output.getvalue(), encoding='utf-8'))
        output.close()
        gz_filepath = f"{upload_id}.csv.gz"
        key= '/'.join(tuple([table.table_name, gz_filepath]))
        s3.put_object(Key=key, Bucket=self.s3_bucket, Body=gzipped)
        return key

    def copy_rows(self, table, key, iam_role):
        s3_path = '/'.join(tuple([self.s3_bucket, key]))
        path = f"s3://{s3_path}"
        cur = self.connection.cursor()
        cur.execute(copy_csv_data(table_name=table.table_name), dict(resource_path=path,
                                          iam_role=iam_role,
                                          region=self.region))


class RedshiftTable:
    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name
        self._primary_key = None
        self._primary_key_col_positions = None
        self._primary_key_col_names = None

    def primary_key_column_names(self):
        columns = self.primary_key_columns()
        names = map(lambda col: col[1], columns)
        return list(names)

    def primary_key_column_positions(self):
        columns = self.primary_key_columns()
        positions = map(lambda col: col[0], columns)
        return list(positions)

    def primary_key_columns(self):
        if not self._primary_key:
            self._primary_key = self.find_primary_key_column_info()
        return self._primary_key

    def find_primary_key_column_info(self):
        cur = self.connection.cursor()
        q = find_primary_key_column_info(self.table_name)
        cur.execute(q)
        rows = cur.fetchall()
        return rows

    def existing_primary_keys(self):
        cur = self.connection.cursor()
        cur.execute(find_distinct_column_permutations(self.table_name,
                                                      *self.primary_key_column_names()))
        rows = cur.fetchall()
        return rows

    def primary_key(self, row):
        key_columns = self.primary_key_column_positions()
        return tuple([row[i-1] for i in key_columns])

    def unique(self, rows: Iterable[List[Any]]):
        results = []
        keys = set([])
        for row in rows:
            key = self.primary_key(row)
            if key in keys:
                continue
            keys.add(key)
            results.append(row)
        return results


    def non_existing(self, rows: Iterable[List[Any]]):
        existing_keys = set(self.existing_primary_keys())
        if not len(existing_keys):
            return rows
        return list(filter(lambda row: self.primary_key(row) not in existing_keys,
                      rows))

    def existing_keys(self, rows: Iterable[List[Any]]):
        existing_keys = set(self.existing_primary_keys())
        keys = set(map(self.primary_key, rows))
        return list(filter(lambda key: key in existing_keys, keys))

    def drop_existing(self, rows: Iterable[List[Any]]):
        existing = self.existing_keys(rows)
        if not existing:
            return
        q = drop_primary_keys_in(self.table_name,
                                         self.primary_key_column_names(),
                                         existing)
        cur = self.connection.cursor()
        cur.execute(q)

