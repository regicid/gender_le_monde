"""
Script to calculate the masculinity rate and names from an given url
"""

import os
import sys
import pandas as pd
import newspaper as np
from datetime import date, timedelta
import datetime
from glob import glob
import numpy
import spacy
import gn_modules.processing.processings.masculinity_rate_and_names as masculinity
nlp = spacy.load("fr_core_news_md")


def process_text_one_article(txt: str):
    """
    Match names from the names_df to the article text and comput the masculinity_rate as the mean
    of each name masculinity.
    """
    # Method without NER extraction (the found first names are matched with any token in the text)
    names_df = __get_names_df()
    txt = masculinity.MasculinityRateAndNames().normalize_txt(txt)
    doc = nlp(txt)
    ents = [ent.text for ent in doc.ents if ent[0].ent_type_ == "PER"]
    if ents:
        # TODO: this assumes that the first tok of the ent is always the first name
        flattened_ents = [ent.split()[0].strip("«».").lower() for ent in ents]
        ner_tokens = pd.DataFrame(flattened_ents, columns=["word"])
        txt_tokens_with_name = pd.merge(ner_tokens, names_df, how='left').dropna(
            subset=["sexratio_prenom"], inplace=False)
        _names = txt_tokens_with_name["word"]
        print(txt_tokens_with_name['sexratio_prenom'])
        m_rate = txt_tokens_with_name['sexratio_prenom'].sum()
    else:
        m_rate = None
        _names = None
    return (m_rate, _names)




def __get_names_df() -> pd.DataFrame:
    """
    Return a pandas dataframe from the data/prenoms_clean.csv file.
    """
    name_file = 'https://raw.githubusercontent.com/getalp/genderednews/cc64c5d5c448ceb6172905a719ee8c5b3d95753c/gn_modules/processing/processings/data/prenoms_clean.csv'
    names_df = pd.read_csv(name_file, sep=';')
    names_df = names_df.rename(columns={'preusuel': 'word'})
    return names_df





start_date = date(1944,12,19)
#start_date = date(1997,1,10)
end_date = date(2023,12,31)
day_count = (end_date - start_date).days + 1
dates = [d for d in (start_date + timedelta(n) for n in range(day_count)) if d <= end_date]


#years = []
#months = []
#days = []
Dates = []
names = []

for date in dates:
    month = date.month
    if month<10:month = "0"+str(month)
    day = date.day
    if day<10:day = "0" + str(day)
    files = glob(f"/opt/bazoulay/louis/{date.year}_{month}_{day}*")
    txt = ""
    for file in files:
        txt += open(file,"r").read()
    a = process_text_one_article(txt)
    if a[0] is not None:
        names.append(numpy.unique(a[1],return_counts=True))
    else:
        names.append([])
    #years.append(date.year)
    #months.append(month)
    #days.append(day)
    Dates.append(date)
    print(date)


result = pd.DataFrame(dates[:len(men)])
result["men"] = men
result["total"] = total


results = list()
for i in range(len(names)):
    if(len(names[i])>0):
        df = pd.DataFrame(names[i][0],columns = ["names"])
        df["n"] = names[i][1]
        df["date"] = Dates[i]
        results.append(df)
    print(Dates[i])

a = pd.concat(results)