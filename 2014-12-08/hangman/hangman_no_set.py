#!/usr/bin/python3
'''
Open a dictionary and extract words suitable for hangman
Original Code: Using combinational filtering.
'''
import time
DICTIONARY_FILE = '/usr/share/dict/british-english'
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 20

def file_exists(filename):
    '''Check for existance of a file that can be read'''
    try:
        with open(filename, 'r') as f:
            return True
    except IOError:
        return False 
        
# hangman_list[] Consists of 18 lists based on length of word
# Lawerence's method of initializing the list of lists        
hangman_list = list([] for i in range(MIN_WORD_LENGTH, MAX_WORD_LENGTH + 1))

if file_exists(DICTIONARY_FILE) == False:
    print( '\nError: Dictionary file {0} is unavailable. \n'
        'Maybe you are not using Linux? Exiting...'.format(
        DICTIONARY_FILE))  # '/usr/share/dict/british-english'
    sys.exit()

# Word in dictonary should be a single word on a line and newline character 
# Hangman rules: Need to ensure / filter out:
#   no blank lines
#   last line might not have a newline
#   line should not have any spaces
#   no words with apostrophies
#   lower case a to z, so no propernames, or names like "eBay".
#       
    
with open(DICTIONARY_FILE, 'r') as f:
    start_time = time.process_time()
    for word in f:
        # Filter out proper nouns, based on first chacacter is upper case.
        #if not word[0].isupper():
        if word[0].islower():

            # Filter out words with apostrophies
            #if not word.find("'") >= 0:
            if word.find("'") == -1:

                # Filter out French words. Start with é. 
                # éclair, éclairs, éclat, élan, émigré, 
                # émigrés, épée, épées, étude, études
                # Huh? 'creche' is not in the dictionary. Too French?
                # Python2 requires 2nd line to be # -*- coding: utf-8 -*-
                # Otherwise SyntaxError: Non-ASCII character '\xc3' 

                if word.find("é") == -1:

                    if word.find("û") == -1:
                                                                                             
                        # strip off the \n
                        word = word[0:len(word)-1]

                        # Based on the words length copy it into its list.
                        if len(word) >= 21:
                            # 21 characters or more discard
                            pass

                        elif len(word) >= MIN_WORD_LENGTH and \
                                len(word) <= MAX_WORD_LENGTH:
                            # Insert 3 to 20 character words in [0] to [17]
                            #3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
                            #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
                            hangman_list[len(word)-MIN_WORD_LENGTH].append(word)

                        else:
                            #ignore any blank lines
                            #ignore 1 and 2 letter words
                            pass    
    
    
    end_time = time.process_time()    
    elapsed_time = end_time - start_time
    print('Time taken:{:.3f}'.format(elapsed_time)) 
          
    total_words = 0
    for i in range(len(hangman_list)): #18
        total_words = total_words + len(hangman_list[i])
     
    print('Total words in hangman_list: {}'.format(total_words))    
    print(hangman_list[0][0])
    print(hangman_list[0][1])
    print(hangman_list[1][0])
    print(hangman_list[1][1])
    print(hangman_list[17][0], len(hangman_list[17][0]))   

'''
Time taken:0.334
Total words in hangman_list: 62802
ace
act
abed
abet
counterrevolutionary 20
'''

