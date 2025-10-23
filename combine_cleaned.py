# Author: Arwin Sepahram 
#Date last edited: August 14

import pandas as pd
import numpy as np


def main():
    file_names_list2020 = [
        "censusprofile2021_WV_clean.csv", "censusprofile2021_NV_clean.csv",
        "censusprofile2021_BUR_clean.csv", "censusprofile2021_AB_clean.csv",
        "censusprofile2021_MR_clean.csv", "censusprofile2021_CW_clean.csv",
        "censusprofile2021_SR_clean.csv","censusprofile2021_RM_clean.csv",
        "censusprofile2021_CQ_clean.csv","censusprofile2021_WR_clean.csv",
        "censusprofile2021_PM_clean.csv","censusprofile2021_LG_clean.csv"]
    

    file_names_list2015 = [
        "censusprofile2016_WV_clean.csv", "censusprofile2016_NV_clean.csv",
        "censusprofile2016_BUR_clean.csv", "censusprofile2016_AB_clean.csv",
        "censusprofile2016_MR_clean.csv", "censusprofile2016_CW_clean.csv",
        "censusprofile2016_SR_clean.csv","censusprofile2016_RM_clean.csv",
        "censusprofile2016_CQ_clean.csv","censusprofile2016_WR_clean.csv",
        "censusprofile2016_PM_clean.csv","censusprofile2016_LG_clean.csv"]
    


    cities = ["west van", "north van", "burnaby", "abbotsford", 
              "maple ridge", "chilliwack", 'surrey', "richmond", 'coquitlam', 'white rock',
              "port moody", "langley"]

    income_numbers_20 = []
    income_numbers_15 = []
    pop_20 = []
    pop_15 = []
    degree_20 = []
    degree_15 = []
    Immigrants_20 = []
    Immigrants_15 = []
    one_parent20 =[]
    one_parent15 = []

    #These for loop just iterate through the file names and read them one by one
    for fname in file_names_list2020:
        df = pd.read_csv(fname, low_memory=False)
        #Eq essentially means where it equals that string, so average tax after income here 
        avg_finder = df["Characteristic"].eq("Average after-tax income of household in 2020 ($)")
        pop_finder = df['Characteristic'].eq('Population, 2021')
        #There are two fields for bachelor, this will grab the first which is what we want. (15 years and above)
        degree_finder =df['Characteristic'].eq("Bachelor's degree or higher")
        imm_finder = df['Characteristic'].eq('Immigrants')
        one_parent_finder = df['Characteristic'].eq('One-parent-family households')
        val_in = int(df.loc[avg_finder, "Total"].iloc[0])
        val_pop = int(df.loc[pop_finder, "Total"].iloc[0])
        val_deg = int(df.loc[degree_finder, "Total"].iloc[0])
        val_imm = int(df.loc[imm_finder, "Total"].iloc[0])
        val_onepa = int(df.loc[one_parent_finder, "Total"].iloc[0])
        income_numbers_20.append(val_in)
        pop_20.append(val_pop)
        degree_20.append(val_deg)
        Immigrants_20.append(val_imm)
        one_parent20.append(val_onepa)
    #All into the dataframe
    df_2020 = pd.DataFrame({
        "city": cities,
        "avg income (AT)": income_numbers_20,
        "bachelor or above": degree_20,
        "population": pop_20,
        "immigrants": Immigrants_20,
        "lone parent": one_parent20,
        "year": 2020
    })

    #Need a rate column, raw numbers are not of much use.
    df_2020["bachelor rate"] = (df_2020["bachelor or above"]/df_2020["population"]) * 100
    df_2020["immigrant rate"] = (df_2020["immigrants"]/df_2020["population"]) * 100
    df_2020['lone parent rate'] = (df_2020['lone parent']/df_2020['population']) * 100

    for fname in file_names_list2015:
        df = pd.read_csv(fname, low_memory=False)
        #Eq essentially means where it equals that string, so average tax after income here 
        avg_finder = df["Characteristic"].eq("Average after-tax income of households in 2015 ($)")
        pop_finder = df['Characteristic'].eq('Population; 2016')
        degree_finder =df['Characteristic'].eq("University certificate; diploma or degree at bachelor level or above")
        imm_finder = df['Characteristic'].eq('Immigrants')
        one_parent_finder = df['Characteristic'].eq('Total lone-parent families by sex of parent')
        val_in = int(df.loc[avg_finder, "Total"].iloc[0])
        val_pop = int(df.loc[pop_finder, "Total"].iloc[0])
        val_deg = int(df.loc[degree_finder, "Total"].iloc[0])
        val_imm = int(df.loc[imm_finder, "Total"].iloc[0])
        val_onepa = int(df.loc[one_parent_finder, "Total"].iloc[0])
        income_numbers_15.append(val_in)
        pop_15.append(val_pop)
        degree_15.append(val_deg)
        Immigrants_15.append(val_imm)
        one_parent15.append(val_onepa)

    #Making the dataframe, year is fixed for them.
    df_2015 = pd.DataFrame({
        "city": cities,
        "avg income (AT)": income_numbers_15,
        "bachelor or above": degree_15,
        "population": pop_15,
        'immigrants': Immigrants_15,
        "lone parent": one_parent15,
        "year": 2015
    })

    #Need a rate column, raw numbers are not of much use.
    df_2015["bachelor rate"] = (df_2015['bachelor or above']/ df_2015['population'])* 100
    df_2015["immigrant rate"] = (df_2015['immigrants']/ df_2015['population'])* 100
    df_2015['lone parent rate'] = (df_2015['lone parent']/df_2015['population']) * 100
    df_combined = pd.concat([df_2015, df_2020], ignore_index=True)

    df_combined = df_combined.sort_values(by = ['year','avg income (AT)'], ascending=False )
    df_combined = df_combined.reset_index()
    df_combined = df_combined.drop('index', axis = 1)
    df_combined.to_csv('censusdatajoint.csv', index=False)

if __name__ == "__main__":
    main()
