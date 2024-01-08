#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# Name: wordsworth
# Description: Frequency analysis tool
# Author: autonomoid
# Date: 2014-06-22
# Licence: GPLv3
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# In[39]:


import collections
import re
import pandas as pd
import os
import spacy  # used to calculate clauses


# In[62]:


class wordsworth:
    args = 0
    ignore_list = []
    out = 0
    words = []
    previous_word = ''
    previous_pair = ''
    previous_triple = ''
    previous_quad = ''
    max_n_word = 4  
    n_words = []
    prev_n_words = []
    counters = []

    word_stats = {
                  'file_name': '',
                  'total_chars': 0,
                  'total_words': 0,
                  'total_sentences': 0,
                  'word_max_length': 0,
                  'word_min_length': 999,
                  'mean_length': -1,
                  'longest_word': '',
                  'shortest_word': '',
                  'sentence_max_length': 0, 
                  'max_tree_depth': 0,                  
                  'longest_sentence': '',
                  'mtd_sentence': '',

                #   'char_counts': {
                #                   'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.0, 'f': 0.0,
                #                   'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0, 'k': 0.0, 'l': 0.0,
                #                   'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.0, 'r': 0.0,
                #                   's': 0.0, 't': 0.0, 'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0,
                #                   'y': 0.0, 'z': 0.0
                #                  },
                #   'char_percentages': {
                #                        'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.0, 'f': 0.0,
                #                        'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0, 'k': 0.0, 'l': 0.0,
                #                        'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.0, 'r': 0.0,
                #                        's': 0.0, 't': 0.0, 'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0,
                #                        'y': 0.0, 'z': 0.0
                #                       },
                  'lexical_density': -1,
                  'num_clauses': -1,
                  'Haliday_density': -1
                  }


    def __init__(self, commandline_args):
        args = commandline_args
        self.ignore_list = str(args.ignore_list).split(",")
        

    def print_results(self):
    # Create a DataFrame from the word_stats dictionary
        df = pd.DataFrame(self.word_stats, index=[0])
        return df
      
        

    def init_word_counters(self):
        self.max_n_word = args.max_n_word
        self.n_words = ['' for i in range(self.max_n_word)]
        self.prev_n_words = ['' for i in range(self.max_n_word)]
        self.counters = [collections.Counter() for i in range(self.max_n_word)]


    def read_file(self):
        print("[+] Analysing '" + args.inputfile + "'")
        self.word_stats['file_name'] = os.path.basename(args.inputfile)
        if args.allow_digits:
            self.words = re.findall(r"['\-\w]+", open(args.inputfile, 'r', encoding='utf-8').read().lower())
        else:
            self.words = re.findall(r"['\-A-Za-z]+", open(args.inputfile, 'r', encoding='utf-8').read().lower())
        self.doc = open(args.inputfile, 'r', encoding='utf-8').read()
    
    # Function to compute the tree depth of a sentence - a measure of Structural Complexity 
    def tree_depth(sentence):
        """
        Calculate the depth of the tree parsed by spaCy.
        """
        def _depth(token):
            if not list(token.children):
                return 1
            else:
             return 1 + max(_depth(child) for child in token.children)
        return max(_depth(token) for token in sentence)
    
    def compute_stats(self):
        for word in self.words:
        
            if word in self.ignore_list:
                continue
        
            word = word.strip(r"&^%$#@!")

            # Allow hyphenated words, but not hyphens as words on their own.
            if word == '-':
                continue

            length = len(word)

            # Record longest word length
            if length > self.word_stats['word_max_length']:
                self.word_stats['word_max_length'] = length
                self.word_stats['longest_word'] = word

            # Record shortest word length
            if length < self.word_stats['word_min_length']:
                self.word_stats['word_min_length'] = length
                self.word_stats['shortest_word'] = word

            # Keep track of the total number of words and chars read.
            self.word_stats['total_chars'] += length
            self.word_stats['total_words'] += 1.0

            # # Note the charaters in each word.
            # for char in word:
            #     if char.lower() in self.word_stats['char_counts']:
            #         self.word_stats['char_counts'][char.lower()] += 1.0

            # Tally words.
            for i in range(1, self.max_n_word):
                if self.prev_n_words[i - 1] != '':
                    self.n_words[i] = self.prev_n_words[i - 1] + ' ' + word
                    self.counters[i][self.n_words[i]] += 1

            self.n_words[0] = word
            self.counters[0][word] += 1

            for i in range(0, self.max_n_word):
                self.prev_n_words[i] = self.n_words[i]

        # Calculate the mean word length
        self.word_stats['mean_length'] = self.word_stats['total_chars'] / self.word_stats['total_words']

        # # Calculate relative character frequencies
        # for char in self.word_stats['char_counts']:
        #     char_count = self.word_stats['char_counts'][char]
        #     total_chars = self.word_stats['total_chars']
        #     percentage = 100.0 * (char_count / total_chars)
        #     self.word_stats['char_percentages'][char] = percentage

        # Calculate the lexical density of the text.
        total_unique_words = len(self.counters[0])
        total_words = sum(self.counters[0].values())
        self.word_stats['lexical_density'] = 100.0 * total_unique_words / float(total_words)
        
        # calculate the Lexical Items to Number of Clauses  - Haliday Lexical density
        # Define a grammar for parsing the sentences
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.doc)
       
        try: 
            num_clauses = sum(1 for sent in doc.sents for token in sent if token.dep_ == 'ROOT' and token.pos_ == 'VERB')
        except ValueError:
            num_clauses = -1
        self.word_stats['total_sentences'] = len(list(doc.sents))
        self.word_stats['num_clauses'] = num_clauses
        self.word_stats['Haliday_density'] = 100.0 * total_unique_words / float(num_clauses)
        longest_sentence = max(doc.sents, key=lambda sentence: len(sentence))
        self.word_stats['longest_sentence'] = longest_sentence.text
        self.word_stats['sentence_max_length'] = len(longest_sentence)
        #shortest_sentence = min(doc.sents, key=lambda sentence: len(sentence))
        #self.word_stats['sentence_min_length'] = len(shortest_sentence)
        #self.word_stats['shortest_sentence'] = shortest_sentence.text
        max_depth = 0 
        sentence_mtd = ''
        for sent in doc.sents:
            # Calculate the depth of the current sentence
            depth = tree_depth(sent)
            # Update the maximum depth if necessary
            if depth > max_depth:
                max_depth = depth
                sentence_mtd = sent.text

        self.word_stats['max_tree_depth'] = max_depth
        self.word_stats['mtd_sentence'] = sentence_mtd                  
                  
                  

        return(self.word_stats)


# In[63]:


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Perform letter, word and n-tuple frequency analysis on text files.')
    parser.add_argument('--filename', '-f', dest='inputfile', required=True, help='Text file to parse.')
    parser.add_argument('--ntuple', '-n', dest='max_n_word', required=False, default=4, type=int, help='The maximum length n-tuple of words. Default is 4.')
    parser.add_argument('--top', '-t', dest='top_n', required=False, default=20, type=int, help='List the top t most frequent n-words. Default is 20.')
    parser.add_argument('--allow-digits', '-d', dest='allow_digits', default=False, required=False, help='Allow digits to be parsed (true/false). Default is false.')
    parser.add_argument('--ignore', '-i', dest='ignore_list', required=False, help='Comma-delimted list of things to ignore')
 
    args = parser.parse_args()
    
    # Update the inputfile argument with the desired file path
    args.inputfile = 'C:/Source/Repos/Research-Proposal-development/Data/RawData/72316.txt'

    w = wordsworth(args)
    w.init_word_counters()
    w.read_file()
    w.compute_stats()  

     
    df = w.print_results()

    # Save the DataFrame to a CSV file
    df.to_csv('output.csv')

    # Or display it in a Jupyter notebook
    display(df)


# In[42]:


file =  open('C:/Source/Repos/Research-Proposal-development/Data/RawData/72316.txt' , 'r', encoding='utf-8').read()       
nlp = spacy.load('en_core_web_sm')
doc = nlp(file)


# In[54]:


longest_sentence = min(doc.sents, key=lambda sentence: len(sentence))
print(longest_sentence.text)
print(len(longest_sentence))


# In[55]:


def tree_depth(sentence):
    """
    Calculate the depth of the tree parsed by spaCy.
    """
    def _depth(token):
        if not list(token.children):
            return 1
        else:
            return 1 + max(_depth(child) for child in token.children)
    return max(_depth(token) for token in sentence)


# In[58]:


max_depth = 0 
sentence_mtd = ''
for sent in doc.sents:
    # Calculate the depth of the current sentence
    depth = tree_depth(sent)
    # Update the maximum depth if necessary
    if depth > max_depth:
        max_depth = depth
        sentence_mtd = sent.text

    


print(f"Maximum tree depth in the document: {max_depth}")
print(f"Sentence with max tree depth: {sentence_mtd}")
print(f"Sentence: {sent.text}")
print(f"Tree depth: {tree_depth(sent)}")

