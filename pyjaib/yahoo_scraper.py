from bs4 import BeautifulSoup
from typing import Final
import requests
from datetime import datetime, timedelta
import logging
import os 

class YahooScraper:
    YAHOO_ROOT_URL: Final[str] = 'https://finance.yahoo.com'

    def __init__(
            self, 
            parser='html.parser', 
            headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'},
            data_foldername='data'):
        self.parser = parser
        self.headers = headers
        self.data_foldername = data_foldername

    def __request_html(self, url):
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 404:
            logging.warning("request to retrieve page failed. URL: {url}".format(url=url))

        html = resp.text
        return html
    
    def __save_html(self, filename, html):
        print(filename)
        with open(filename, 'w+', encoding="utf-8") as file:
            file.write(html)
    
    def get_data_folder_full_file_path(self):
        dir_filepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_filepath, self.data_foldername)
    
    
    def ensure_data_folder_exists(self, data_folder_full_filepath):
        if not os.path.exists(data_folder_full_filepath):
            os.makedirs(data_folder_full_filepath)

    def format_epoch_secs_to_yy_mm_dd(self, epoch_secs):
        return datetime.fromtimestamp(epoch_secs).strftime('%Y-%m-%d')

    def get_stock_history_full_filepath(self, symbol, start_of_period_epoch, end_of_period_epoch):
        data_folder_full_filepath = self.get_data_folder_full_file_path()

        self.ensure_data_folder_exists(data_folder_full_filepath)

        start_of_period_date = self.format_epoch_secs_to_yy_mm_dd(start_of_period_epoch)
        end_of_period_date = self.format_epoch_secs_to_yy_mm_dd(end_of_period_epoch)
        stock_history_filename = '{symbol}_{start_of_period_date}_{end_of_period_date}.html'.format(
            symbol = symbol,
            start_of_period_date = start_of_period_date,
            end_of_period_date = end_of_period_date,
        )
        
        stock_history_full_filepath = os.path.join(data_folder_full_filepath, stock_history_filename)
        return stock_history_full_filepath

    @staticmethod
    def __epoch_secs_now():
        epoch_secs_now = datetime.now().timestamp()
        rounded_epoch_secs_now = round(epoch_secs_now)
        return rounded_epoch_secs_now
    
    @staticmethod
    def __epoch_secs_years_ago(year_count = 1):
        days_in_year = 365
        epoch_secs_now = YahooScraper.__epoch_secs_now()
        secs_in_a_year = (timedelta(days=days_in_year) / timedelta(seconds=1))
        epoch_secs_years_ago = epoch_secs_now - (secs_in_a_year * year_count)
        rounded_epoch_secs_years_ago = round(epoch_secs_years_ago)
        return rounded_epoch_secs_years_ago
    
    
    def __get_historical_data_url(self, symbol, start_of_period_epoch, end_of_period_epoch):
        return "{base_url}/quote/{symbol}/history/?period1={start_of_period_epoch}&period2={end_of_period_epoch}".format(
            base_url = self.YAHOO_ROOT_URL,
            symbol = symbol,
            start_of_period_epoch = start_of_period_epoch,
            end_of_period_epoch = end_of_period_epoch
        )
    
    def parse_stock_price_history_page(self, stock_history_html):
        soup = BeautifulSoup(stock_history_html, self.parser)


    def get_stock_price_history(self, symbol, start_of_period_epoch=None, end_of_period_epoch=None, saveHtml=False):
        if end_of_period_epoch is None:  
            end_of_period_epoch = self.__epoch_secs_now()

        if start_of_period_epoch is None:
            start_of_period_epoch = self.__epoch_secs_years_ago(year_count=1)

        stock_history_url = self.__get_historical_data_url(symbol, start_of_period_epoch, end_of_period_epoch)
        stock_history_html = self.__request_html(stock_history_url)

        if (saveHtml):
            stock_history_full_filepath = self.get_stock_history_full_filepath(symbol, start_of_period_epoch, end_of_period_epoch)
            self.__save_html(stock_history_full_filepath, stock_history_html)

        soup = BeautifulSoup(stock_history_html, self.parser)
        
    def parseStockHistoryHtml():
        return 0
