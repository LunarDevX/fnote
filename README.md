# f-Note 
<p align="center">
  <img src=img/example.png>
</p>

My first repository on GitHub.

f-Note is a simply command line note taking application written in python. 

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

## Motivation 
The final task from NCLabs' Python Developer Career Course to show all my learned skills. 

## Run application 
- Download logo.txt and the current version into same folder 
- Run fnote-xx.py 
 
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
- Changed 'Ad note'
  - Use of sys.stdin.read instead of input() 
  - Goal: enter notes over multiple lines 
- Added 'Quit Program' 
  - Application ends due to user input 

#### Version-02 
- Changed 'Ad note' 
  - Use of input()-function again
  - Loop over the input function
  - 'Add note' ends due to pressing 'Enter' if input() is empty 
- Add 'Edit note' 
  - Use of readline module

