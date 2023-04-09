# InformationRetrieval
This repo consists of all the assignments, projects, tasks of Information Retrieval course of FAST NUCES Spring 2023.

# Assignment 1
## Implementation of Boolean Retrieval Model
Link to Article: [Boolean Retrieval Model](https://medium.com/@syed.faheem.official/how-to-implement-the-boolean-retrieval-model-610e2776f2b6)

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


# Assignment 2
## Implementation of Vector Space Model

### Introduction
The Vector Space Model is a commonly used information retrieval technique where documents are represented as vectors in a high-dimensional space and ranked based on their similarity to a user's query.

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

### Results 

The results are written after applying threshold using alpha value= 0.05

Results Format:
Query
Ranked Documents
Respective Cosine Similarities


* cricket politics
  [5, 26, 29, 14]
  [0.10483768357856904, 0.0733026052948556, 0.05747687349155568, 0.051814006141766254]
* dharamsala to indore
  [17]
  [0.5669900905084869]
* retirement
  [14]
  [0.05884903818579923]
* test captain
  [3, 6, 21, 17, 14, 23, 22]
  [0.2169788724831718, 0.16412707621815958, 0.12857575540015573, 0.109537249881213, 0.06924332012356993, 0.05976605662540713,     0.05556857004383423]
* pcb psl
  [11, 29, 4]
  [0.3987613437849497, 0.23786386254409053, 0.07810602325184351]
* hate
  []
  []
* bowling coach
  [29, 6, 24]
  [0.15946207811500823, 0.10025156193891573, 0.06560991594156915]
* relative comfort
  []
  []
* possible
  [23, 15]
  [0.05534812091736982, 0.051743525151666955]
* batter bowler
  [2, 3, 16]
  [0.09290690948714346, 0.08726633903001002, 0.05206958459212497]

