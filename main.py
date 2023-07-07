import requests
import time
import scraper_helper
import pandas as pd
from parsel import Selector
from utils import exporter, get_driver, quantity_fetcher, scroller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

r = requests.Session()

def alfatah():
    url = 'https://www.alfatah.pk/pages/grocery'
    req = r.get(url)
    resp = Selector(text=req.text)
    links = []
    links1 = resp.xpath('//div[@id="shopify-section-home-sub-banner"]/div/div/div/div/div/div/a/@href').getall()
    links2 = resp.xpath('//div[@id="shopify-section-home-sub-banner-2"]/div/div/div/div/div/div/a/@href').getall()
    for x in links1: links.append(x)
    for y in links2: links.append(y)
    for link in links:
        link = 'https://www.alfatah.pk' + link
        req = r.get(link)
        resp = Selector(text=req.text)
        category = resp.xpath('//h1/span/text()').get()
        try: category = category.strip()
        except: pass
        while True:
            divs = resp.xpath('//div[@class="grid-item col-6 col-md-4 col-lg-3 col5 grid-item-border "]/div/div')
            for div in divs:
                title = div.xpath('./div[2]/div[1]/a/span/text()').get()
                quantity = quantity_fetcher(title)

                a_price = div.xpath('./div[2]/div[2]/div/span[1]/text()').get()
                try: a_price = (a_price.replace('Rs.','')).strip()
                except: pass

                d_price = div.xpath('./div[2]/div[2]/div/span[2]/text()').get()
                try: d_price = (d_price.replace('Rs.','')).strip()
                except: pass

                stock = div.xpath('./div[4]/div/form/button/text()[2]').get()
                try: stock = stock.strip()
                except: pass
                if stock == 'Add to Cart' or stock == 'Select options':
                    stock = 'In stock'
                else:
                    stock = 'Out of stock'

                items = {
                    'Title' : title,
                    'Quantity' : quantity,
                    'Actual Price in Rs' : a_price,
                    'Discounted Price in Rs' : d_price,
                    'Stock' : stock,
                    'Category' : category,
                    'Store' : 'Al Fatah'
                }
                print(items)
                exporter(items,'./results/alfatah.csv')

            next = resp.xpath('//div[@class="infinite-scrolling"]/a/@href').get()
            if next is None:
                break
            next = 'https://www.alfatah.pk' + next
            req = r.get(next)
            resp = Selector(text=req.text)

def naheed():
    url = 'https://www.naheed.pk/groceries-pets'
    req = r.get(url)
    resp = Selector(text=req.text)
    categories = resp.xpath('//div[@class="sub-category-title"]/a/@href').getall()
    for cat in categories:
        req = r.get(cat)
        resp = Selector(text=req.text)
        category = resp.xpath('(//h1[@class="page-title"]/span/text())[2]').get()
        while True:
            try: 
                divs = resp.xpath('//ol[@class="products list items product-items"]/li/div')
                for div in divs:
                    title = div.xpath('./div/div[2]/h2/a/text()').get()
                    quantity = quantity_fetcher(title)
                    price = div.xpath('./div/div[2]/div/span/span/span/text()').get()
                    try: price = (price.replace('Rs.', '').replace('.00','')).strip()
                    except: pass
                    stock = div.xpath('./div/div/div[2]/div/div/div/form/button/span/text()').get()
                    if stock == 'Add to Cart':
                        stock = 'In stock'
                    else:
                        stock = 'Out of stock'
                    items = {
                        'Title' : title,
                        'Quantity' : quantity,
                        'Actual Price in Rs' : price,
                        'Discounted Price in Rs' : '',
                        'Stock' : stock,
                        'Category' : category,
                        'Store' : 'Naheed'
                    }
                    print(items)
                    exporter(items,'./results/naheed.csv')
                next = resp.xpath('(//a[@class="action  next"])[2]/@href').get()
                req = r.get(next)
                resp = Selector(text=req.text)
            except:
                break
        
def qne():
    url = 'https://qne.com.pk/collections/grocery'
    req = r.get(url)
    resp = Selector(text=req.text)
    links = resp.xpath('(//div[@class="rte"])[1]/p/a/@href').getall()
    for link in links:
        req = r.get(link)
        resp = Selector(text=req.text)
        category = resp.xpath('//ol[@class="breadcrumb__list"]/li[position()>1]/span/text()').get()
        while True:
            divs = resp.xpath('//div[@id="Huratips-Loop"]/div/div')
            for div in divs:
                title = div.xpath('./div[2]/div[1]/a[1]/text()').get()
                if title is None:
                    title = div.xpath('./div[1]/div/a[1]/text()').get()

                quantity = quantity_fetcher(title)
                
                a_price = div.xpath('./div[2]/div/div/span[2]/text()[2]').get()
                try: a_price = (a_price.replace('Rs.', '').replace('.00','')).strip()
                except: pass

                d_price = div.xpath('./div[2]/div/div/span[1]/text()[2]').get()
                try: d_price = (d_price.replace('Rs.', '').replace('.00','')).strip()
                except: pass

                if a_price is None:
                    a_price = div.xpath('./div[1]/div/div/span/text()[2]').get()
                    try: a_price = (a_price.replace('Rs.', '').replace('.00','')).strip()
                    except: pass
                    d_price = ''

                stock = div.xpath('//div[@id="Huratips-Loop"]/div/div/div/form/button[1]/text()').get()
                if stock == 'Add to cart':
                    stock = 'In stock'
                else:
                    stock = 'Out of stock'

                items = {
                    'Title' : title,
                    'Quantity' : quantity,
                    'Actual Price in Rs' : a_price,
                    'Discounted Price in Rs' : d_price,
                    'Stock' : stock,
                    'Category' : category,
                    'Store' : 'QNE'
                    } 
                print(items)
                exporter(items,'./results/qne.csv')

            next = resp.xpath('//a[@class="pagination__next link"]/@href').get()
            if next is None:
                break
            next = 'https://qne.com.pk' + next
            req = r.get(next)
            resp = Selector(text=req.text)

def keryana():
    url = 'https://keryana.pk/'
    req = r.get(url)
    resp = Selector(text=req.text)
    links = resp.xpath('//div[@class="multiple-items"]/a/@href').getall()
    for link in links:
        req = r.get(link)
        resp = Selector(text=req.text)
        category = resp.xpath('//h3[@class="cate-title"]/text()').get()
        try: category = (category.replace('Search Result :','')).strip()
        except: pass

        while True:
            try:
                divs = resp.xpath('//li[@class="col-sm-3 product-item "]/div')
                for div in divs:
                    title = div.xpath('./div/div[2]/strong/a/text()').get()
                    if title is not None:
                        quantity = quantity_fetcher(title)

                        price = div.xpath('./div/div[2]/div/div/span/text()').get()
                        try: price = (price.replace('Rs', '')).strip()
                        except: pass

                        stock = div.xpath('./div/div[1]/button/span/text()').get()
                        if stock == 'Add to Cart':
                            stock = 'In stock'
                        else:
                            stock = 'Out of stock'

                        items = {
                            'Title' : title,
                            'Quantity' : quantity,
                            'Actual Price in Rs' : price,
                            'Discounted Price in Rs' : '',
                            'Stock' : stock,
                            'Category' : category,
                            'Store' : 'Keryana'
                        }
                        print(items)
                        exporter(items,'./results/keryana.csv')

                next = resp.xpath('//a[@rel="next"]/@href').get()
                req = r.get(next)
                resp = Selector(text=req.text)
            except:
                break

def fresh_basket():
    driver = get_driver()
    url = 'https://freshbasket.com.pk/?utm_source=googleads&utm_medium=search&utm_campaign=FreshBasket_GoogleAds_Search2021&gclid=CjwKCAjw-IWkBhBTEiwA2exyO6XUqS4w8mqoOKD5nuY28XgqIL-U6Qe8isW3ilVB8TjWjB9xXUs3mhoCSyMQAvD_BwE'
    driver.get(url)
    time.sleep(3)
    resp = Selector(text=driver.page_source)
    links = resp.xpath('(//a[@class="menu-link"])[position()>1]/@href').getall()
    for link in links:
        driver.get(link)
        time.sleep(3)
        scroller(driver)
        resp = Selector(text=driver.page_source)
        category = resp.xpath('//h1[@class="page-title"]/span/text()').get()
        divs = resp.xpath('//div[@class="product-item-info cat-border"]')
        for div in divs:
            title = div.xpath('./div[2]/strong/a/text()').get()
            try: title = title.strip()
            except: pass

            quantity = quantity_fetcher(title)
            price = div.xpath('./div[2]/div/span/span/span/span/text()').get()
            if price is None:
                price = div.xpath('./div[2]/div/span/span/span[@class="price"]/text()').get()
            try: price = (price.replace('Rs.','')).strip()
            except: pass
            
            items = {
                'Title' : title,
                'Quantity' : quantity,
                'Actual Price in Rs' : price,
                'Discounted Price in Rs' : '',
                'Stock' : '',
                'Category' : category,
                'Store' : 'Fresh Basket'
                }
            print(items)
            exporter(items,'./results/fresh-basket.csv')

def aljadeed():
    urls = []
    driver = get_driver()
    url = 'https://www.aljadeed.pk/'
    driver.get(url)
    time.sleep(6)
    resp = Selector(text=driver.page_source)
    links = resp.xpath('(//div[@class="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 MuiCard-root blink-style-f4juc9"])[1]/div[3]/div/div/a/@href').getall()
    for link in links:
        link = 'https://www.aljadeed.pk' + link
        driver.get(link)
        time.sleep(3)
        resp = Selector(text=driver.page_source)
        s_links = resp.xpath('(//div[@class="MuiGrid-root MuiGrid-container blink-style-1d3bbye"])[2]/div/a/@href').getall()
        for link in s_links:
            link = 'https://www.aljadeed.pk' + link
            driver.get(link)

            try: WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//a[contains(text(),"See more")]'))).click()
            except: pass

            try:
                elements = WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.XPATH,'//li[contains(text(),"Sections")]/following-sibling::li/label/span[2]')))
                for element in elements:
                    element.click()
                    time.sleep(5)
                    print(driver.current_url)
                    urls.append(driver.current_url)
            except:
                print(driver.current_url)
                urls.append(driver.current_url)
        
    for url in urls:
        driver.get(url)
        time.sleep(3)
        resp = Selector(text=driver.page_source)
        categories = ' > '.join(resp.xpath('//ol[@class="MuiBreadcrumbs-ol blink-style-nhb8h9"]/li[@class="MuiBreadcrumbs-li"][position()>1]//text()').getall())
        while True:
            divs = resp.xpath('//div[@class="MuiGrid-root MuiGrid-container blink-style-1a5qh6e"]/div/div')
            for div in divs:
                title = div.xpath('./div/div[1]/div/h4/text()').get()
                quantity = quantity_fetcher(title)
                price = div.xpath('.//div[@class="hazle-product-item_product_item_price_label__ET_we"]/span/text()').getall()
                if len(price) == 1:
                    try: a_price = ((''.join(price)).replace('Rs.','').replace('.00','')).strip()
                    except: pass
                    d_price = ''
                else:
                    a_price = price[0]
                    d_price = price[1]
                    try:
                        a_price = (a_price.replace('Rs.','').replace('.00','')).strip()
                        d_price = (d_price.replace('Rs.','').replace('.00','')).strip()
                    except:
                        pass

                stock = div.xpath('./div/div[2]/div/button/@aria-label').get()
                if stock == 'Add To Cart':
                    stock = 'In stock'
                else:
                    stock = 'Out of stock'
                items = {
                    'Title' : title,
                    'Quantity' : quantity,
                    'Actual Price in Rs' : a_price,
                    'Discounted Price in Rs' : d_price,
                    'Stock' : stock,
                    'Category' : categories,
                    'Store' : 'Al Jadeed'
                }
                print(items)
                exporter(items,'./results/aljadeed.csv')

            try: WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(),"Next")]'))).click()
            except: break
            time.sleep(3)
            resp = Selector(text=driver.page_source)

def imtiaz():
    driver = get_driver()
    driver.get('https://shop.imtiaz.com.pk/')
    time.sleep(3)
    try: 
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//input[@placeholder="Select Area"]'))).send_keys('Askari 1')
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//input[@placeholder="Select Area"]'))).send_keys(Keys.DOWN)
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//input[@placeholder="Select Area"]'))).send_keys(Keys.ENTER)
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(text(),'Select')]"))).click()
    except: pass
    time.sleep(2)

    resp = Selector(text=driver.page_source)
    links = resp.xpath('(//div[@class="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 MuiCard-root mui-style-f4juc9"])[1]/div[3]/div/div/a/@href').getall()
    for link in links:
        link = 'https://shop.imtiaz.com.pk/' + link
        driver.get(link)
        time.sleep(4)
        resp = Selector(text=driver.page_source)
        s_links = resp.xpath('(//div[@class="MuiGrid-root MuiGrid-container mui-style-1d3bbye"])[2]/div/a/@href').getall()
        for link in s_links:
            link = 'https://shop.imtiaz.com.pk/' + link
            driver.get(link)
            time.sleep(3)
            try:
                try: WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,'//a[contains(text(),"See more")]'))).click()
                except: pass
                spans = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH,"//li[contains(text(),'Section')]/../li[position()>1]/label/span[2]")))
                for span in spans:
                    span.click()
                    time.sleep(2)
                    resp = Selector(text=driver.page_source)
                    no_results = resp.xpath('//div[contains(text(),"No result found")]').get()
                    if no_results != 'No result found':
                        category = ' > '.join(resp.xpath('//ol[@class="MuiBreadcrumbs-ol mui-style-nhb8h9"]/li[@class="MuiBreadcrumbs-li"][position()>1]//text()').getall())
                        while True:
                            divs = resp.xpath('//div[@class="hazle-product-item_product_item__FSm1N MuiBox-root mui-style-5bkk4b"]')
                            for div in divs:
                                title = div.xpath('./div[2]/div[1]/div/h4/text()').get()
                                quantity = quantity_fetcher(title)
                                price = div.xpath('./div[2]/div[2]/div/div/span/text()').get()
                                try: price = (price.replace('Rs.','')).strip()
                                except: pass
                                stock = div.xpath('./div[2]/div[2]/div/button/@aria-label').get()
                                if stock == 'Add To Cart':
                                    stock = 'In stock'
                                else:
                                    stock = 'Out of stock'
                                items = {
                                    'Title' : title,
                                    'Quantity' : quantity,
                                    'Actual Price in Rs' : price,
                                    'Discounted Price in Rs' : '',
                                    'Stock' : stock,
                                    'Category' : category,
                                    'Store' : 'Imtiaz'
                                }
                                print(items)
                                exporter(items,'./results/imtiaz.csv')
                            try: WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(),"Next")]'))).click()
                            except: break
                            time.sleep(3)
                            resp = Selector(text=driver.page_source)
            except:
                resp = Selector(text=driver.page_source)
                category = ' > '.join(resp.xpath('//ol[@class="MuiBreadcrumbs-ol mui-style-nhb8h9"]/li[@class="MuiBreadcrumbs-li"][position()>1]//text()').getall())
                while True:
                    divs = resp.xpath('//div[@class="hazle-product-item_product_item__FSm1N MuiBox-root mui-style-5bkk4b"]')
                    for div in divs:
                        title = div.xpath('./div[2]/div[1]/div/h4/text()').get()
                        quantity = quantity_fetcher(title)
                        price = div.xpath('./div[2]/div[2]/div/div/span/text()').get()
                        try: price = (price.replace('Rs.','')).strip()
                        except: pass
                        stock = div.xpath('./div[2]/div[2]/div/button/@aria-label').get()
                        if stock == 'Add To Cart':
                            stock = 'In stock'
                        else:
                            stock = 'Out of stock'
                        items = {
                            'Title' : title,
                            'Quantity' : quantity,
                            'Actual Price in Rs' : price,
                            'Discounted Price in Rs' : '',
                            'Stock' : stock,
                            'Category' : category,
                            'Store' : 'Imtiaz'
                        }
                        print(items)
                        exporter(items,'./results/imtiaz.csv')
                    try: WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(),"Next")]'))).click()
                    except: break
                    time.sleep(3)
                    resp = Selector(text=driver.page_source)

def bin_hashim():
    driver = get_driver()
    url = 'https://binhashimonline.pk'
    driver.get(url)
    time.sleep(3)
    resp = Selector(text=driver.page_source)
    links = resp.xpath('//div[@id="category-slider"]/div[2]/div[3]/div/div/a/@href').getall()
    links = links[1:7]
    for link in links:
        link = 'https://binhashimonline.pk' + link
        driver.get(link)
        time.sleep(3)
     
        try: WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,'(//a[contains(text(),"See more")])[1]'))).click()
        except: pass

        divs = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH,'//li[contains(text(),"Sections")]/../li[position()>1]/label/span[2]')))
        for div in divs:
            div.click()
            time.sleep(5)
            resp = Selector(text=driver.page_source)
            categories = ' > '.join(resp.xpath('//ol[@class="MuiBreadcrumbs-ol blink-style-nhb8h9"]/li[@class="MuiBreadcrumbs-li"][position()>1]//text()').getall())
            while True:
                spans = resp.xpath('//div[@class="hazle-product-item_product_item__FSm1N MuiBox-root blink-style-1m795b"]')
                for span in spans:
                    title = span.xpath('./div[2]/div[1]/div/h4/text()').get()
                    quantity = quantity_fetcher(title)
                    price = span.xpath('./div[2]/div[2]/div/div/span/text()').get()
                    try: price = (price.replace('Rs.','').replace('.00','')).strip()
                    except: pass
                    stock = span.xpath('./div[2]/div[2]/div/button/@aria-label').get()
                    if stock == 'Add To Cart':
                        stock = 'In stock'
                    else:
                        stock = 'Out of stock'
                    items = {
                        'Title' : title,
                        'Quantity' : quantity,
                        'Actual Price in Rs' : price,
                        'Discounted Price in Rs' : '',
                        'Stock' : stock,
                        'Category' : categories,
                        'Store' : 'Bin Hashim'
                    }
                    print(items)
                    exporter(items,'./results/binhashim.csv')
                try: 
                    WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(text(),'Next')][@disabled]")))
                    break
                    
                except:
                    WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(text(),'Next')]"))).click()
                    time.sleep(3)
                    resp = Selector(text=driver.page_source)

def metro():
    driver = get_driver()
    driver.get('https://www.metro-online.pk/home?itm_pm=pk:nav_online-store-bucket:ctr:bhc:0:0')
    time.sleep(3)
    urls = [
        'https://www.metro-online.pk/store/grocery/desserts/jellies-and-custards',
        'https://www.metro-online.pk/store/grocery/desserts/traditional-mixes',
        'https://www.metro-online.pk/store/grocery/snacks/cakes-and-chocolates',
        'https://www.metro-online.pk/store/grocery/snacks/biscuits-and-wafers',
        'https://www.metro-online.pk/store/grocery/snacks/crisps-and-popcorn',
        'https://www.metro-online.pk/store/grocery/snacks/sweets-and-toffees'
        'https://www.metro-online.pk/store/grocery/snacks/jellies-and-marshmallows',
        'https://www.metro-online.pk/store/grocery/tea-and-coffee/tea',
        'https://www.metro-online.pk/store/grocery/tea-and-coffee/coffee-and-whiteners',
        'https://www.metro-online.pk/store/grocery/packaged-food/ready-to-eat-meals',
        'https://www.metro-online.pk/store/grocery/packaged-food/noodles-and-pasta',
        'https://www.metro-online.pk/store/grocery/canned-food/canned-fruits',
        'https://www.metro-online.pk/store/grocery/canned-food/canned-vegetables',
        'https://www.metro-online.pk/store/grocery/canned-food/pickles-and-olives',
        'https://www.metro-online.pk/store/Grocery/Home-Baking'
    ]
    for url in urls:
        driver.get(url)
        time.sleep(3)  
        resp = Selector(text=driver.page_source)
        categories = ' > '.join(resp.xpath('//ol[@class="MuiBreadcrumbs-ol css-nhb8h9"]/li[@class="MuiBreadcrumbs-li"][position()>1]/div/div/text()').getall())
        time.sleep(3)
        while True: 
            try:
                elements = len(driver.find_elements(By.XPATH,'//div[@class="MuiBox-root css-i9gxme"]/div/div[position()<last()]'))
                print(elements)
                driver.find_element(By.XPATH,'//button[contains(text(),"See more")]').click()
                time.sleep(3)
            except:
                break

        resp = Selector(text=driver.page_source)
        divs = resp.xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 MuiGrid-spacing-md-3 css-17ujhgm"]/div/div/div[1]')
        for div in divs:
            title = div.xpath('./div[4]/div/text()').get()
            quantity = quantity_fetcher(title)
            a_price = div.xpath('./div[6]/text()').get()
            d_price = div.xpath('./div[6]/span//text()').get()
            try: a_price = (a_price.replace('Rs.','')).strip()
            except: pass
            try: d_price = (d_price.replace('Rs.','')).strip()
            except: pass

            img = div.xpath('./div[2]/div/div/img/@src').get()
            items = {
                'Title' : title,
                'Quantity' : quantity,
                'Actual Price (in Rs.)' : a_price,
                'Discounted Price (in Rs.)' : d_price,
                'Category' : categories,
                'Image': img
            }
            print(items)
            exporter(items,'./output/metro.csv')
        time.sleep(3)

def chaseup():
    driver = get_driver()
    driver.get('https://chaseupgrocery.com/gulistan-e-johar-karachi')
    time.sleep(3)
    resp = Selector(text=driver.page_source)
    links = resp.xpath('(//a[@class="w-full"])[position()>1]/@href').getall()
    for link in links:
        link = 'https://chaseupgrocery.com' + link
        driver.get(link)
        time.sleep(3)
        resp = Selector(text=driver.page_source)
        s_links = resp.xpath('//div[@class="flex flex-row"]/a/@href').getall()
        for link in s_links:
            link = 'https://chaseupgrocery.com' + link
            driver.get(link)
            time.sleep(3)
            scroller(driver)
            resp = Selector(text=driver.page_source)
            category = ' > '.join(resp.xpath('//div[@class="flex flex-row text-xs font-normal w-full"]/a[position()>2]/text()').getall())
            divs = resp.xpath('//div[@class="infinite-scroll-component__outerdiv"]/div/div/div/div')
            for div in divs:
                title = div.xpath('./div[2]/div[2]/p/text()').get()
                quantity = div.xpath('./div[2]/div[3]/span/text()[1]').get()
                a_price = div.xpath('./div[2]/div[1]/div[1]/span/text()').get()
                try: a_price = (a_price.replace('PKR','')).strip()
                except: pass
                d_price = ''
                stock = div.xpath('./div[2]/div[4]/div/div/span[contains(text(),"Add to Cart")]/text()').get()
                if stock == 'Add to Cart':
                    stock = 'In stock'
                else:
                    stock = 'Out of stock'
                store = 'Chase up'
                items = {
                    'Title' : title,
                    'Quantity' : quantity,
                    'Actual Price in Rs' : a_price,
                    'Discounted Price in Rs' : d_price,
                    'Stock' : stock,
                    'Category' : category,
                    'Store' : store
                }
                print(items)
                exporter(items,'./results/chaseup.csv')
            
def carrefour():
    url = 'https://www.carrefour.pk/mafpak/en/'
    driver = get_driver()
    driver.get(url)
    time.sleep(3)
    resp = Selector(text=driver.page_source)
    links = resp.xpath('(//a[@rel="menu"])[position()>1]/@href').getall()
    for link in links:
        link = 'https://www.carrefour.pk' + link
        driver.get(link)
        time.sleep(3)
        resp = Selector(text=driver.page_source)
        s_links = resp.xpath('//div[@data-testid="banner-container"]/a/@href').getall()
        for link in s_links:
            link = 'https://www.carrefour.pk' + link
            driver.get(link)
            time.sleep(3)
            resp = Selector(text=driver.page_source)
            category = resp.xpath('//div[@class="css-qo9h12"]/div/div[2]/div/ol/li[position()>1]//text()').get()
            divs = resp.xpath('//ul[@data-testid="scrollable-list-view"]/div/div/div/div/div/div/ul/div')
            for div in divs:
                title = div.xpath('./div[3]/div[3]/a/text()').get()
                d_price = div.xpath('./div[3]/div[1][@data-testid="product_price"]/div/div/div[1]/text()').get()
                a_price = div.xpath('./div[3]/div[2][@data-testid="product-card-original-price"]/div/text()').get()
                if title is None:
                    title = div.xpath('./div[3]/div[2]/a/text()').get()
                    a_price= div.xpath('./div[3]/div[1]/div[1]/div[1]/div[1]/text()').get()
                quantity = quantity_fetcher(title)
                stock = 'In stock'
                items = {
                    'Title' : title,
                    'Quantity' : quantity,
                    'Actual Price in Rs' : a_price,
                    'Discounted Price in Rs' : d_price,
                    'Stock' : stock,
                    'Category' : category,
                    'Store' : 'Carrefour'
                }
                print(items)
                exporter(items,'./results/carrefour.csv')

if __name__ == '__main__':
    alfatah()
    naheed()
    qne()
    keryana()
    fresh_basket()
    aljadeed()
    imtiaz()
    chaseup()
    carrefour()
    metro()
    bin_hashim()