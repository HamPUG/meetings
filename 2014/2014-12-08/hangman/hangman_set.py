#!/usr/bin/python3
'''
Open a dictionary and extract words suitable for hangman
Use issubset for filtering.

References on using sets:
http://www.python-course.eu/python3_sets_frozensets.php
https://docs.python.org/3.4/library/stdtypes.html#set
https://docs.python.org/3/tutorial/datastructures.html
'''
import time
DICTIONARY_FILE = '/usr/share/dict/british-english'
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 20

valid_letter_set = set('abcdefghijklmnopqrstuvwxyz')
word_set = set('')

def file_exists(filename):
    '''Check for existance of the dictionary'''
    try:
        with open(filename, 'r') as f:
            return True
    except IOError:
        return False 
        
# hangman_list[] Consists of 18 lists based on length of word
# Lawerence's method of initializing the list of lists         
hangman_list = list([] for i in range(MIN_WORD_LENGTH, MAX_WORD_LENGTH + 1))

junk = []

if file_exists(DICTIONARY_FILE) == False:
#if file_exists(DICTIONARY_FILE) == False:
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
        # if it ends with a \n then strip off the \n 
        word = word[:-1] if word.endswith('\n') else word 
        
        # load the word set
        word_set.clear()
        word_set = set(word)

        # Are the letters in the word a subset of the valid letters set
        # See: http://www.python-course.eu/python3_sets_frozensets.php
        
        if word_set.issubset(valid_letter_set):        
            #print(word_set, word) 

            # Based on the words length copy it into its list.
            if len(word) >= 21:
                # 21 characters or more discard
                pass

            elif len(word) >= MIN_WORD_LENGTH and len(word) <= MAX_WORD_LENGTH:
                hangman_list[len(word)-MIN_WORD_LENGTH].append(word)
                
                # Insert 3 to 20 character words in [0] to [17]
                #3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
                #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
                
            else:
                #ignore any blank lines
                #ignore 1 and 2 letter words
                pass            

        else:
            junk.append(word)
            
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

    print('Total words discarded: {}'.format(len(junk)))
    
    
    #with open("junk.txt", 'w') as w:
    #    for i in range(len(junk)):
    #        w.write(junk[i] + '\n')
 
'''       
Time taken:0.924
Total words in hangman_list: 62763
ace
act
abed
abet
counterrevolutionary 20
Total words discarded: 36300

Words in sets look like this...   
{'O', 'i', 'o', 'h'}            #Ohio <-- needs propernoun stripped Eg. eBay
{'s', 'e', 'a', 'n', 'c', "'"}  #acne's <-- needs apostrophy stripped       
{'a', 'e', 'b', 'i', 'd'}       #abide <== Good
  
'''


