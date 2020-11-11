# markov_analysis
This project implements Markov analysis for text prediction from a given text file. Utilizes urllib.request to read text file from project gutenberg. 
The program works by first gathering a text file of a book from project gutenberg. Words are then stripped of punctuation. 
A dictionary is then created for that book, with each unique word being a key, and the words that follow it composing a list as that key's value.
So if the word 'he' is followed in the book at different times by 'went', 'said', 'will', 'needs', 'went', 'said', 'said', and 'can', then 
the entry in our dictionary would be wordDic['went'] = ['went', 'said', 'will', 'needs', 'went', 'said', 'said', 'can']. 
Then, when we predict a sentence, a word is chosen at random from our value list. Since words appear in different frequencies,
the probability of any word these words following 'went' is probabilistically chained to how often each word actually follows 'went' in our book.
If we wanted to predict a 10-word sentence, and our second word cosen is 'said,' then our next word will be chosen from the dictionary values
for the key 'said'. So our sentence becomes 'he said'...some word, up through ten words.
