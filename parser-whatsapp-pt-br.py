import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def startsWithDate(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}) ([0-9][0-9]):([0-9][0-9]) -'
    # Expressão regular do formato de data
    result = re.match(pattern, s)
    if result:
        return True
    return False


def startsWithAuthor(s):
    pattern = '([+]\d{2} \d{2} \d{5}\D\d{4})'
    # Expressão regular que identifica o autor não salvo no formato de número Brasileiro
    result = re.search(pattern, s)
    if result:
        return True
    return False


def getDataPoint(line):
    # line = 19/10/18 23:58 - ‪+55 11 98207-0044‬: bolsonaro tem muito trabalho
    
    splitLine = line.split(' - ') # splitLine = ['19/10/18 23:58', '+55 11 98207-0044‬: bolsonaro tem muito trabalho']
    
    dateTime = splitLine[0] # dateTime = '19/10/18 23:58'
    
    date, time = dateTime.split(' ') # date = '19/10/18'; time = '23:58'
    
    message = ' '.join(splitLine[1:]) # message = '+55 11 98207-0044‬: bolsonaro tem muito trabalho'
    
    if startsWithAuthor(message): # True
        splitMessage = message.split(': ') # splitMessage = ['+55 11 98207-0044‬', 'bolsonaro tem muito trabalho']
        author = splitMessage[0] # author = '+55 11 98207-0044‬'
        message = ' '.join(splitMessage[1:]) # message = 'bolsonaro tem muito trabalho'
    else:
        author = None
    return date, time, author, message


parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
conversationPath = 'b17.txt' 

with open(conversationPath, encoding="utf-8") as fp:
    fp.readline() # Skipping first line of the file (usually contains information about end-to-end encryption)
        
    messageBuffer = [] # Buffer to capture intermediate output for multi-line messages
    date, time, author = None, None, None # Intermediate variables to keep track of the current message being processed
    
    while True:
        line = fp.readline() 
        if not line: # Stop reading further if end of file has been reached
            break
        line = line.strip() # Guarding against erroneous leading and trailing whitespaces
        if startsWithDate(line): # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
            if len(messageBuffer) > 0: # Check if the message buffer contains characters from previous iterations
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) # Save the tokens from the previous message in parsedData
            messageBuffer.clear() # Clear the message buffer so that it can be used for the next message
            date, time, author, message = getDataPoint(line) # Identify and extract tokens from the line
            messageBuffer.append(message) # Append message to buffer
        else:
            messageBuffer.append(line) # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer
            
df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
df.head()            
   

