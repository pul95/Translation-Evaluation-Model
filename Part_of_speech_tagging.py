import codecs
import pickle
import spacy

#English Sentence Corpus
input2 = open("eng-hin-src.txt",encoding="utf8") 
input3 = input2.read()

#Hindi Sentence Corpus
with codecs.open("eng-hin-mt.txt", encoding='utf-8')as f:
    input1 = f.read()

#Creating list of English Hindi Sentence Pairs
English_sentence_list = input3.split("\n")

Hindi_sentence_list = input1.split("\n")

#Length of each sentence in the given parallel corpus
len_eng = []#list containing length of each sentence in english dataset
len_hindi = []#list containg length of each sentence in Hindi Dataset

for i in English_sentence_list:
    s = len(i.split(" "))
    len_eng.append(s)

for i in Hindi_sentence_list:
    s = len(i.split(" "))
    len_hindi.append(s)

#Plotting the graph between length of english and hindi sentences.
import matplotlib.pyplot as plt

plt.scatter(len_eng, len_hindi)
plt.title('Scatter plot between length of english sentence and hindi sentence')
plt.xlabel('English sentence length')
plt.ylabel('Hindi sentence length')
plt.show()

#Chunking in English Sentence

nlp = spacy.load('en')

chunk_text_list=[]  #chunks of English sentences
chunk_text_label=[] #POS tags for english chunks

for temp in  English_sentence_list:
    doc = nlp(temp)
    a=[]
    b=[]
    for chunk in doc.noun_chunks:
        a.append(chunk.text)
        b.append(chunk.label_)
    chunk_text_list.append(a)
    chunk_text_label.append(b)

#Saving the lists for future use to save time
with open('chunk_tags.pickle', 'wb') as f:
    pickle.dump([chunk_text_list, chunk_text_label], f)

with open('chunk_tags.pickle', 'rb') as f:
    chunk_text_list, chunk_text_label = pickle.load(f)
    
g = open('INPFILE.out', encoding='ISO-8859-1') #INPFILE contains output of Shallow Parser of Hindi Tags
Hindi_tags = g.read()

hindi_list = Hindi_tags.split("</Sentence>")

import re
from collections import Counter
#chunk level Hindi Tags
chunk_hindi_tags = [] #chunk level tags of hindi sentences
sentence_hindi_tags = [] #word level pos tags of hindi sentence
for i in hindi_list:
    a = re.split('\(\(', i)
    temp = []
    clt = []
    for j in a:
        if j==a[0]:
            continue
        else:
            s = re.findall('[A-Z]+', j)
            if 'S' in s:
                s.remove('S')
            if 'NM' in s:
                count = Counter(s)
                count = dict(count)
                for i in range(count['NM']):
                    s.remove('NM')
            clt.append(s[1:])
            temp.append(s[0])
    sentence_hindi_tags.append(clt) 
    chunk_hindi_tags.append(temp)
    
    print(chunk_hindi_tags[0]) #Chunk level tags for first Hindi Sentence in corpus
    print(chunk_text_label[0]) #Chunk level tags for first English Sentence in corpus
 #Word level POS tags for given sentences

hindi_words_tags = [] #List of POS tags for Hindi sentences 
for i in range(len(sentence_hindi_tags)):
    temp=[]
    for j in sentence_hindi_tags[i]:
        temp.extend(j)
    hindi_words_tags.append(temp)
    
    
#POS Tagging English
import spacy

nlp = spacy.load('en_core_web_sm')


POS_eng = [] #Initializing List containing POS of all English sentence
TAG_eng = [] #Initializing List containing TAG of all English sentence

for temp in  English_sentence_list:
    doc = nlp(temp)
    a=[]
    b=[]
    for token_eng in doc:
        a.append(token_eng.pos_)
        b.append(token_eng.tag_)
    POS_eng.append(a)
    TAG_eng.append(b)

#Saving the POS_eng and TAG_eng variables to use it later
import pickle

with open('POS_TAG_eng.pickle', 'wb') as f:
    pickle.dump([POS_eng, TAG_eng], f)
    
#Loading variables in our program
with open('POS_TAG_eng.pickle', 'rb') as f:
    POS_eng, TAG_eng = pickle.load(f)
    
print(hindi_words_tags[1]) # POS tag for Hindi Sentence 2
print(TAG_eng[1]) #POS tag for English Sentence 2
