import requests
from bs4 import BeautifulSoup
import re
import smtplib
import time

def remove_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def send_mail(price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('email@gmail.com', 'password')

    subject = 'Price fell down!'
    body = (f'Xbox now at {price}')

    msg = (f'Subject: {subject}\n\n{body}')
    server.sendmail(
        'email@gmail.com',
        'email@gmail.com',
        msg)
    print('Email has been sent')
    server.quit()

def check_price(URL, headers):
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id= "productTitle")

    price = soup2.find(id= "priceblock_ourprice")

    cleantitle = remove_tags(str(title))
    cleanprice = remove_tags(str(price))
    converted_price = int(cleanprice[1:4])

    if (converted_price > 250):
        send_mail(converted_price)

    print(cleantitle)
    print(converted_price)



URL = 'https://www.amazon.com/Xbox-One-X-1TB-Console/dp/B074WPGYRF/ref=sxin_0_osp34-f3f88392_cov?ascsubtag=amzn1.osa.f3f88392-19fd-4e1f-9af9-631ad943523a.ATVPDKIKX0DER.en_US&creativeASIN=B074WPGYRF&cv_ct_cx=nintendo+switch&cv_ct_id=amzn1.osa.f3f88392-19fd-4e1f-9af9-631ad943523a.ATVPDKIKX0DER.en_US&cv_ct_pg=search&cv_ct_wn=osp-search&dchild=1&keywords=nintendo+switch&linkCode=oas&pd_rd_i=B074WPGYRF&pd_rd_r=81dcbe0a-7ae5-479b-8d06-dc5ae8589402&pd_rd_w=kVFpP&pd_rd_wg=84ugY&pf_rd_p=b6bd5224-05d9-4fef-a730-ce19a634e012&pf_rd_r=CEEPMFQEYJ3D4TJY7AA2&qid=1586390286&sr=1-2-32a32192-7547-4d9b-b4f8-fe31bfe05040&tag=lifewirepublish-20'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}


while True:
    check_price(URL, headers)
    time.sleep(60*60*24)
