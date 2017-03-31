#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Greg Flood
#CS 5970 Text Analytics
#
#Test Code for Project 1 functions that retrieve text.
#Each of the 8 collections will be retrieved via the 8
#test functions below.  The length of the retrieved file
#will be tested to ensure that its lenght matches the
#known length of the collection.  Additionally, each
#element of the returned text (which is returned as a 
#list of lists) will be tested to ensure that its length
#is exactly 9.   This obviates the need to test that 
#the insertion functions work for each text, as we can
#be certain that the functions will insert properly if
#they all have length 9, or put differently, have the
#correct number of data attributes relative to the database.
#

import os, sys
import sqlite3
lib_path = os.path.abspath(os.path.join('..','project1'))
sys.path.append(lib_path)

import project1
from project1 import project1
import pytest

def test_claudius():
#Function to test project1.fetchClaudius().  The speeches
#of Claudius is known to have 80 entries.  Thus, the length
#of the retreived text should be 80. Also, since the database
#that text will be inserted into has 9 data fields, the length
# of each of the 80 entries should be 9.
    data = project1.fetchClaudius()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 80 and flag


def test_creeds():
#Function to test project1.fetchCreeds().  The Christian
#creeds have 69 entries based on separation scheme.  Thus, the length
#of the retreived text should be 69. Also, since the database
#that text will be inserted into has 9 data fields, the length
# of each of the 69 entries should be 9.
    data = project1.fetchCreeds()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 69 and flag
    

def test_epitaphs():
#Function to test project1.fetchEpitaphs().  The Roman
#epitaphs have 225 entries based on separtion scheme. Thus,
#the length of the retrieved test should be 225.  Also, since
#the database that text will be inserted into has 9 data fields,
#the length of each of the 225 entries should be 9.
    data = project1.fetchEpitaphs()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 225 and flag
    
    
def test_anselm():
#Function to test project1.fetchAnselm().  The writings of
#Anselm have 96 entries based on the separtion scheme. Thus,
#the length of the retrieved test should be 96.  Also, since
#the database that text will be inserted into has 9 data fields,
#the length of each of the 96 entries should be 9.
    data = project1.fetchAnselm()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 96 and flag
    
    
def test_severus():
#Function to test project1.fetchSeverus().  The writings of
#Sulpicius Severus have 885 entries based on the separtion scheme. Thus,
#the length of the retrieved test should be 885.  Also, since
#the database that text will be inserted into has 9 data fields,
#the length of each of the 885 entries should be 9.
    data = project1.fetchSeverus()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 885 and flag
    

def test_bernard():
#Function to test project1.fetchBernard().  The writings of
#Bernard have 39 entries based on the separtion scheme. Thus,
#the length of the retrieved test should be 39.  Also, since
#the database that text will be inserted into has 9 data fields,
#the length of each of the 39 entries should be 9.
    data = project1.fetchBernard()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 39 and flag
    
    
def test_diesIrae():
#Function to test project1.fetchDiesIrae().  Dies Irae
#has 57 entries based on the separtion scheme. Thus,
#the length of the retrieved test should be 57.  Also, since
#the database that text will be inserted into has 9 data fields,
#the length of each of the 57 entries should be 9.
    data = project1.fetchDiesIrae()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 57 and flag
    
    
def test_gregory():
#Function to test project1.fetchGregory().  The writings of
#Gregory IX have 4581 entries based on the separtion scheme. Thus,
#the length of the retrieved test should be 4581.  Also, since
#the database that text will be inserted into has 9 data fields,
#the length of each of the 4581 entries should be 9.
    data = project1.fetchGregory()
    textLength = len(data)
    flag = True
    for text in data:
        if len(text) != 9:
            flag = False
    assert textLength == 4581 and flag


