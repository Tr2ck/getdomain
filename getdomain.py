import requests
import json
import xlwt
from time import sleep



# 初始化一个excel
excel = xlwt.Workbook(encoding='utf-8')
# 新建一个sheet
sheet = excel.add_sheet('xlwt_sheet1')
# 设置样式
style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 创建字体
font.name = u'微软雅黑'  # 字体类型
font.colour_index = 6  # 字体颜色
font.underline = True  # 下划线
font.italic = True  # 斜体
font.height = 400  # 字体大小   200等于excel字体大小中的10
style.font = font  # 设定样式
sheet.write(0, 0, 'title')
sheet.write(0, 1, 'site_domain')
sheet.write(0, 2, 'site')
sheet.write(0, 3, 'ip')
sheet.write(0, 4, 'status')
sheet.write(0, 5, 'cname')
sheet.write(0, 6, 'headers')


i=1

domain="baidu.com"   #域名


#填充cookies信息
cookies_value = {'_riskivy_identity':'',
				'access_token':'',
				'Hm_lpvt_54d3c7dc24fe556804419ed26990c8d7':'',
				'Hm_lvt_54d3c7dc24fe556804419ed26990c8d7':'',
				'PHPSESSID':''}

def get_domain(k):
	global i
	url="https://console.riskivy.com/spy?page="+str(k)+"&per-page=10&query=domain:%22"+str(domain)+"%22"
	response = requests.get(url=url,cookies=cookies_value)
	data = str(response.content,'utf-8')
	data = json.loads(data)
	for j in range(0,10):
		title = data['data']['items'][j]['title']
		site_domain = data['data']['items'][j]['site_domain']
		site = data['data']['items'][j]['site']
		ip = data['data']['items'][j]['ip']
		status = data['data']['items'][j]['status']
		cname = data['data']['items'][j]['cname']
		headers = data['data']['items'][j]['headers']
		sheet.write(i, 0, title)
		sheet.write(i, 1, site_domain)
		sheet.write(i, 2, site)
		sheet.write(i, 3, ip)
		sheet.write(i, 4, status)
		sheet.write(i, 5, cname)
		sheet.write(i, 6, headers)
		i = i+1
	





def main():
	url = "https://console.riskivy.com/spy?query=domain:%22"+domain+"%22"
	rs = requests.get(url=url,cookies=cookies_value)
	e_data = str(rs.content,'utf-8')
	e_data = json.loads(e_data)
	pageCount = e_data['data']['_meta']['pageCount']

	sleep(1)
	
	
	for x in range(1,int(pageCount)):
		print(x)
		get_domain(x)
		sleep(1)
	excel.save('//Users/tr2ck/'+domain+'.xlsx')
	
	

if __name__ == "__main__":
	main()
