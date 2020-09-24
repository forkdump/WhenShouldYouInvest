# When Should You Invest?
This repository features the data and methods used that leads to the graphs and
conclusions that I mention in [this Medium article]().

In this repository you are able to find the actual functions that are used to do the calculations
as well as the pickles that are used to generate the graphs. As the full analysis took several hours,
I created pickles to be able to properly store the results in an efficient way.

The graph shown below explains the method uses and explanation for some adjustments to the data.

| Variable  | Description  |
| --------- | ------------ |
| Period    | I have taken a 10 year period starting from 2010-09-27 until 2020-09-23 where I filled any missing values up to 3 days and dropped any tickers that still had NaNs afterwards. Furthermore, all date gaps like weekend days are included and forward-filled to prevent skipping months. Thus the assumption is made that you trade one day earlier if the selected date is a weekend day. I find this a reasonable assumption to take.
| Tickers   | The tickers used are all tickers from [Yahoo Finance's World Indices](https://finance.yahoo.com/world-indices) with the exception of 'IMOEX.ME', '^JKSE', '^TWII', '^IPSA', '^TA125.TA', '^CASE30', '^JN0U.JO' that were not included due to NaNs or not  enough date available for the full 10 year period.
| Trades    | Trades occurred on the specific day and are assumed to happen straight away. This means you are also affected by the return that day. This results in a total of 120 trades in a 10 year period.
| Returns   | Returns are calculated by the "New minus Old" principle. You invested a total of 120 * $100,- which is compared to the accumlated value at the end of the 10 year period.
| Graphs    | The graphs aggregate the returns and calculate the median values to give an average of the total return in the 10 year period. Quantiles are then calculated based on these median returns.


