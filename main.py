#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Greg Flood
#CS 5970 - Text Analytics
#
#Main program that will fetch all collections, insert
#the collections into the database, and test the status
#of the database
#

import project1
from project1 import project1
def main():
    # create database
    project1.createDB()
    
    #insert each of the collections
    project1.insertClaudius()
    project1.insertCreeds()
    project1.insertEpitaphs()
    project1.insertDiesIrae()
    project1.insertAnselm()
    project1.insertSeverus()
    project1.insertBernard()
    project1.insertGregory()
    
    #Check the status of the database by printing its
    #length and drawing 5 rows randomly.
    project1.status()
    
if __name__ == '__main__':
    main()
