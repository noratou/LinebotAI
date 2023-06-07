'''
import requests
from bs4 import BeautifulSoup
def read(word):
    url = f'https://dict.revised.moe.edu.tw/search.jsp?md=1&word={word}#searchL'

    html = requests.get( url )
    bs = BeautifulSoup(html.text,'lxml')
    data = bs.find('table', id='searchL')
    try:
        row = data.find_all('tr')[2]
        chinese = row.find('cr').text
        phones = row.find_all('code')
        phone = [e.text for e in phones]
        s = " ".join( phone )
        # s = row.find('sub')
        return( chinese + s )
    except:
        return( '查無此字' )
'''
import requests
from bs4 import BeautifulSoup
from opencc import OpenCC

#簡中轉為繁中
def translate_to_traditionalch(text):
    cc = OpenCC('s2tw')  
    return cc.convert(text)

word = input('請輸入英文單字或詞句：')
url = f'https://dict.youdao.com/result?word={word}&lang=en'

html = requests.get(url)
bs = BeautifulSoup(html.text, 'lxml')
translation = bs.find('span', class_='trans')
phonetic = bs.find('span', class_='phonetic')
example_sentences_en = bs.find_all('div', class_='sen-eng')
example_sentences_ch = bs.find_all('div', class_='sen-ch')

if translation :
    trans = translation.text
    trans = translate_to_traditionalch(trans)
    print(f"中文翻譯：{trans}")
else:
    print("無翻譯資料")

if phonetic :
    pht = phonetic.text
    print(f"英文音標：{pht}")
else:
    print("無音標資料")

if len(example_sentences_en) > 0:
    for i in range(min(2, len(example_sentences_en))): #min取最小值
        example = example_sentences_en[i].text
        example = translate_to_traditionalch(example)
        print(f"英文例句{i+1}：{example}")

        example_ch = example_sentences_ch[i].text
        example_ch = translate_to_traditionalch(example_ch)
        print(f"例句中文{i+1}：{example_ch}")
else:
    print("無例句資料")
