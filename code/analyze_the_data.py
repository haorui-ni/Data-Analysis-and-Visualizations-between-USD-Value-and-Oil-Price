import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import csv
import seaborn as sns
import numpy as np
import statsmodels.api as sm
import os

def pearson_correlation(a: list, b: list) -> float:
    lst_pc = scipy.stats.pearsonr(a, b)
    co_cor = lst_pc[0]
    return co_cor

def createcsv(csvname, headline):
    with open(csvname, 'w') as file:
        dw = csv.DictWriter(file, delimiter=',', fieldnames=headline)
        dw.writeheader()

def correlation_yearly(csvname, colname):
    df = pd.read_csv("../data/index_wti_brent.csv")
    for year in range(2013, 2023):
        df_year = df[df['Year'] == year]
        cor_year = pearson_correlation(df_year["last_close"], df_year[colname])
        data_year = [year, cor_year]
        with open(csvname, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data_year)
    file.close()

def correlation_yearly_plot(csvname, savename, title):
    df_year_cor = pd.read_csv(csvname)
    sns.set(rc={'figure.figsize': (7, 3)})
    plt.plot(df_year_cor.year, df_year_cor.co_co)
    plt.title("correlation coefficient yearly change" + title)
    plt.xlabel('year')
    plt.ylabel('correlation_coefficient')
    plt.savefig(savename)
    plt.close()

def sta_model(iv, dv):
    iv = sm.add_constant(iv) # independent variable and dependent variable
    reg_model = sm.OLS(dv, iv).fit()
    print(reg_model.summary())

def reg_plot(savename, col, title, xlabel, ylabel):
    sns.set(rc={'figure.figsize': (7, 5)})
    sns.regplot(x='last_close', y=col,
                data=df, scatter_kws={'s': 5}, line_kws={"color": "orange"})
    plt.title("linear regression model" + title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(savename)
    plt.close()

if __name__ == '__main__':
    # correlation coefficient from 2013 to 2022
    df = pd.read_csv("../data/index_wti_brent.csv")
    pearson_correlation(df["last_close"], df["adj_close_wti"])


    sta_model(df['last_close'], df['adj_close_wti'])
    sta_model(df['last_close'], df['adj_close_brent'])

    reg_plot("../result/regression_model_wti", "adj_close_wti", " (WTI)", "USD index value", "WTI crude oil price")
    reg_plot("../result/regression_model_brent", "adj_close_brent", " (Brent)", "USD index value", "Brent crude oil price")


    hdline = ['year', 'co_co']
    createcsv("../data/cor_year_wti.csv", hdline)
    correlation_yearly("../data/cor_year_wti.csv", "adj_close_wti")
    correlation_yearly_plot("../data/cor_year_wti.csv", "../result/correlation_yearly_wti", " (WTI)")

    createcsv("../data/cor_year_brent.csv", hdline)
    correlation_yearly("../data/cor_year_brent.csv", "adj_close_brent")
    correlation_yearly_plot("../data/cor_year_brent.csv", "../result/correlation_yearly_brent", " (Brent)")











