from pip._vendor import requests
from bs4   import BeautifulSoup
from mysql import connector
import re 

Company=input("Enter the name of brand: ")
Model=input("Enter the model of the car: ")
url="https://www.truecar.com/used-cars-for-sale/listings/%s/%s/"%(Company,Model)
Table_name=Company+"_"+Model
the_header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
conn=requests.get(url,headers=the_header)
print(conn)
the_soup=BeautifulSoup(conn.text,'html.parser')
browse_list=the_soup.find_all('div',attrs={'data-test':'cardContent'})
sql_connector=connector.connect(user="user" ,password="123456789",host="localhost",database="truecar")
cursor_sql_connector=sql_connector.cursor()
i =1
cursor_sql_connector.execute("CREATE TABLE %s (model_year VARCHAR(100),type_of_car VARCHAR(100), price_label VARCHAR(100), price VARCHAR(100), milage VARCHAR(100), location  VARCHAR(100), colors VARCHAR(100), condition_of_car  VARCHAR(100)) "%(Table_name))

for each_div in browse_list:
     model_year=each_div.find('span',attrs={"class":["vehicle-card-year","font-size-1"]}).text
     type_of_car=each_div.find('div',attrs={"data-test":"vehicleCardTrim"}).text
     price_label=each_div.find('span',attrs={"data-test":"graphIconLabel"}).text
     price=re.sub("\$","",each_div.find('div',attrs={"data-test":"vehicleCardPricingBlockPrice"}).text)
     milage=each_div.find('div',attrs={"data-test":"vehicleMileage"}).text
     location=each_div.find('div',attrs={"data-test":"vehicleCardLocation"}).text
     colors=each_div.find('div',attrs={"data-test":"vehicleCardColors"}).text
     condition_of_car=each_div.find('div',attrs={"data-test":"vehicleCardCondition"}).text
     cursor_sql_connector.execute("INSERT INTO  %s VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"%(Table_name,model_year,type_of_car,price_label,price,milage,location,colors,condition_of_car))
     if i==20:
          break
     
     i+=1
sql_connector.commit()