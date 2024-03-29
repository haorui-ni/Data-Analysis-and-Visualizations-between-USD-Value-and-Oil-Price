
import requests
import yfinance as yf
import pandas as pd
import json
import csv

def download_usdindex_json(json_name):
    url = 'https://api.scraperlink.com/investpy/?email=nihaorui715@gmail.com&type=historical_data&product=indices&from_date=2013-01-01&to_date=2022-11-22&time_frame=Daily&symbol=DXY'
    response = requests.request("GET", url)
    # save in JSON format
    with open(json_name, 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)

def convert_json_csv(jname, cname):
    with open(jname) as json_file:
        usd_index = json.load(json_file)
    index_data = usd_index['data']
    csv_data_file = open(cname, 'w')
    fwriter = csv.writer(csv_data_file)
    h = 0
    for index in index_data:
        if h == 0:
            header = index.keys()
            fwriter.writerow(header)
            h += 1
        fwriter.writerow(index.values())
    csv_data_file.close()

def download_oil_csv(tickers, start, end, interval, csvname):
    tick = yf.download(tickers=tickers, start = start, end = end, interval=interval)
    tick.to_csv(csvname)

def drop_column(csvname, drop_col):
    df = pd.read_csv(csvname)
    df = df.drop(columns = drop_col)
    df.to_csv(csvname, index = False)

def check_null(csvname):
    df = pd.read_csv(csvname)
    print(df.isnull().sum())

def change_col_name(csvname, ori_name, changed_name):
    df = pd.read_csv(csvname)
    df.rename(columns = {ori_name: changed_name}, inplace = True)
    df.to_csv(csvname, index = False)

def merge_dataset(csv_one, csv_two, col, merge_name):
    df_one = pd.read_csv(csv_one)
    df_two = pd.read_csv(csv_two)
    df_one[col] = pd.to_datetime(df_one[col])
    df_two[col] = pd.to_datetime(df_two[col])
    df_merge = df_one.merge(df_two, on = col)
    df_merge.to_csv(merge_name, index = False)

def del_below_zero(csvname, col):
    df = pd.read_csv(csvname)
    df = df[(df[col] > 0)]
    df.to_csv(csvname, index = False)

def add_year_month(csvname):
    df = pd.read_csv(csvname)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df.to_csv(csvname)




