# Author: Arwin Sepahram 
#Date last edited: August 14

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from scipy.stats import linregress
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr
from scipy.stats import mannwhitneyu
from sklearn.cluster import KMeans


#Bunch of functions that calculate gorwth for income, population and degree holder number.
def in_growth(g):
    d15 = g.loc[g['year']==2015, 'avg income (AT)'].iloc[0]
    d20 = g.loc[g['year']==2020, 'avg income (AT)'].iloc[0]
    return (d20 - d15) / d15 * 100

def po_growth(g):
    d15 = g.loc[g['year']==2015, 'population'].iloc[0]
    d20 = g.loc[g['year']==2020, 'population'].iloc[0]
    return (d20 - d15) / d15 * 100


def deg_growth(g):
    d15 = g.loc[g['year']==2015, 'bachelor or above'].iloc[0]
    d20 = g.loc[g['year']==2020, 'bachelor or above'].iloc[0]
    return (d20 - d15) / d15 * 100


def main():
    seaborn.set_theme()
    df = pd.read_csv('censusdatajoint.csv')
    #Let's look at some graphs of average income after tax for each city for 2020
    #Is there a huge difference between incomes in these 6 different cities
    df2020 = df[df['year'] == 2020]
    df2015 = df[df['year'] == 2015]
    plt.bar(df2020['city'], df2020['avg income (AT)'])
    plt.xlabel('City')
    plt.ylabel('Average After-Tax Income ')
    plt.title('Average After-Tax Household Income by City (2020)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('avg_income_by_city_2020.png', dpi=300, bbox_inches='tight')
    plt.close()


    
    plt.bar(df2015['city'], df2015['avg income (AT)'])
    plt.xlabel('City')
    plt.ylabel('Average After-Tax Income ')
    plt.title('Average After-Tax Household Income by City (2015)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('avg_income_by_city_2015.png', dpi=300, bbox_inches='tight')
    plt.close()


    #Let's look at income growth
    income_growth = (df.groupby('city').apply(in_growth, include_groups=False).rename('income growth'))
    income_growth = income_growth.sort_values(ascending=False)
    print(income_growth.sort_values(ascending=False))
    print("Average growth for cities:", np.mean(income_growth.values))

    top_6 = income_growth.head(6)
    print("Top 6 cities by income growth:")
    print(top_6)

    bottom_6 = income_growth.tail(6)
    print("bottom 6 cities by income growth:")
    print(bottom_6)

    print("Average growth (Top 6):", np.mean(top_6.values))
    print("Average growth (Bottom 6):", np.mean(bottom_6.values))

    #West van has had a suspiciously low growth. But lower income cities are catching up. 
    plt.bar(income_growth.index, income_growth.values)
    plt.xlabel('City')
    plt.ylabel('Income growth')
    plt.title('income growth (AT) (2015 to 2020)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('Income growth (AT).png', dpi=300, bbox_inches='tight')
    plt.close()

    #Let's graph it, and look at a best fit line and it's p-value 
    slope, intercept, r_value, p_value, std_error = linregress(df2020['bachelor rate'], 
                                                               df2020['avg income (AT)'])
    print("Slope:",slope)
    print("P-value:",p_value)

    # Scatter plot and best fit line
    plt.figure(figsize=(8,5))
    plt.scatter(df2020['bachelor rate'], df2020['avg income (AT)'], label='Data points')
    plt.plot(df2020['bachelor rate'], intercept + slope * df2020['bachelor rate'], color='red', 
             label='Best fit line')

    plt.xlabel('Degree Rate')
    plt.ylabel('Average Income (AT)')
    plt.title('Degree holder Rate vs Average After-Tax Income (2020)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('bestfitline(degandincome).png', dpi=300, bbox_inches='tight')
    plt.close()

    x = df2020['bachelor rate'].to_numpy()
    y = df2020['avg income (AT)'].to_numpy()

    #Lets do a cubic fit since it fits it better 
    #I don't think I need to do this twice since I have already done it. But to be safe lets do it again.
    slope, intercept, r_value, p_value, std_error = linregress(x, y)
    print("Slope:", slope)
    print("P-value:", p_value)
    y_lin = intercept + slope * x

    coeffs = np.polyfit(x, y, 3)       
    poly3 = np.poly1d(coeffs)

    # Making a smooth curve to fit it 
    x_smooth = np.linspace(x.min(), x.max(), 300)
    y_cubic = poly3(x_smooth)

    plt.figure(figsize=(8,5))
    plt.scatter(x, y, label='Data points')
    plt.plot(x, y_lin, color='red', label='Linear fit')
    plt.plot(x_smooth, y_cubic, label='Cubic fit of deg = 3)')
    plt.xlabel('Degree Rate')
    plt.ylabel('Average Income (AT)')
    plt.title('Degree holder Rate vs Average After-Tax Income (2020)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('cubicandregr.png', dpi=300, bbox_inches='tight')
    plt.close()

    Highest_in20 = max(df2020['avg income (AT)'])
    lowest_in20 = min(df2020['avg income (AT)'])
    #Massive difference between lowest and highest income
    difference_perc20 = (Highest_in20 - lowest_in20)/ lowest_in20 * 100
    #What about 2016, was it more or less?
    Highest_in15 = max(df2015['avg income (AT)'])
    lowest_in15 = min(df2015['avg income (AT)'])
    difference_perc15 = (Highest_in15 - lowest_in15)/ lowest_in15 * 100
    #Unlike what I expected, it's gotten much better over 5 years. 
    print("difference between highest and lowest income (2016):", difference_perc15)
    print("difference between highest and lowest income (2020):", difference_perc20)

    #The second highest income and min income. 
    df2020_WWV = df2020[df2020['city'] != 'west van']
    df2015_WWV = df2015[df2015['city'] != 'west van']
    second_highest_20 = max(df2020_WWV['avg income (AT)'])
    second_highest_15 = max(df2015_WWV['avg income (AT)'])

    difference_perc20_second = (second_highest_20 - lowest_in20)/ lowest_in20 * 100
    difference_perc15_second = (second_highest_15 - lowest_in15)/ lowest_in15 * 100
    print("difference between second highest and lowest income (2016):", difference_perc15_second)
    print("difference between second highest and lowest income (2020):", difference_perc20_second)

    #degree rate growing? if so what is the correlation
    #Degree growth and income growth cor
    degree_growth = (df.groupby('city').apply(deg_growth, include_groups=False).rename('degree growth'))
    degree_growth = degree_growth.sort_values(ascending=False)
    print(degree_growth)
 

    #Is there correlation between population growth and income growth 
    population_growth = (df.groupby('city').apply(po_growth, include_groups=False).rename('population growth'))
    print(population_growth.sort_values(ascending=False))


    #Because of small data set, let's look at a scatter plot
    together = pd.concat([degree_growth, income_growth], axis=1, join='inner')
    together.columns = ['degree_growth', 'income_growth']
    plt.scatter(together['degree_growth'], together['income_growth'])
    plt.xlabel("Degree holder number growth (%)")
    plt.ylabel("Average income growth (AT) (%)")
    plt.title("Degree Growth vs Income Growth (2015 to 2020)")
    plt.tight_layout()
    plt.savefig('degree_vs_income_growth.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Lets cluster the data because why not
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    together['cluster'] = kmeans.fit_predict(together)

    plt.scatter(together['degree_growth'], together['income_growth'], c=together['cluster'], cmap='viridis')
    plt.xlabel("Degree holder number growth (%)")
    plt.ylabel("Average income growth (AT) (%)")
    plt.title("K-Means clustering (3): Degree vs Income Growth")
    for city, row in together.iterrows():
        plt.text(row['degree_growth']+0.5, row['income_growth']+0.5, city, fontsize=8)

    plt.savefig('growth_cluster.png', dpi=300, bbox_inches='tight')
    plt.close()


    #Next we will look at whether university degrees corelate to average income
    corr = df2020['avg income (AT)'].corr(df2020['bachelor rate'])
    print('income and degree correlation:',corr)

    #correlation between degree growth and income growth 
    deg_corr = income_growth.corr(degree_growth)
    print("degree growth and income growth correlation:",deg_corr)

    #Is there correlation between population growth and income growth 
    population_growth = (df.groupby('city').apply(po_growth, include_groups=False).rename('population growth'))
    print(population_growth.sort_values(ascending=False))
    pop_corr = population_growth.corr(income_growth)
    print('income growth and population growth:',pop_corr)
    #There is moderately strong correlation. 


    #correlation between lone parent rate and average income 
    corronerate = df2020['avg income (AT)'].corr(df2020['lone parent'])
    print('correlation between lone parent  and average income:',corronerate)

    #None normilized version of lone and income 
    corrone_nonenormalized = df2020['avg income (AT)'].corr(df2020['lone parent rate'])
    print('correlation between lone parent and income after normilizing: ',corrone_nonenormalized)

    #Correlation between lone parent and population
    corrone = df2020['population'].corr(df2020['lone parent'])
    print('Correlation between lone parent and population:',corrone)


    #Next we will look at whether university degrees corelate to average income
    corr = df2020['avg income (AT)'].corr(df2020['bachelor rate'])
    print('Correlation between Degree and income:',corr)


    #Is there relation between rate of immigrants and income
    corr2 = df2020['avg income (AT)'].corr(df2020['immigrant rate'])
    print('rate of immigrants and income correlation:',corr2)
    #There isn't a strong correlation

    #I am just using the feature importance to see which features are the most important. 
    #We are not actually predicting anything here since our data is small. 
    X = df2020[['bachelor rate','immigrant rate','lone parent rate','population']]
    y = df2020['avg income (AT)']
    rf = RandomForestRegressor(random_state=42)
    rf.fit(X, y)
    importances = rf.feature_importances_
    print('which features are more important?',importances)


    # Mann–Whitney U test, did we really have an income growth?
    income_2015 = df.loc[df['year'] == 2015, 'avg income (AT)']
    income_2020 = df.loc[df['year'] == 2020, 'avg income (AT)']

    statvar, p_val = mannwhitneyu(income_2015, income_2020, alternative='two-sided')
    print('Mann-Whitney U test results')
    print("U statistic:", statvar)
    print("p-value:", p_val)

if __name__ == "__main__":
    main()