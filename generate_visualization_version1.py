import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.dates as mdates


def time_visual(csv_one, csv_two, csv_three, col, savename):
    sns.set(rc={'figure.figsize': (10, 6)})
    df_one = pd.read_csv(csv_one)
    df_two = pd.read_csv(csv_two)
    df_three = pd.read_csv(csv_three)
    df_one[col] = pd.to_datetime(df_one[col])
    df_two[col] = pd.to_datetime(df_two[col])
    df_three[col] = pd.to_datetime(df_three[col])
    plt.plot(df_one.Date, df_one.last_close, label = 'USD index')
    plt.plot(df_two.Date, df_two.adj_close_wti, color='green', label = 'WTI')
    plt.plot(df_three.Date, df_three.adj_close_brent, color='orange', label = 'Brent')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Time series plot')
    plt.yticks(np.arange(0, 130, 5))
    plt.savefig(savename)
    plt.close()


def boxplot_time(csvname, col, ylab, savename):
    df = pd.read_csv(csvname)
    df['Date'] = pd.to_datetime(df['Date'])
    df_date = df.set_index('Date')
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    for colname, ylabel, ax in zip(col, ylab, axes):
        sns.boxplot(data=df_date, x='Year', y=colname, ax=ax)
        ax.set_ylabel(ylabel)
    fig.savefig(savename)
    plt.close()


def resample_timeseries(csvname, cols, start, end, savename):
    sns.set(rc={'figure.figsize': (9, 6)})
    df = pd.read_csv(csvname)
    # set 'Date' as the DataFrame index
    df['Date'] = pd.to_datetime(df['Date'])
    df_date = df.set_index('Date')
    # Resample to weekly frequency, aggregating with mean
    df_weekly = df_date[cols].resample('W').mean()
    # Plot daily and weekly resampled time series together
    plt.plot(df_weekly.loc[start:end, cols[0]],
            marker='o', markersize=5, linestyle='-', color = 'blue', label='USD index')
    plt.plot(df_weekly.loc[start:end, cols[1]],
            marker='o', markersize=5, linestyle='--', color = 'green', label='WTI crude oil')
    plt.plot(df_weekly.loc[start:end, cols[2]],
            marker='o', markersize=5, linestyle='-.', color = 'orange', label='Brent crude oil')
    plt.ylabel('Price/week')
    plt.savefig(savename)
    plt.close()

def every_year(csvname, col, title, xlab, ylab, savename):
    df = pd.read_csv(csvname)
    df['Date'] = pd.to_datetime(df['Date'])
    df_date = df.set_index('Date')

    sns.set_theme(style="whitegrid")

    eachplot = sns.relplot(
        data=df_date,
        x="Month", y=col, col="Year", hue="Year",
        kind="line", palette="crest", linewidth=5, zorder=5,
        col_wrap=2, height=5, aspect=2, legend=False,
    )

    for year, ax in eachplot.axes_dict.items():
        ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")
        sns.lineplot(
            data=df_date, x="Month", y=col, units="Year",
            estimator=None, color=".7", linewidth=1, ax=ax,
        )

    eachplot.set_titles(title)
    eachplot.set_axis_labels(xlab, ylab)
    eachplot.tight_layout()

    eachplot.savefig(savename)
    plt.close()

def heat_map(csvname, col, title, savename):
    df = pd.read_csv(csvname)
    df['Date'] = pd.to_datetime(df['Date'])
    df_date = df.set_index('Date')
    sns.set_theme()
    mat = pd.pivot_table(df_date, index="Month", columns="Year", values = col)
    f, ax = plt.subplots(figsize=(9, 6))
    plt.title(title)
    sns.heatmap(mat, annot=True, fmt=".2f", linewidths=.5, ax=ax, cmap='YlOrRd')
    plt.savefig(savename)
    plt.close()

if __name__ == '__main__':
    cols = ['last_close', 'adj_close_wti', 'adj_close_brent']
    ylabels = ['USD index', 'WTI oil price', 'Brent oil price']

    time_visual("data/USD_index.csv", "data/tick_wti.csv", "data/tick_brent.csv", "Date", "image/time_series_plot")

    boxplot_time("data/index_wti_brent.csv", cols, ylabels, "image/boxplot")

    heat_map("data/index_wti_brent.csv", cols[0], "USD index heatmap", "image/usd_index_heatmap")
    heat_map("data/index_wti_brent.csv", cols[1], "WTI oil heatmap", "image/wti_heatmap")
    heat_map("data/index_wti_brent.csv", cols[2], "Brent oil heatmap", "image/brent_heatmap")

    resample_timeseries("data/index_wti_brent.csv", cols, '2021-11', '2022-11', "image/resampel_plot_2122")

    every_year("data/index_wti_brent.csv", cols[0], "USD Index Yearly Data", "Month", ylabels[0],
               "image/usd_index_yearly_plot")
    every_year("data/index_wti_brent.csv", cols[1], "WTI Crude Oil Yearly Data", "Month", ylabels[1],
               "image/wti_yearly_plot")
    every_year("data/index_wti_brent.csv", cols[1], "Brent Crude Oil Yearly Data", "Month", ylabels[2],
               "image/brent_yearly_plot")