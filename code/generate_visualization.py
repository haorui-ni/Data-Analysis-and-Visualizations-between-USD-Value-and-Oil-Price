import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.dates as mdates
import kaleido
import plotly.graph_objects as go

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
    plt.xlabel('Year')
    plt.ylabel("Price")
    plt.title('Time series plot')
    plt.yticks(np.arange(0, 130, 5))
    plt.legend()
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

def slider_time_plot(csvname, savename):
    df = pd.read_csv(csvname)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list(df.Date), y=list(df.last_close), name="USD index value"))
    fig.add_trace(go.Scatter(x=list(df.Date), y=list(df.adj_close_wti), name = "WTI crude oil price"))
    fig.add_trace(go.Scatter(x=list(df.Date), y=list(df.adj_close_brent), name = "Brent crude oil price"))

    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 3},
        mode="lines+markers",
        showlegend=False
    )

    fig.update_layout(
        title_text="USD index, WTI oil price, and Brent oil price time seires"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),

        yaxis=dict(
            anchor="x",
            autorange=True,
            linecolor="#673ab7",
            mirror=True,
            showline=True,
            side="right",
            tickfont={"color": "#673ab7"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#673ab7"},
            type="linear",
            zeroline=False,
        ),
        yaxis2=dict(
            anchor="x",
            autorange=True,
            linecolor="#E91E63",
            mirror=True,
            showline=True,
            side="right",
            tickfont={"color": "#E91E63"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#E91E63"},
            type="linear",
            zeroline=False
        ),
        yaxis3=dict(
            anchor="x",
            autorange=True,
            linecolor="#795548",
            mirror=True,
            showline=True,
            side="right",
            tickfont={"color": "#795548"},
            tickmode="auto",
            ticks="",
            title="mg/L",
            titlefont={"color": "#795548"},
            type="linear",
            zeroline=False
        )
    )

    fig.update_layout(
        dragmode="zoom",
        hovermode="x",
        legend=dict(traceorder="reversed"),
        height=600,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
    )
    fig.write_html(savename)


if __name__ == '__main__':
    cols = ['last_close', 'adj_close_wti', 'adj_close_brent']
    ylabels = ['USD index', 'WTI oil price', 'Brent oil price']

    time_visual("../data/USD_index.csv", "../data/tick_wti.csv", "../data/tick_brent.csv", "Date", "../result/time_series_plot")

    boxplot_time("../data/index_wti_brent.csv", cols, ylabels, "../result/boxplot")

    heat_map("../data/index_wti_brent.csv", cols[0], "USD index heatmap", "../result/usd_index_heatmap")
    heat_map("../data/index_wti_brent.csv", cols[1], "WTI oil heatmap", "../result/wti_heatmap")
    heat_map("../data/index_wti_brent.csv", cols[2], "Brent oil heatmap", "../result/brent_heatmap")

    resample_timeseries("../data/index_wti_brent.csv", cols, '2021-11', '2022-11', "../result/resampel_plot_2122")

    every_year("../data/index_wti_brent.csv", cols[0], "USD Index Yearly Data", "Month", ylabels[0],
               "../result/usd_index_yearly_plot")
    every_year("../data/index_wti_brent.csv", cols[1], "WTI Crude Oil Yearly Data", "Month", ylabels[1],
               "../result/wti_yearly_plot")
    every_year("../data/index_wti_brent.csv", cols[1], "Brent Crude Oil Yearly Data", "Month", ylabels[2],
               "../result/brent_yearly_plot")

    slider_time_plot("../data/index_wti_brent.csv", "../result/slider.html")
