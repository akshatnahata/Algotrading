
from selenium import webdriver
from time import sleep
import os

class TA_Handler:
    """ TA_Handler class
    Create an instance of this class to get TradingView's technical analysis.
    Values:
        symbol (string): Pair/symbol, not case-sensitive (ex: "btcusd" or "googl").
        interval (string): Interval rate, case-sensitive (default: "1m" for 1 minute).
        str_driver (string): Webdriver name, not case-sensitive (default: "chrome").
        headless (bool): Use headless browser for chrome and firefox (default: True).
        last_analysis (list): return the last analysis.
    Functions:
        start_driver(): Start the webdriver.
        get_analysis(): Return a list of analysis.
    """
    #Values
    driver = "chrome"
    symbol = ""
    interval = "1m"
    headless = True
    webdriver = None
    last_analysis = []

    #Set webdriver
    def start_driver(self):
        """ start_driver Function
        This function will set up a webdriver.
    
        Returns:
            bool: True if success, False if error.
        """
        self.driver = self.driver.lower()
        
        if self.webdriver != None:
            self.webdriver.quit()
        
        if self.driver in ["chrome", "chromedriver"]:
            if self.headless:
                from selenium.webdriver.chrome.options import Options
                options = Options()
                options.add_argument("--headless")
                self.webdriver = webdriver.Chrome(options=options)
            else:
                self.webdriver = webdriver.Chrome()
            return True
        elif self.driver in ["edge", "microsoft edge"]:
            self.webdriver = webdriver.Edge()
            return True
        elif self.driver in ["firefox", "mozilla", "mozilla firefox", "geckodriver"]:
            if self.headless:
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.add_argument("--headless")
                self.webdriver = webdriver.Firefox(options=options)
            else:
                self.webdriver = webdriver.Firefox()
            return True
        elif self.driver == "safari":
            self.webdriver = webdriver.Safari()
            return True
        elif self.driver == "heroku":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            self.webdriver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
            return True
        else:
            return False

    #Get analysis
    def get_analysis(self):
        """ get_analysis Function
        This function will return a list containing recommendation (buy/sell) and counters (number of analysis of sell, neutral, and buy).
    
        Returns:
            list: Recommendation and counters, format: ["Buy/Sell", sell_count, neutral_count, buy_count](ex: ["Buy", 3, 8, 17]).
            --- OR ---
            bool: False if error occured.
        """

        if self.webdriver == None:
            return False
    
        #Declare variable
        analysis = []

        #Open tradingview's site
        self.webdriver.get("https://s.tradingview.com/embed-widget/technical-analysis/?locale=en#%7B%22interval%22%3A%22{}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Afalse%2C%22height%22%3A%22100%25%22%2C%22symbol%22%3A%22{}%22%2C%22showIntervalTabs%22%3Atrue%2C%22colorTheme%22%3A%22dark%22%2C%22utm_medium%22%3A%22widget_new%22%2C%22utm_campaign%22%3A%22technical-analysis%22%7D".format(self.interval, self.symbol))
        self.webdriver.refresh()
        
        #Wait for site to load elements
        while len(self.webdriver.find_elements_by_class_name("speedometerSignal-pyzN--tL")) == 0:
            sleep(0.1)

        #Recommendation
        recommendation_element = self.webdriver.find_element_by_class_name("speedometerSignal-pyzN--tL")
        analysis.append(recommendation_element.get_attribute('innerHTML'))

        #Counters
        counter_elements = self.webdriver.find_elements_by_class_name("counterNumber-3l14ys0C")

        #Sell
        analysis.append(int(counter_elements[0].get_attribute('innerHTML')))

        #Neutral
        analysis.append(int(counter_elements[1].get_attribute('innerHTML')))
    
        #Buy
        analysis.append(int(counter_elements[2].get_attribute('innerHTML')))

        self.last_analysis = analysis
        return analysis


ta_instance = TA_Handler()
ta_instance.symbol = "NSE:infy"
ta_instance.interval = "1m"
ta_instance.driver = "safari"
ta_instance.headless = True
ta_instance.start_driver()
analysis = ta_instance.get_analysis()
print(analysis)