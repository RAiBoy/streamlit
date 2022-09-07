#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import nltk
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import time
import requests
import random
import os
import numpy as np
import syllables


# In[2]:


def sylco(word) :

    return syllables.estimate(word)


# In[3]:


# coding=utf-8
import requests
from lxml import html


# In[4]:


# flesch reading ease score
def flesch_reading_ease (word_num, sentence_num, syllable_num):

#     flesch reading ease formula
    score = 206.835 - 1.015 * (word_num/sentence_num) - 84.6 * (syllable_num/word_num)

#     classify the resource according to flesch reading ease score
    if score <=10.0 and score > 0.0:
        readability_class = 'professional'
    elif score <=30.0 and score > 10.0:
        readability_class = 'college graduate'
    elif score <=50.0 and score > 30.0:
        readability_class = 'college'
    elif score <=60.0 and score > 50.0:
        readability_class = '10th to 12th grade'
    elif score <=70.0 and score > 60.0:
        readability_class = '8th & 9th grade'
    elif score <=80.0 and score > 70.0:
        readability_class = '7th grade'
    elif score <=90.0 and score > 80.0:
        readability_class = '6th grade'
    elif score <=100.0 and score > 90.0:
        readability_class = '5th grade'
    else:
        readability_class = 'easy'

    return (score, readability_class)




def cal(t):
    input_string = t
    input_words = input_string.split()

    syllable = 0
    for word in input_words:
        syllable += sylco(word)

    sentence = len(sent_tokenize(input_string))

    word = len(input_words)

    score, page_class = flesch_reading_ease(word, sentence, syllable)

    return score, page_class


# In[6]:


path = "/Users/congwang/Downloads/input_2/"

ex_list = [4]

input_score_list = []
class_list = []

for i in range(337):
    f = open(path+str(i)+".txt", "r")
    input_string = f.read()
    f.close()
    cal(input_string)
    input_words = input_string.split()

    syllable = 0
    for word in input_words:
        syllable += sylco(word)

    sentence = len(sent_tokenize(input_string))

    word = len(input_words)


    score, page_class = flesch_reading_ease(word, sentence, syllable)

    input_score_list.append(int(score))
    class_list.append(page_class)


# In[38]:


input_score_list
len(input_score_list)


# In[51]:


import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

df_score_input = pd.DataFrame({'input':input_score_list})

plt.hist(df_score_input)
plt.title('Readability score of the original EHRs')
plt.ylabel('The amount of EHRs')
plt.xlabel('Readability score')
plt.show()


df_score_input


# In[16]:


print(class_list.count('college'))
print(class_list.count('college graduate'))
print(class_list.count('professional'))


# In[18]:


path = "/Users/congwang/Downloads/output_readability/"

output_score_list = []
output_class_list = []

for i in range(337):
# for i in ex_list:
    f = open(path+str(i)+".txt", "r")
    input_string = f.read()
#     print(input_string)
    f.close()
    input_words = input_string.split()

    syllable = 0
    for word in input_words:
        syllable += sylco(word)

    sentence = len(sent_tokenize(input_string))

    word = len(input_words)

    score, page_class = flesch_reading_ease(word, sentence, syllable)

#     print(sentence, word, syllable)
#     print(i, score, page_class)
    output_score_list.append(int(score))
    output_class_list.append(page_class)


# In[19]:


x = np.arange(1,338,1)
y = output_score_list
figure(num=None, figsize=(20,18), dpi=80, facecolor='w', edgecolor='r')
sns.barplot(x=x, y=y)
plt.title('Readability score of the explained EHRs')
plt.xlabel('EHRs index')
plt.ylabel('Readability score')
plt.show()


# In[32]:


import pandas as pd

data_box = [input_score_list, output_score_list]

df_box = pd.DataFrame({'input': input_score_list,
                       'output': output_score_list})

sns.boxplot(x='variable',y='value',data=pd.melt(df_box)).set(xlabel='EHRs',ylabel='Readability score')


csvfile = df_box.to_csv("/Users/congwang/Downloads/csvfile.csv",index=False)


# In[18]:


print(max(output_score_list))
print(min(output_score_list))
print(np.mean(output_score_list))


# In[20]:


print(output_class_list.count('college'))
print(output_class_list.count('college graduate'))
print(output_class_list.count('professional'))
