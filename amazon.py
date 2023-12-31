from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import re
import traceback
#直接コードで呼び出さないためグレー表示
import chromedriver_binary

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
driver = webdriver.Chrome(options=options)
driver.set_window_size(950, 800)
#暗黙的な待機
driver.implicitly_wait(10)


def amazon(word):
    
    try:#*Amazonのurlを取得
        print("Amazon_スクレイピング開始")
        driver.get("https://www.amazon.co.jp/")

        #暗黙的な待機
        driver.implicitly_wait(10)

        #検索欄のタグを取得、keywordと入力
        text_box=driver.find_element_by_id("twotabsearchtextbox")
        text_box.send_keys(word)

        #検索ボタンのタグを取得、クリック
        btn=driver.find_element_by_id("nav-search-submit-button")
        btn.click()

        print("Amazon_検索完了")

        #検索結果一覧のurlを取得し、beautiful soupのrequestsで価格をまとめて取得
        from bs4 import BeautifulSoup

        #検索結果のurlを取得し、きれいに抽出
        page_source=driver.page_source
        html_amazon=BeautifulSoup(page_source,"lxml")

        #商品名、価格、送料、ポイント,検索結果のurlを表示
        product_name_amazon=html_amazon.find(class_="a-size-base-plus a-color-base a-text-normal")
        price_amazon=html_amazon.find(class_="a-price-whole")
        shipping_fee_amazon=html_amazon.find(class_="a-row a-size-base a-color-secondary s-align-children-center")
        #ポイントだけ抽出、正規表現で数字だけ取り出す
        point=html_amazon.find(class_="a-size-base a-color-price")
        point_amazon=re.findall("[0-9]+",point.text)
        url_amazon=driver.current_url

        #リスト化、カンマを取り除いて見やすくする
        list_amazon=["【Amazon】",product_name_amazon.text,"￥"+price_amazon.text,shipping_fee_amazon.contents[1].text,point_amazon[0],url_amazon]
        traceback.print_exc()
        print("Amazon_スクレイピング完了")
        
    except Exception as e:
        print("Amazon_スクレイピング失敗")
        print(e)
        traceback.print_exc()
        list_amazon=["【Amazon】","-","-","-","-","-"]

    return list_amazon