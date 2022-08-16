# f-Note 
<p align="center">
  <img src=img/example.png>
</p>

My first repository on GitHub.

f-Note is a simple command-line note-taking application written in python. 

## Overview 


## Suported Platform 

| OS      | Tested satus       
| ------- |:-------------:
| Linux   | &#9746;
| Mac OS  | &#9744; 
| Windows | &#9744; 

## Necessary Modules 
These are all the modules that one might have to install. 

- Sqlite3 
  - https://pypi.org/project/pysqlite3/
- Texttable 
  - https://pypi.org/project/texttable/
- readline 
  - Might not work on Mac OS and Windows. 

## Features 
- Simple to use 
- Add note 
  - Insert title, tag and note
  - Date and Id are generated automatically
- Edit Note 
  - Edit title, tag and note 
 - Delete note 
 - Search for one tag 

## Motivation 
The final task from NCLabs' Python Developer Career Course to show all my learned skills. 

## Run application 
- Download logo.txt and the current version into same folder 
- Run fnotexx.py 
 
## Unit testing 

#### Necessary modules
- unittest 
  - https://docs.python.org/3/library/unittest.html
 
#### Run unittest
- Download the current version of fnotexx.py and test_fnotexx.py and create_database.py into same folder 
- In fnotexx.py:
  - Comment out N.start() 
- Run test_fnotexx.py 
 
## Documentation 
#### Version-00 
- Initial release 
  - Concept of OOP 
  - Display an ASCII-text
  - Create database 
  - Display database 
  - Display menu 
  - Add note to database 
    - for user input --> input()-function 

#### Version-01
- Changed 'Add note'
  - Use of sys.stdin.read instead of input() 
  - Goal: enter notes over multiple lines 
- Added 'Quit Program' 
  - Application ends due to user input 

#### Version-02 
- Changed 'Add note' 
  - Use of input()-function again
  - Loop over the input function
  - 'Add note' ends due to pressing 'Enter' if input() is empty 
- Added 'Edit note' feature  
  - Use of readline module

#### Version-03
- Added 'Delete note' feature 
- Added 'Search for tag' feautre 

#### Version04 
- Preparing for unit testing 
- Change file name 
  - Removed the hyphen to import class fnote() 
- Start app with class method: start() 
- Adjusted all methods which connect to the database 
  - Added new parameter table_name to get unit tests run 
  
#### Version05
- Added regular expression for search tag method 

#### testfnote00
- Initialize class Testfnote() 
- Set up connection to the database 'test.db' 
- Tear down the database 'test.db' 
- Test following methods: 
  - get_title_database()
  - get_note_database()
  - get_tag_database()
  
  #### test_fnote01 
  - No need to download 'test.db' 
  - Create Database temporary and delete it afterwars 
  - New test methods: 
    - test_insertVariableIntoTable()
    - test_update_database()
    - test_check_id_in_database()
    - test_get_last_id() 
    - test_generate_id() 
    - test_delete_note_database()
    - test_search_tag_table()
    
#### create_database
- Create Database "test.db" 
- Creates a table named 'overview' with following row (id, title, date, tag, note) 
- Values for testing purposes: 
  - '1', 'title_test01', 'date_test01', 'tag_test01', 'note_test01'
  - '2', 'title_test02', 'date_test02', 'tag_test02', 'note_test02'
  - '3', 'title_test03', 'date_test03', 'tag_test03', 'note_test03'



