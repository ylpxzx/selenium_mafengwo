from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import time
import os
import urllib

browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)
url='http://www.mafengwo.cn/jd/10206/gonglve.html'
browser.get(url)
aomeng={}

def index_page():
    try:

        #获取总页数
        page_total=browser.find_elements_by_css_selector('span.count')
        total=page_total[0].text
        total_page=total[1:3]

        for i in range(1,int(total_page)-4):
            print('正在爬取第',str(i),'页')
            #实现下一页
            submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.m-pagination > a.pi.pg-next')))
            submit.click()

            html=browser.page_source
            parse_page(html)
            #print(html)
    except TimeoutException:
        print('超时')

    finally:
        browser.close()

def parse_page(html):
    doc=pq(html,parser="html")
    items=doc('.bd .scenic-list.clearfix .img').parent().items()
    for item in items:
        #标题
        aomeng['title']=item.find('h3').text()
        #子页链接
        aomeng['href']=item.attr('href')

        #图片链接
        aomeng['img']=item.find('.img').find('img').attr('src')
        time.sleep(3)
        save_img(aomeng)
def save_img(aomeng):
    if not os.path.exists(aomeng['title']):
        os.makedirs(aomeng['title'])
    with open('{0}/{0}.{1}'.format(aomeng['title'], 'txt'), 'a',encoding='utf-8')as f:
        f.write(aomeng['href'])
        print('写入txt文件成功')
    try:
        file_path = '{0}/{0}.{1}'.format(aomeng['title'], 'jpg')
        if not os.path.exists(file_path):
            urllib.request.urlretrieve(aomeng['img'], file_path)
            print('img 存入success!')
        else:
            print('Already Download or error')
    except :
        print('img 存入fail!')
        pass

index_page()