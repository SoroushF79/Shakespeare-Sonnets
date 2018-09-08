""" Created by Soroush Famili(Github SoroushF79) from 5/27/18 to 6/4/18. This script scrapes sonnetaday.org every other day 
for the sonnet that is posted. From then, approximately every 10th non-stopword is replaced by the name of a random 
dead Shakespearean character. The revised "sonnet" is then posted on Twitter. I did this with tweaking for a week on my 
Twitter account @FamilyWithAnI.
"""

import tweepy
import urllib, urllib.request, nltk
from bs4 import BeautifulSoup as bs
import numpy.random as np
import time


auth = tweepy.OAuthHandler("", "")
auth.set_access_token("","")
api = tweepy.API(auth)

#This part is to get the stopwords that we want to ignore into a list we can reference later

file = open("Added Stop Words.txt", "r")
file_m = file.read()
words = []

for i in file_m:
    words.append(i)
file.close()

#This part is to get the names of the dead Shakespearean characters into a list we can reference later
death = []

file = open("Everyone That Dies.txt", "r")
file_m = file.read()

string = ""
for i in file_m:
    if(i == "\n"):
        death.append(string)
        string = ""
    else:
        string += i
    
file.close()

# I use a function because I want the main loop to be a continuous while nd to only do the main stuff iff the time is correct

def TheFunc():
    # This is what parses the html of the sonnet, inserts the random dead character, and then tweets it. 
    # This first part finds the sonnet from within the html text and then uses nltk to tokenize the words 
    theurl = "http://sonnetaday.com/about.php"
    thepage = urllib.request.urlopen(theurl)
    soup = bs(thepage, "html.parser")
    
    sonnet = soup.find_all("span")[4].text
    actual_sonnet = nltk.tokenize.word_tokenize(sonnet)

    filtered = []
            
    string1 = ""
    string2 = ""
    count = 0
    
    # Counts the number of words/characters in the sonnet. Since Twitter has a max character length of 280 characters and
    # I don't want the sonnet to be cut mid-word, I must count the number of words and characters, here starting with the number of characters.
    for i in actual_sonnet[0]:
        count += 1
        if(i == "."):
            break
    
    counter = 0
    for i in actual_sonnet:
        counter += len(i)
        if(counter > 200):
            j = actual_sonnet.index(i) - 1
            break
        else:
            filtered.append(i)
    
    # To preface the tweet with the number of sonnet it is.
    string1 = "Sonnet " + filtered[0][0:count]
    string2 = filtered[0][count:]
    filtered[0] = string1 + " " + string2
    
    """
     To change the ~10th word to be the name of a random dead character. I didn't want to replace a stopword such as "it," "a," "when," etc. 
     or punctuation. I only wanted to change actual words so if the 10th word was a listed stopword it wouldn't be replaced. Rather, I'd move onto the next word,
     check that, etc. I also had to make sure that I was still within the Twitter 280 character limit.
     """
    for i in filtered:
        if (((filtered.index(i) % 13) == 0) and (i not in words) and (filtered.index(i) != 0)):
            filtered[filtered.index(i)] = death[np.randint(0, 61)]
        elif(((filtered.index(i) % 13) == 0) and (i in words)):
            for q in range(filtered.index(i), len(filtered)):
                if ((filtered[q] not in words) and (q != 0)):
                    try:
                        filtered[q] = death[np.randint(0, 59)]
                        break
                    except IndexError:
                        filtered[q] == 42

    finished = ""
    for i in filtered:
        if((i != ",") and (filtered.index(i) != 0) and (i != ";") and (i != "!") and (i != "?") and (i != ":") and (i != ".")):
            finished += " " + i
        else:
            finished += i
    
    print("Done") # For debugging purposes
    api.update_status(finished)
    

    """
    sonnetaday.org posts a new sonnet every other day so I don't want to upload a new sonnet everyday. Thus, I flip n between 1 and 2 
    and on the days when I don't want to tweet n becomes a 1 so I can tweet the next day, and the days that I do tweet I make n a 1 so it
    doesn't tweet the following day. I chose to tweet everyday at 12:00 pm Chicago time. However, I kept my code running on an 
    Amazon Web Services server which uses Universal time so it would 17:00 in Universal Time is 12:00 pm Chicago time.
    """
n = 2
while(True):

    localt = time.localtime(time.time())
    if((localt.tm_hour == 17) and (localt.tm_min == 0) and (localt.tm_sec >= 0) and (localt.tm_sec < 1) and (n == 2)):
        TheFunc()
        time.sleep(10)
        n = 1
    if((localt.tm_hour == 17) and (localt.tm_min == 0) and (localt.tm_sec >= 0) and (localt.tm_sec < 1) and (n == 1)):
        n = 2
        time.sleep(10)
        
