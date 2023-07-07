import pandas as pd
import re
import time

switch = True
def exporter(row,filename):
    global switch 
    if switch:
        switch = False
        pd.DataFrame(row,index=[0]).to_csv(filename,index=False,mode='a')
    else:
        pd.DataFrame(row,index=[0]).to_csv(filename,index=False,mode='a',header=False)


def get_driver():
    import undetected_chromedriver as uc
    options = uc.ChromeOptions()
    options.headless=False
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    return driver

def quantity_fetcher(title):
    pattern = r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)'
    match = re.search(pattern, title)
    
    if match:
        quantity = str(match.group(1))
        unit = match.group(2)
        quantity = quantity + ' ' + unit
        return quantity
    else:
        return None

def scroller(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_driver_headless():
    import undetected_chromedriver as uc
    options = uc.ChromeOptions()
    options.headless=True
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    return driver