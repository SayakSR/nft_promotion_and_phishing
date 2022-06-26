from nltk.corpus import stopwords # Import the stop word list
from nltk.tokenize import wordpunct_tokenize
from stop_words import get_stop_words


with open('./profile_desc.txt', 'r', encoding='utf8') as f:
    words = f.read().split()

d = {}

stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
stop_words.extend(nltk_words)

for w in words:
    if w not in stop_words:
        if w in d:
            d[w] += 1
        else:
            d[w] = 1

lst = sorted([(d[w],w) for w in d],reverse=True)
print (stop_words)
print ([word for word in lst if word not in stop_words])
print('\n The 50 most frequent words are /n')

word_list=[]

i = 1
for count, word in lst[:500]:
    if(word.isalpha()):
        word=word.lower()
        word_list.append(word)
    i += 1

print(len(word_list))

# Creating unique wordlist 

wordlist_unique = []
for i in word_list:
    if i not in wordlist_unique:
        wordlist_unique.append(i)

print(len(wordlist_unique))
print(wordlist_unique)

with open('word_list.txt', 'w') as f:
    for item in wordlist_unique:
        f.write("%s\n" % item)