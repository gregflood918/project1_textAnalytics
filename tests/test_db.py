#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Greg Flood
#CS 5970 Text Analytics
#
#Test that constructs a database that will be used in project 1
#and tests it's existence by in querying that the desired table
#titled "latintext" has been created.  Additionally, an arbitrary
#insertion is performed via the project1.populatedDB() utility
#function.  This is a general utility function that is called to
#insert each collection into the database.  It accepts a list of lists.
#
#Note that the pytest fixture has a session wide scope, meaning that
#the database created in the fixture will persist through the test,
#with the code after the yield occurring upon test completion.
#

import sqlite3, os, sys

lib_path = os.path.abspath(os.path.join('..','project1'))
sys.path.append(lib_path)

import project1
from project1 import project1
import pytest


@pytest.fixture(scope="session")
def provide_db():
#pytest fixture that creates creates a latintext database by executing
#the createDB() commmand from project1.py.  This fixture simplifies
#cleanup by setting the scope of the fixture to "session."  This will
#cause the created database to persist through testing.  After completion
#of tests, the code under the yield statement will execute, which removes
#the created database from memory.
    project1.createDB()
    yield
    os.system("rm latintext.db")


def test_DB(provide_db):
#Test that queries database for tables named 'latintext'.  If the result set
#is not null, then the database has been successfully created.
    conn = sqlite3.connect('latintext.db')
    c = conn.cursor()
    c.execute('''select count(*) from sqlite_master where type="table" and name="latintext";''')
    j = c.fetchone()[0]!=0 #This is where the test occurs
    conn.close()
    assert j


def test_populate_db(provide_db):
#Function that tests project1.populateDB().  This is the bulk insertion
#utility function that is called by each of the 8 collection specific 
#insertion function.  It is tested by creating an arbitrary list for
#insertion and then inserting into the database via function call.  The
#test will be that the inserted record has a length of 9
    arbitrary_list = [[1,2,3,4,5,6,7,8,9]]
    project1.populateDB(arbitrary_list)
    conn = sqlite3.connect('latintext.db')
    c = conn.cursor()
    c.execute('''select * from latintext''')
    query_result = c.fetchone()
    c.execute('''delete  from latintext;''') #Clean db for other tests
    conn.commit()
    conn.close()
    assert len(query_result)==9


