import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
 
num = 0
numPicture = 0
file = ''
List = []
 
 
# 根据地址去查找 对应的图片的信息
def Find(url, A):
    global List  # 保存信息的列表
    print('正在检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        # 时间戳 不简单刷新访问网址
        Url = url + str(t)
        try:
            # get获取数据
            Result = A.get(Url, timeout=7, allow_redirects=False)
        except BaseException:
            t = t + 60
            continue
        else:
            # 拿到网站的数据
            result = Result.text
            # 找到图片url
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)
            # 图片总数
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s
 
 
# 记录相关数据
def recommend(url):
    Re = []
    try:
        html = requests.get(url, allow_redirects=False)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        # html文件解析
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re
 
 
# 下载图片
def dowmloadPicture(html, keyword):
    global num
    # 找到图片url
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    print('找到关键词:' + keyword + '的图片，开始下载图片....')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = file + r'\\' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return
 
 
if __name__ == '__main__':  # 主函数入口
    # 模拟浏览器 请求数据 伪装成浏览器向网页提取服务
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Upgrade-Insecure-Requests': '1'
    }
 
    # 创建一个请求的会话
    A = requests.Session()
    # 设置头部信息
    A.headers = headers
 
    word = input("输入要搜索的关键词:")
    # 拼接路径
    url = 'https://image.baidu.com/search/flip?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs1&word=' + word
 
    # 根据路径去查找
    total = Find(url, A)
    # 记录相关推荐图片
    Recommend = recommend(url)
    print('经过检测%s类图片共有%d张' % (word, total))
 
    numPicture = int(input('输入要下载的数量'))
    file = input('请建立一个存储图片的文件夹，输入文件夹名称即可: ')
    y = os.path.exists(file)
    if y == 1:
        print('该文件已存在，请重新输入')
        file = input('请建立一个存储图片的文件夹，)输入文件夹名称即可: ')
        os.mkdir(file)
    else:
        os.mkdir(file)
    print(f"文件路径：{file}")
 
    t = 0
    tmp = url
 
    while t < numPicture:
        try:
            url = tmp + str(t)
            result = requests.get(url, timeout=10)
            print(url)
        except error.HTTPError as e:
            print('网络错误，请调整网络后重试')
            t = t + 60
        else:
            dowmloadPicture(result.text, word)
            t = t + 60