import requests
import json
import pymysql
from time import sleep


#SET @@global.sql_mode='';    需要在mysql中执行的命令，否则程序报错

i=1

domain="lenovo.com.cn"

table = domain.split('.')
table = table[0]
number=0


#cookie信息填充

cookies_value = {'_riskivy_identity':'',
				'access_token':'',
				'Hm_lpvt_54d3c7dc24fe556804419ed26990c8d7':'',
				'Hm_lvt_54d3c7dc24fe556804419ed26990c8d7':'',
				'PHPSESSID':''}

def get_domain(k):
	global i
	global number
	url="https://console.riskivy.com/spy?page="+str(k)+"&per-page=10&query=domain:%22"+str(domain)+"%22"
	response = requests.get(url=url,cookies=cookies_value)
	data = str(response.content,'utf-8')
	data = json.loads(data)
	for j in range(0,10):
		#print(j)
		#print(data)
		#print(data['data']['items'][j])
		title = data['data']['items'][j]['title']
		site_domain = data['data']['items'][j]['site_domain']
		site = data['data']['items'][j]['site']
		ip = data['data']['items'][j]['ip']
		status = data['data']['items'][j]['status']
		cname = data['data']['items'][j]['cname']
		headers = data['data']['items'][j]['headers']


		db = pymysql.connect('','','','')    #host,username,password
		cursor = db.cursor()

		number = int(j)+int(number)
		number = int(number)
		
		

		qy = 'insert into '+table+' (title,site_domain,site,ip,status,cname,headers) values(%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(qy,(pymysql.escape_string(title),pymysql.escape_string(site_domain),pymysql.escape_string(site),pymysql.escape_string(ip),pymysql.escape_string(str(status)),pymysql.escape_string(str(cname)),pymysql.escape_string(headers)))
		cursor.close()
		db.commit()
		db.close()

		i = i+1
	

def init_database():
	db = pymysql.connect('','','')  #host,username,password
	cursor = db.cursor()
	cursor.execute('CREATE DATABASE IF NOT EXISTS domain DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
	cursor.colse()
	db.close()



def init_table():
	db = pymysql.connect('localhost','root','','domain')
	cursor = db.cursor()

	cursor.execute('drop table if exists '+table)
	sql = "CREATE TABLE "+table+" ( ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,TITLE VARCHAR(100) NOT NULL,SITE_DOMAIN VARCHAR(100) NOT NULL,SITE VARCHAR(100) NOT NULL,IP VARCHAR(20) NOT NULL,STATUS VARCHAR(10) NOT NULL,CNAME VARCHAR(20) NOT NULL,HEADERS VARCHAR(2000) NOT NULL)AUTO_INCREMENT=1"
	
	cursor.execute(sql)
	db.close()


def main():
	url = "https://console.riskivy.com/spy?query=domain:%22"+domain+"%22"
	rs = requests.get(url=url,cookies=cookies_value)
	e_data = str(rs.content,'utf-8')
	#print(e_data)
	e_data = json.loads(e_data)
	totalCount = e_data['data']['_meta']['totalCount']
	pageCount = e_data['data']['_meta']['pageCount']

	print(totalCount)
	sleep(1)
	
	
	for x in range(1,int(pageCount)):
		print(x)
		if(number<totalCount):
			get_domain(x)
			sleep(1)
	
	

if __name__ == "__main__":
  init_db()
	init_table()
	main()
