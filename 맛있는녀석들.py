from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
from time import sleep
import re
from time import sleep

# 주소 정리한 블로그
web_url = 'http://nagae.tistory.com/4'
r = urllib.request.urlopen(web_url)

soup = BeautifulSoup(r,"lxml")

restaurant_detail = []
restaurant_detail.append({})


location = 0
episode = ''
food = ''
temp = 0

x = re.compile('[0-9]*회')


for i in soup.select('div.area_view p'):
    if '<br/>' in str(i):
        for text in str(i).split('<br/>'):
            text = re.sub('<.+?>','',text,0).strip()
            if x.findall(text):
                episode = x.findall(text)[-1]
            elif '[' in text:
                a = text.find('[')
                b = text.find(']')
                food = text[a+1:b]
                temp = 1
            elif temp == 1:
                if '~' in text:
                    text=text[:text.find('~')]
                info = text
                restaurant_detail[location]['food'] = food
                restaurant_detail[location]['episode'] = episode
                restaurant_detail[location]['info'] = info
                temp = 0
                location+=1
                restaurant_detail.append({})
                
    else:
        i = i.get_text()
        if x.findall(i):
            episode = x.findall(i)[-1]
        elif '[' in i:
            a = i.find('[')
            b = i.find(']')
            food = i[a+1:b]
            temp = 1
        elif temp == 1:
            if '~' in i:
                i = i[:i.find('~')]
            info = i 
            restaurant_detail[location]['food'] = food
            restaurant_detail[location]['episode'] = episode
            restaurant_detail[location]['info'] = info
            temp = 0
            location+=1
            restaurant_detail.append({})

restaurant_detail.pop()
restaurant_detail
        
final = {}
for i in range(len(restaurant_detail)):
    final[i] = {}
    for x in restaurant_detail[i]:
        final[i][x] = restaurant_detail[i][x]

# 크롬 드라이버 주소
drivers = webdriver.Chrome('')
drivers.get('https://map.naver.com/v5/search/%EC%84%9C%EA%B0%95%EA%B3%B1%EC%B0%BD/place/1841110864?c=14130109.6359549,4516243.5977155,15,0,0,0,dh')
sleep(5)

food_data = []
exception = []

for i in range(len(final)):

    food_data.append({})
    html = "/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-entry/entry-layout/entry-place/search-box/div/div/div/input"
    html_temp = "/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-box/div/div/div/input"
    try:
        element = drivers.find_element_by_xpath(html)
    except:
        element = drivers.find_element_by_xpath(html_temp)
    element.clear()
    element.send_keys(final[i]['info']+'\n')
    sleep(3)

    try:
        drivers.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-entry/entry-layout/entry-place/div/div[2]/div/div[1]/div[4]/entry-common-info/div/div[6]/button').click()
    except:
        try:
            drivers.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-entry/entry-layout/entry-place/div/div[2]/div/div[1]/div[4]/entry-common-info/div/div[7]/button').click()
        except:

    
    try:
        title = drivers.find_element_by_class_name('summary_title')
        food_data[i]['title'] = title.text
        food_data[i]['link'] = 'http://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query='+title.text
        food_data[i]['main_food'] = final[i]['food']
        food_data[i]['episode'] = final[i]['episode']
    except:
        exception.append(final[i]['info'])
        continue
    
    pageString = drivers.page_source
    bsObj = BeautifulSoup(pageString,"lxml")
    category = bsObj.find('span',{'class':'summary_category ng-star-inserted'})
    
    if category:
        category = category.get_text()
    else:
        category = None
    
    food_data[i]['category'] = category

    address = bsObj.find('a',{'class':'end_title ng-star-inserted'})
    if address:
        address = address.get_text()
    else:
        address = None
        
    food_data[i]['address'] = address

    temp = bsObj.find('div',{'class':'item_end phone ng-star-inserted'})
    phoneNum = temp.find('a',{'class':'link_end'})
    if phoneNum:
        phoneNum = phoneNum.get_text()
    else:
        phoneNum = None
        
    food_data[i]['phoneNum'] = phoneNum

    trivialInfo = bsObj.find('ul',{'class':'list_business'})
    if trivialInfo:
        trivialInfo = trivialInfo.get_text()
    else:
        trivialInfo = None

    food_data[i]['trivialInfo'] = trivialInfo
    
        
    menu_temp = bsObj.find_all('li',{'class':'item_menu ng-star-inserted'})
    food_data[i]['menus'] = []
    for j in menu_temp:
        menu = j.find('span',{'class':'menu_name'}).get_text()
        price = j.find('span',{'class': 'menu_price'}).get_text()
        food_data[i]['menus'].append(menu+'   '+price)
    
    sleep(2)

 
final_data = food_data[:]
while True:
    if {} not in final_data:
        break
    final_data.remove({})

final_data

#크롬 드라이버 주소
drivers = webdriver.Chrome()
drivers.get('http://www.dawuljuso.com/index.php')
html = '/html/body/div[4]/div[1]/div[1]/div[1]/input'
button = '/html/body/div[4]/div[1]/div[1]/div[2]'

x = re.compile('[0-9]*[0-9]')

for i in range(len(final_data)):
    element = drivers.find_element_by_xpath(html)
    element.clear()
    element.send_keys(final_data[i]['address'])
    drivers.find_element_by_xpath(button).click()
    sleep(1)
    pageString = drivers.page_source
    bsObj = BeautifulSoup(pageString,"lxml")
    s1 = bsObj.find('td',{'id':'insert_data_5'}).get_text()
    
    temp = x.findall(s1)
    if temp:
        lat = temp[2]+'.'+temp[3]
        lng = temp[0]+'.'+temp[1]
        final_data[i]['lat'] = lat
        final_data[i]['lng'] = lng
    sleep(2)
    
final_final = []
for i in range(len(final_data)):
    if 'lat' in final_data[i]:
        final_final.append(final_data[i])
