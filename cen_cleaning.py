# Author: Arwin Sepahram 
#Date last edited: August 14

import pandas as pd 
import numpy as np
import re
from pathlib import Path


#The purpose of this file is to make it easier to navigate the census data. 
#We don't need these rows.
list_of_drops_rows = ['Mother tongue', 'Language spoken most often at home', 
                          'Knowledge of languages', "Ethnic or cultural origin", 
                          'Religion','Language used most often at work',
                          'All languages used at work', 'Other language(s) used regularly at work',
                          'Citizenship', 
                          'Selected places of birth for the immigrant population',
                          'Admission category and applicant type',
                          'Pre-admission experience',
                          'Visible minority',
                          'Mobility status 5 years ago',
                          'Mobility status 1 year ago',
                          'Main mode of commuting',
                          'Selected places of birth for the recent immigrant population ',
                          'Location of study compared with province or territory of residence',
                          'First official language spoken',
                          'All languages spoken at home',
                          'Age at immigration',
                          'Other language spoken regularly at home',
                          ]

def cleaner_2021(filename):
    #The first 3 rows are absolutely useless (Idk why they do it this way...)
    file = pd.read_csv(filename, encoding="cp1252", low_memory=False, skiprows = 3)
    messydf = file 
    # We don't need the starting rows nor the ending rows (there is an essay at the end lol)
    #The keyword is 'symbols:', in every dataset everything after that is useless
    x = messydf['Topic'] == 'Symbols:'
    x = x.tolist()
    if True in x:
         position = x.index(True)
         messydf = messydf.iloc[:position]
    #Getting rid of useless stuff
    # I can't seem to figure out a way to do this with apply() or without a loop unfortunately. 
    for i in list_of_drops_rows:
        to_drop_rows = messydf['Topic'].str.contains(i, case=False, na=False, regex=False)
        messydf = messydf[~to_drop_rows]

    #We don't need these columns 
    #Lets do a regex to drop the flag stuff, there are duplicates of each 
    flag_dropper = re.compile(r'_Flag(?:\.\d+)?$')
    messydf = messydf.drop(['Note'], axis = 1)
    to_drop_col = messydf.columns[messydf.columns.str.contains(flag_dropper)]
    messydf = messydf.drop(columns=to_drop_col, errors='ignore')
    # lots of empty columns for some reason
    messydf = messydf.dropna(axis=1, how='all')

    #They named the percentages the same as other columns. :/
    #Since pandas renames duplicates with .1, we can change them to perc
    messydf = messydf.rename(columns = {'Men+':'Men','Women+':'Wowen',"Total.1": 'Total_perc', "Men+.1": "Men_perc", 
                                        "Women+.1": "Women_perc"})
    #Gotta remove spaces at the end and start 
    messydf['Characteristic'] = messydf['Characteristic'].str.strip()


    return messydf



def cleaner_2016(filename):
    #Most of this one is the same as 2021 cleaner. 

    file = pd.read_csv(filename, encoding="cp1252", low_memory=False, skiprows = 1)
    messydf = file

    messydf = messydf.drop(index=messydf.index[0])

    x = messydf['Topic'] == 'Symbols:'
    x = x.tolist()
    if True in x:
         position = x.index(True)
         messydf = messydf.iloc[:position]
    
    for i in list_of_drops_rows:
        to_drop_rows = messydf['Topic'].str.contains(i, case=False, na=False, regex=False)
        messydf = messydf[~to_drop_rows]


    flag_dropper = r'(^Flag_.*|.*_Flag(?:\.\d+)?$)'
    messydf = messydf.drop(columns=['Note'], errors='ignore')
    messydf = messydf.drop(
        columns=messydf.columns[messydf.columns.str.contains(flag_dropper)],
        errors='ignore'
    )

    messydf = messydf.rename(columns = {'Male':'Men','Female':'Wowen', "Male.1": "Men_perc", 
                                        "Female.1": "Women_perc",'Characteristics' : 'Characteristic'})
    
    messydf['Characteristic'] = messydf['Characteristic'].str.strip()
    
    return messydf 


def clean_saver(filename, dataframe):
    src = Path(filename)
    out = src.with_name(src.stem + "_clean.csv")
    dataframe.to_csv(out, index=False, encoding="utf-8", na_rep="")



def main():

    name_list_2021 = ['censusprofile2021_NV.csv','censusprofile2021_AB.csv', 
                      'censusprofile2021_BUR.csv', 'censusprofile2021_CW.csv', 
                      'censusprofile2021_WV.csv', 'censusprofile2021_MR.csv',
                      'censusprofile2021_SR.csv','censusprofile2021_RM.csv',
                      'censusprofile2021_WR.csv','censusprofile2021_CQ.csv',
                      'censusprofile2021_PM.csv','censusprofile2021_LG.csv']
    
    name_list_2016 = ['censusprofile2016_NV.csv','censusprofile2016_AB.csv', 
                      'censusprofile2016_BUR.csv', 'censusprofile2016_CW.csv', 
                      'censusprofile2016_WV.csv', 'censusprofile2016_MR.csv',
                      'censusprofile2016_SR.csv','censusprofile2016_RM.csv',
                      'censusprofile2016_WR.csv','censusprofile2016_CQ.csv',
                      'censusprofile2016_PM.csv', 'censusprofile2016_LG.csv']

    for i in name_list_2021:
        df = cleaner_2021(i)
        clean_saver(i, df)



    for i in name_list_2016:
        df = cleaner_2016(i)
        clean_saver(i, df)

    #print(messydf.tail(3))
    #col_names = messydf.columns
    #print(col_names)
    #rows, cols = messydf.shape
    #print(f"Rows: {rows}, Columns: {cols}")

if __name__ == "__main__":
    main()