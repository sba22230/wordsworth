wordsworth
==========

Frequency analysis of letters, words and arbitrary-length n-tuples of words.

###Basic wordworth:

####Example 1: Print the top 50 n-words in textfile.txt

```
python wordsworth --filename textfile.txt --top 50
```

```
python wordsworth -f textfile.txt -t 50
```

####Example 2: Print the top n-tuples of up to 10 words in textfile.txt

```
python wordsworth --filename textfile.txt --ntuple 10
```

```
python wordsworth -f textfile.txt -n 10
```

###NLTK-enabled wordsworth:
wordsworth-nltk.py provides exxtended analysis, including a frequency analysis of verbs, nouns, adjectives, pronouns etc.
To run this script you will need to install the python Natural Language Toolkit (NLTK)
and the Brown dataset which is used for token tagging. Fortunately this is very simple to install.

Step 1. Install NLTK 
```
$ sudo pip install nltk
```
Step 2. Launch the python interpretter
```
$ python
```
Step 3. Download the Brown dataset
```python
>>> import nltk
>>> nltk.download('brown')
```

Example output:

![Alt text](/screenshots/screenshot1.png?raw=true "screenshot1.png")
<br>
![Alt text](/screenshots/screenshot2.png?raw=true "screenshot2.png")
<br>
![Alt text](/screenshots/screenshot3.png?raw=true "screenshot3.png")
<br>
![Alt text](/screenshots/screenshot4.png?raw=true "screenshot4.png")
<br>
![Alt text](/screenshots/screenshot5.png?raw=true "screenshot5.png")
