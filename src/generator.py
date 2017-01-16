"""
Program to read a list of words and generate some levels for the word game. The
levels should contain a few words made up with the same letters (but not
necessarily using all the letters). 
Example: The letters are ifno. The words would be if, in, no, of, on.

Author: Brandon Hostetter
Date: 1 January 2016
"""

import sys, json

def readWords(fileName):
    """
    Read a list of words from a text file.

    Args: 
        fileName: name of the file to be read

    Returns:
        words: the list of words
    """
    f = open(fileName, 'r')
    words = []
    
    for index, line in enumerate(f):
        words.append(line.rstrip())

    words.sort()
    f.close()
    return words

def listWithMinLength(words, minLength):
    return [word for word in words if len(word) >= minLength]

def listWithExactLength(words, exactLength):
    return [word for word in words if len(word) == exactLength]

def findLettersInWord(word):
    """
    Take a word return a dictionary where each key is a letter in the word and 
    each value is the number of times that letter appears in the word.

    Args: 
        word
    
    Returns:
        letters: dict of letter frequency found in 'word'
    """
    letters = {}
    
    for char in word:
        if char in letters:
            letters[char] = letters[char] + 1
        else:
            letters[char] = 1
    return letters

def findWordPairs(words, wordLength, matchesMinLength):
    """
    First, get a list of words that are the exact length of 'wordLength'. This
    will be the list of words we get a list of letters from (we want this list
    to be sufficiently large so we have a decent pool of letters to build other
    words from). Next, loop over each word in this new list and get a list of
    words from 'words' that can be constructed with just the letters provided
    in the word from 'wordsWithExactLength'.

    Args:
        words: list of all words
        wordLength: the length we want each word in 'words' to be when we 
            search for letters in it
        matchesMinLength: the minimum length of the list of words that can
            be constructed with a given set of letters

    Returns:
        possibleWords: the list of lists containing words that can be
            constructed with some set of letters
        possibleWordsLetters: the list of dicts containing the letters
            used to construct the words in the cooresponding index of
            'possibleWords'
    """
    wordsWithExactLength = listWithExactLength(words, wordLength)
    possibleWords = []
    possibleWordsLetters = []

    for index, word in enumerate(wordsWithExactLength):
        letters = findLettersInWord(wordsWithExactLength[index])
        possEntry = findWordsMadeFromLetters(words, letters)
        if len(possEntry) >= matchesMinLength:
            possibleWords.append(possEntry)
            possibleWordsLetters.append(letters)

    return possibleWords, possibleWordsLetters

def findWordsMadeFromLetters(words, letters):
    possWords = []
    
    for word in words:
        copy = letters.copy()
        validWord = True

        for char in word:
            if char not in copy:
                validWord = False
                break
            copy[char] = copy[char] - 1
            if copy[char] < 0:
                validWord = False
                break

        if validWord:
            possWords.append(word)
    return possWords

def formatLists(wordsList, lettersList):
    wordsList = [sorted(words, key=len) for words in wordsList]
    lettersListArr = []

    for letters in lettersList:
        arr = []
        for letter in sorted(letters.keys()):
            for number in range(letters[letter]):
                arr.append(letter)
        lettersListArr.append(arr)

    return wordsList, lettersListArr

def exportJSON(wordsList, lettersList):
    counter = 1

    for words, letters in zip(wordsList, lettersList):
        outputObj = {}
        outputObj['words'] = words
        outputObj['letters'] = letters
        with open('./levels/level_' + str(counter).zfill(3) + '.json', 'w') as outfile:
            json.dump(outputObj, outfile)

        counter += 1
    return

def printPretty(wordList, letterList):
    for letters, words in zip(letterList, wordList):
        print('Letters', letters)
        print('Words: ', words)
    return

def main():
    """
    The main method to generate levels.
    """
    # words = readWords('./words/google-10000-english-master/google-10000-english-usa-no-swears-short.txt')
    # https://gist.github.com/deekayen/4148741
    words = readWords('./words/1-1000.txt')
    # Remove any 1 letter words
    words = listWithMinLength(words, 2)
    possibleWords, possibleWordsLetters = findWordPairs(words, 5, 3)
    possibleWords, possibleWordsLetters = formatLists(possibleWords, possibleWordsLetters)
    # printPretty(possibleWords, possibleWordsLetters)
    exportJSON(possibleWords, possibleWordsLetters)

    return

# Call the main method to begin program
if __name__ == '__main__':
    main()