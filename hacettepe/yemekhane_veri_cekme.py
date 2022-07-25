import requests
from bs4 import BeautifulSoup
import pandas as pd ##pandas kütüphanesi veriyi çektikten sonra daha düzgün bir tablo haline getirmemizi sağlamakta
import psycopg2

url = "http://www.sksdb.hacettepe.edu.tr/bidbnew/grid.php?parameters=qbapuL6kmaScnHaup8DEm1B8maqturW8haidnI%2Bsq8F%2FgY1fiZWdnKShq8bTlaOZXq%2BmwWjLzJyPlpmcpbm1kNORopmYXI22tLzHXKmVnZykwafFhImVnZWipbq0f8qRnJ%2BioF6go7%2FOoplWqKSltLa805yVj5agnsGmkNORopmYXam2qbi%2Bo5mqlXRrinJdf1BQUFBXWXVMc39QUA%3D%3D"
response = requests.get(url)
html_icerigi = response.content
soup = BeautifulSoup(html_icerigi,"html.parser")

#panel = soup.find_all("div",{"class":"panel-grid-cell col-md-6"})
tarih = soup.find_all("div",{"class":"popular"})  ##html bloğunun class özelliğinin ismine göre seçim yapılıyor
yemekler = soup.find_all("p")

liste = list()

for i in range(len(tarih)):  #veriler listeye ekleniyor
    tarih[i] = (tarih[i].text).strip("\n").strip()
    yemekler[i] = (yemekler[i].text).strip("\n").strip()
    liste.append([tarih[i],yemekler[i]])

df = pd.DataFrame(liste,columns = ["tarih","yemekler"])  ##“DataFrame“ fonksiyonu kullanarak tüm bilgileri içinde bulunduran listeyi daha okunur bir tablo haline getirilmekte
print(df)

df.to_csv('hacettepe_yemekhane_liste.csv', encoding='utf-8-sig') ##excel dosyasına yazdırma

connection = psycopg2.connect(user="postgres",
                          password="5432",
                          host="localhost",
                          port="5432",
                          dbname="gmk654")
