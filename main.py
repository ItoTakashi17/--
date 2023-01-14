import requests
import xlsxwriter
from bs4 import BeautifulSoup
import lxml

workbook = xlsxwriter.Workbook('vulnerability.xlsx')  # 建立文件
worksheet = workbook.add_worksheet()  # 建表
worksheet.write(0, 0, 'name')
worksheet.write(0, 1, 'description')
worksheet.write(0, 2, 'URL')

keyword = input("请输入漏洞名称的关键字：")
data = requests.get('https://cve.mitre.org/cgi-bin/cvekey.cgi', params={'keyword': keyword})
soup = BeautifulSoup(data.text, 'lxml')
tb = soup.find('div', id='TableWithRules')

i = 0
k = 0
for v_list in tb.find_all('td'):
    if i % 2 == 0:
        name = v_list.text
        worksheet.write(k + 1, 0, name)
        href = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + v_list.a.attrs['href']
        worksheet.write(k + 1, 2, href)
    else:
        description = v_list.text
        worksheet.write(k + 1, 1, description)
    i = i + 1
    k = i // 2  # 在python3中，//表示向下取整除，/带有浮点数

workbook.close()
