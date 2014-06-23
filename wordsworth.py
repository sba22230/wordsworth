#!/usr/bin/env python

# Name: wordsworth
# Description:  Frequency analysis tool
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

import re
import collections

# Font effects --> fancy console colours in bash
underline = "\x1b[1;4m"
black = "\x1b[1;30m"
red = "\x1b[1;31m"
green = "\x1b[1;32m"
yellow = "\x1b[1;33m"
blue = "\x1b[1;34m"
purple = "\x1b[1;35m"
turquoise = "\x1b[1;36m"
normal = "\x1b[0m"

previous_word = ''
previous_pair = ''
previous_triple = ''
previous_quad = ''

word_stats = {
              'total_chars': 0,
              'total_words': 0,
              'max_length': 0,
              'min_length': 999,
              'mean_length': -1,
              'longest_word': '',
              'shortest_word': '',
              'char_counts': {
                              'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.0, 'f': 0.0,
                              'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0, 'k': 0.0, 'l': 0.0,
                              'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.0, 'r': 0.0,
                              's': 0.0, 't': 0.0, 'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0,
                              'y': 0.0, 'z': 0.0
                             },
              'char_percentages': {
                                   'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.0, 'f': 0.0,
                                   'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0, 'k': 0.0, 'l': 0.0,
                                   'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.0, 'r': 0.0,
                                   's': 0.0, 't': 0.0, 'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0,
                                   'y': 0.0, 'z': 0.0
                                  }
             }


def print_n_word_frequencies(n_word_counter, top_n, output_file):
    total_entries = sum(n_word_counter.values())
    unique_entries = len(n_word_counter)
    if total_entries > 0:
        m = n_word_counter.most_common(min(unique_entries, top_n))
        n = len(m[0][0].split(' '))

        print '\n===' + blue + ' Commonest ' + str(n) + '-words' + normal + '==='
        out.write('\n=== Commonest ' + str(n) + '-words ===\n')

        for i in range(0, min(unique_entries, top_n)):
            n_word = m[i][0]
            count = m[i][1]
            perc = 100.0 * (count / float(total_entries))

            print (str(i + 1) + ' = ' + purple + n_word +
                   normal + ' (' + purple + str(count).split('.')[0] + normal +
                   ' = ' + purple + str(perc)[:5] + '%' + normal + ')')

            output_file.write(str(i + 1) + ' = ' + n_word + ' (' + str(count).split('.')[0] +
            ' = ' + str(perc)[:5] + '%)\n')


def print_results(word_stats, output_file):
    print '\n===' + blue + ' RESULTS ' + normal + '==='
    out.write('=== RESULTS ===\n')

    print 'File = ' + purple + str(args.inputfile) + normal
    out.write('File = ' + str(args.inputfile) + '\n')

    print ('Longest word = ' + purple + str(word_stats['longest_word']) + normal +
           ' (' + purple + str(word_stats['max_length']) + normal + ')')

    out.write('Longest word = ' + str(word_stats['longest_word']) +
           ' (' + str(word_stats['max_length']) + ')\n')

    print ('Shortest word = ' + purple + str(word_stats['shortest_word']) + normal +
           ' (' + purple + str(word_stats['min_length']) + normal + ')')

    out.write('Shortest word = ' + str(word_stats['shortest_word']) +
           ' (' + str(word_stats['min_length']) + ')\n')

    print ('Mean word length /chars = ' + purple + str(word_stats['mean_length']) +
            normal)

    out.write('Mean word length /chars = ' + str(word_stats['mean_length']) + '\n')

    print ('Total words parsed = ' + purple +
            str(word_stats['total_words']).split('.')[0] + normal)

    out.write('Total words parsed = ' +
            str(word_stats['total_words']).split('.')[0] + '\n')

    print ('Total chars parsed = ' + purple + str(word_stats['total_chars']) +
            normal)

    out.write('Total chars parsed = ' + str(word_stats['total_chars']) + '\n')

    print_n_word_frequencies(count_words, args.top_n, out)
    print_n_word_frequencies(count_pairs, args.top_n, out)
    print_n_word_frequencies(count_triples, args.top_n, out)
    print_n_word_frequencies(count_quads, args.top_n, out)
    print_n_word_frequencies(count_5_words, args.top_n, out)

    total_dev = 0.0

    print '\n===' + blue + ' FREQUENCY ANALYSIS ' + normal + '==='
    out.write('\n=== FREQUENCY ANALYSIS ===\n')

    for char in sorted(word_stats['char_percentages'].iterkeys()):
        bar = ''
        perc = word_stats['char_percentages'][char]

        # Percentage deviation from random distribution of characters.
        dev = 100.0 * (abs((100.0 / 26.0) - perc) / (100.0 / 26.0))
        total_dev += dev

        for i in range(0, int(perc)):
            bar += '#'

        print (char + ' |' + red + bar + normal + ' ' + str(perc)[:4] +
                '% (' + str(dev)[:4] + '% deviation from random)')

        out.write(char + ' |' + bar + ' ' + str(perc)[:4] + '% (' +
                str(dev)[:4] + '% deviation from random)\n')

    print ('\nTotal percentage deviation from random = ' +
            str(total_dev).split('.')[0] + '%')

    out.write('\nTotal percentage deviation from random = ' +
            str(total_dev).split('.')[0] + '%')

    average_dev = total_dev / 26.0

    print ('Average percentage deviation from random = ' +
            str(average_dev)[:4] + '%')

    out.write('\nAverage percentage deviation from random = ' +
              str(average_dev)[:4] + '%')

    print '\nWritten results to ' + args.inputfile.split('.')[0] + '-stats.txt\n'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Perform letter, word and n-tuple frequency analysis on text files.')
    parser.add_argument('--filename', '-f', dest='inputfile', required=True, help='Text file to parse.')
    parser.add_argument('--top', '-t', dest='top_n', required=False, default=20, type=int, help='List the top t most frequent n-words')
    args = parser.parse_args()

    count_words = collections.Counter()
    count_pairs = collections.Counter()
    count_triples = collections.Counter()
    count_quads = collections.Counter()
    count_5_words = collections.Counter()

    # Read in all of the words in a file
    print "[+] Analysing '" + args.inputfile + "'"
    words = re.findall(r"['\-\w]+", open(args.inputfile).read().lower())

    for word in words:
        word = word.strip(r"&^%$#@!")
        word_pair = ''
        word_triple = ''
        word_quad = ''

        length = len(word)

        # Record longest word length
        if length > word_stats['max_length']:
            word_stats['max_length'] = length
            word_stats['longest_word'] = word

        # Record shortest word length
        if length < word_stats['min_length']:
            word_stats['min_length'] = length
            word_stats['shortest_word'] = word

        # Keep track of the total number of words and chars read.
        word_stats['total_chars'] += length
        word_stats['total_words'] += 1.0

        # Note the charaters in each word.
        for char in word:
            if char.lower() in word_stats['char_counts']:
                word_stats['char_counts'][char.lower()] += 1.0

        # Tally words.
        count_words[word] += 1

        if previous_word != '':
            # Tally word-pairs.
            word_pair = previous_word + ' ' + word
            count_pairs[word_pair] += 1

        if previous_pair != '':
            # Tally word-triples
            word_triple = previous_pair + ' ' + word
            count_triples[word_triple] += 1

        if previous_triple != '':
            # Tally word-quads
            word_quad = previous_triple + ' ' + word
            count_quads[word_quad] += 1

        if previous_quad != '':
            # Tally word-quads
            word_5 = previous_quad + ' ' + word
            count_5_words[word_5] += 1

        previous_word = word
        previous_pair = word_pair
        previous_triple = word_triple
        previous_quad = word_quad

    # Calculate the mean word length
    word_stats['mean_length'] = word_stats['total_chars'] / word_stats['total_words']

    # Calculate relative character frequencies
    for char in word_stats['char_counts']:
        char_count = word_stats['char_counts'][char]
        total_chars = word_stats['total_chars']
        percentage = 100.0 * (char_count / total_chars)
        word_stats['char_percentages'][char] = percentage

    # Print results
    out = open(args.inputfile.split('.')[0] + '-stats.txt', 'w')
    print_results(word_stats, out)
    out.close()
