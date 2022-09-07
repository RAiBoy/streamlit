import streamlit as st
import pandas as pd
import numpy
import requests
from bs4 import BeautifulSoup
import os
from medcat.cat import CAT
import re
from wikiapi import WikiApi
from zipfile import ZipFile

st.title('ExplainHealth')

def medterm_identify(text):

    source_list = []
    pretty_list = []

    entities = cat.get_entities(text)

    jargon_class_list = [['Injury or Poisoning'], ['Acquired Abnormality'], ['Laboratory Procedure'], ['Antibiotic'], ['Disease or Syndrome'], ['Pharmacologic Substance'], ['Organ or Tissue Function'], ['Gene or Genome'], ['Immunologic Factor'], ['Cell'], ['Tissue'], ['Congenital Abnormality'], ['Body Space or Junction'], ['Medical Device'], ['Pathologic Function'], ['Diagnostic Procedure'], ['Embryonic Structure'], ['Cell Component']]

    for key in entities['entities']:
        types = entities['entities'][key]['types']
        if types in jargon_class_list:

          pretty = entities['entities'][key]['pretty_name']
          source = entities['entities'][key]['source_value']
          source_list.append(source)
          pretty_list.append(pretty)

    return source_list, pretty_list

def translation(source,med):

    wiki_dict = {}
    for i in range(len(med)):
        results = wiki.find(med[i])
        length = len(results)

        if len(results) == 0:
            continue

        else:
            if len(med[i]) == len(results[0].lower()):
                article = wiki.get_article(results[0])
                summary = article.summary
                m = re.match(search, summary)
                wiki_first = m.group(1)
                if "may refer to:" not in wiki_first:
                    wiki_dict[source[i]] = wiki_first

    return wiki_dict

def output(text, dict):

    c = "<!DOCTYPE html><style>.tooltip {position: relative;display: inline-block;border-bottom: 1px dotted black;}.tooltip .tooltiptext {visibility: hidden;width: 120px;background-color: black;color: #fff;text-align: center;border-radius: 6px;padding: 5px 0;/* Position the tooltip */position: absolute;z-index: 1;bottom: 100%;left: 50%;margin-left: -60px;}.tooltip:hover .tooltiptext {visibility: visible;}</style><body style='text-align:left;'>"
    for key, value in dict.items():
        combin = '<div class="tooltip">'+key+'<span class="tooltiptext">'+value+'</span></div>'

        text = text.replace(key, combin)
    a = c + text

    return a

file = st.text_input('records')

if st.button('translate'):

    cat = CAT.load_model_pack('medmen_wstatus_2021_oct')
    med_terms,prettys = medterm_identify(file)

    wiki = WikiApi()
    wiki = WikiApi({ 'locale' : 'en'})

    search = re.compile(r"^([^.]*).*")
    wiki_dict = translation(med_terms,prettys)

    output = output(file, wiki_dict)
    st.markdown(output, unsafe_allow_html=True)
