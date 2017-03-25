#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:44:30 2017

@author: gregflood918
"""

#External Links to Latin Text Corpora

#Aquinas - http://thelatinlibrary.com/aquinas.html
#Claudius Caesar - http://thelatinlibrary.com/claud.inscr.html
#Bernard of Clairvaux - http://www.thelatinlibrary.com/bernardclairvaux.shtml
#Roman Epitaphs - http://www.thelatinlibrary.com/epitaphs.html
#Anselm - http://www.thelatinlibrary.com/anselm.html
#Christian Creeds - http://www.thelatinlibrary.com/creeds.html
#Sulpicius Severus - http://www.thelatinlibrary.com/sulpiciusseverus.html



#Imported packages
import urllib.request
import re
from bs4 import BeautifulSoup
import sqlite3
import os
import random

#We will start with Claudius Caesar (smaller collection)
#Gregory the 9th
#Dies Ires
links={"Gregory IX":"http://www.thelatinlibrary.com/gregory.html",
       "Claudius Caesar":"http://thelatinlibrary.com/claud.inscr.html",
       "Bernard of Clairvaux":"http://www.thelatinlibrary.com/bernardclairvaux.shtml",
       "Roman Epitaphs":"http://www.thelatinlibrary.com/epitaphs.html",
       "Anselm":"http://www.thelatinlibrary.com/anselm.html",
       "Dies Irae":"http://www.thelatinlibrary.com/diesirae.html",
       "Christian Creeds":"http://www.thelatinlibrary.com/creeds.html",
       "Sulpicius Severus":"http://www.thelatinlibrary.com/sulpiciusseverus.html"}
 
       
'''
Database function.  Creates a database and a utility function
for inserting contents into the database
'''       
             
def createDB():
#Function to create database that will be populated by elements of the
#parsed latin text
    try:         
        conn = sqlite3.connect(r"latintext.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE latintext
        (title TEXT,book TEXT,language TEXT,author TEXT,
        dates TEXT,chapter TEXT,verse TEXT, passage TEXT,
        link TEXT)''')   
        c.commit()
        c.close()
        return         
    except:
        print("Table Already Exists")
        return
        
def populateDB(records):    
    conn = sqlite3.connect(r"latintext.db")
    c = conn.cursor()
    #Loop through array length
    for i in range(len(records)):
        c.execute("INSERT INTO latintext VALUES (?,?,?,?,?,?,?,?,?)",
                  (records[i][0],records[i][1],records[i][2],records[i][3],\
                   records[i][4],records[i][5],records[i][6],records[i][7],records[i][8]))
    c.commit()
    c.close()
    return

    
'''
Text manipulation utility function.  One function cleans the text and 
returns formatted text.  Other parses text for hrefs.
'''

def cleanText(soup):
#Utility function that returns a cleaned list of text from a BeautifulSoup
#object
    temp = re.sub('<.*?>',"",str(soup.body)) #Remove tags
    temp = re.sub(r' +',' ',temp) #replace multiple spaces with single space
    temp = re.sub(r'\xa0','\n',temp) #replace \xa0 w/ \n
    temp = re.sub(r'[ ]*\|[ ]*'," ",temp) #replace | with spaces
    temp = re.sub(r'\([0-9]+\)','\n',temp) #For parsing sulpicius severus
    #MOVE BACK IF THIS CAUSES PROBLEMS
    temp = temp.split(('\n')) #split on newlines
    textList = [x for x in temp if x] #remove empty elements
    textList = [x for x in textList if x != " "] #remove space elements
    textList = [x.strip() for x in textList if x!= " "] 
    textList = [x for x in textList if x] #fixes problem with Anselm

    return textList
    
def getLinks(soup):
#Utility function that returns links on a page
    links=[]
    for j in soup.find_all('a'):
        avoid = r'The|Christian'
        if re.search(avoid,j.text):
            continue
        links.append(j['href'])
    return links

  
'''
Text Scrapers.  8 functions that access individual latin collections and
returns their contents as a list of lists
'''   
       
def fetchClaudius():
#Function that retrives parses the Claudius Beautiful Soup object.  Returns
# a list of list, where each inner list consists of the seven elements 
#consistent with the sqlite db schema.  Note that the 'verses' in this work 
#are replaced by paragraph number. Since the online text is unlabled, it is
#easier to count paragraphs rather than count | characters
    global links
    currLink = links["Claudius Caesar"]    
    f = urllib.request.urlopen(currLink).read().decode('utf-8')
    soup = BeautifulSoup(f,'html.parser')
    
    #Use BeautifulSoup and Regex to parse HTML content
    title = soup.title.text.strip()  #Get title
    author = "Claudius Caesar"
    
    chapters = r'Column'  #2 re expressions for use in parsing
    avoid = r'The'   
    textList = cleanText(soup)  
    book = textList[0] #Save book name, which we assume to be the first line
    textList = textList[1:] #trim
    returnList = []   
    paragraphNum = 1
    
    #Cycle through elements of text list and reformat to match db
    for i in textList:
        if re.search(chapters,i):
            chapter = i
            continue
        if re.search(avoid,i):
            continue
        innerList = [title,book,"Latin",author,"",chapter,paragraphNum,
                     i,currLink]
        returnList.append(innerList)
        paragraphNum +=1
    return returnList    
   
     
def fetchCreeds():
#Function that retrives parses the Early Christian Creeds.  Returns
# a list of list, where each inner list consists of the seven elements 
#consistent with the sqlite db schema.  Note that since there are not any
#labeled verses in this text, the natural text breaks will be used as verse
#number.  The verses will reset for each new creed in the work.
    global links
    currLink = links["Christian Creeds"]    
    f = urllib.request.urlopen(currLink).read().decode('utf-8')
    soup = BeautifulSoup(f,'html.parser')
    
    #Use BeautifulSoup and Regex to parse HTML content
    title = soup.title.text.strip()  #Get title
    author = "" #unknown
    dates = "" #unknown
    book = "" #We will leave books blank, as there is pnly one "book" here
    
    chapters = set() #we will use this set for parsing of chapters
    pageHeads=soup.find_all("p",class_="pagehead") #prayer names stored in paghead class
    for i in pageHeads:
        chapters.add(re.sub('\n','',i.text))
        
    avoid = r'The|Christian' #To avoid links
    textList = cleanText(soup)
    returnList = []   
    verseNum = 1 #will reset at new chapters
    
    #Cycle through elements of text list and reformat to match db
    for i in textList:
        if i in chapters:
            chapter = i
            verseNum = 1
            continue
        if re.search(avoid,i):
            continue
        innerList = [title,book,"Latin",author,dates,chapter,verseNum,
                     i,currLink]
        returnList.append(innerList)
        verseNum +=1
    return returnList   
    
         
def fetchEpitaphs():
#Function that retrives parses the Roman Epitaphs.  Returns
# a list of list, where each inner list consists of the seven elements 
#consistent with the sqlite db schema.  Note that since there are not any
#labeled verses in this text, the natural text breaks will be used as verse
#number.  The verses will reset for each new epitaph in the work.    
    global links
    currLink = links["Roman Epitaphs"]    
    f = urllib.request.urlopen(currLink).read().decode('utf-8')
    soup = BeautifulSoup(f,'html.parser')
    
    #Use BeautifulSoup and Regex to parse HTML content
    title = soup.title.text.strip()  #Get title
    author = "" #unknown
    dates = "" #unknown
    book = "" #We will leave books blank, as there is pnly one "book" here
    
    avoid = r'The'
    chapters = r'[B|CIL] [0-9]'
    textList = cleanText(soup)
    returnList = []   
    verseNum = 1 #will reset at new chapters
    chapter = ""
    
    for i in textList:
        if re.search(chapters,i):
            chapter = i
            verseNum = 1
            continue
        if re.search(avoid,i):
            continue
        innerList = [title,book,"Latin",author,dates,chapter,verseNum,
                     i,currLink]
        returnList.append(innerList)
        verseNum +=1
    return returnList 
            
         
def fetchAnselm():
#A function that fetches the works of Saint Anselm from the Latin Library.
#There are two separate books in this collection, with substantailly different
#formatting.  Thus, this function is bespoke for this collection and is a little
#longer than desirous. But it returns a list of list containtaining all elements
#from the collection in an sqlite db format
    global links
    currLink = links["Anselm"] 
    f = urllib.request.urlopen(currLink).read().decode('utf-8')
    soup = BeautifulSoup(f,'html.parser')
    avoid = r'The|Christian' #To avoid links
    title = soup.title.text.strip()
    
    temp = soup.find('p',{'class':'pagehead'}).text.split('\n')
    author = temp[0]
    dates = re.sub(r'[\(\)]',"",temp[1]) #remove parentheses
            
    #get links
    testLinks = getLinks(soup)

    #Create a list of beautiful soup objects for each separate book
    #in the collection
    soupsOn = []
    for l in testLinks:
        f = urllib.request.urlopen("http://thelatinlibrary.com/" + l).\
        read().decode('utf-8','ignore')
        soupsOn.append(cleanText(BeautifulSoup(f,'html.parser')))
     
    book = soupsOn[0][1]
    paraNum = 1
    returnList = []
    innerList = []
    soupsOn[0] = soupsOn[0][2:]
    
    #parsing first book
    for s in soupsOn[0]:
        if re.search(avoid,s):
            continue
        chapter = re.search(r'^[0-9]',s)
        if chapter:
            s = re.sub(r'^[0-9]+\. *',"",s)
            chapter = chapter.group(0)
        else:
            chapter = ""
        innerList = [title,book,"Latin",author,dates,chapter,paraNum,
                     s,("http://thelatinlibrary.com/" + testLinks[0])]
        paraNum += 1
        returnList.append(innerList)
    
    #parsing book 2
    book = soupsOn[1][1]
    soupsOn[1][26:]  #Trim out the extraneous
    chapter = ""
    verseNum = 1
    for s in soupsOn[1]:
        if re.search(avoid,s):  #check if it is an unnecesarry href
            continue
        if re.search(r'^[0-9]',s):
            chapter = re.search(r'^[0-9]',s).group(0)
            verseNum = 1
        if re.search(r'^Prooemium',s):
            chapter = 'Prooemium'
            verseNum = 1
        
        innerList = [title,book,"Latin",author,dates,chapter,verseNum,
                     s,("http://thelatinlibrary.com/" + testLinks[1])]
        verseNum += 1
        returnList.append(innerList)
        
    return returnList

        
def fetchSeverus():
#Functin that fetches text from the collection of works by Sulpicius Severus
#on the latin library.  Returns a list of list in the format defined in the
#problem description, i.e. a format conducive to sqlite db storage.
    global links
    currLink = links["Sulpicius Severus"] 
    f = urllib.request.urlopen(currLink).read().decode('utf-8','ignore')
    soup = BeautifulSoup(f,'html.parser')
    avoid = r'The|Christian' #To avoid links
    title = soup.title.text.strip()
    
    #Extract author and dates
    temp = soup.find('p',{'class':'pagehead'}).text.split('\n')
    author = temp[0]
    dates = re.sub(r'[\(\)]',"",temp[1]) #remove parentheses
                   
    #get links
    testLinks = getLinks(soup)
    soupsOn = []
    for l in testLinks:
        f = urllib.request.urlopen("http://thelatinlibrary.com/" + l).\
        read().decode('utf-8','ignore')
        soupsOn.append(cleanText(BeautifulSoup(f,'html.parser')))
    
    returnList = []
    innerList = []

    #nested for loop to cycle through each link
    #all text from each link is added to the same list of lists
    for s in soupsOn:
        verseNum = 1
        if re.search(r'^Praefatio',s[1]): #Special case for last book
            book = s[0]
            chapter = 'Praefatio'
            s=s[1:]
        else:
            book = s[0]+ " - " + s[1]
            s=s[2:]

        for innerS in s:
            if re.search(avoid,innerS):  #check if it is an unnecesarry href
                continue
            if re.search(r'^[0-9]',innerS):
                chapter = re.search(r'^[0-9]+',innerS).group(0)
                verseNum = 1
                continue
            innerList = [title,book,"Latin",author,dates,chapter,verseNum,
                     innerS,("http://thelatinlibrary.com/" + testLinks[1])]
            verseNum += 1
            returnList.append(innerList)       
    return returnList        #Possibly may have to come back here and cast the versenum to a string
        
   
def fetchBernard():  
#Function that retrieves the works of St. Bernard of Clairvaux from the
#latin library and returns a list of list formatted per the database
#schema of sqlite createDB function
    global links
    currLink = links["Bernard of Clairvaux"] 
    f = urllib.request.urlopen(currLink).read().decode('utf-8','ignore')
    soup = BeautifulSoup(f,'html.parser')
    avoid = r'The|Medieval' #To avoid links
    chapterFlag = r'^ADMONITIO|^CAPUT'
    title = soup.title.text.strip()
    soup = cleanText(soup)  #use clean text method
    
    author = "Bernard of Clairvaux"
    date = re.search(r'\(.*\)',soup[1]).group(0)
    date = re.sub(r'\(|\)',"",date)
    verseNum = ""
    returnList = []
    innerList = []
    chapter = ""
    for s in soup:
        if re.search(avoid,s):  #check if it is an unnecesarry href
            continue
        if re.search(chapterFlag,s):
            chapter = s
            continue
        if re.search(r'^[0-9]+',s):
                verseNum = re.search(r'^[0-9]+',s).group(0)
                s = re.sub(r'^[0-9]+\.* *',"",s)
        innerList = [title,"Latin",author,date,chapter,verseNum,
                     s,currLink]
        returnList.append(innerList)
    return returnList

                
def fetchDiesIrae():  
#Function that retrieves the poem (?) 'Dies Irae' from the
#latin library and returns a list of list formatted per the database
#schema of sqlite createDB function
    global links
    currLink = links["Dies Irae"] 
    f = urllib.request.urlopen(currLink).read().decode('utf-8','ignore')
    soup = BeautifulSoup(f,'html.parser')
    avoid = r'The|Christian' #To avoid links
    title = soup.title.text.strip()
    book = "" #No books in this collection
    author = "" #No author for this poem appears in html
    date = "" #No obvious date in this collection
    chapter = "" #No chapters in this collection.  This appears to be a poem
    soup = cleanText(soup)  #use clean text method
    soup = soup[1:] #remove redundant title
    verseNum = 1 #Each line will be considered a verse
    returnList = []
    innerList = []
     
    #Loop through cleaned text                  
    for i in soup:
        if re.search(avoid,i):
            continue
        innerList = [title,book,"Latin",author,date,chapter,verseNum,
                     i,currLink]
        returnList.append(innerList)
        verseNum +=1
    return returnList    

   
def fetchGregory():
#Function that retrieves the decrees of Pope Gregory IX.  There are 5 large books 
#total.  All 4 books are returned within a single list of lists in the format of
#the sqlite database.  The verse number gives teh chapter from the text, followed
#by the paragraph number within that subsection.  This is more helpful if trying
#to find something in the text
    global links
    currLink = links['Gregory IX']
    f = urllib.request.urlopen(currLink).read().decode('utf-8','ignore')
    soup = BeautifulSoup(f,'html.parser')
    avoid = r'The|Christian|(FINIS LIBRI)' #To avoid links
    title = soup.title.text.strip() #Pull out title
    
    dates="" #No apparent dates in the html
    author= "Gregory IX" #Obvious  
    #get links
    testLinks = getLinks(soup)
    soupsOn = []
    for l in testLinks:
        f = urllib.request.urlopen("http://thelatinlibrary.com/" + l).\
        read().decode('utf-8','ignore')
        soupsOn.append(BeautifulSoup(f,'html.parser'))

    returnList = []
    innerList = []
    chapterMatch = r'TITULUS|GREGORIxUS'
    verseMatch = r'CAP\.* *[A-Z]+\.*'
    chapter = ""
    verseNum = 1
    verse = ""
    versePrefix = "" #trying to create more helpful verse numbers

    #nested for loop to cycle through each link
    #all text from each link is added to the same list of lists
    for s in soupsOn:  
        print(type(s))
        #Get book name
        pageHeads = s.find("p",class_="pagehead")
        print(pageHeads)
        pageHeads = re.sub('<.*?>',"\n",pageHeads.text) #Remove tags
        pageHeads = pageHeads.split('\n')
        book = " ".join(pageHeads).strip()

        #Manual parsing of text.  CleanText function not appropriate for
        #this particular format
        temp = s.text
        temp = re.sub(r' +',' ',temp) #replace multiple spaces with single space
        temp = re.sub(r'\xa0','\n',temp) #replace \xa0 w/ \n
        temp = temp.split(('\n')) #split on newlines
        textList = [x for x in temp if x] #remove empty elements
        textList = [x for x in textList if x != " "] #remove space elements
        textList = [x.strip() for x in textList if x!= " "] 
        verseNum = 1
        #Inner loop
        for inner in textList:
            if re.search(avoid,inner):  #check if it is an unnecesarry href
                continue
            if re.search(chapterMatch,inner):
                chapter = inner
                verseNum = 1
                continue
            if re.search(verseMatch,inner):
                versePrefix = inner
                verseNum = 1
                continue
            if not chapter: #skips the pageheader.  won't go until it has a chapter name
                continue
            verse = str(versePrefix) + " : " + str(verseNum) #More helpful numbers
            innerList = [title,book,"Latin",author,dates,chapter,verse,
                     inner,("http://thelatinlibrary.com/" + testLinks[1])]
            verseNum += 1
            returnList.append(innerList)       
    return returnList       
    

'''
Insertion functions.  Calls scrapers and inserts their contents into the
database

'''    
    
def insertClaudius():
#Simple function to insert Claudius text into database
    text = fetchClaudius()
    populateDB(text)
    return
               
def insertCreeds():
#Simple function to insert Creeds text into database
    text = fetchCreeds()
    populateDB(text)
    return
 
def insertEpitaphs():
#Simple function to insert Epitaphs into database
    text = fetchEpitaphs()
    populateDB(text)
    return

def insertDiesIrae():
#Simple function to insert Dies Irae into database
    text = fetchDiesIrae()
    populateDB(text)
    return

def insertAnselm():
#Simple function to insert Anselm into database
    text = fetchAnselm()
    populateDB(text)
    return
    
def insertSeverus():
#Simple function to insert Severus into database
    text = fetchSeverus()
    populateDB(text)
    return
    
def insertBernard():
#Simple function to insert St. Bernard into database
    text = fetchBernard()
    populateDB(text)
    return
    
def insertGregory():
#Simple function to insert St. Gregory IX into database
    text = fetchGregory()
    populateDB(text)
    return

    
def status():
#Function to randomly select contents from the DB.  This is for testing
#purposes, and exactly mirrors code form normandb project   
    conn = sqlite3.connect(r"latintext.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM latintext")
    dbLength=c.fetchone()[0]
    #Print db length
    print("Total Number of Rows: ",dbLength)  
    
    #Grab 5 random rows
    for i in range(5):
        c.execute("SELECT book,verse FROM latintext ORDER BY RANDOM() LIMIT 1")
        print(c.fetchall())
        
    conn.close()
    
    return

    