# -*- coding: utf-8 -*-
import sys
s=sys.argv[1]

# Function to analyse the frequency of letters in a given string
def freqAnalyse(string, percentage=False):
    # count number of letters in the string
    letterCount = float(len(string))

    # dictionary to hold letters in the string with their frequency
    letterFrequency = {}

    # loop through each letter in the string
    for letter in string:

        # if percentage is set to false, calculate frequency as letter count
        if percentage == False:
            # if letter is in the list, increment its count
            # if its not in the list, add it
            if letter in letterFrequency:
                letterFrequency[letter] += 1
            else:
                letterFrequency[letter] = 1

        # if percentage is set to true, calculate frequency as percentage
        else:
            # if letter is in the list, increment its percentage
            # if its not in the list, add it
            if letter in letterFrequency:
                letterFrequency[letter] += (1.0 / letterCount) * 100
            else:
                letterFrequency[letter] = (1.0 / letterCount) * 100

    # sort the list and return it
    return sorted(letterFrequency.items(), key=lambda x: x[1], reverse=True)


# Function to split a given string into columns
def splitColumn(string, length):
    # dictionary to hold the final columns as they are being constructed
    finalColumns = {}

    # loop over the string and split it into columns
    count = 1
    for letter in string:
        if count <= length:
            if count in finalColumns:
                finalColumns[count] += letter
            else:
                finalColumns[count] = letter
            count += 1
        else:
            finalColumns[1] += letter
            count = 2

    # return the dictionary holding the columns
    return finalColumns


# Function to frequency analyse columns
def columnFreqAnalyse(columns, maxFrequent):
    # dictionary to hold the frequency analysis of each column
    columnFrequcies = {}

    # frequency analyse each column and
    # store the result in the dictionary
    for column in columns:
        columnFrequcies[column] = freqAnalyse(columns[column])[0:maxFrequent]

    # return the dictionary with the results
    return columnFrequcies


# Function to find the shift value between two letters
def findShiftValue(firstLetter, secondLetter, alphabet):
    # work out the shift
    # for letter in alphabet:
    #	if letter[0] == firstLetter:
    #		index1 = letter[1]
    #	if letter[0] == secondLetter:
    #		index2 = letter[1]

    if type(firstLetter) == str:
        index1 = alphabet[firstLetter]
    else:
        index1 = firstLetter

    if type(secondLetter) == str:
        index2 = alphabet[secondLetter]
    else:
        index2 = secondLetter

    # if the first letter comes before the second then
    # shift value is found by: alphabetLength - (index1 - index2)
    if index1 > index2:
        shiftValue = len(alphabet) - (index1 - index2)

    # if the second letter comes before the first then
    # shift value is found by: index1 - index2
    else:
        shiftValue = index1 - index2

    # return the shift value as a positive integer
    return abs(shiftValue)


# Function to find the smallest shift from a list of letters
def findSmallestShift(letters, shiftValueOccuranceList, alphabet, frequentLetters):
    # letters are received in this format:
    # [('r', 17), ('v', 15), ('a', 11)]

    # shiftValueOccuranceList is received in this format:
    # [5, 8, 14]

    # dictionary to hold the shift value of each letter
    letterShiftValues = {}

    # loop through shift values
    for shiftValue in shiftValueOccuranceList:

        # loop through each letter
        for letter in letters:

            # shift each letter by current shiftValue and
            # get the location in the alphabet of the resulting letter
            resultingShift = findShiftValue(shiftValue, letter[0], alphabet) - 1

            # find the resulting letter after the shift
            for alphabetLetter in alphabet:
                if alphabet[alphabetLetter] == resultingShift + 1:
                    resultingLetter = alphabetLetter

            # find the frequency of the resulting letter and
            # if it is in the dictionary, incrememnt it. if not in dictionaty, add it
            resultingLetterFrequency = frequentLetters.index(resultingLetter) + 1

            if shiftValue in letterShiftValues:
                letterShiftValues[shiftValue] += resultingLetterFrequency
            else:
                letterShiftValues[shiftValue] = resultingLetterFrequency

    # find the shift value that has the lowest frequency
    lowestFrequencyShift = min(letterShiftValues, key=letterShiftValues.get)

    # return smallest shift
    return lowestFrequencyShift


# Function to find the keyword from shift values
def findKeyword(shiftValues, alphabet):
    # string to hold the keyword
    keyword = ""

    # sort the shift values by key
    sortedKeys = sorted(shiftValues.keys())

    # find the correstponding value for each shift
    for key in sortedKeys:

        for letter in alphabet:
            if alphabet[letter] - 1 == shiftValues[key]:
                correstpondingLetter = letter
                break

        # append it to the keyword
        keyword += correstpondingLetter

    # return the keyword
    return keyword


# Function to decipher the ciphertext using a keyword
def decipher(cipherTextColumns, keyword, alphabet):
    # dictionary to hold the deciphered columns
    clearColumns = {}

    # string to hold the cleartext
    clearText = ""

    # loop through columns
    for column in cipherTextColumns:

        # clear text for each column will be stored in this variable as it is being deciphered
        columnClearText = ""

        # get the shift value using the corresponding letter of the keyword
        columnShiftValue = alphabet[keyword[column - 1]] - 1

        # shift every letter in the column to get the clear letter
        for letter in cipherTextColumns[column]:

            letterPosition = alphabet[letter] - 1

            # shift the letter to find the clear letter

            # shift value is greater than the position of the letter in the alphabet
            if columnShiftValue > letterPosition:

                clearLetterPosition = len(alphabet) - (columnShiftValue - letterPosition)

                for alphabetLetter in alphabet:
                    if alphabet[alphabetLetter] == clearLetterPosition + 1:
                        clearLetter = alphabetLetter

                        # append the clear letter to column clear text
                        columnClearText += clearLetter

                        break

            # shift value is less than the position of the letter in the alphabet
            else:
                for alphabetLetter in alphabet:
                    if alphabet[alphabetLetter] == letterPosition - columnShiftValue + 1:
                        clearLetter = alphabetLetter

                        # append the clear letter to column clear text
                        columnClearText += clearLetter

                        break

        # add the decipher column to clearColumns
        clearColumns[column] = columnClearText

    # go through each clear column to construct the cleartext
    totalColumns = len(clearColumns)
    columnNumber = 1
    while columnNumber <= totalColumns:

        if len(clearColumns[columnNumber]) > 0:

            clearText += clearColumns[columnNumber][0]
            clearColumns[columnNumber] = clearColumns[columnNumber][1:]
            if columnNumber < totalColumns:
                columnNumber += 1
            else:
                columnNumber = 1

        else:
            columnNumber = totalColumns + 1

    # return the cleartext
    return clearText


# Main function
def main():
    ################################## INITIAL SETUP ##################################

    keywordLength = 12
    cipherTextFile = "ciphertext.txt"

    alphabet = {'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5, 'е': 6, 'ё': 7, 'ж': 8, 'з': 9, 'и': 10, 'й': 11,
                'к': 12, 'л': 13, 'м': 14, 'н': 15, 'о': 16, 'п': 17, 'р': 18, 'с': 19, 'т': 20, 'у': 21,
                'ф': 22, 'х': 23, 'ц': 24, 'ч': 25, 'ш': 26,'щ':27,'ъ':28,'ы':29,"ь":30,"э":31,"ю":32,"я":33}

    frequentLetters = ["о","е","а","и","н","т","с","р","в","л","к","м","д","п","у","я","ы","ь","г","з","б","ч","й","х","ж","ш","ю","ц","щ","э","ф","ъ","ё"]

    # how many of the most frequent letters of a column to get
    maxFrequent = 3

    # how many of the most frequent letters in the alphabet to compare to
    maxFrequentAlphabet = 8

    ###################################################################################

    # open ciphertext

    cipherText = "".join(s.split()).lower()

    # split ciphertext into columns
    cipherTextColumns = splitColumn(cipherText, keywordLength)

    # frequency analyse the ciphertext columns
    # and get the most frequent letters
    columnAnalysis = columnFreqAnalyse(cipherTextColumns, maxFrequent)

    # work out the shift values of each of the three letters
    # with the most frequent letters of the alphabet

    # dictionary to store the shift values of the 8*3 table for each column
    shiftValueDict = {}

    # dictionary to store the letter of the keyword corresponding to each column
    columnKeyLetter = {}

    for frequentLetter in frequentLetters[:maxFrequentAlphabet]:

        # work out shift values for each column
        for column in columnAnalysis:

            # work out shift values of each letter in the column and
            # store them in the dictionary
            for columnLetter in columnAnalysis[column]:

                # get shift value from columnLetter to frequentLetter
                shiftValue = findShiftValue(frequentLetter, columnLetter[0], alphabet)

                # and store it in shiftValueDict
                if column not in shiftValueDict:
                    shiftValueDict[column] = {}
                shiftValueDict[column][columnLetter[0] + frequentLetter] = shiftValue

            if frequentLetter == frequentLetters[maxFrequentAlphabet - 1]:
                # list of all of the shift values
                shiftValues = list(shiftValueDict[column].values())
                # make a dictionary of how many times each value occurs
                shiftValueOccurance = dict((i, shiftValues.count(i)) for i in shiftValues)

                # check if only one value occurs 3 times
                if list(shiftValueOccurance.values()).count(3) == 1:
                    # this value is this column's key letter
                    for value in shiftValueOccurance:
                        if shiftValueOccurance[value] == 3:
                            columnKeyLetter[column] = value

                # check if multiple values occur 3 times
                elif list(shiftValueOccurance.values()).count(3) > 1:

                    # make a list of all values that occur three times
                    valueOccuranceThree = []
                    for value in shiftValueOccurance:
                        if shiftValueOccurance[value] == 3:
                            valueOccuranceThree.append(value)

                    # the value that gives the lowest frequency is this column's key letter
                    value = findSmallestShift(columnAnalysis[column], valueOccuranceThree, alphabet,
                                              frequentLetters)

                    # column's key letter is found, add it to the dictionary
                    columnKeyLetter[column] = value

                # check if only one value occures 2 times
                elif list(shiftValueOccurance.values()).count(2) == 1:
                    # this value is this column's key letter
                    for value in shiftValueOccurance:
                        if shiftValueOccurance[value] == 2:
                            columnKeyLetter[column] = value

                # check if multiple values occur 2 times
                elif list(shiftValueOccurance.values()).count(2) > 1:

                    # make a list of all values that occur two times
                    valueOccuranceTwo = []
                    for value in shiftValueOccurance:
                        if shiftValueOccurance[value] == 2:
                            valueOccuranceTwo.append(value)

                    # the value that gives the lowest frequency is this column's key letter
                    value = findSmallestShift(columnAnalysis[column], valueOccuranceTwo, alphabet,
                                              frequentLetters)

                    # column's key letter is found, add it to the dictionary
                    columnKeyLetter[column] = value

                else:
                    # at this point there shouldn't be a duplicate in the shiftValueOccurance table
                    # the value that gives the lowest frequency is this column's key letter
                    value = findSmallestShift(columnAnalysis[column], shiftValueOccurance.keys(),
                                              alphabet, frequentLetters)

                    # column's key letter if found, add it to the dictionary
                    columnKeyLetter[column] = value

    # find the keyword from shift values
    keyword = findKeyword(columnKeyLetter, alphabet)

    # decipher the ciphertext
    clearText = decipher(cipherTextColumns, keyword, alphabet)

    print (
    "KEYWORD: ", keyword)

    print (
    "CLEARTEXT: ", clearText)
   


main()
