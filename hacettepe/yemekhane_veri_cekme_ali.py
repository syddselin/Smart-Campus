import psycopg2
import requests
from bs4 import BeautifulSoup
import re

url = "http://www.sksdb.hacettepe.edu.tr/new/grid.php?parameters=qbapuL6kmaScnHaup8DEm1B8maqturW8haidnI%2Bsq8F%2FgY1fiZWdnKShq8bTlaOZXq%2BmwWjLzJyPlpmcpbm1kNORopmYXI22tLzHXKmVnZykwafFhImVnZWipbq0f8qRnJ%2BioF6go7%2FOoplWqKSltLa805yVj5agnsGmkNORopmYXam2qbi%2Bo5mqlXRt"
response = requests.get(url)
html_icerigi = response.content
soup = BeautifulSoup(html_icerigi, "html.parser")

tarih = soup.find_all("div", {"class":"popular"})  ##html bloğunun class özelliğinin ismine göre seçim yapılıyor
yemekler = soup.find_all("p")


def bulkInsert(records):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="443316",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()


        sql_insert_query = f""" INSERT INTO campuslife_yemekhane ("Tarih", "Gün", "Çorba", "Ana_Yemek", "Yan_Yemekler", "Kalori") 
                               VALUES (%s,%s,%s,%s,%s,%s) """
        result = cursor.executemany(sql_insert_query, records)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into yemekhane table")


    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into table ".format(error))

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


yemeklist = []
callist = []
records_to_insert = []
for i in range(len(tarih)):  #veriler listeye ekleniyor
    tarih[i] = (tarih[i].text).strip("\n").strip()
    t = tarih[i].split(" ")
    date = t[1]
    gun = t[2]

    yemekler[i] = str(yemekler[i]).split("Kalori")
    yemeklist.append(str(yemekler[i][0]).split("br"))
    a = list(map(lambda x: (x.translate({ ord(c): None for c in "></[]'" })).strip(), yemeklist[i]))
    corba = a[1]
    anayemek = (a[2] + "/" + a[-2])
    yan1 = [x for x in a if (x != a[0] and x != a[1] and x != a[2] and x != a[-1] and x != a[-2])]
    yan = ('-'.join(yan1))

    b = str(yemekler[i][1]).split("br")
    res = re.findall(r'\d+', str(b))
    calori = (''.join(res))

    records_to_insert.append((date, gun, corba, anayemek, yan, calori))
    
print(records_to_insert)

bulkInsert(records_to_insert)
