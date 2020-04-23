######################################### IMPORTING LIBRARIES #################################################
import os
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0
import re
import pandas as pd
import numpy as np
import platform
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import warnings


import spacy
from spacy.lang.en.stop_words import STOP_WORDS as SW_en
from spacy.lang.es.stop_words import STOP_WORDS as SW_es

from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

######################################### DEFINING PARAMETERS #################################################

key_words_DA = ['data analyst', 'analisis de datos',
                      'data analytics', 'analitica de datos',
                      'business analyst', 'analisis de negocios',
                      'sql',
                      'python',
                      'business intelligence', 'inteligencia de negocios', ' bi ',
                      'excel', 'microsoft office', 'ms office',
                      'dashboard', 'kpi',
                      'reporting', 'informes',
                      'tableau', 'powerbi', 'power bi', 'microsoft bi', 'qlik', 'spotfire',
                      ]

key_words_DS = ['data analyst', 'analisis de datos',
                      'data analytics', 'analitica de datos',
                      'business analyst', 'analisis de negocios',
                      'sql',
                      'python',
                      'business intelligence', 'inteligencia de negocios', ' bi ',
                      'excel', 'microsoft office', 'ms office',
                      'dashboard', 'kpi',
                      'reporting', 'informes',
                      'tableau', 'powerbi', 'power bi', 'microsoft bi', 'qlik', 'spotfire',
                      ]

key_words_DE = ['data engineer', 'ingeniero de datos',
                       'sql', 'nosql', 'no sql', 'bases de datos no relacionales',
                       'python', ' r ', 'scala', 'java ', 'spark', 'hadoop', 'haddop' 'hive', 'impala', 'kafka',
                       'data wrangling', 'limpieza de datos',
                       'etl', 'extract, transform and load', 'map reduce', 'mapreduce',
                       'data acquisition', 'adquisicion de datos',
                       'big data', 'bigdata', 'bigquery',
                       'data warehouse',
                       ' aws ', 'azure',
                       'software engineering'
                       ]

dic_key_words = \
    {'data analyst'    : key_words_DA,
     'data scientist'  : key_words_DS,
     'data engineer'   : key_words_DE,
     'analista datos'  : key_words_DA,
     'cientifico datos': key_words_DS,
     'ingeniero datos' : key_words_DE
     }

# Defining current date time
now = datetime.now()
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
now_file = now_str.replace(':', '.')

# Warnings
warnings.simplefilter(action="ignore")

# Pandas tables configuration
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

######################################### ANALYZING DATA #################################################
def analyzing_data(df_profile, df_jobs):

    # LINKEDIN PROFILE
    profile_name = df_profile.loc['profile','info']
    profile_open = df_profile.loc['open new jobs', 'info']
    if profile_open == True:
        open_to_jobs = "YES"
    else:
        open_to_jobs = "NO"
    years_of_experience = df_profile.loc['total years', 'info']
    profile_headline = df_profile.loc['headline', 'info']

    # LINKEDIN JOB SEARCH
    location    = df_jobs.loc[0, 'LOCATION']
    date_search = df_jobs.loc[0, 'SEARCH DATETIME']
    result_jobs = df_jobs.shape[0]

    print(f"""
    *******************  OPTIMIZED JOB SEARCH ON LINKEDIN *******************

    *********** DATA ANALYSIS:
    
    > LINKEDIN PROFILE: {profile_name}
    Headline: {profile_headline}
    Open to job offers? : {open_to_jobs}
    Years of experience: {years_of_experience} years

    > LINKEDIN JOB SEARCH:
    Location: {location}
    Search Datetime: {date_search} 
    Raw results: {result_jobs} 
    """)

    print('\r   ... Click to continue\r')
    input()

    print('\n   *** MATCHING PROFILE\n')

    ### CLEANING JOBS

    # JOB TITLE_ID < concat
    df_jobs['JOB TITLE_ID'] = df_jobs.apply(lambda x: x['JOB TITLE'] + "_" + str(x['Current Job Id']), axis=1)
    df_jobs.drop_duplicates(subset='JOB TITLE_ID', keep='first', inplace=True)

    ### ANALYZING JOBS > PANDAS

    # New column identifying the language of Job Description
    df_jobs['Info Language'] = df_jobs['Job Description'].apply(lambda x: detect(x))
    unique_languages = list(df_jobs['Info Language'].unique())

    # Identifying how many times is every job post repeated on the list
    unique_jobs = list(df_jobs['JOB TITLE'].unique())
    pivot_ID_TITLES = pd.pivot_table(df_jobs,
                                     values="LOCATION",
                                     index=['Current Job Id'],
                                     columns=['JOB TITLE'],
                                     aggfunc=np.count_nonzero
                                     ).reset_index()
    unique_results = pivot_ID_TITLES.shape[0]
    pivot_ID_TITLES['Multiple Job Post'] = ""
    for j in unique_jobs:
        pivot_ID_TITLES[j] = pivot_ID_TITLES[j].apply(lambda x: job_key_generator(j) if x == 1.0 else '')
        pivot_ID_TITLES['Multiple Job Post'] = pivot_ID_TITLES['Multiple Job Post'] + pivot_ID_TITLES[j] + '-'
    df_jobs = df_jobs.merge(pivot_ID_TITLES[['Current Job Id', 'Multiple Job Post']], on='Current Job Id', how='left')


    # JOB DEFINITIONS > Coincidences with definitions for each job:
    coincidences_jobs = []
    for j in unique_jobs:
        skills_list = dic_key_words.get(j)  # dictionary
        jkey = job_key_generator(j)
        coincidences_jobs.append(f'{jkey} coincidences')
        df_jobs[f'{jkey} coincidences'] = \
            df_jobs['Job info'].apply(lambda x:      coincidencias(skills_list, clean_text(x)))
        df_jobs[f'{jkey} coincidences_list'] = \
            df_jobs['Job info'].apply(lambda x: list_coincidencias(skills_list, clean_text(x)))

    # PROFILE > Coincidences with profile skills for each job:
    profile_skills = clean_text(df_profile.loc['skills', 'info'])
    profile_skills = profile_skills.replace('[', '').replace(']', '').replace("'", "").split(', ')
    df_jobs['PROFILE coincidences'] = \
        df_jobs['Job info'].apply(lambda x:      coincidencias(profile_skills, clean_text(x)))
    df_jobs['PROFILE coincidences_list'] = \
        df_jobs['Job info'].apply(lambda x: list_coincidencias(profile_skills, clean_text(x)))

    top = int(input(f"""
    Your profile has been compared with every job in the list!
    >>> There are {unique_results} unique job posts
    
    How many matches would you like to see in a table?:
    > """))

    # Creating table
    df_top_jobs = df_jobs \
        .drop_duplicates(subset='Current Job Id', keep='first') \
        .sort_values(by=['PROFILE coincidences'], ascending=False).head(top) \
        [['Job name', 'Company name', 'Company location', 'Posted date', 'Employment Type',
         'Easy apply','Job html', 'Multiple Job Post','Info Language','PROFILE coincidences'] + coincidences_jobs
        ] # 'JOB TITLE','Seniority Level',
    # Creating links
    df_top_jobs['Job html'] = df_top_jobs['Job html'].apply(lambda x: f'<a href={x}>link</a>')

    # Exporting to html
    # render dataframe as html
    html = df_top_jobs.to_html(escape=False)
    # write html to file
    if platform.system() == 'Linux':
        text_file = open(f"data/results/TOP_LIST/top_{top}_jobs_in_{location}.html", "w")
        text_file.write(html)
        text_file.close()
        print(f"""
    >>> Table has been saved as: data/results/TOP_LIST/top_{top}_jobs_in_{location}.html
    """)
    elif platform.system() == 'Windows':
        text_file = open(f"\\data\\results\\TOP_LIST\\top_{top}_jobs_in_{location}.html", "w")
        text_file.write(html)
        text_file.close()
        print(f"""
    >>> Table has been saved as: data\\results\\TOP_LIST\\top_{top}_jobs_in_{location}.html
    """)

    print('\r   ... Click to continue\r')
    input()

    ### ANALYZING JOBS > NLP

    # Loading libraries
    print('''\n   *** APPLYING NLP\n
    ... Loading NLP libraries''')
    nlp_en = spacy.load('en_core_web_md')
    nlp_es = spacy.load('es_core_news_md')

    # Creating blacklist
    black_list = [location,
                 'empresa', 'work', 'skill',
                 'parir', 'comer', 'timar',
                 'job', 'industry', 'type', 'employment', 'full', 'functions', 'seniority', 'level',
                 'company', 'experience', 'help', 'time', 'new', 'role', 'use', 'year', 'enable',
                ]

    # Creating corpus / filtered tokens / common_words
    dict_corpus = {}
    dict_filtered_corpus = {}
    dict_filtered_tokens = {}
    dict_word_freq = {}
    dict_common_words_100 = {}

    # dict_filtered_corpus_NN = {}
    # dict_filtered_tokens_NN = {}
    # dict_word_freq_NN = {}
    # dict_common_words_100_NN = {}

    print('''\n    ... Analyzing job posts''')
    print(f"""\n    Files will be saved with frequency of words: """)

    # Each job / each language
    for job in unique_jobs:
        job_key_s = job_key_generator(job)

        for lang in unique_languages:

            # CORPUS
            filter_job = df_jobs['JOB TITLE'] == job
            filter_lang = df_jobs['Info Language'] == lang
            corpus = df_jobs['Job Description'][filter_job & filter_lang].str.cat(sep=" || ")

            dict_corpus.update({f'{job_key_s}_{lang}': corpus})

            # TOKENS
            if lang == 'en':
                tokens = nlp_en(corpus)
                STOP_WORDS = SW_en
            elif lang == 'es':
                tokens = nlp_es(corpus)
                STOP_WORDS = SW_es

            filtered_corpus = ""
            filtered_tokens = []
            # # NOUNS
            # filtered_corpus_NN = ""
            # filtered_tokens_NN = []

            for word in tokens:
                lemma = word.lemma_.lower().strip()
                NN = word.pos_.lower().strip()

                if lemma not in STOP_WORDS and re.search('^[a-z]+$', lemma) and lemma not in black_list and len(
                        lemma) > 1:
                    filtered_corpus += lemma + " "
                    filtered_tokens.append(lemma)

                    # # NOUNS
                    # if word.pos_ == 'NOUN':
                    #     filtered_corpus_NN += lemma + " "
                    #     filtered_tokens_NN.append(lemma)

            dict_filtered_corpus.update({f'{job_key_s}_{lang}': filtered_corpus})
            dict_filtered_tokens.update({f'{job_key_s}_{lang}': filtered_tokens})

            # # NOUNS
            # dict_filtered_corpus_NN.update({f'{job_key_s}_{lang}': filtered_corpus_NN})
            # dict_filtered_tokens_NN.update({f'{job_key_s}_{lang}': filtered_tokens_NN})

            # 100 COMMON WORDS
            word_freq = Counter(filtered_tokens)
            common_words_100 = word_freq.most_common(100)
            dict_word_freq.update({f'{job_key_s}_{lang}': word_freq})
            dict_common_words_100.update({f'{job_key_s}_{lang}': common_words_100})

            # # NOUNS
            # word_freq_NN = Counter(filtered_tokens_NN)
            # common_words_100_NN = word_freq_NN.most_common(100)
            # dict_word_freq_NN.update({f'{job_key_s}_{lang}': word_freq_NN})
            # dict_common_words_100_NN.update({f'{job_key_s}_{lang}': common_words_100_NN})

            if platform.system() == 'Linux':
                print(f'    >>> data/results/WORD_FREQ/dict_word_freq{job_key_s}_{lang}_{now_file}.json')
                with open(f'data/results/WORD_FREQ/dict_word_freq{job_key_s}_{lang}_{now_file}.json', 'w') as fp:
                    json.dump(dict_word_freq, fp)
            elif platform.system() == 'Windows':
                with open(f'data\\results\\WORD_FREQ\\dict_word_freq{job_key_s}_{lang}_{now_file}.json', 'w') as fp:
                    json.dump(dict_word_freq, fp)

    print('\r   ... Click to continue\r')
    input()

    ### ANALYZING JOBS > CLOUD

######################################### FUNCTIONS #################################################
def coincidencias(job_skills, post_skills):
    c = 0
    for i in job_skills:
        if re.search(i, post_skills):
            c += 1
    return c


def list_coincidencias(job_skills, post_skills):
    l = []
    for i in job_skills:
        if re.search(i, post_skills):
            l.append(i)
    return l


def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('/', ' ')
    text = text.replace('á', 'a')
    text = text.replace('é', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o')
    text = text.replace('ú', 'u')
    text = text.replace('.', ' ')
    text = text.lower()

    return text


def job_key_generator(job):
    job_key_s = ""
    job_name_splitted = job.split(" ")
    for string in job_name_splitted:
        job_key_s += string[0].upper()

    return job_key_s

