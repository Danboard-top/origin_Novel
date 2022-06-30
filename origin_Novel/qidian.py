import re
import requests
# 用于转变文件
from fontTools.ttLib import TTFont, BytesIO

url = 'https://book.qidian.com/info/1033903093/'
response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
# print(response.text)
# 1.获取加密字符类型的包
demo = re.compile(r"@font-face.*?src: url.*? src: url\('(.*?)'\) format\('woff'\)", re.S)
font_url = re.search(demo, response.text).group(1)
# print(font_url)
# 2.获取文件内容
font_response = requests.get(font_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}).content
# print(font_response)
# 3.写入本地文件
# wb：以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
with open('1.woff', 'wb') as f:
    f.write(font_response)

# 4.将'1.woff'转变为 xml文件；TTFont打开当前目录中的woff文件
f = TTFont('1.woff')
f.saveXML('1.xml')

# 5.将加密字符正则提取出来：
demo2 = re.compile(r'<div class="book-info ">.*?<p>.*?<em>.*?<span class=".*?">(.*?)</span>', re.S)
data = re.search(demo2, response.text).group(1)
# print(data)
# &#100175;&#100171;&#100170;&#100169;&#100171;
num_list = []
numbers = data.split(';')
for num in numbers:
    if num:
        # 转为16进制，删除&#
        res = '%x' % int(num.replace('&#', ''))
        num_list.append(res)
# print(num_list)


from xml.etree import ElementTree
# # 获取xml文件的根节点(文档树对象) obj(<Element object xxx>) = etree.HTML(page_source, parse=etree.HTMLParse(encoding="utf8"))
root_obj = ElementTree.parse('1.xml').getroot()
# # 在root_obj的基础上，开始查找<map>标签。
# # find()类似于selenium中的find()
# # <Element 'cmap_format_12' at 0x0000000003B2F548>
maps_element = root_obj.find('cmap').find('cmap_format_12').findall('map')
# # 遍历maps_element这个列表，里面保存的全部都是<Element 'map' at xxx>对象。
map_ele_dict = {}
for map_ele in maps_element:
    # 取出map标签内的code和name属性的值。
    # 以code为键，以name为值，保存到字典map_ele_dict
    map_ele_dict[map_ele.attrib['code'].replace('0x', '')] = map_ele.attrib['name']
print(num_list)
print(map_ele_dict)
dicts_num = {'zero': '0', 'six': '6', 'one': '1', 'three': '3', 'period': '.', 'two': '2'}
strs = ''
for i in num_list:
    strs += dicts_num[map_ele_dict[i]]
print(strs)


