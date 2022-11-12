import requests
from bs4 import BeautifulSoup
import xlwt
import re
'''
用requests.get获取url响应对象
'''
def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except requests.RequestException:
        return None
'''
对数字中间的非数字符号进行处理,正则表达式
'''
def number_process(s):
	rr = re.split('(\d+)',s)
	dd = rr[1]+re.split(rr[1],s)[1]    
	return dd
'''
将结果写入excel,不过其实可以用dataframe集体输入csv也可以,还避免excel的不稳定。
'''     
book1=xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet=book1.add_sheet('中国企业500强',cell_overwrite_ok=True)
sheet.write(0,0,'排名')
sheet.write(0,1,'名称')
sheet.write(0,2,'营收(百万元)')
sheet.write(0,3,'利润(百万元)')
sheet.write(0,4,'行业')
sheet.write(0,5,'公司地址')
sheet.write(0,6,'员工数')
sheet.write(0,7,'网站')

n=1

'''
此处特性为观察网页得到的结果
'''
def save_to_excel(soup):
	list = soup.find(attrs={"style":'word-break:break-all'}).find_all('a')
	'''
	对于所有style为word的行找到其所有的的'a',实质是网页中的主体中获取所有企业对应的详细信息网址
	'''
	for item in list:
		item_name=item.string
		item_revenue=item.find_parent().find_next_sibling().string
		item_revenue=item_revenue.replace(',','')
		'''
		带a的条目中文字内容为企业名,.string获取
		通过一个企业内部的整块中获取语句相应关系找到其他信息
		'''
		sub_url=item.get('href')
		'''
		获取该'a'中的href属性,即该企业更详细信息
		'''
		sub=sub_url.lstrip('../../')
		new_url="https://www.caifuzhongwen.com/fortune500/"+sub
		new_html=request_url(new_url)

		'''
		对于新链接格式的处理,主要是相对路径的问题
		'''
		text=BeautifulSoup(new_html,'lxml')

		'''
		对于新获取页面处理成beautifulsoup对象,该函数最初页面在外面调用了,其实不够严谨,直接内部调用也可以。
		'''

		'''
		item_name=text.find(class_='ui-title3').find_all('h1')
		temp=''
		for i in range(4,len(item_name)):
			if item_name[i]!='<':
				temp += temp.join(str(item_name[i]))
		item_name=temp
		'''
		
		'''
		这个地方对象不对 一个返回的是text就搞不了html了?
		所以findall的对象需要时啥,response步行 str没这个方法,就只有text对应find?可问题有没有key(此处的问题好像是没加text的bs处理的备注?s
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
		'''
		设置一个全局变量,方便每次计数,确定第几个企业
		'''
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
此处不能保存为xlsx
'''

'''
未解决的问题：
1. 为什么换成xls保存就可以了
2. 对于不对称标签页如何获取文字
3. 异常抛出,董事长名字缺失(try catch就行)
'''
