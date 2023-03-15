# InformationRetrieval
This repo consists of all the assignments, projects, tasks of Information Retrieval course of FAST NUCES Spring 2023.

# Assignment 1
## Implementation of Boolean Retrieval Model
Link to Article: [Boolean Retrieval Model]()

### Introduction
The Boolean retrieval model is a search model that retrieves documents that match a Boolean expression (a query) of terms, where the terms are connected by Boolean operators (AND, OR, NOT).

### How to run?
* install python 🐍 latest version and set it up on your computer.
* clone this repository in a specific folder.
* unzip the folder and open the assignment folder in a preferred code editor or IDE.
* #### Install Dependencies 
  * `pip install nltk`
  * `pip install unidecode`
  * `pip install pycontractions`
  * `pip install AST`
  * `pip install tk`
* #### For Linux
  `python3 main.py`
* #### For Windows
  `python main.py`
### Queries Format
#### Simple Query
* word
#### Complement Query
* not word
#### Intersection Query
* word1 and word2
* word1 and word2 and word3
* not word1 and word2
* word1 and not word2
* not word1 and not word2
* not word1 and word2 and word3
* word1 and not word2 and word3
* word1 and word2 and not word3
* not word1 and not word2 and not word3
#### Union Query
* word1 or word2
* word1 or word2 or word3
* not word1 or word2
* word1 or not word2
* not word1 or not word2
* not word1 or word2 or word3
* word1 or not word2 or word3
* word1 or word2 or not word3
* not word1 or not word2 or not word3
#### Mixed Query
* It includes query with mixed boolean opearators (AND, OR, NOT) and word limit upto 3 words max.
#### Proximity Query
* word1 word2 \k, here 'k' represents the no. of words word2 is distant from word1.
