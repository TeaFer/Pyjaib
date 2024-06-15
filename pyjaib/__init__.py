from yahoo_scraper import YahooScraper

def main():
    yahoo_scraper = YahooScraper()
    print("bob")
    yahoo_scraper.get_stock_price_history(
        symbol="NFLX",
        saveHtml=True
    )

if __name__=="__main__": 
    main() 