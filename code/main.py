from get_data import *
from analyze_the_data import *
from generate_visualization import *

if __name__ == '__main__':
    # get data
    download_usdindex_json("../data/USD_index.json")
    convert_json_csv("../data/USD_index.json", "../data/USD_index.csv")

    download_oil_csv('CL=F', '2013-01-01', '2022-11-22', '1d', "../data/tick_wti.csv")
    download_oil_csv('BZ=F', '2013-01-01', '2022-11-22', '1d', "../data/tick_brent.csv")

    col = ['direction_color', 'rowDateRaw', 'rowDateTimestamp', 'volume', 'volumeRaw', 'last_closeRaw',
           'last_openRaw', 'last_maxRaw', 'last_minRaw', 'change_precentRaw']
    drop_column("../data/USD_index.csv", col)

    check_null("../data/USD_index.csv")
    check_null("../data/tick_wti.csv")
    check_null("../data/tick_brent.csv")

    change_col_name("../data/USD_index.csv", 'rowDate', 'Date')
    change_col_name("../data/tick_wti.csv", 'Adj Close', 'adj_close_wti')
    change_col_name("../data/tick_brent.csv", 'Adj Close', 'adj_close_brent')

    del_below_zero("../data/tick_wti.csv", 'adj_close_wti')

    merge_dataset("../data/USD_index.csv", "../data/tick_wti.csv", 'Date', "../data/index_wti.csv")
    merge_dataset("../data/USD_index.csv", "../data/tick_brent.csv", 'Date', "../data/index_brent.csv")
    merge_dataset("../data/index_wti.csv", "../data/tick_brent.csv", 'Date', "../data/index_wti_brent.csv")

    add_year_month("../data/index_wti_brent.csv")


    # analyses
    # correlation coefficient from 2013 to 2022
    df = pd.read_csv("../data/index_wti_brent.csv")
    pearson_correlation(df["last_close"], df["adj_close_wti"])

    sta_model(df['last_close'], df['adj_close_wti'])
    sta_model(df['last_close'], df['adj_close_brent'])

    reg_plot("../result/regression_model_wti", "adj_close_wti", " (WTI)", "USD index value", "WTI crude oil price")
    reg_plot("../result/regression_model_brent", "adj_close_brent", " (Brent)", "USD index value",
             "Brent crude oil price")

    hdline = ['year', 'co_co']
    createcsv("../data/cor_year_wti.csv", hdline)
    correlation_yearly("../data/cor_year_wti.csv", "adj_close_wti")
    correlation_yearly_plot("../data/cor_year_wti.csv", "../result/correlation_yearly_wti", " (WTI)")

    createcsv("../data/cor_year_brent.csv", hdline)
    correlation_yearly("../data/cor_year_brent.csv", "adj_close_brent")
    correlation_yearly_plot("../data/cor_year_brent.csv", "../result/correlation_yearly_brent", " (Brent)")



    # visualizations
    cols = ['last_close', 'adj_close_wti', 'adj_close_brent']
    ylabels = ['USD index', 'WTI oil price', 'Brent oil price']

    time_visual("../data/USD_index.csv", "../data/tick_wti.csv", "../data/tick_brent.csv", "Date",
                "../result/time_series_plot")

    boxplot_time("../data/index_wti_brent.csv", cols, ylabels, "../result/boxplot")

    heat_map("../data/index_wti_brent.csv", cols[0], "USD index heatmap", "../result/usd_index_heatmap")
    # heat_map("../data/index_wti_brent.csv", cols[1], "WTI oil heatmap", "../result/wti_heatmap")
    heat_map("../data/index_wti_brent.csv", cols[2], "Brent oil heatmap", "../result/brent_heatmap")

    # resample_timeseries("../data/index_wti_brent.csv", cols, '2021-11', '2022-11', "../result/resampel_plot_2122")

    every_year("../data/index_wti_brent.csv", cols[0], "USD Index Yearly Data", "Month", ylabels[0],
               "../result/usd_index_yearly_plot")
    # every_year("../data/index_wti_brent.csv", cols[1], "WTI Crude Oil Yearly Data", "Month", ylabels[1],
               # "../result/wti_yearly_plot")
    every_year("../data/index_wti_brent.csv", cols[1], "Brent Crude Oil Yearly Data", "Month", ylabels[2],
               "../result/brent_yearly_plot")

    slider_time_plot("../data/index_wti_brent.csv", "../result/slider.html")

    # LSTM prediction
    lstm_predict("../data/USD_index.csv", "../result/USD_index_value_prediction", "%b %d, %Y", ["last_open", "last_max", "last_min", "change_precent"],
                 "USD index value", "Prediction on USD index value")
    lstm_predict("../data/tick_brent.csv", "../result/Brent_oil_price_prediction", "%Y-%m-%d", ["Open", "High", "Low", "Close", "Volume"], "Brent oil price",
                 "Prediction on Brent oil price")