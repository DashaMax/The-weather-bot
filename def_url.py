import requests, re
from bs4 import BeautifulSoup

def text_weather_time(url):

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        list_div_1 = soup.find_all('div', class_='weather-now-info')
        now_time = re.findall(r'(\d{2}:\d{2}, \d \w{3})', str(list_div_1))
        weather_now_1 = re.findall(r'([+-]\d{1,2})', str(list_div_1))
        weather_now_2 = re.findall(r'title="([\s\w]+)"></span', str(list_div_1))
        list_div_2 = soup.find_all('div', id='weather-now-description')
        sensetive = re.findall(r'([+-]\d{1,2}.)', str(list_div_2))
        bar = re.findall(r'(\d{3} мм рт\. ст\.)', str(list_div_2))
        vlaj = re.findall(r'(\d{1,2}%)', str(list_div_2))
        text_mess = 'Время: ' + str(now_time[0]) + '\nПогода:\n' + str(weather_now_1[0]) + ' ' + str(weather_now_2[0]) + '\nОщущается: ' + str(sensetive[0]) + '\nДавление: ' + str(bar[0]) + '\nВлажность: ' + str(vlaj[0])
    except:
        pass
    return text_mess