import requests
from bs4 import BeautifulSoup
from translate import Translator
import xml.etree.ElementTree as ET
from googletrans import Translator

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.60'
    , 'accept': '*/*'}

translator = Translator()


def translate_text(text):
    translator = Translator(to_lang="uk")
    translation = translator.translate(text)
    return translation



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
	

    horoscope_data = {
        "date_today": '',
        "horoscop_data": {
           	"aries":		  { },
		    "taurus":		  { },
		    "gemini":		  { },
		    "cancer":		  { },
		    "leo":		  	  { },
		    "virgo":		  { },
		    "libra":		  { },
		    "scorpio":		  { },
		    "sagittarius":	  { },
		    "capricorn":	  { },
		    "aquarius":		  { },
		    "pisces":		  { },
        }
    }

    date_element = soup.find('date')
    horoscope_data["date_today"] = {
        "yesterday": date_element["yesterday"],
        "today": date_element["today"],
        "tomorrow": date_element["tomorrow"],
        "tomorrow02": date_element["tomorrow02"]
    }
    
    
    for sign in horoscope_data["horoscop_data"]:
        sign_element = soup.find(sign)
        horoscope_data["horoscop_data"][sign] = {
            "yesterday": 	translator.translate(sign_element.find("yesterday").text.strip(),   dest='uk').text,
            "today": 		translator.translate(sign_element.find("today").text.strip(),       dest='uk').text,
            "tomorrow": 	translator.translate(sign_element.find("tomorrow").text.strip(),    dest='uk').text,
            "tomorrow02": 	translator.translate(sign_element.find("tomorrow02").text.strip(),  dest='uk').text
        }

    return horoscope_data
   


def parse(URL="https://ignio.com/r/export/utf/xml/daily/com.xml"):
    html = get_html(URL)
    if html.status_code == 200:
        json = get_content(html.text)
        return json
    else:
        print('Error')
        
        


if __name__ == "__main__":
    data = parse()
    for key in data['horoscop_data']:
        print(data['horoscop_data'][key]['yesterday'])
        print(data['horoscop_data'][key]['today'])
        print(data['horoscop_data'][key]['tomorrow'])
        print(data['horoscop_data'][key]['tomorrow02'])

