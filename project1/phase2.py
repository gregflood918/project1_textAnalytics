#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:31:18 2017

@author: gregflood918
"""


#Project1 - phase2.py
#Greg Flood
#CS 5970 - Text Analytics
#
#Fulfills the requirements of part 3 and 4 of the Project One assignment fo
#This code assumes that an FTS table has already been built (i.e. through
#a call to project1.py) and provides an interface for translation of
#the full text search via the command line
#
#Calls to the command line menu can be made via supplying the command
#'python3 phase2.py'
#While in the project1 directory
#
#Translations will be made using command line arguments and the 
#mymemory.translated.net API


#Imported packages
import urllib.request
import sqlite3
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import operator
import re

 
class color:
#Color utility class.  This will provide some basic command line formatting
#and allow for important terms to be displayed in bol on a linux/unix OS
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   RED = '\033[91m'
   END = '\033[0m'

   
def searchMenu():
#User interface for the translation command line tool.  The user is allowed to
#select between 3 different options

    test = False
    while not test:
    
        print("\nPlease select " +color.UNDERLINE + "one" + color.END + 
        " of the following options:")
        print("Enter '1' for Help")
        print("Enter '2' to search for a " + color.BOLD + "Latin " + color.END + "term")
        print("Enter '3' to search for an " + color.BOLD + "English " + color.END + "term")
        print("Enter '0' to quit")
        choice = input ("Select: ")
        
        #User options
        if choice == "1":
            s = (color.BOLD + "\nDescription: " + color.END + "\nThis program will search "
                 "for a Latin or English word in the "
                 "following Latin collections:\n\n" + color.BOLD +
                 "Speech of Claudius Caesar\n"
                 "Early Christian Creeds\n"
                 "Dies Irae\n"
                 "The works of St. Anselm\n"
                 "The works of St. Bernard of Clairvaux\n"
                 "Sulpicius Severus\n"
                 "Gregory IX\n\n" 
                 "Option 2: " + color.END + "\nSearches for a user supplied Latin word in all of the "
                 "aforemention corpuses and returns passages contain the supplied "
                 "word, along with the Title, Book, Chapter, Verse, and link for "
                 "the passage.   Additionally, a barplot displaying the frequency of "
                 "the word usage across all 8 collections will be returned.\n\n" + color.BOLD +
                 "Option 3: " + color.END + "\nSearches for a user supplied English word in all of the "
                 "aforemention corpuses and returns passages contain the supplied "
                 "word, along with the Title, Book, Chapter, Verse, and link for "
                 "the passage.  The English term is translated to Latin via the "
                 "mymemory.translated.net translation API, and the translation "
                 "will be given alongside the prevoius results. Additionally, a "
                 "barplot displaying the frequency of the word usage across all "
                 "8 collections will be returned.\n\n" + color.BOLD + 
                 "Option 4: \n" + color.END + "Exits the program\n\n")  
            print(s)
        elif choice == "2":
            searchword = input ("\nPlease enter a " + color.BOLD + "Latin " + color.END + "word for searching: ")
            searchLatin(searchword)
        elif choice == "3":
            searchword = input ("\nPlease enter an " + color.BOLD + "English " + color.END + "word for translation/search: ")
            searchEnglish(searchword)
        elif choice == "0":
            print("\nGoodbye")
            test = True
        else:
            print("\nInvalid Entry")

       
def searchLatin(word, englishWord = ""):
 #Function that perform an full-text search on the 'latintext.db' FTS table.
#It will return the collection title (which also contains the author of the
#collection), the book name, the chapter number/name, the verse name, and the
#passage matching the latin term.  This query only searchs the PASSAGE conents
#and not the titles, chapter, et cetera.
#Also note that if the passage is over 30 words in length, then the passage
#is trimmed to only include the search term plus the 10 words preceding and
#following the word.  This is mostly for Gregory IX and Bernard, which had
#very long verses. 
#Optional english argument is for the case where the word being passed was
#translated.  IF this is the case, then the translation is displayed.
    try:
        conn = sqlite3.connect(r"latintext.db")
        c = conn.cursor()
        c.execute("SELECT * FROM latintext WHERE passage MATCH ' " + word + " ';")
        matches = c.fetchall()
        numMatches = len(matches)
        if matches: #Tests if matches actually contains anything
            for i in matches:    
                trimFlag = False
                passage = str(i[7])
                pattern = re.compile(' ' + re.escape(word) + '[ ,:;\.]|^'+re.escape(word) + '[:,; ]|\"'+re.escape(word)+' ',
                                     re.IGNORECASE)
                testArray = passage.split()
                #If the passage is too long, we will keep only 10 words before
                #and 10 words after the matched term
                if len(testArray)>30:             
                    keep = r'(\S+\s+){0,10}\S*\b'+re.escape(word)+r'\b\S*(\s+\S+){0,10}'
                    passage = re.search(keep,passage,re.IGNORECASE).group()
                    trimFlag = True
                    
                #Now for some cool formatting
                passage = re.sub(pattern," " + color.UNDERLINE + color.BOLD + 
                                 color.RED  + word + color.END + " ",passage)
                print(color.BOLD + "Title: "+  color.END + str(i[0]) )
                print(color.BOLD + "Book: " + color.END +str(i[1]))
                print(color.BOLD + "Chapter: " + color.END +str(i[5]))
                print(color.BOLD + "Verse: " + color.END +str(i[6]))
                if trimFlag: #Show if passage was trimmed
                    print(color.BOLD + "(trimmed) Passage: " + color.END +passage)
                else:
                    print(color.BOLD + "Passage: " + color.END +passage)
                print(color.BOLD + "Link: " + color.END +str(i[8]) + "\n")
                        
            print(color.BOLD+"Total Matches: "+color.END  + str(numMatches)) 

            #If an english word is passed, display translation
            if englishWord:
                print("English: "+ englishWord)
                print("Latin: " + word + '\n')
             
            #While loop to ensure the user selects the approriate response 
            #for wether or not to display a flag
            plotFlag = False
            while not plotFlag:               
                print("\nWould you like to see the frequency distribution across all corpuses?")
                print("Enter 1 for yes, 0 for no:\n ")
                user_input = input ("Select: ")
                print('\n')
                if user_input == '1' and englishWord:
                    createFrequencyPlot(matches, englishWord)
                    plotFlag = True
                elif user_input == '1' and not englishWord:
                    createFrequencyPlot(matches,word)
                    plotFlag = True
                elif user_input =='0':
                    plotFlag = True
                else:
                    "Invalid Entry\n"          
        else:
            print("No Matches for " + word + "\n")
            if englishWord:
                print("English: "+ englishWord)
                print("Latin: " + word + '\n')
               
    except (sqlite3.IntegrityError,sqlite3.OperationalError):
        print("\nInvalid Entry")
        print("Please exclude any quotation marks or apostrophes in search\n")
    conn.close()
    return

    
def translateAPI(word):
#Function that requests a translation from English to Latin for the
#passed string.  Utilizes the mymemory.translated.net API 
    link = 'http://mymemory.translated.net/api/get?q=' + word + '&langpair=en|la'
    response = requests.get(link).json()
    return response.get("responseData").get("translatedText") #API specfic info
    
 
def createFrequencyPlot(matches, word):
#Function that produces a matplotlib barplot showing the frequency of 
#each word with respect to the collection it was take from.  The function
#accepts a list of tuple (i.e. the value returned from the sqlite3 query)
#and first iterates over the list with a default dictionary, to count 
#the occurrences of each collection in the list.
    collection_counts= defaultdict(int)
    for i in matches:
        title = str(i[0])
        collection_counts[title] +=1
    #Create a sorted representation of the default dictionary
    sorted_dict = sorted(collection_counts.items(), key=operator.itemgetter(1),
                         reverse=True)
    titles, freq = zip(*sorted_dict)
    
    #Creating a map of titles to plot friendly x-label formatting
    plot_key = {'Speech of Claudius':'Claudius',
                 'Early Christian Creeds':'Christian\nCreeds',
                 'ROMAN EPITAPHS':'Roman\nEpitaphs',
                 'Dies Irae':'Dies\nIrae',
                 'Anselm':'Anselm','St. Bernard':'St.\nBernard',
                 'Sulpicius Severus':'Sulpicius\nSeverus',
                 'Gregory IX: Decretals':'Gregory\nIX'}
    #Now, making a neat plot
    xs = [i + .1 for i, _ in enumerate(titles)] #Getting bar off y-axis
    labels = [plot_key[i] for i in titles] #Using our key for formatted text
    plt.bar(xs, freq)
    plt.ylabel("Word Frequency")
    plt.title(str("Usage of '" + str(word) + "'"))
    plt.xticks([i + .5 for i,_ in enumerate(titles)],labels)
    plt.show()   
    return
    

def searchEnglish(word):
#Function that accepts a word to be translated, calls the translateAPI()
#to retrieve the translation, then searches the 8 corpuses of Latin text
#for instances of the word
    trans = translateAPI(word)
    if not trans:
        print("No translation found\n")
    else:
        searchLatin(trans, word)
    
    return
    
    

 
