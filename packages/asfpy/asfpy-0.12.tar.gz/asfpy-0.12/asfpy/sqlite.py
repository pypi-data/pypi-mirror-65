#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
 #the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" SQLite document-store wrapper for ASF """
import sqlite3

class asfpyDBError(Exception):
    pass

class db:
    def __init__(self, fp):
        self.connector = sqlite3.connect(fp)
        self.connector.row_factory = sqlite3.Row
        self.cursor = self.connector.cursor()
        # Need sqlite 3.25.x or higher for upserts
        self.upserts_supported = True if sqlite3.sqlite_version >= "3.25.0" else False

    def run(self, cmd, *args):
        self.cursor.execute(cmd, args)

    def runc(self, cmd, *args):
        self.cursor.execute(cmd, args)
        self.connector.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def delete(self, table, **target):
        """ Delete a row where ..."""
        if not target:
            raise asfpyDBError("DELETE must have at least one defined target value for locating where to delete from")
        k, v = next(iter(target.items()))
        statement = f'''DELETE FROM {table} WHERE {k} = ?;'''
        values = [v]
        self.runc(statement, *values)

    def update(self, table, document, **target):
        """ Update a row where ..."""
        k, v = next(iter(target.items()))
        updates = ", ".join("%s = ?" % x for x in document.keys())
        statement = f'''UPDATE {table} SET {updates} WHERE {k} = ?;'''
        values = list(document.values())  # update values
        values.append(v)  # unique constraint
        self.runc(statement, *values)

    def insert(self, table, document):
        """ Standard insert, document -> sql """
        keys = list(document.keys())
        variables = ", ".join(keys)
        questionmarks = ", ".join('?' for x in keys)
        statement = f'''INSERT INTO {table} ({variables}) VALUES ({questionmarks});'''
        values = []
        values.extend(document.values())  # insert values
        self.runc(statement, *values)

    def upsert(self, table, document, **target):
        """ Performs an upsert in a table with unique constraints. Insert if not present, update otherwise. """
        # Always have the target identifier as part of the row
        if not target:
            raise asfpyDBError("UPSERTs must have at least one defined target value for locating where to upsert")
        k, v = next(iter(target.items()))
        document[k] = v

        # table: foo
        # bar: 1
        # baz: 2
        # INSERT INTO foo (bar,baz) VALUES (?,?) ON CONFLICT (bar) DO UPDATE SET (bar=?, foo=?) WHERE bar=?,(1,2,1,2,1,)
        if self.upserts_supported:
            keys = list(document.keys())
            variables = ", ".join(keys)
            questionmarks = ", ".join('?' for x in keys)
            upserts = ", ".join("%s = ?" % x for x in keys)

            statement = f'''INSERT INTO {table} ({variables}) VALUES ({questionmarks}) ON CONFLICT({k}) DO UPDATE SET {upserts} WHERE {k} = ?;'''
            values = []
            values.extend(document.values())  # insert values
            values.extend(document.values())  # update values
            values.append(v)  # unique constraint
            self.runc(statement, *values)
        # Older versions of sqlite do not support 'ON CONFLICT', so we'll have to work around that...
        else:
            try:  # Try to insert
                self.insert(table, document)
            except sqlite3.IntegrityError: # Conflict, update instead
                self.update(table, document, **target)

    def fetch(self, table, limit=1, **params):
        """ Searches a table for matching params, returns up to $limit items that match, as dicts. """
        search = ", ".join("%s = ?" % x for x in params.keys())
        if not params:
            search = "1"
        values = list(params.values())
        statement = f'''SELECT * FROM {table} WHERE {search}'''
        if limit:
            statement += f' LIMIT {limit}'
        self.cursor.execute(statement, values)
        a = 0
        rows_left = limit
        while rows_left != 0:
            row = self.cursor.fetchone()
            if not row:
                if a == 0:
                    yield None
                else:
                    return  # break iteration
                break
            doc = dict(row)
            yield doc
            rows_left -= 1
            a += 1
        return

    def fetchone(self, table, **params):
        return next(self.fetch(table, **params))

    def table_exists(self, table_name):
        """ Simple check to see if a table exists or not """
        self.run(f'''SELECT name FROM sqlite_master WHERE type='table' AND name="{table_name}"''')
        return self.fetchone() and True or False


def test():
    testdb = db('foo.db')
    cstatement = '''CREATE TABLE test (\
                foo        varchar unique, \
                bar   varchar, \
                baz   real \
            )'''

    # Create if not already here
    try:
        testdb.runc(cstatement)
    except sqlite3.OperationalError as e:  # Table exists
        assert (str(e) == "table test already exists")

    # Insert (may fail if already tested)
    try:
        testdb.insert('test', {'foo': 'foo1234', 'bar': 'blorgh', 'baz': 5})
    except sqlite3.IntegrityError as e:
        assert(str(e) == "UNIQUE constraint failed: test.foo")

    # This must fail
    try:
        testdb.insert('test', {'foo': 'foo1234', 'bar': 'blorgh', 'baz': 2})
    except sqlite3.IntegrityError as e:
        assert(str(e) == "UNIQUE constraint failed: test.foo")

    # This must pass
    testdb.upsert('test', {'foo': 'foo1234', 'bar': 'blorgssh', 'baz': 8}, foo='foo1234')

    # This should fail with no target specified
    try:
        testdb.upsert('test', {'foo': 'foo1234', 'bar': 'blorgssh', 'baz': 8})
    except asfpyDBError as e:
        assert(str(e) == "UPSERTs must have at least one defined target value for locating where to upsert")

    # This should all pass
    testdb.update('test', {'foo': 'foo4321'}, foo='foo1234')
    obj = testdb.fetchone('test', foo='foo4321')
    assert(type(obj) is dict and obj.get('foo') == 'foo4321')
    obj = testdb.fetch('test', limit=5, foo = 'foo4321')
    assert(str(type(obj)) == "<class 'generator'>")
    assert (next(obj).get('foo') == 'foo4321')
    obj = testdb.fetchone('test', foo='foo9999')
    assert(obj is None)
    testdb.delete('test', foo='foo4321')


if __name__ == '__main__':
    test()
