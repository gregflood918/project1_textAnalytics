#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#Greg Flood
#CS 5970 Text Analytics
#
#Test to ensure that the functionalities in phase2.py are working properly.
#This .py file consists of 2 tests, one to ensure that the api is functioning
#and returning the expected value and a second to ensure that the fts match
#query works properly. Since the latin and english searches in phase2.py rely
#on "MATCH" to find word matches in the passage, the fts functionalies of the
#latintext.db fts table must be validated
#

import sqlite3, os, sys
'''
lib_path = os.path.abspath(os.path.join('..',''))
sys.path.append(lib_path)

from phase2 import *
'''

lib_path = os.path.abspath(os.path.join('..','project1'))
sys.path.append(lib_path)

import project1
from project1 import phase2
import pytest


def test_translate_api():
#Uses translation API to test if it returns the approriate word.
    test_word = phase2.translateAPI('death')
    assert test_word == 'necro'
 

def test_fts_query():
#Test function that ensure the fts match  works properly.  This is
#used in the phase2 searchEnglish and searchLatin functions.
    conn = sqlite3.connect('latintext.db')
    c = conn.cursor()
    c.execute('''insert into latintext values (1,2,3,4,5,6,7,'necro',9);''')
    c.execute('''select passage from latintext where passage match 'necro';''')
    query_result = c.fetchone()[0]
    c.execute('''delete  from latintext;''')
    conn.close()
    assert query_result == 'necro'
