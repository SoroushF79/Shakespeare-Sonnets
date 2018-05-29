import tweepy
import urllib, urllib.request, nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup as bs
import numpy.random as np


file = open("Added Stop Words.txt", "r")
file_m = file.read()
words = []

for i in file_m:
    words.append(i)
file.close()

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

stop_words = set(stopwords.words("english"))
for i in stop_words:
    if i not in words:
        words.append(i)



theurl = "http://sonnetaday.com/about.php"
thepage = urllib.request.urlopen(theurl)
soup = bs(thepage, "html.parser")

sonnet = soup.find_all("span")[4].text

actual_sonnet = nltk.tokenize.word_tokenize(sonnet)



filtered = []
        
string1 = ""
string2 = ""
count = 0

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

print(j)
string1 = "Sonnet " + filtered[0][0:count]
string2 = filtered[0][count:]
filtered[0] = string1 + " " + string2


for i in filtered:
    if (((filtered.index(i) % 13) == 0) and (i not in words) and (filtered.index(i) != 0)):
        filtered[filtered.index(i)] = death[np.randint(0, 61)]
    elif(((filtered.index(i) % 13) == 0) and (i in words)):
        for q in range(filtered.index(i), len(filtered)):
            if ((filtered[q] not in words) and (q != 0)):
                filtered[q] = death[np.randint(0, 60)]
                break
        
        
print(filtered)      

finished = ""
for i in filtered:
    if((i != ",") and (filtered.index(i) != 0) and (i != ";") and (i != "!") and (i != "?") and (i != ":")):
        finished += " " + i
    else:
        finished += i
 
print(finished)

"""
auth = tweepy.OAuthHandler("Iu2bL60n8TBJN4XU40Q95qT3G", "x4plYdRldb2zdhqzVu2kqWYSmh4P35Y9uw1JIXL8eSbAaUt139")
auth.set_access_token("2556368518-ah0T6Qi5zMYu7HQcVDbynv3mz6smYeIwlXP5Tij","qGGWJMXubP3WEEmAJUJP5UztTpBDmS4u3OXlDBMBBtm8S")

api = tweepy.API(auth)

api.update_status(finished)
"""