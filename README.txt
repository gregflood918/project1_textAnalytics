
Project 1 - Phase One and Two
Greg Flood
gflood@ou.edu


##############################################################################
##############################################################################

Assignment:
Phase One- The goal was to extract data from an online collection
(thelatinlibrary.com) and populate a database with the parsed texts. 

Phase Two - The goal was to create a FTS interface on the collections
parsed in part one and use an API to provide translation services
to a search interface.  

Extra Credit - As part of phase two, a bar plot will be created displaying
the usage (frequency) of the search term across all 8 Latin text collections.

Both phase one and phase two may be completed by a single call
to the main method:

'python3 main.py'

'main.py' proceeds to check if 'latintext.db' exists and is populated.
The database is not populated, the Latin corpuses will be downloaded
using the functions from 'project1.py'.  Next, the search menu
will be displayed using the functions in "phase2.py"

More specific Details for each phase will be provided below:


##############################################################################
PHASE ONE
##############################################################################

Text Extraction:
8 collections from thelatinlibrary.com were selected to be extracted and
parsed from the latin library.  These collections include:

Speeches of Claudius Caesar
Roman Epitaphs
Sulpicius Severus
Christian Creeds
Gregory IX
Anselm
Bernard of Clairvaux
Dies Irae

These texts are all pulled from html format and parsing into a standardized
format for database insertion.  Due to differences in the formatting for
each collection, there are separate functions to extract each text.  Worth noting is
that while the database that is ultimately produced has specific data fields, these
data fields are defined somewhat differently from collection to collection based
on how each individual collection was delimited.  For example, verses in Claudius
Caesar were delimited by the '|' character, whereas Anselm didn't have any verse
delimiter.  Given that Anselm was divided by book, section, and chapter, the verse
number instead refers to the paragraph number within a specific book, section, and
chapter, as this would be more helpful and instructive to a reader than giving
a sentence number (which requires the tedious task of counting punctuation marks).

The subtleties of each of the formats and their effects on the extraction function
for each collection is outlined in the dicussion section.

##############################################################################

Database Population:
Each text extraction function returns a list of list, each inner list containing
the 9 data fields of the sql database.  The database created by within main.py
is title 'latintext.db' with the specific table being called 'latintext'.  The
table has the following schema:

title : text
book : text
language : text
author : text
dates : text
chapter : text
verse : text
passage : text
link : text

Most of the data fields are self explanatory, however, there are differences between
what each field means with respect to specifc collections. The differences will be
discussed in the 'discussion' section.

All of the data fields in the latintext.db table were set as text.  The reason for this
is the diversity in all of the 8 collections.  As discussed above regarding Claudius
Caesar and Anselm, there was no one uniform structure.  Keeping each data field as a
text element allowed maximum flexibility for what was included in the field.  For
example, some Chapter have titles, so it did not make sense to store this as a numeric
element because that would have required the title to be discarded.  Preservation of all
text from the collection was paramount.

Finally, Pytest is used in the assignment to test the functions in the project1 package.
In total, there are 3 test modules and 11 tests.


##############################################################################
PHASE TWO
##############################################################################

Translation Services:
All of the features of Phase two of this project can be found in 'phase2.py'.  The
translation services are provided by the mymemory.translation api (see link at bottom
of readme) to provide english to latin translation.  The call to the API is made in the 
translateAPI() function, which returns the Latin translation of the supplied English word.
This function is called within a call to searchEnglish(word)  where word is the user-
supplied english word to be translated.


##############################################################################

Search Results:
Latin or English words can be searched in the latintext.db fts table through the 
command line menu.  The menu will be displayed by running the following command
line command:

'python3 main.py'

The user is provided 4 selection options, 1-Help, 2-Search Latin term, 3-Search
English term, 0-Quit.  Options 2 and 3 are essentially the same, except for the
translation step in option 3.  2 and 3 perform the FTS search and return the results
that match the supplied word to the command line in the following format:

title : text
book : text
language : text
author : text
dates : text
chapter : text
verse : text
passage : text
link : text

If the passage exceeds 30 words, then the passage will be trimmed to only
include the 10 words preceding and the 10 words following the searched term.
This is to make the command line format more user-friendly.  Gregory IX has
some particularly lengthy verses that were taking up most of the console window

Also for simplicity, the matched term is bold, underlined, and highlighted in red

Finallly, the menu display will persist until it is supplied with a 0 (quit) argument
##############################################################################

EXTRA CREDIT - Data Visualization:

Along with the search results, a matplotlib barplot will be displayed.  This plot gives
the usage of the search termed in all 8 corpuses (usage meaning how often the word is
used in the collection).   The y axis shows how many times the word appeared, and the x
axis shows each collection in decreasing order of frequency.   


##############################################################################
##############################################################################

Language:
Python 3

##############################################################################
##############################################################################

Instructions
To run, please change directories into the project1_textAnalytics directory contained
within the zipped file project1_Phase1_floo1166.tar.gz.  The code structure in the
directory should have the following format:

project1_textAnalytics/
        project1/
                project1.py
		phase2.py
                __init__.py
        README
        setup.py
	setup.cfg
        requirements.txt
        main.py
	example_db
        		latintext.db 
	tests/
		test_db.py
		test_text_insertion.py
		test_text_retrieval.py
		test_phase2.py
	docs/


The file requirements.txt list the package requirements to run this package.
Please consult this file to see the full requirements, but note that BeautifulSoup4
and Pytest are used heavily in project1.py.  Install these packages, either in a virtual environment 
or to your system.

The test functions can be executed with the following command:

"python3 setup.py test"

Run the file main method using the following command:

"python3 main.py"

Note that running the main method will first check if the latintext.db file exists in the current
working directory and that it is populated.  If it isn't populated/doesn't exist, it will run
the methods form project1.py to create the database.  Next, the search menu of the FTS
table will be displayed.

Note: running setup.py assumes that there is no database 'latintext.db' in the current working directory.




##############################################################################
##############################################################################

Discussion

Each function in the project1.py will be discussed in turn, and their subtleties highlighted.

##############################################################################
PHASE1

createDB() : Function to create database that will be populated by elements of the parsed latin text.
This database has the structure outlined in the 'assignment' section above.

populateDB(records) : Utility function for batch insertion of latin text into the database 'latintext.db'.  The 
function accepts a list of lists as an argument, where each inner list has a length 9 that
corresponds to the fields of the database.  

cleanText(soup) : Utility function that accepts a beautiful soup object, parses the html, and returns a list
of text, where each element is selected based on the html demarcations.

cleanJustText(textList) : Utility function that accepts a list of text, parses, and returns a 
cleaned version of the list. 

getLinks(soup) : Utility function that will extract valid links from a Beautiful Soup object.  Here, "valid"
means that the link doesn't take you up a directory.


##############################################################################

Retrieval Functions - All functions in the section below have the same general format, returning 
a list of 9 element lists.   They all make one or more calls to cleanText, cleanJustText, and
getLinks.   Only the differences in the meaning of the respective elements will be discussed below.
The links for each collection can be found at the bottom of this document.  In all cases, the
functions kept the most natural division already present within the text.

fetchClaudius() : Function that retrieves the Speeches of Claudius Caesar
from the link at the bottom of this document.  The collection is delimited by the | character
and verseNum is formatted as "Paragraph ### : Verse ###".  Returns a list of lists

fetchCreeds() : Function that retrieves and parses the Christian Creeds.  The text is separated
by Creed name, which is held in chapter number, and line, which is enumerated in verse number.

fetchEpitaphs() : Function that retrieves and parses the collection of Roman Epitaphs.  The 
text is separated by Epitaph label, which is held in chapter number, and lines, which is
held in the verse number.

fetchAnselm() : Function that retrieves the works of Saint Anselm.  The text is separated by
Book, Chapter (which is stored as chapter number and title), and verse number, which here
refers to the paragraph within a chapter, as the text lacks helpful delimiters (white space
between paragraphs is the most helpful and obvious delimiter in the text).

fetchSeverus() : Function that retrieves the works of Sulpicius Severus.  The text is separated
by Book, paragraph number (which is stored as Chapter number in the db), and verse number.
The verses are marked in the text by (#) and the paragraphs have a number preceding the text
that is taken as the paragraph number.

fetchBernard() : Function that retrieves the works of St. Bernard of Clairvaux.  The text is separated
by book number, chapter number (which also stores chapter title), and verse number, which is 
delimited in the collection by #. preceding the text of each paragraph.

fetchDiesIrae() : Function that retrieves the Dies Irae collection.  The text is only separated by
line number, as there are no other demarcation.  It is a short collection

fetchGregory() : Function that retrieves the works of Gregory IX.  the text is separated by book number,
section name (which is stored in the chapter field), chapter name / paragraph.  The last field bears further
explanation.  Each subchapter has a number and a title.  To provide more granular parsing, this is stored
along with the paragraph within the subchapter according to the following format: "CAP. ### : ####"

##############################################################################
Insertion function - for each of the retrieval functions above, there is also a specific insertion function
that consists of two lines of code, a call to the retrieval function (storing the returned list of lists), and
a call to the populateDB function, passing the text to insert.  The name of each of these functions is below
but no further discussion will be given, as they share nearly identical formatting:

insertClaudius()
insertCreeds()
insertEpitaphs()
insertDiesIrae()
insertAnselm()
insertSeverus()
insertBernard()
insertGregory()


status() : Function that prints the number of rows in the 'latintext' table and returns
true if the database is populated (i.e. length>1)


##############################################################################
PHASE TWO

All the following functions are contained within 'phase2.py'

searchMenu() - Displays the search menu to the console window.  The user is allowed to input
1 of 4 options that will either display the help menu, search an English term, search a Latin term,
or quit.  Will call the following methods based on user response and input

searchLatin(word, englishWord="") - Searches the latintext table for matches to passed word.  Displays all
the fields from the database with some formatting. If an optional EnglishWord argument is supplied,
then the translation will be displayed.   Also calls createFrequencyPlot()

translateAPI(word) - Utilizes mymemory.translated.net API to translate an English word to Latin.  Returns
the translated latin word

searchEnglish(word) - Makes a call to translateAPI(word) to translate the provided English word.
It then makes a call to searchLatin(word) and performs the standard latin text search.  Following this,
it will provide an output showing the English word and its latin translation.

createFrequencyPlot(matches, word) - Called form the searchLatin(word) function, this function
utilizes matplotlib to create a bar chart showing the word usage frequency across all of the 
Latin corpuses.  Bars are arranged in descending order of usage, with frequency on y axis and
the corpus on the x axis.  Note that the displayed plot must be closed for the the function to
stop running.


##############################################################################
main.py - This module consists of a call to createDB() followed by a call to project1.status()
to check if the DB is populated.  If it isn't the project1 functions are called to build the database.
Either way, the next step is to run phase2.searchMenu()



##############################################################################
TESTING

There are four testing modules,  each of which will be discussed briefly.

test_db.py - Consists of two test functions.  Also creates a pytest fixture with a session scope.
This fixture, called "provide_db" initializes a latintext.db file in the current working directory 
for use in the tests.  The session scope ensures that the database persists through testing,
and the code below the yield serves as cleanup.

	test_DB(provide_db) : constructs a database and queries that the database exists

	test_populate_db(provide_db) : inserts an arbitrary element into the database and check
	that the element was inserted

test_text_retrieval.py - Consists of 8 test that all consist of a call to their respective 
retrieval function (1 for each of the 8 collection).  The test occurs by checking that
the dimensions of the list of list match the expected numbers for each collection.  The
lengths of each collection are as follows:

Claudius =80
Creeds =60
Epitaphs = 225
Anselm =96
Severus =885
Bernard =39
DiesIrae =57
Gregory IX =4610

The tests also check that the inner lists are of length 9.  This ensures that the returned
lists can easily be inserted into the latintext.db

test_text_insertion.py - Consists of 1 test that runs project1.insertClaudius() and checks
that the length of the database is the expected number (80).  Because each of the
extraction methods were tested in the other test methods, and because the insertion 
functions are simple, we can rest assured that the other insertion functions will
work if the text extraction tests pass.

test_phase2.py - Consists of two tests.  One test ensures that the translation API is working
by translating an English word and comparing the returned result to its known Latin translation.
The second test ensure that FTS features are available on latintext.db by performing a MATCH
search after inserting a single row.

In total, there are 13 tests.


##############################################################################
##############################################################################
Bugs:

Note that the latintext.db file should not exist in the main.py directory when running the
testing files. The latintext.db file of pre-populated data is in the example_db directory for reference.

The visual display for matplotlib must be CLOSED before the program can move to the
next step in the loop

The matplotlib display seems to run slowly on the gpel machines, but works, so be
patient if you select yes!

##############################################################################
##############################################################################
References:

"Gregory IX":"http://www.thelatinlibrary.com/gregory.html",
"Claudius Caesar":"http://thelatinlibrary.com/claud.inscr.html",
"Bernard of Clairvaux":"http://www.thelatinlibrary.com/bernardclairvaux.shtml",
"Roman Epitaphs":"http://www.thelatinlibrary.com/epitaphs.html",
"Anselm":"http://www.thelatinlibrary.com/anselm.html",
"Dies Irae":"http://www.thelatinlibrary.com/diesirae.html",
"Christian Creeds":"http://www.thelatinlibrary.com/creeds.html",
"Sulpicius Severus":"http://www.thelatinlibrary.com/sulpiciusseverus.html"

Translation API:
http://mymemory.translated.net/api/


