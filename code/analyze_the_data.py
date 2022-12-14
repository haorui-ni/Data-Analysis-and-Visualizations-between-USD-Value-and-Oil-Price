import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import csv
import seaborn as sns
import numpy as np
import statsmodels.api as sm
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.metrics import mean_squared_error
# from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler

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
    df = pd.read_csv("../data/index_wti_brent.csv")
    sns.set(rc={'figure.figsize': (7, 5)})
    sns.regplot(x='last_close', y=col,
                data=df, scatter_kws={'s': 5}, line_kws={"color": "orange"})
    plt.title("linear regression model" + title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(savename)
    plt.close()

def create_data_set(_data_set, window_len=1):
    data_x, data_y = [], []
    for i in range(len(_data_set) - window_len - 1):
        a = _data_set[i:(i + window_len), 0]
        data_x.append(a)
        data_y.append(_data_set[i + window_len, 0])
    return np.array(data_x), np.array(data_y)


def lstm_predict(csvname, savename, date_format, drop_columns, label_one, label_two):
    dateparse = lambda x: pd.datetime.strptime(x, date_format)
    df = pd.read_csv(csvname, parse_dates=['Date'], date_parser=dateparse)
    df.set_index('Date', inplace=True)
    df = df.drop(columns=drop_columns)
    sc = MinMaxScaler(feature_range=(0, 1))
    df = sc.fit_transform(df)
    train_size = int(len(df) * 0.80)
    test_size = len(df) - train_size
    train, test = df[0:train_size, :], df[train_size:len(df), :]
    X_train, Y_train, X_test, Ytest = [], [], [], []
    X_train, Y_train = create_data_set(train, 60)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test, Y_test = create_data_set(test, 60)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    regressor = Sequential()
    regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=50))
    regressor.add(Dropout(0.2))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error')
    history = regressor.fit(X_train, Y_train, epochs=200, batch_size=32)
    train_predict = regressor.predict(X_train)
    test_predict = regressor.predict(X_test)
    train_predict = sc.inverse_transform(train_predict)
    Y_train = sc.inverse_transform([Y_train])
    test_predict = sc.inverse_transform(test_predict)
    Y_test = sc.inverse_transform([Y_test])
    print('Train Mean Absolute Error:', mean_squared_error(Y_train[0], train_predict[:, 0]))
    print('Test Mean Absolute Error:', mean_squared_error(Y_test[0], test_predict[:, 0]))
    a = [x for x in range(100)]
    plt.figure(figsize=(9, 6))
    plt.plot(a, Y_test[0][:100], marker='.', label=label_one)
    plt.plot(a, test_predict[:, 0][:100], 'r', label=label_two)
    plt.tight_layout()
    plt.title(label_one + " prediction plot")
    plt.ylabel(label_one)
    plt.xlabel('Time')
    plt.legend()
    plt.savefig(savename)
    plt.close()











