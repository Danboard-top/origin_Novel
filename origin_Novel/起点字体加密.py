import requests
import re
from fontTools.ttLib import TTFont,BytesIO
# 4. 请求字体文件的url，获取字体文件的内容。
url = 'https://book.qidian.com/info/1004608738'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
# print(response.text)
font_url = re.search(re.compile(r"@font-face.*?src.*?src: url\('(.*?)'\)", re.S), response.text).group(1)
# print(font_url)
font_response = requests.get(font_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}).content
with open('1.woff', 'wb') as f:
    f.write(font_response)

# 5. 将本地保存的qd.woff转化成qd.xml文件。
f = TTFont('1.woff')
f.saveXML('1.xml')
#
# # <span class="MZYjnXxB">&#100098;&#100098;&#100094;&#100090;&#100093;&#100094;</span></em>
# url = 'https://book.qidian.com/info/1004608738'





# 有用
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
# print(response.text)
font_url = re.search(re.compile(r"@font-face.*?src.*?src: url\('(.*?)'\)", re.S), response.text).group(1)
# print(font_url)
data = re.search(re.compile(r'<div class="book-info ">.*?<p>.*?<em>.*?<span class=".*?">(.*?)</span>', re.S), response.text).group(1)
# print(data)
#
num_list = []
numbers = data.split(';')
for num in numbers:
    if num:
        # %x：十六进制的占位符
        # print(num)
        res = '%x' % int(num.replace('&#', ''))
        # print(res)
        num_list.append(res)
print(num_list)










# print(font_url, num_list)
# # 4. 请求字体文件的url，获取字体文件的内容。
# font_response = requests.get(font_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}).content
# with open('qd.woff', 'wb') as f:
#     f.write(font_response)
#
# # 5. 将本地保存的qd.woff转化成qd.xml文件。
# f = TTFont('qd.woff')
# f.saveXML('qd.xml')
#
# # 6. 根据十六进制的列表，从xml中根据code的值获取map标签。解析xml标签结构。
# # [186f1, 186f2, 186f3, 186f4, 186f5]


# 有用
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
dicts_num = {'six':'6','one':'1','three':'3','period':'.','two':'2'}
strs = ''
for i in num_list:
    strs+=dicts_num[map_ele_dict[i]]
print(strs)


# def get_font(url):
#     response = requests.get(url)
#     font = TTFont(BytesIO(response.content))
#     cmap = font.getBestCmap()
#     font.close()
#     return cmap
# # http://www.dianping.com/shop/l5UJpRuaHBYaTjY3
# url = 'http://vfile.meituan.net/colorstone/f0a30a4dda64b4f8f344858115f54fc92296.woff'
# dicts=get_font(url)
# print(dicts)
# data = '&#xe343;&#xe7a1;&#xe137;&#xe7a1;'
# num_list = []
# numbers = data.split(';')
# for num in numbers:
#     if num:
#         # %x：十六进制的占位符
#         print(num)
#         res = int(num.replace('&#x', ''),16)
#         print(res)
#         num_list.append(res)
# print(num_list)
#
# from xml.etree import ElementTree
# root_obj = ElementTree.parse('猫眼.xml').getroot()
# maps_element = root_obj.find('GlyphOrder').findall('GlyphID')
# dict1={}
# for id in maps_element:
#     dict1[id.attrib['name']] = id.attrib['id']
#
# dict2 = {
# '2':6,
# '3':3,
# '4':7,
# '5':9,
# '6':1,
# '7':8,
# '8':0,
# '9':4,
# '10':2,
# '11':5,
# }
# strs = ''
# for i in num_list:
#     num = dict2[dict1[dicts[i]]]
#     strs+=str(num)
# print(strs[:-1]+'.'+strs[-1])
# # 在root_obj的基础上，开始查找<map>标签。
# # find()类似于selenium中的find()




