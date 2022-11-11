import requests
from bs4 import BeautifulSoup
import xlwt
import re

def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except requests.RequestException:
        return None

def number_process(s):
	rr = re.split('(\d+)',s)
	dd = rr[1]+re.split(rr[1],s)[1]    
	return dd
      
book1=xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet=book1.add_sheet('中国企业500强',cell_overwrite_ok=True)
sheet.write(0,0,'排名')
sheet.write(0,1,'名称')
sheet.write(0,2,'营收（百万元）')
sheet.write(0,3,'利润（百万元）')
sheet.write(0,4,'行业')
sheet.write(0,5,'公司地址')
sheet.write(0,6,'员工数')
sheet.write(0,7,'网站')

n=1


def save_to_excel(soup):
	list = soup.find(attrs={"style":'word-break:break-all'}).find_all('a')
	for item in list:
		item_name=item.string
		item_revenue=item.find_parent().find_next_sibling().string
		item_revenue=item_revenue.replace(',','')
		
		sub_url=item.get('href')
		sub=sub_url.lstrip('../../')
		new_url="https://www.caifuzhongwen.com/fortune500/"+sub
		new_html=request_url(new_url)
		text=BeautifulSoup(new_html,'lxml')
		'''
		
		item_name=text.find(class_='ui-title3').find_all('h1')
		temp=''
		for i in range(4,len(item_name)):
			if item_name[i]!='<':
				temp += temp.join(str(item_name[i]))
		item_name=temp
		'''
		
		'''
		这个地方tmd对象不对 一个返回的是text就他妈搞不了html了？
		所以findall的对象需要时啥，response步行 str没这个方法，就只有text对应find？可问题有没有key
		'''
		
		'''
		item_main = text.find(class_='ui-homerank box-s1').find_all('p')
		item_revenue=number_process((item_main[0].text))
		item_profit=number_process(item_main[1].text)
		item_rank=number_process(item_main[3].text)
		'''
		item_main = text.find(class_='ui-homerank box-s1').find_all('p')
		item_profit=number_process(item_main[1].text)
		item_profit=item_profit.replace(',','')
		item_sub = text.find(class_='ui-table1 box-s1').find_all('tr')
		item_info=[]
		for tr in item_sub:
			item_info.append(tr.find(attrs={"align":'right'}).string)
		item_industry=item_info[2]
		item_location=item_info[3]
		item_number=item_info[4]
		item_website=item_info[5]

		global n
		# print('爬取电影：' + item_index + ' | ' + item_name +' | ' + item_img +' | ' + item_score +' | ' + item_author +' | ' + item_intr )
		print(str(n) + ' | ' + item_name + ' | ' +item_revenue + ' | '  +item_profit + ' | ' + item_industry +' | ' + item_location +' | ' + item_number+' | ' + item_website )
		

		sheet.write(n, 0, str(n))
		sheet.write(n, 1, item_name)
		sheet.write(n, 2, float(item_revenue))
		sheet.write(n, 3, float(item_profit))
		sheet.write(n, 4, item_industry)
		sheet.write(n, 5, item_location)
		sheet.write(n, 6, item_number)
		sheet.write(n, 7, item_website)

		n = n + 1


url = 'https://www.caifuzhongwen.com/fortune500/paiming/china500/2022_%e4%b8%ad%e5%9b%bd500%e5%bc%ba.htm'
html = request_url(url)
soup = BeautifulSoup(html, 'lxml')
save_to_excel(soup)

book1.save(u'中国企业500强.xls')

'''
未解决的问题：
1. 为什么换成xls保存就可以了
2. 对于不对称标签页如何获取文字
3. 异常抛出，董事长名字缺失

'''
