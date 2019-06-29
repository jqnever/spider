import requests
import re
import pymysql

class Mysql:

    conn = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'root',
        db = 'novel',
        charset = 'utf8'   #不要写-8
    )

    def addChapter(self,name,content):
        cursor = self.conn.cursor()  #创建游标
        cursor.execute('insert into novel.novel(name,content) values ("{}","{}")'.format(name,content)) #执行sql语句
        cursor.close()  #关闭
        self.conn.commit()  #提交 否则不存在

#获取小说列表
def getNovelUrlList(page=1):
    reponse = requests.get('https://www.quanben.net/list/1_{}.html'.format(page))
    reponse.encoding = 'gbk'
    html = reponse.text
    reg = r'<span class="s2"><a href="(.*?)">(.*?)</a>'
    novellist = re.findall(reg, html)
    return novellist

#获取小说章节
def getNovelChapterList(url):
    reponse = requests.get(url)
    reponse.encoding = 'gbk'
    html = reponse.text
    reg = r'<dd><a href="/.*?/.*?/(.*?).html">(.*?)</a></dd>'
    chapterlist = re.findall(reg, html)
    return chapterlist

def getNovelContent(url):  #获取小说内容
    reponse = requests.get(url)
    reponse.encoding = 'gbk'
    html = reponse.text
    reg = '''>下一页</a></div>
            <div id="BookText">(.*?)</div>
			<center><script>'''
    reg = re.compile(reg, re.S)
    content = re.findall(reg, html)
    return content

mysql = Mysql()   #实例化一个对象

for page in range(1,1345):

    for novelurl in getNovelUrlList(page):
        print(novelurl)
        for chapterlist in getNovelChapterList(novelurl[0]):
            # print(chapterlist)
            contentpage = '%s%s.%s' %(novelurl[0],chapterlist[0],'html')

            for content in getNovelContent(contentpage):
                mysql.addChapter(chapterlist[1],content)
                print("正在存储------>{}".format(chapterlist[1]))


