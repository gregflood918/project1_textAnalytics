#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 09:53:06 2017

@author: gregflood918
"""

#
#Greg Flood
#CS 5970 Text Analytics
#
#Test that calls one of the insert text functions from Project1
#to ensure that the general insertion utility is working properly whe
#called through the collection specific insertion functions.  test_db.py
#tests the utility function specficially.  Since test_text_retrieval.py
#checks that all text retrieval functions have the expected dimensions, we
#can be sure that if the insert function works for one of the tests below,
#it will work for all.
#
#The collection specfiic insertion functions consist of 2 lines of code:
#a call to the collection retrieval function, and a call to the insertion 
#utility.  Validating all of these functions is unnecessarily redundant.
#

import sqlite3, os, sys

lib_path = os.path.abspath(os.path.join('..','project1'))
sys.path.append(lib_path)

import project1
from project1 import project1
import pytest
           
def test_claudius_insert():
#Test function that will call insertClaudius() from project1 and
#test that it has been properly inserted.  
    project1.insertClaudius()
    conn = sqlite3.connect('latintext.db')
    c = conn.cursor() 
    c.execute('''select * from latintext;''')
    j = c.fetchall()
    c.execute('''delete from latintext;''') #clean db for other tests
    conn.close()
    assert len(j) == 80
