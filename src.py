
#%%
import urllib.request
from string import punctuation
from string import whitespace
import numpy as np

#%%
def cleanse(word):
    '''
    This function removes punctuation and whitespace from word,
    the string that we pass as an argument

    Parameters
    word: str

    Returns
    cleaned: str
    '''

    cleaned = '' # we will only include non whitespace, non punctuation characters
    for char in word:
        if ((char in whitespace) or (char in punctuation)):
            pass
        else:
            cleaned += char.lower()
    return cleaned

#%%
def gatherBook(url):
    with urllib.request.urlopen(book) as file_object:
        # *** demarcates actual text of book in gutenberg files
        words = file_object.read().decode('utf-8-sig').split('***')[2]
        words = words.split()
    return words

#%%
if __name__ == '__main__':
    word = 'hey there,. '
    print(cleanse(word))
#%%
def make_word_dict(word_list):
    '''
    This function will create a dictionary of key-value pairs of form word-wordcount,
    with wordcount being the number of times each respective word appears in word_list

    Parameters
    word_list: list 
        list of words created from full text file, 
        preferably cleansed of punctuation and whitespace
    
    Returns
    myDict: dict 
        dict of key-value pairs of word-wordcount
    
    '''

    myDict = {}
    for word in word_list:
        if word not in myDict:
            myDict[word] = 1 # add word to myDict if word not already in myDict
        else:
            myDict[word] += 1 # increase value += 1 if word already in myDict

    return myDict

#%%
if __name__ == '__main__':
    url = 'http://www.gutenberg.org/cache/epub/61995/pg61995.txt'
    words = gatherBook(url)
    bookDict = make_word_dict(words)
    print(bookDict)


#%%
def make_markov_dict(cleansedWords, n):
    '''
    This function will create a dictionary whose keys are n-word-length prefixes,
    and whose values are lists of 1-word suffixes that follow those prefixes.
    The longer the prefix, the more specific that prefix is, and as such, the value
    corresponding to that prefix, which is a list of suffixes, will be shorter

    the values in this dictionary will be lists of words. These lists, which will 
    include repeats, will help us determine, probabilistically, which word/suffix
    should follow any argued n-word-length prefix

    Parameters
    cleansedWords: list 
        list of words with punctuation and whitespace stripped
    n: int 
        length of prefix that you want to be utilized in markov analysis
    
    Returns
    markovDict: dict 
        dictionary of form key = 'word1 word2...wordn', value = [worda, wordb, wordc, ...]
        where word1 word2...wordn are all possible n-length prefixes gathered from text,
        and worda, wordb,... are all possible suffixes for each of those n-length prefixes

    '''

    preSubList = []
    for i in range(len(cleansedWords) - n):
        preSubList.append(cleansedWords[i:i+n+1])
        # this will create a list of lists of words so we can analyze n-word prefixes
        # so if you want to analyze suffixes for a a 2-word entry, you create a dictionary
        # with all two-word entries as keys, and we'll then enter suffixes as values in that dict
    markovDict = {}
    for _ in preSubList:
        strings = _[0]
        for i in range(1, n):
            strings = strings + ' ' + _[i] # we're creating a string of n-length, which is our prefix length
        if strings not in markovDict:
            markovDict[strings] = [_[n]] #add suffix, which is _[n] to our dictionary
        else:
            markovDict[strings].append(_[n]) # our values are lists, so we append to them if a prefix is already present as a key

    return markovDict

#%%
if __name__ == '__main__':
    url = 'http://www.gutenberg.org/cache/epub/61995/pg61995.txt'
    words = gatherBook(url)
    
    markovDict = make_markov_dict(words, 2)
    ml = list(enumerate(markovDict.items()))
    print(ml[200:210])
    

#%%
def generate_suffixes(markovDict, prefix):
    '''
    Parameters
    markovDict : dict
        dictionary created using function make_markov_dict
    prefix : str
        prefix that you would like to generate suffixes for

    Returns
    sortedTups : list of tuples
        list of sorted tuples containing (suffix, count), corresponding to prefix input.
    alternatively, if you argue a prefix that is not present in markovDict, then a message will alert you
    '''

    tupList = []
    seenList = []
    try:
        for _ in markovDict[prefix]:
            if _ not in seenList:
                seenList.append(_)
                tupList.append((_, markovDict[prefix].count(_)))
                # this list of tuples does not HAVE to be sorted, but it's useful if we want 
                # to quickly visualize the frequency of suffixes for a given prefix
        sortedTups = sorted(tupList, key = lambda x: x[1], reverse = True)
        
        return sortedTups

    except (KeyError):
        return f'"{prefix}" is not present as a key in your markov Dictionary'

#%%
if __name__ == '__main__':
    url = 'http://www.gutenberg.org/cache/epub/61995/pg61995.txt'
    words = gatherBook(url)
    
    markovDict = make_markov_dict(words, 2)
    
    sortedTups = generate_suffixes(markovDict, 'He said')
    print(sortedTups)

    sortedTups = generate_suffixes(markovDict, 'yolo ay')
    print(sortedTups)

#%%

def predict_sentence(cleansed_words, prefix, n):
    '''
    Parameters
    cleansed_words : list
        List of words from text with whitespace and punctuation removed (though the function will also accept words with punctuation).
    prefix : str
        String you want your generated sentence to begin with.
    n : int
        Number of times you want predict_sentence to predict a suffix.

    Returns
    sentence : str
        Predicted sentence with n suffixes predicted.

    '''
    multiDict = make_markov_dict(cleansed_words, len(prefix.split()))
    prefix = prefix.lower()
    # we convert to lower because our cleanse function automatically converts to lower
    sentence = prefix #initialize our sentence to just be our prefix
    
    for _ in range(n-1):
        sortedTups = generate_suffixes(multiDict, prefix) #find suffixes for our prefix from multiDict
        words, nums = list(zip(*sortedTups)) #doing this to produce a list of frequences we can use for np.random.choice
        denom = sum(nums)
        probs = [_ / denom for _ in nums]
        suffix = np.random.choice(words, p = probs) 
        #select suffix based on probability of being chosen
        #np.random.choice is useful here because it maps list of words to list of thier frequencies (probs)
        sentence = sentence + ' ' +  suffix #add suffix to our sentence
        
        prefix = sentence.split()[-len(prefix.split()):] # redefining prefix by dropping first word from previous prefix
        prefix = (' ').join(prefix)
        
    return sentence

#%%
if __name__ == '__main__':
    url = 'http://www.gutenberg.org/cache/epub/61995/pg61995.txt'
    words = gatherBook(url)

    cleansedWords = [cleanse(word) for word in words]

    print(predict_sentence(cleansedWords, 'he said', 10)) 
    # this will predict an 11-word sentence (first input word, plus 10 suffixes)
    

