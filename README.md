# top_500_enterprises
​

1. 首先爬取公司名字和营收（百万元），可以看的style以及规整的tr

2. 任意选中1个可以发现公司的名字在<a  href >中间，且我们接下来要爬取的信息也要建立在超链接之上，所以这里将所有超链接的标签储存在list中：

list = soup.find(attrs={"style":'word-break:break-all'}).find_all('a')

 这样接下来直接string就可以获取公司名字：

for item in list:
		item_name=item.string

3. 然后通过寻找父母节点和兄弟节点确定营收：

		item_revenue=item.find_parent().find_next_sibling().string

//一开始并没有选择此处来爬取信息，而是直接打开超链接，但下一页的信息的标签不规整，处理起来对象关系太复杂，故最好一开始找规整的整理，会更为方便



 4. 通过get方法获取超链接，此处需要处理相对路径；且由于打开新的页面，需要将html转为soup

笔者在写的时候遇到了response不能进行处理，亦或是str没法使用方法（用了response.content）

        sub_url=item.get('href')
		sub=sub_url.lstrip('../../')
		new_url="主站网址"+sub
		new_html=request_url(new_url)
		text=BeautifulSoup(new_html,'lxml')

 5. 接下来的处理就相当规整了：class——tr——align：right，直接find_all 当成数组处理



        item_sub = text.find(class_='ui-table1 box-s1').find_all('tr')
		item_info=[]
		for tr in item_sub:
			item_info.append(tr.find(attrs={"align":'right'}).string)
		item_industry=item_info[2]
		item_location=item_info[3]
		item_number=item_info[4]
		item_website=item_info[5]
6. 遇到的问题及解决：

（1）对于<br>的处理：非标准的标签先find_all获取数组，再".text"获取文本，之后用正则表达式选取数字出来就好了



def number_process(s):
	rr = re.split('(\d+)',s)
	dd = rr[1]+re.split(rr[1],s)[1]    
	return dd        

        item_main = text.find(class_='ui-homerank box-s1').find_all('p')
		item_profit=number_process(item_main[1].text)
 （2）数字导出到excel是文本，且有逗号：

		item_revenue=item_revenue.replace(',','')
float（）或int（）转换就好

（3）导出格式为xlsx会打不开，转成xls即可

（4）收集的数据有中文：

def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except requests.RequestException:
        return None
将response.text 变为response.content即可

完整代码见下：

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
		new_url="主站网址"+sub
		new_html=request_url(new_url)
		text=BeautifulSoup(new_html,'lxml')
		
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


url = '目标网址'
html = request_url(url)
soup = BeautifulSoup(html, 'lxml')
save_to_excel(soup)

book1.save(u'文件名.xls')
//整体框架参考：

python爬虫08 | 你的第二个爬虫，要过年了，爬取豆瓣最受欢迎的250部电影慢慢看
