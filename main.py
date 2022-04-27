from stock import Stock
import datetime as dt
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
'''


'''




def main():
    # tick_sym = askForTickerSym()
    # tick_sym2 = 'KO'
    # start_date = askForDate()
    # end_date = dt.datetime.now()

    # selection = Stock(tick_sym)   
    # selection.generateTickerObj()

    # MAIN FUNCTIONS
    ans = listOrPick()
    stock_list = None
    if ans == 'S':
        stock_list = askForTickerSym()
        
    if ans == 'D':
        stock_list = generateSP500Data()
    
    createLineChart(stock_list)

    # testTickerFunctions(test)
    # testStockDataFunctions(test)


def listOrPick():
    ans = input('Pick stocks or dataset? (S -> Stocks | D -> Dataset)').upper()
    return ans




def testTickerFunctions(test):
    test.generateTickerObj()

def createLineChart(stock_list):
    

    
    y_var_selection = '_' + str(input('Enter desired price catagory: ')).capitalize()
    stock_list[0].his_data = stock_list[0].his_data.rename(columns={"Open": str(stock_list[0].ticker_sym) + "_Open", "High": str(stock_list[0].ticker_sym) + "_High", "Low": str(stock_list[0].ticker_sym) + "_Low", "Close": str(stock_list[0].ticker_sym) + "_Close", "Volume": str(stock_list[0].ticker_sym) + "_Volume", "Dividends": str(stock_list[0].ticker_sym) + "_Dividends", "Stock Splits": str(stock_list[0].ticker_sym) + "_Stock Splits"})
    combined = stock_list[0].his_data
    column_name_list = []
    

    for stock in stock_list[1:]:
        stock.his_data = stock.his_data.rename(columns={"Open": str(stock.ticker_sym) + "_Open", "High": str(stock.ticker_sym) + "_High", "Low": str(stock.ticker_sym) + "_Low", "Close": str(stock.ticker_sym) + "_Close", "Volume": str(stock.ticker_sym) + "_Volume", "Dividends": str(stock.ticker_sym) + "_Dividends", "Stock Splits": str(stock.ticker_sym) + "_Stock Splits"})
        combined = pd.concat([combined, stock.his_data], axis=1)

 
    for col in combined.columns:
        if y_var_selection in col:
            column_name_list.append(col)
    print()


    trimmed = combined.loc[: , column_name_list]
    
    c_area = px.line(combined, title = 'Stock ' + y_var_selection[1:] + ' PRICE',  y=trimmed.columns[:] )

    c_area.update_xaxes(
    title_text = 'Date',
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = list([
            dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
            dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
            dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
            dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
            dict(count = 5, label = '5Y', step = 'year', stepmode = 'backward'),
            dict(step = 'all')])))

    c_area.update_yaxes(title_text = 'Stock ' + y_var_selection[1:] + ' PRICE', tickprefix = '$')
    c_area.update_layout(showlegend = True,    
        title = {
            'text': 'Stock ' + y_var_selection[1:] + ' PRICE',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    c_area.show()



def askForTickerSym():
    stock_list = []
    print('(DONE->Exit)')
    ans = input('Enter ticker to display: ').upper()
    while(ans != 'DONE'):
        selection = Stock(ans)
        selection.generateTickerObj()
        stock_list.append(selection)
        print('(DONE->Exit)')
        ans = input("Enter ticker to display: ").upper()
    return stock_list



def testStockDataFunctions(test):
    """
    input: Stock Object
    Tests yahoo finance webscraping functions 
    """
    test.generateAll()
    print("stat_dict TEST")
    print(test.stat_dict['Fiscal Year Ends'])
    print()
    print("sum_dict TEST")
    print(test.sum_dict['Open'])
    print()
    print('val_mes_table TEST')
    print(test.val_mes_table.loc[0])
    print()
    print('anal_tables TEST')
    print(test.anal_table_dict['Earnings Estimate'])
    print()

def getSP500():
    """
    Returns a list of dictionaries containing the rank, name, ticker, and weight of all S&P 500 stocks
    """
    HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                        'Accept-Language': 'en-US, en;q=0.5'})
    url = "https://www.slickcharts.com/sp500"
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    table = soup.find('table', attrs={'class': 'table table-hover table-borderless table-sm'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    all_SP500_data = []
    for row in rows:
        stock_info = dict()
        cells = row.find_all('td')
        stock_info['rank'] = cells[0].string
        stock_info['name'] = cells[1].string
        stock_info['symbol'] = cells[2].string
        stock_info['weight'] = cells[3].string
        all_SP500_data.append(stock_info)
    return all_SP500_data


def generateSP500Data():
    stock_list = []
    SP_list = getSP500()
    for row in SP_list[0:50]:
        ticker = row['symbol']
        print(row['rank'])
        temp = Stock(ticker)
        temp.generateTickerObj()
        stock_list.append(temp)
    return stock_list




if __name__ == '__main__':
    main()
