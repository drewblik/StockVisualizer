from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials


class Stock:
    """
    TBD
    """

    def __init__(self, ticker_sym):
        self.ticker_sym = ticker_sym
        self.HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                         'Accept-Language': 'en-US, en;q=0.5'})
        self.sum_dict = None
        self.stat_dict = None
        self.val_mes_table = None
        self.anal_table_dict = None
        self.ticker_obj = None
        self.his_data = None

    def generateSummaryData(self):
        url = "https://finance.yahoo.com/quote/" + self.ticker_sym + "/"
        webpage = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        # finds table and creates dictionary
        data = []
        table = soup.find('table', attrs={'class': 'W(100%)'})
        table_body = table.find('tbody')
        sum_dict = dict()
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols])  # Get rid of empty value
            for pair in data:
                sum_dict[pair[0]] = pair[1]
        # replaces strings with numbers when needed
        middle = sum_dict['52 Week Range'].find('-')
        sum_dict['52 Week High'] = float(sum_dict['52 Week Range'][middle+2:].replace(',', ''))
        sum_dict['52 Week Low'] = float(sum_dict['52 Week Range'][:middle].replace(',', ''))
        middle = sum_dict["Day's Range"].find('-')
        sum_dict['Day High'] = float(sum_dict["Day's Range"][middle+2:].replace(',', ''))
        sum_dict['Day Low'] = float(sum_dict["Day's Range"][:middle].replace(',', ''))
        sum_dict['Previous Close'] = float(sum_dict['Previous Close'].replace(',', ''))
        sum_dict['Open'] = float(sum_dict['Open'].replace(',', ''))
        sum_dict['Volume'] = float(sum_dict['Avg. Volume'].replace(',', ''))
        print("getSummary complete")
        self.sum_dict = sum_dict

    def generateAnalTable(self):
        url = "https://finance.yahoo.com/quote/" + self.ticker_sym + "/analysis"
        webpage = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        # finds table and creates dictionary
        section = soup.find(id='Col1-0-AnalystLeafPage-Proxy')
        tables = section.find_all('table')
        anal_table_dict = dict()
        for table in tables:
            data = []
            table_headings = table.find('thead')
            headings = table_headings.find_all('th')
            headings = [ele.text.strip() for ele in headings]
            table_title = headings[0]
            headings[0] = ''
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols])
            temp_df = pd.DataFrame(data, columns=headings)
            anal_table_dict[table_title] = temp_df
        print("getAnalTable complete")
        self.anal_table_dict = anal_table_dict

    def generateStatistics(self):
        # sets up scraping
        url = "https://finance.yahoo.com/quote/" + self.ticker_sym + "/key-statistics"
        webpage = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        # finds al tables
        section = soup.find(id='Col1-0-KeyStatistics-Proxy')
        tables = section.find_all('table')
        # converts valuation measures table into pandas DataFrame
        table = tables[0]
        data = []
        table_headings = table.find('thead')
        headings = table_headings.find_all('th')
        headings = [ele.text.strip() for ele in headings]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols])
        valuation_measures = pd.DataFrame(data, columns=headings)
        # converts rest of table into dictionary
        stat_dict = dict()
        for table in tables[1:]:
            table_body = table.find('tbody')
            data = []

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols])  # Get rid of empty value
                for pair in data:
                    stat_dict[pair[0]] = pair[1]
        self.stat_dict = stat_dict
        self.val_mes_table = valuation_measures
        print("getStatistics complete")

    def generateTickerObj(self):
        
        df = yf.Ticker(self.ticker_sym)
        df = df.history(period="max", interval="1d")
        for i in ['Open', 'High', 'Close', 'Low']:
            df[i] = df[i].astype('float64')
        self.his_data = df

    def generateAll(self):
        self.generateStatistics()
        self.generateAnalTable()
        self.generateSummaryData()
