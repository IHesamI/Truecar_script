from pip._vendor import requests
from bs4 import BeautifulSoup
from mysql import connector
import re 

the_header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
sql_connector=connector.connect(user="root" ,password="hesam1379",host="localhost",database="truecar")
cursor_sql_connector=sql_connector.cursor()
cursor_sql_connector.execute("SHOW TABLES;")
list_of_tables=cursor_sql_connector.fetchall()


for x in list_of_tables :
     if ('cars_of_truecar' in x ):
          cursor_sql_connector.execute("DROP TABLE cars_of_truecar")

cursor_sql_connector.execute("CREATE TABLE cars_of_truecar (car_brand_and_model VARCHAR(100) ,model_year VARCHAR(100),type_of_car VARCHAR(100), price_label VARCHAR(100), price VARCHAR(100), milage VARCHAR(100), location  VARCHAR(100), colors VARCHAR(100), condition_of_car  VARCHAR(100)) ")
for i in range (1,25):
     url="https://www.truecar.com/used-cars-for-sale/listings/?page=%i"%(i)
     conn=requests.get(url,headers=the_header)
     the_soup=BeautifulSoup(conn.text,'html.parser')
     browse_list=the_soup.find_all('div',attrs={'data-test':'cardContent'})
     for each_div in browse_list:
          car_brand_and_model=re.sub("\W"," ",each_div.find('span',attrs={"class":["vehicle-header-make-model text-truncate"]}).text)
          model_year=each_div.find('span',attrs={"class":["vehicle-card-year","font-size-1"]}).text
          type_of_car=re.sub("\W"," ",each_div.find('div',attrs={"data-test":"vehicleCardTrim"}).text)
          price_label=each_div.find('span',attrs={"data-test":"graphIconLabel"}).text
          price=re.sub("\$","",each_div.find('div',attrs={"data-test":"vehicleCardPricingBlockPrice"}).text)
          milage=each_div.find('div',attrs={"data-test":"vehicleMileage"}).text
          location=each_div.find('div',attrs={"data-test":"vehicleCardLocation"}).text
          colors=each_div.find('div',attrs={"data-test":"vehicleCardColors"}).text
          condition_of_car=each_div.find('div',attrs={"data-test":"vehicleCardCondition"}).text
          cursor_sql_connector.execute("INSERT INTO  cars_of_truecar (car_brand_and_model,model_year,type_of_car,price_label,price,milage,location,colors,condition_of_car) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"%(car_brand_and_model,model_year,type_of_car,price_label,price,milage,location,colors,condition_of_car))
     
sql_connector.commit()
