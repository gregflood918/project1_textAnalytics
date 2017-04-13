#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Greg Flood
#CS 5970 - Text Analytics
#
#Main program that will fetch all collections, insert
#the collections into the database, and test the status
#of the database.  Following the database creation (or
#existence check), a command line search menu is provided
#to the user.  See README for full details
#

import project1
from project1 import project1
from project1 import phase2

def main():
    # create database
    project1.createDB()
    
    #Test to see if the database exists.  If it does, skip to menu
    if(project1.status()):
        print("Downloading Latin Corpuses")
        #insert each of the collections
        project1.insertClaudius()
        project1.insertCreeds()
        project1.insertEpitaphs()
        project1.insertDiesIrae()
        project1.insertAnselm()
        project1.insertSeverus()
        project1.insertBernard()
        project1.insertGregory()
    
    #Provide search menus for user
    phase2.searchMenu()

    
if __name__ == '__main__':
    main()
