from selenium import webdriver
import json
import csv
import time


def result(urls):
    start_time = time.clock()
    spis=[]
    i = 0
    urls = dict() #Создаем словарь, т.к. Расширяемый кодировщик JSON для структур данных Python. Поддерживает словари Python, как объекты JSON, исходя из example.json
    with open('result.csv', mode="r", encoding="utf-8") as csvfile: #Открываем файл result.csv, который мы создали из inn_list.xls
        reader = csv.DictReader(csvfile, delimiter=';')
        data = [] #Создаем список для хранения в нем значений инн
        for row in reader:
            #print(row)
            data.append(row) #Добавляем в список данные, полученные из result.csv

    while i < len(data): #Проходимся по всему списку
        s = ''
        s = str(data[i].values()) #Преобразуем данные из объекта в строку, чтоб изменить их
        s = s.replace('odict_values','').replace('([','').replace('])', '').replace(';','').replace("'","") #убираем лишние символы
        base_url = "https://fedresurs.ru/search/entity?code=" + s #получаем URL который будем парсить
        sp = {gug
            base_url
        }
        spis.append(sp) #Заносим URL'ы в список
        i = i + 1
    for url in spis: #Проходимся по списку URL'ов
         s = str(url).replace("{",'').replace("}",'').replace("'",'') #Убираем лишние символы
         if(len(str(url))== 56): #Проверяем длину URL'a т.к. инн у физ.лиц и у юр.лиц отличаются на 2
             person(s,urls) #вызываем парсер для физ.лица
         if(len(str(url))== 54):
             company(s,urls) #вызываем парсер для юр.лица
    print (time.clock() - start_time,"seconds") #используем таймер, чтобы вычислить время выполнения программы для 100 иннов






def person(base_url,urls): #Функция для парсинга данных физических лиц
    driver = webdriver.Chrome(executable_path = "C:/chromedriver.exe") #создаем элемент класса Chrome WebDriver
    driver.get(base_url) #метод GET перенаправляет к URL странице в параметре
    search = driver.find_elements_by_xpath("//td [@class = 'td_name']//a")
    for i in search:
        a = i.get_attribute('href') #Находим ссылку и обрезаем ее, чтобы получить GUID
        a = str(a)
        a = a.replace('https://fedresurs.ru/person/','')
        a = a.replace('https://fedresurs.ru/company/', '') #Данная обрезка создана чтоб получить валидный GUID, т.к. в инн листе было юр.лицо с длинной инн как у физ.лица.
    searchactive = driver.find_element_by_xpath("//table [@class = 'search-result']//td[3]").text #Определяем статус
    if (searchactive == 'Действующее'):
        isActive = True
    else:
        isActive = False
    boolorgnip = driver.find_element_by_xpath("//table [@class = 'search-result']//td[2]//div").text #Определяем ОРГН если он есть и инн
    if "ОГРН" in boolorgnip:
        searchorgnip = driver.find_element_by_xpath("//div [@class = 'field']//div[2]").text
        searchinn = driver.find_element_by_xpath("//div[2] [@class = 'field']//div[2]").text
    else:
        searchorgnip = " "
        searchinn = driver.find_element_by_xpath("//table [@class = 'search-result']//td[2]//div[2]").text
    searchfullname = driver.find_element_by_xpath("//table [@class = 'search-result']//td").text
    strisActive = str(isActive)
    innstr = str(searchinn)
    #Создаем элемент словаря URLS
    element_in_urls = {
        innstr: {
            "guid: ":str(a),
            "fullname: ":searchfullname,
            "orgnip: ":searchorgnip,
            "inn: ":searchinn,
            "isActive: ":strisActive
        }
    }
    urls.update(element_in_urls)
    # urls.append('fullname:' + searchfullname)
    # urls.append('ogrnip:' +searchorgnip)
    # urls.append('inn:' +searchinn)
    # urls.append('isActive:' +str(isActive))

    #print(urls)

    #Загружаем словарь в JSON файл
    with open("data_file.json","w",encoding="UTF-8") as write_file:
         json.dump(urls,write_file,ensure_ascii=False)

    driver.quit()

#Все комментарии аналогичны,кроме некоторых моментов
def company(base_url,urls):
    driver = webdriver.Chrome(executable_path = "C:/chromedriver.exe")
    driver.get(base_url)
    searchguid = driver.find_elements_by_xpath("//td [@class = 'td_name']//a")
    for i in searchguid:
        a = i.get_attribute('href')
        a = str(a)
        a = a.replace('https://fedresurs.ru/company/','')
        a = a.replace('https://fedresurs.ru/person/', '')
    searchactive = driver.find_element_by_xpath("//table [@class = 'search-result']//td[3]").text
    if (searchactive == 'Действующее'):
        isActive = True
    else:
        isActive = False

    searchorgnip = driver.find_element_by_xpath("//div [@class = 'field']//div[2]").text
    searchinn = driver.find_element_by_xpath("//div[2] [@class = 'field']//div[2]").text
    searchfullname = driver.find_element_by_xpath("//table [@class = 'search-result']//td").text
    #Обрезаем ту часть наименования, которая содержит адрес
    temp = searchfullname.find('\n')
    s = searchfullname[:temp]
    searchfullname = s

    strisActive = str(isActive)
    innstr = str(searchinn)

    element_in_urls = {
        innstr: {
            "guid: ":str(a),
            "fullname: ":searchfullname,
            "orgnip: ":searchorgnip,
            "inn: ":searchinn,
            "isActive: ":strisActive
        }
    }
    urls.update(element_in_urls)
    # urls.append('guid:' +a)
    # urls.append('fullname:' + searchfullname)
    # urls.append('ogrnip:' +searchorgnip)
    # urls.append('inn:' +searchinn)
    # urls.append('isActive:' +str(isActive))
    #print(urls)


    with open("data_file.json","w",encoding="UTF-8") as write_file:
        json.dump(urls,write_file,ensure_ascii=False)

    driver.quit()


#person("https://fedresurs.ru/search/entity?code=320700368070")
#company("https://fedresurs.ru/search/entity?code=5902174893")
result(urls=dict())
