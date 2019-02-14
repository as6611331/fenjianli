import requests, time, os, random,re,csv,xlwt,json,pymysql
from docx import Document
from win32com import client as wc
from bs4 import BeautifulSoup
from selenium import webdriver

class downloader(object):
    def __init__(self):

        # 符合html条件对文件位置
        self.url_all=[]
        self.cookie = ''
        self.data_D_max = 100
        self.data_D_min = 0
        self.data_U_max = 440
        self.condition={}
        self.account=''


        # 纷简历1
        self.url_fenjianli_1 =[]
        self.url_fenjianli_1_title = ('更新时间','姓名','手机号码','电子邮件','工作年限','职业状态','国籍','性别','年龄','教育程度','婚姻状况','所在地','户籍','所在行业','公司名称','所任职位','目前薪资','期望地点','期望薪资','工作经历','文件位置')
        self.url_fenjianli_1_datas = []

        # 纷简历2
        self.url_fenjianli_2 =[]
        self.url_fenjianli_2_title = ('更新时间', '姓名','性别','手机号','年龄','电子邮箱','学历','婚姻状况','工作年限','现居住地','户籍','期望行业','期望职业','期望地点','期望薪资','工作性质','目前状态','文件位置')
        self.url_fenjianli_2_datas = []

        # 纷简历3
        self.url_fenjianli_3 = []
        self.url_fenjianli_3_title=['简历更新时间','简历编号','姓名','性别','手机号码','年龄','电子邮箱','学历','婚姻状况','工作年限','现居住地','户籍','期望行业','期望职业','期望地点','期望薪资','工作性质','目前状态','自我评价','工作经历','项目经历','教育经历','语言能力','培训经历','专业技能','证书','简历来源','创建时间']
        self.url_fenjianli_3_datas=[]

        # 纷简历4
        self.url_fenjianli_4 = []
        self.url_fenjianli_4_title=['更新时间','简历编号','姓名','性别','手机号码','年龄','电子邮件','教育程度','工作年限','婚姻状况','职业状态','国籍','所在地','户籍','期望行业','期望职位','期望地点','期望薪资','工作经历','项目经历','教育经历','培训经历','专业技能','语言能力','自我评价','所获证书','简历来源','创建时间']
        self.url_fenjianli_4_datas=[]

        self.conversion_situation={'正确简历':0,'错误简历':0,'其他类型':0}
        self.upload_situation={'上传成功':0,'已存在相同简历':0,'上传失败':0}
        self.download_situation = {'下载成功': 0,'下载失败': 0}

    # 获得cookie
    def get_cookies(self):
        login = 'http://www.fenjianli.com/login'
        diver = webdriver.Chrome()
        diver.get(login)
        start_time = time.time()
        while True:
            # #超过120秒就结束进程
            # if time.time() - start_time > 120:
            #     break
            time.sleep(1)
            try:
                self.cookie = diver.get_cookies()[1]['value']
                # print(diver.get_cookies())
                break
            except:
                pass
        diver.quit()

    '''--------------------上传程序--------------------'''

    #上传文件
    def post_files(self,path):

        #给个随机文件名
        name = str(random.randint(10000000, 100000000))+os.path.splitext(path)[-1]

        url = 'http://www.fenjianli.com/share/upload'

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Content-Length': '12097',
            # 'Content-Type': 'multipart/form-data',
            'Host': 'www.fenjianli.com',
            'Origin': 'http://www.fenjianli.com',
            'Referer': 'http://www.fenjianli.com/share',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        cookies = {'fid': self.cookie}

        # files = {'file': (name,open(path, 'rb'))}
        # r = requests.post(url, files=files, cookies=cookies, headers=headers)
        files = {'file': (name, open(path, 'rb'), 'application/msword', {'Expires': '0'})}
        r = requests.post(url, files=files, cookies=cookies)
        r=str(json.loads(r.text))
        # print(r)
        if '上传成功' in r:
            msg = '上传成功'
            self.upload_situation['上传成功']+=1

        elif '已存在相同简历' in r:
            msg = '已存在相同简历'
            self.upload_situation['已存在相同简历'] += 1

        elif '登录状态已失效' in r:
            msg = '登录状态已失效'

        else:
            msg = '上传失败'
            self.upload_situation['上传失败'] += 1
        return msg

    #启动上传程序
    def up_data_program(self):
        cwd = os.getcwd()
        for root, dirs, files in os.walk(cwd + '\data-上传'):
            for file in files:
                self.url_all.append(os.path.join(root, file))

        if len(dl.url_all) == 0:
            print('请放入上传文件')
            time.sleep(5)

        # elif dl.cookie == "":
        #     print('------登录失败------')

        else:
            try:
                htmlf = open('cookie.txt', 'r', encoding='UTF-8')
                self.cookie = htmlf.read()
                htmlf.close()
            except:
                dl.get_cookies()
                htmlf = open('cookie.txt', 'w', encoding='UTF-8')
                htmlf.write(self.cookie)
                htmlf.close()

            # print(dl.cookie)
            while True:
                try:
                    for i in range(len(dl.url_all)):
                        time.sleep(random.randint(10, 20) / 10)
                        data_report = dl.post_files(dl.url_all[i])
                        while data_report=='登录状态已失效':
                            print('----------《登录失效请重新登录账户》----------')
                            dl.get_cookies()
                            htmlf = open('cookie.txt', 'w', encoding='UTF-8')
                            htmlf.write(self.cookie)
                            htmlf.close()
                            data_report = dl.post_files(dl.url_all[i])

                        print(data_report+ "："+ dl.url_all[i])
                except Exception as e:
                    print(e)
                finally:
                    print()
                    print("上传成功：%d | 已存在相同简历：%d | 上传失败：%d"  % (dl.upload_situation['上传成功'], dl.upload_situation['已存在相同简历'],dl.upload_situation['上传失败']))
                    input("回车结束程序")
                    # print()
                    # print('五秒后自动结束程序')
                    # time.sleep(5)
                    break

    '''--------------------转换程序--------------------'''

    # 判断文件的类型
    def file_name(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            if 'doc_cache' not in root:
                for file in files:
                    names = os.path.splitext(file)
                    if names[1] == '.html':
                        self.url_all.append(os.path.join(root, file))

                    #旧版doc程序
                    # elif names[1] == '.doc':
                    #
                    #     # 新建文件夹
                    #     mkdir = os.path.join(root, 'doc_cache')
                    #     isExists = os.path.exists(mkdir)
                    #     if not isExists:
                    #         os.makedirs(mkdir)
                    #
                    #     # 读取文件名称和改后缀名
                    #     word_url_doc = os.path.join(root, file)
                    #     word_url_html = os.path.join(root, 'doc_cache', names[0] + '.html')
                    #     self.url_all.append(word_url_html)
                    #     # print(word_url_html)
                    #
                    #     # 判断是否已经转换成html
                    #     isExists2 = os.path.exists(word_url_html)
                    #     if not isExists2:
                    #         print('转换：' + word_url_doc)
                    #         downloader.wordsToHtml(self, word_url_doc, word_url_html)

                    elif names[1] == '.doc':
                        self.url_all.append(os.path.join(root, file))

                    else:
                        self.conversion_situation['其他类型'] += 1
                        print('其他类型：', os.path.join(root, file))

    # 判断编码
    def file_coding(self, file):
        global htmlf
        try:
            htmlf = open(file, 'r', encoding="utf-8")
            BeautifulSoup(htmlf, 'lxml')
            return file, 'utf-8'
        except:
            try:
                htmlf = open(file, 'r', encoding="gbk")
                BeautifulSoup(htmlf, 'lxml')
                return file, 'gbk'
            except:
                try:
                    htmlf = open(file, 'r', encoding="UTF-16")
                    BeautifulSoup(htmlf, 'lxml')
                    return file, 'utf-16'
                except:
                    return file, 'utf-8'
        finally:
            htmlf.close()

    # 转换doc/docx/mht格式成html
    def wordsToHtml(self,word_url_old, word_url_new):
        # global doc
        # global word

        # kwps.Application WPS接口转换
        # wps.Application WPS接口转换
        # word.Application office接口转换
        try:
            word = wc.Dispatch('word.Application')
            doc = word.Documents.Open(word_url_old)
            doc.SaveAs(word_url_new, 8)
            doc.Close()
            word.Quit()

        except:
            print('错误转换：', word_url_old)

    # csv模块导出csv
    def csv_to_csv(self, name,title, datas):
        headers = list(title)
        with open(name + '.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, headers, delimiter=',', quotechar='"')
            writer.writeheader()
            # print(datas)
            for row in datas:
                writer.writerow(row)
        # # 清除缓存
        # url.clear()
        # datas.clear()

    # xlwt模块导出xls
    def xlwt_to_xls(self,name,title,datas):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(name)

        for i in range(len(title)):
            worksheet.write(0, i, label=title[i])

        for n in range(1,len(datas)+1):
            for i in range(len(title)):
                worksheet.write(n,i,str(list(datas[n-1].values())[i]))

        workbook.save(name+'.xls')

    # 纷简历-1清洗程序
    def get_url_fenjianli_1(self, url):
        global htmlf
        try:
            htmlf = open(url[0], 'r', encoding=url[1])
            soup = BeautifulSoup(htmlf, 'lxml')
            dicts = dict.fromkeys(self.url_fenjianli_1_title, '')

            boxs = soup.find(class_='menu-box')
            update = boxs.findAll(class_='update')[0].text.replace('更新时间：', '')
            # print(box)
            dicts['更新时间'] = update

            box = boxs.select("dd")
            # print(box)
            for i in box:
                # print(i)
                s = i.select("label")[0].text
                i = i.select("div")[0].text
                # print(s)
                if '姓名：' == s:

                    dicts['姓名'] = i
                elif '手机号码：' == s:
                    # i=i.select("div")[0].text
                    dicts['手机号码'] = i
                elif '性别：' == s:
                    # i=i.select("div")[0].text
                    dicts['性别'] = i
                elif '年龄：' == s:
                    # i=i.select("div")[0].text
                    dicts['年龄'] = i
                elif '电子邮件：' == s:
                    # i=i.select("div")[0].text
                    dicts['电子邮件'] = i
                elif '教育程度：' == s:
                    # i=i.select("div")[0].text
                    dicts['教育程度'] = i
                elif '工作年限：' == s:
                    # i=i.select("div")[0].text
                    dicts['工作年限'] = i
                elif '婚姻状况：' == s:
                    # i=i.select("div")[0].text
                    dicts['婚姻状况'] = i
                elif '职业状态：' == s:
                    # i=i.select("div")[0].text
                    dicts['职业状态'] = i
                elif ' 所在地：' == s:
                    # i=i.select("div")[0].text
                    dicts['所在地'] = i
                elif '国籍：' == s:
                    # i=i.select("div")[0].text
                    dicts['国籍'] = i
                elif '户籍：' == s:
                    # i=i.select("div")[0].text
                    dicts['户籍'] = i
                elif '所在行业：' == s:
                    # i=i.select("div")[0].text
                    dicts['所在行业'] = i
                elif '公司名称：' == s:
                    # i=i.select("div")[0].text
                    dicts['公司名称'] = i
                elif '所任职位：' == s:
                    # i=i.select("div")[0].text
                    dicts['所任职位'] = i.replace('\n', '')
                elif '目前薪资：' == s:
                    # i=i.select("div")[0].text
                    dicts['目前薪资'] = i
                elif '期望地点：' == s:
                    # i=i.select("div")[0].text
                    dicts['期望地点'] = i
                elif '期望薪资：' == s:
                    # i=i.select("div")[0].text
                    dicts['期望薪资'] = i.replace('\n', '').replace(' ', '')

            boxt = boxs.findAll(class_='exp')[0]
            boxz = boxt.select('tr th[class="times"]')
            boxd = boxt.select('td table[class="table table-noborder table-form"]')
            d = 0
            kk = []
            for i in boxz:
                tt = []
                # print('--------------------------------+',d)
                tt.append(i.text)
                # print(i.text)
                # 双
                dd = boxd[d].select('th')
                tt.append(str('公司：' + dd[0].text.replace(' ', '').replace('\n', '')))
                # print(dd[0].text.replace(' ', ''))

                aa = boxd[d].select('span')
                for s in aa:
                    tt.append(s.text.replace('\n', ''))
                    # print(s.text)
                # 单
                ddd = boxd[d + 1].select('span')
                tt.append(str('职位：' + ddd[0].text))
                # print(ddd[0].text)
                d = d + 2
                # print(tt)
                kk.append(tt)
                # print('--------------------------------=')
            dicts['工作经历'] = str(kk).replace('], [', '\n').replace("', '", '|').replace("[[' ", '').replace("']]",'').replace("'", '').replace(" ", '')

            dicts['文件位置'] = url[0]
            # print(dicts)
            self.url_fenjianli_1_datas.append(dicts)
        except:
            self.conversion_situation['错误简历'] += 1
            # self.false +=1
            print('错误简历-纷简历-1：',url[0])
        else:
            self.conversion_situation['正确简历'] += 1
            # self.true +=1
            print('正确简历-纷简历-1：', url[0])
        finally:
            htmlf.close()

    # 纷简历-2清洗程序
    def get_url_fenjianli_2(self, url):
        global htmlf
        try:
            htmlf = open(url[0], 'r', encoding=url[1])
            soup = BeautifulSoup(htmlf, 'html.parser')
            dicts = dict.fromkeys(self.url_fenjianli_2_title, '')

            WordSection1 = soup.find(class_="WordSection1")
            # print(WordSection1)
            MsoNormal = WordSection1.select('p[class="MsoNormal"]')[0]
            MsoNormal = MsoNormal.text.replace('简历更新时间:', '')
            # print(MsoNormal)
            dicts['更新时间'] = MsoNormal

            ResumeContentStyle = soup.select('table[class="ResumeContentStyle"]')
            mso_yfti_irow = ResumeContentStyle[0].findAll(style=re.compile("mso-yfti-irow:"))
            for irow in mso_yfti_irow[1:]:
                # print(irow)
                irow = irow.text.replace('： \n\n\n', '：').replace('\xa0', '').split('\n')
                irow = [i for i in irow if i != '']
                # print(irow)
                for i in irow:
                    if '姓名：' in i:
                        dicts['姓名'] = i.replace('姓名：', '')
                    elif '性别：' in i:
                        dicts['性别'] = i.replace('性别：', '')
                    elif '手机号：' in i:
                        dicts['手机号'] = i.replace('手机号：', '')
                    elif '年龄：' in i:
                        dicts['年龄'] = i.replace('年龄：', '')
                    elif '电子邮箱：' in i:
                        dicts['电子邮箱'] = i.replace('电子邮箱：', '')
                    elif '学历：' in i:
                        dicts['学历'] = i.replace('学历：', '')
                    elif '婚姻状况：' in i:
                        dicts['婚姻状况'] = i.replace('婚姻状况：', '')
                    elif '工作年限：' in i:
                        dicts['工作年限'] = i.replace('工作年限：', '')
                    elif '现居住地：' in i:
                        dicts['现居住地'] = i.replace('现居住地：', '')
                    elif '户籍：' in i:
                        dicts['户籍'] = i.replace('户籍：', '')
            mso_yfti_irow = ResumeContentStyle[1].findAll(style=re.compile("mso-yfti-irow:"))
            # print(mso_yfti_irow)
            for irow in mso_yfti_irow[1:]:
                # print(irow)
                irow = irow.text.replace('： \n\n\n', '：').replace('\xa0', '').split('\n')
                irow = [i for i in irow if i != '']
                # print(irow)
                for i in irow:
                    if '期望行业：' in i:
                        dicts['期望行业'] = i.replace('期望行业：', '')
                    elif '期望职业：' in i:
                        dicts['期望职业'] = i.replace('期望职业：', '')
                    elif '期望地点：' in i:
                        dicts['期望地点'] = i.replace('期望地点：', '')
                    elif '期望薪资：' in i:
                        dicts['期望薪资'] = i.replace('期望薪资：', '')
                    elif '工作性质：' in i:
                        dicts['工作性质'] = i.replace('工作性质：', '')
                    elif '目前状态：' in i:
                        dicts['目前状态'] = i.replace('目前状态：', '')

            dicts['文件位置'] = url[0]
            # print(dicts)
            self.url_fenjianli_2_datas.append(dicts)
        except:
            print('错误简历-纷简历-2：',url[0])
        else:
            print('正确简历-纷简历-2：', url[0])
        finally:
            htmlf.close()

    # 纷简历-3清洗程序
    def get_url_fenjianli_3(self,url):
        try:
            # print(url)
            dicts = dict.fromkeys(self.url_fenjianli_3_title, "")

            doc_tables=Document(url).tables

            dicts['简历更新时间']=doc_tables[0].cell(0, 0).text.replace('简历更新时间:', '')
            dicts['简历编号']=doc_tables[0].cell(0, 1).text.replace('简历编号：', '')

            dicts['姓名']=doc_tables[2].cell(1, 1).text
            dicts['性别']=doc_tables[2].cell(1, 3).text
            dicts['手机号码']=doc_tables[2].cell(2, 1).text
            dicts['年龄']=doc_tables[2].cell(2, 3).text
            dicts['电子邮箱']=doc_tables[2].cell(3, 1).text
            dicts['学历']=doc_tables[2].cell(3, 3).text
            dicts['婚姻状况'] = doc_tables[2].cell(4, 1).text
            dicts['工作年限'] = doc_tables[2].cell(4, 3).text
            dicts['现居住地'] = doc_tables[2].cell(5, 1).text
            dicts['户籍'] = doc_tables[2].cell(5, 3).text

            dicts['自我评价'] = "".join([paragraph.text for paragraph in Document(url).paragraphs if paragraph.text != ''])

            professional_skills_lists = []
            for i in range(len(doc_tables)):
                doc_tables_text=doc_tables[i].cell(0, 0).text
                # print(doc_tables_text)

                if '职业发展意向' in doc_tables_text:
                    # print("职业发展意向：")
                    doc_tables_data=doc_tables[i + 1]
                    for rows in range(len(doc_tables_data.rows)):
                        if '期望行业'in doc_tables_data.cell(rows, 0).text:
                            dicts['期望行业'] = str(doc_tables_data.cell(rows, 1).text.split(';')).replace("'",'"')
                        elif '期望职业'in doc_tables_data.cell(rows, 0).text:
                            dicts['期望职业'] = str(doc_tables_data.cell(rows, 1).text.split(';')).replace("'",'"')
                        elif '期望地点'in doc_tables_data.cell(rows, 0).text:
                            dicts['期望地点'] = str(doc_tables_data.cell(rows, 1).text.split('-')).replace("'",'"')
                        elif '期望薪资'in doc_tables_data.cell(rows, 0).text:
                            dicts['期望薪资'] = doc_tables_data.cell(rows, 1).text
                        elif '工作性质'in doc_tables_data.cell(rows, 0).text:
                            dicts['工作性质'] = doc_tables_data.cell(rows, 1).text
                        elif '目前状态'in doc_tables_data.cell(rows, 0).text:
                            dicts['目前状态'] = doc_tables_data.cell(rows, 1).text

                elif '工作经历' in doc_tables_text:
                    # print("工作经历：")
                    doc_tables_data=doc_tables[i + 1]
                    lists = []
                    for rowss in range(len(doc_tables_data.rows)):
                        if len(doc_tables_data.cell(rowss, 0).text) > 6:
                            tables=['任职时间','公司','行业','职位','工作描述']
                            tables_dicts = dict.fromkeys(tables, '')
                            tables_dicts['任职时间']=doc_tables_data.cell(rowss, 0).text
                            tables_dicts['公司'] = doc_tables_data.cell(rowss, 1).text.replace(re.search(re.compile(r'\((\d*(年|个月))+\)'), doc_tables_data.cell(rowss, 1).text.replace('()','(0年)')).group(), '')
                            for rows in range(len(doc_tables_data.rows)):
                                if '行业' in doc_tables_data.cell(rows, 0).text:
                                    tables_dicts['行业'] = doc_tables_data.cell(rows, 1).text
                                elif '职位' in doc_tables_data.cell(rows, 0).text:
                                    tables_dicts['职位'] = doc_tables_data.cell(rows, 1).text
                                elif '工作描述' in doc_tables_data.cell(rows, 0).text:
                                    tables_dicts['工作描述'] = doc_tables_data.cell(rows, 1).text
                            lists.append(tables_dicts)
                            # print(tables_dicts)
                    dicts['工作经历']=str(json.dumps(lists,ensure_ascii=False))

                elif '项目经历' in doc_tables_text:
                    # print("项目经历：")
                    doc_tables_data=doc_tables[i + 1]
                    lists = []
                    for rowss in range(len(doc_tables_data.rows)):
                        if len(doc_tables_data.cell(rowss, 0).text) > 6:
                            tables=['项目时间','项目名称','项目职责','项目描述']
                            tables_dicts = dict.fromkeys(tables, '')
                            tables_dicts['项目时间'] = doc_tables_data.cell(rowss, 0).text
                            tables_dicts['项目名称'] = doc_tables_data.cell(rowss, 1).text.replace(re.search(re.compile(r'\((\d*(年|个月))+\)'), doc_tables_data.cell(rowss, 1).text.replace('()','(0年)')).group(), '').replace(' ','')
                            for rows in range(len(doc_tables_data.rows)):
                                if "项目职责" in doc_tables_data.cell(rows, 0).text:
                                    tables_dicts['项目职责'] = doc_tables_data.cell(rows, 1).text
                                if "项目描述"in doc_tables_data.cell(rows, 0).text:
                                    tables_dicts['项目描述'] = doc_tables_data.cell(rows, 1).text
                            lists.append(tables_dicts)
                            # print(tables_dicts)
                    dicts['项目经历']=str(json.dumps(lists,ensure_ascii=False))

                elif '教育经历' in doc_tables_text:
                    # print("教育经历：")
                    doc_tables_data=doc_tables[i + 1]
                    lists = []
                    lens = []
                    for row in doc_tables_data.rows:
                        for cell in row.cells:
                            lens.append(cell.text)

                    for i in range(len(lens)):
                        try:
                            if lens[i][8] =='-':
                                tables = ['就读时间', '学校', '学历', '专业']
                                tables_dicts = dict.fromkeys(tables, '')
                                tables_dicts['就读时间'] = lens[i]
                                r=i+1
                                for n in range(3):
                                    try:
                                        if lens[r] == '学校：':
                                            tables_dicts['学校'] = lens[r + 1]
                                        elif lens[r] == '学历：':
                                            tables_dicts['学历'] = lens[r + 1]
                                        elif lens[r] == '专业：':
                                            tables_dicts['专业'] = lens[r + 1]
                                    except:
                                        pass
                                    finally:
                                        r=r+2
                                # print(tables_dicts)
                                lists.append(tables_dicts)
                        except:
                            pass
                    # print(lists)
                    dicts['教育经历'] = str(json.dumps(lists,ensure_ascii=False))

                elif '语言能力' in doc_tables_text:
                    # print("语言能力：")
                    doc_tables_data=doc_tables[i + 1]
                    lists = []
                    for rows in range(len(doc_tables_data.rows))[1:]:
                        tables=['语言','读写情况','听说情况']
                        tables_dicts = dict.fromkeys(tables, '')
                        split = doc_tables_data.cell(rows, 0).text.split(':')
                        tables_dicts['语言'] = split[0]
                        tables_dicts['读写情况'] = split[1]
                        tables_dicts['听说情况'] = split[2]
                        lists.append(tables_dicts)
                        # print(tables_dicts)
                    dicts['语言能力'] = str(json.dumps(lists,ensure_ascii=False))

                elif '培训经历' in doc_tables_text:
                    # print("培训经历：")
                    doc_tables_data=doc_tables[i + 1]
                    for rows in range(len(doc_tables_data.rows)):
                        try:
                            if doc_tables_data.cell(rows, -1).text[11] == '-':
                                tables=['培训时间','培训机构','培训课程']
                                tables_dicts = dict.fromkeys(tables, '')
                                tables_dicts['培训时间'] = doc_tables_data.cell(rows, -1).text
                                tables_dicts['培训机构'] = doc_tables_data.cell(rows, 0).text
                                tables_dicts['培训课程'] = doc_tables_data.cell(rows, 1).text
                                professional_skills_lists.append(tables_dicts)
                                # print(tables_dicts)
                        except:
                            pass

                elif '专业技能' in doc_tables_text:
                    # print("专业技能：")
                    doc_tables_data=doc_tables[i + 1]
                    lists = []
                    for rows in range(len(doc_tables_data.rows))[1:]:
                        lists.append(doc_tables_data.cell(rows, 0).text)
                    # print(lists)
                    dicts['专业技能'] = str(lists).replace("'",'"')

                elif '证书' in doc_tables_text:
                    # print("证书：")
                    doc_tables_data=doc_tables[i + 1]
                    lists = []
                    for rows in range(len(doc_tables_data.rows))[1:]:
                        tables=['获得时间','证书名称']
                        tables_dicts = dict.fromkeys(tables, '')
                        tables_dicts['获得时间'] = doc_tables_data.cell(rows, 0).text
                        tables_dicts['证书名称'] = doc_tables_data.cell(rows, 1).text
                        lists.append(tables_dicts)
                        # print(tables_dicts)
                    dicts['证书'] = str(json.dumps(lists,ensure_ascii=False))

            if len(professional_skills_lists)>0:
                dicts['培训经历'] = str(json.dumps(professional_skills_lists,ensure_ascii=False))

            dicts['简历来源'] ='纷简历doc'
            dicts['创建时间'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

            # print(dicts)
            self.url_fenjianli_3_datas.append(dicts)
        except:
            self.conversion_situation['错误简历'] += 1
            # self.false += 1
            print('错误简历-纷简历-3：',url)
        else:
            self.conversion_situation['正确简历'] += 1

            # self.true += 1
            print('正确简历-纷简历-3：', url)
            dl.up_mysql(dicts, 'fenjianli_doc')
            # dicts['简历编号']

    # 纷简历-4清洗程序
    def get_url_fenjianli_4(self, url):
        try:
            htmlf = open(url, 'r', encoding='UTF-8')
            soup = BeautifulSoup(htmlf, 'lxml')
            dicts = dict.fromkeys(dl.url_fenjianli_4_title, '')
            try:
                dicts['简历编号'] = soup.find('input').get('value')
            except:
                pass
            soup = soup.find(class_='menu-box')

            pointer = soup.findAll(class_='update')[0].text.replace('更新时间：', '')
            dicts['更新时间'] = pointer

            pointer = soup.find(class_='cont relative')
            label = pointer.findAll('label')
            col = pointer.findAll(class_='col')
            for i in range(len(label)):
                if '姓名' in label[i].text:
                    dicts['姓名'] = col[i].text
                elif '性别' in label[i].text:
                    dicts['性别'] = col[i].text
                elif '手机号码' in label[i].text:
                    dicts['手机号码'] = col[i].text
                elif '年龄' in label[i].text:
                    dicts['年龄'] = col[i].text
                elif '电子邮件' in label[i].text:
                    dicts['电子邮件'] = col[i].text
                elif '教育程度' in label[i].text:
                    dicts['教育程度'] = col[i].text
                elif '工作年限' in label[i].text:
                    dicts['工作年限'] = col[i].text
                elif '婚姻状况' in label[i].text:
                    dicts['婚姻状况'] = col[i].text
                elif '职业状态' in label[i].text:
                    dicts['职业状态'] = col[i].text
                elif '国籍' in label[i].text:
                    dicts['国籍'] = col[i].text
                elif '所在地' in label[i].text:
                    dicts['所在地'] = col[i].text
                elif '户籍' in label[i].text:
                    dicts['户籍'] = col[i].text
                elif '期望行业' in label[i].text:
                    dicts['期望行业'] = str(col[i].text.split(';')).replace("'",'"')
                elif '期望职位' in label[i].text:
                    dicts['期望职位'] = str(col[i].text.replace('\n', '').split(';')).replace("'",'"')
                elif '期望地点' in label[i].text:
                    dicts['期望地点'] = str(col[i].text.split('-')).replace("'",'"')
                elif '期望薪资' in label[i].text:
                    dicts['期望薪资'] = col[i].text.replace(' ', '').replace('\n', '')

            float = soup.select('section[class="board"] span[class="float-left"]')
            cout=0
            for n in float:
                #0
                if '工作经历' in n.text:
                    pointer = soup.find(id='workexp_anchor').select('div[class="exp"] > table > tbody > tr')
                    tables = ['任职时间', '公司', '公司性质', '公司规模', '公司行业', '职位', '所在部门', '职责']
                    lists = []
                    for i in pointer:
                        tables_dicts = dict.fromkeys(tables, '')
                        tables_dicts['任职时间'] = i.find(class_='times').text

                        tables_dicts['公司'] = i.findAll(class_='table table-noborder table-form')[0].find(
                            class_="section-content").text.replace(' ', '').replace('\n', '')
                        try:
                            get_dey = re.search(re.compile(r'（(\d*(年|个月))+）'), tables_dicts['公司']).group()
                        except:
                            get_dey = ''
                        tables_dicts['公司'] = tables_dicts['公司'].replace(get_dey, '')

                        comp_info = i.findAll(class_='table table-noborder table-form')[0].findAll(class_='comp-info')
                        for td in comp_info:
                            if '公司性质：' in td.text:
                                tables_dicts['公司性质'] = td.text.replace('\n', '').replace(' ', '').replace('公司性质：', '')
                            elif '公司规模：' in td.text:
                                tables_dicts['公司规模'] = td.text.replace('\n', '').replace(' ', '').replace('公司规模：', '')
                            elif '公司行业：' in td.text:
                                tables_dicts['公司行业'] = td.text.replace('\n', '').replace(' ', '').replace('公司行业：', '')

                        tables_dicts['职位'] = i.findAll(class_='table table-noborder table-form')[1].find(
                            class_="section-content").text.replace(' ', '').replace('\n', '')
                        comp_info = i.findAll(class_='table table-noborder table-form')[1].findAll('tr')
                        for td in comp_info:
                            if '所在部门：' in td.text:
                                tables_dicts['所在部门'] = td.text.replace('\n', '').replace(' ', '').replace('所在部门：', '')
                            elif '职责：' in td.text:
                                tables_dicts['职责'] = td.text.replace('\n', '').replace(' ', '').replace('职责：', '')

                        lists.append(tables_dicts)
                    dicts['工作经历'] = str(json.dumps(lists, ensure_ascii=False))
                #1
                elif '项目经历' in n.text:
                    # print(1)
                    tables = ['项目时间', '项目名称', '项目简介', '项目职责']
                    lists = []
                    pointer = soup.select('section[class="board"] div[class="exp"]')[1]
                    pointer=[i for i in pointer.find("tbody").children if i != '\n']
                    for i in pointer:
                        tables_dicts = dict.fromkeys(tables, '')
                        tables_dicts['项目时间']=i.find(class_='times').text
                        tables_dicts['项目名称'] =i.select('table thead tr th')[0].text
                        k=0
                        for s in i.select('table tbody tr th'):
                            if '项目简介：' in s.text:
                                tables_dicts['项目简介']=i.select('table tbody tr td')[k].text.replace('\n', '').replace(' ', '')
                                k+=1
                            elif '项目职责：'in s.text:
                                tables_dicts['项目职责'] = i.select('table tbody tr td')[k].text.replace('\n', '').replace(' ', '')
                                k += 1
                        lists.append(tables_dicts)
                        # print(tables_dicts)
                    dicts['项目经历'] = str(json.dumps(lists,ensure_ascii=False))
                    # print(pointer)
                #2
                elif '教育经历' in n.text:
                    # print(2)
                    tables = ['就读时间', '学校', '学历', '专业']
                    lists = []
                    pointer = soup.select('section[class="board"] div[class="cont"]')[cout]
                    pointer = pointer.select('tbody tr')
                    for i in pointer:
                        pointers =i.select('td')
                        # print(pointers)
                        tables_dicts = dict.fromkeys(tables, '')
                        for s in pointers:
                            if '专业：' in s.text:
                                tables_dicts['专业']=s.text.replace('专业：', '')
                            elif '学历：' in s.text:
                                tables_dicts['学历'] = s.text.replace('学历：', '')
                            else:
                                tables_dicts['就读时间'] =re.search(re.compile(r'\d+\/+\d+( - )+(\d+\/+\d*|至今)'), s.text).group()
                                tables_dicts['学校'] =s.text.replace(tables_dicts['就读时间'],'')
                        lists.append(tables_dicts)
                        # print(tables_dicts)
                    dicts['教育经历'] = str(json.dumps(lists,ensure_ascii=False))
                    # print(pointer)
                    cout+=1
                #3
                elif '培训经历' in n.text:
                    # print(3)
                    tables = ['培训时间', '培训机构', '培训课程']
                    lists = []
                    pointer = soup.select('section[class="board"] div[class="cont"]')[cout]
                    pointer = pointer.select('tbody tr')
                    for i in pointer:
                        tables_dicts = dict.fromkeys(tables, '')
                        pointers=i.select('td')
                        lens=len(pointers)
                        if lens==1:
                            tables_dicts['培训时间'] = pointers[0].text
                        else:
                            tables_dicts['培训时间'] = pointers[0].text
                            tables_dicts['培训机构'] = pointers[1].text
                            tables_dicts['培训课程'] = pointers[2].text
                        lists.append(tables_dicts)
                        # print(tables_dicts)

                    dicts['培训经历'] = str(json.dumps(lists,ensure_ascii=False))
                    # print(lists)
                    # print(pointer)
                    cout+=1
                #4
                elif '专业技能' in n.text:
                    # print(4)
                    pointer = soup.select('section[class="board"] div[class="cont"]')[cout]
                    dicts['专业技能'] = pointer.text.replace(' ', '').split('\n')
                    dicts['专业技能'] = str([i for i in dicts['专业技能'] if i != '']).replace("'",'"')
                    # print(dicts['专业技能'] )
                    # print(pointer)
                    cout+=1
                #5
                elif '语言能力' in n.text:
                    # print(5)
                    tables = ['语言', '读写情况', '听说情况']
                    lists = []
                    pointer = soup.select('section[class="board"] div[class="cont"]')[cout]
                    pointer=pointer.findAll(class_="language")
                    for i in pointer:
                        tables_dicts = dict.fromkeys(tables, '')
                        i=i.text.replace(' ', '').replace('：', '/').replace('\n', '').split('/')
                        for n in i:
                            if '读写能力'in n:
                                tables_dicts['读写情况'] = n.replace('读写能力', '')
                            elif'听说能力'in n:
                                tables_dicts['听说情况'] = n.replace('听说能力', '')
                            else:
                                tables_dicts['语言']=n
                        lists.append(tables_dicts)
                        # print(tables_dicts)
                    dicts['语言能力'] = str(json.dumps(lists,ensure_ascii=False))
                    # print(pointer)
                    cout+=1
                #6
                elif '自我评价' in n.text:
                    # print(6)
                    pointer = soup.select('section[class="board"] div[class="cont"]')[cout]
                    dicts['自我评价'] = pointer.text.replace('\n', '')
                    # print(dicts['自我评价'])
                    # print(pointer)
                    cout+=1
                #7
                elif '所获证书' in n.text:
                    # print(7)
                    tables = ['获得时间', '证书名称']
                    lists = []
                    pointer = soup.select('section[class="board"] div[class="cont"]')[cout]
                    pointer=pointer.findAll('p')
                    for i in pointer:
                        tables_dicts = dict.fromkeys(tables, '')
                        i=i.text.replace('\n', '').replace(' ', '').split('\xa0')
                        i= [n for n in i if n != '']
                        if len(i)==1:
                            tables_dicts['获得时间'] = i[0]
                        else:
                            tables_dicts['获得时间'] = i[0]
                            tables_dicts['证书名称'] = i[1]
                        lists.append(tables_dicts)
                        # print(tables_dicts)
                    dicts['所获证书'] = str(json.dumps(lists,ensure_ascii=False))
                    # print(pointer)
                    cout += 1

            dicts['简历来源'] ='纷简历html'
            dicts['创建时间'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

            # print(dicts)
            self.url_fenjianli_4_datas.append(dicts)
        except:
            self.conversion_situation['错误简历'] += 1
            # self.false += 1
            print('错误简历-纷简历-4：',url)
        else:
            self.conversion_situation['正确简历'] += 1
            # self.true += 1
            print('正确简历-纷简历-4：', url)
            dl.up_mysql(dicts, 'fenjianli_html')

    # 简易转换分类控制
    def get_task(self, name, get_url, url, title, datas):
        for i in url:
            get_url(i)

        # 利用csv模块导出csv
        # downloader.csv_to_csv(self, name, title, datas)

        # 利用xlwt导出xls
        downloader.xlwt_to_xls(self, name, title, datas)

    #上传到数据库里
    def up_mysql(self,data,table_name):
        data=list(data.values())
        resume_id = data[1]
        phone_number = data[4]

        # table_name = 'fenjianli_html'  # 数据表名称
        # table_name = 'fenjianli_doc'  # 数据表名称

        if phone_number != '':
            db = pymysql.connect(host="192.168.0.41", user="root", password="", db="it-data", port=3306,charset='utf8mb4')  # 连接数据库
            cur = db.cursor(cursor=pymysql.cursors.DictCursor)  # 获取一个列表游标
            # cur=db.cursor() # 获取一个游标

            #ret1
            cur.execute("select `手机号码` from {0} where `手机号码`='{1}'".format(table_name, phone_number))
            ret1 = cur.fetchone()

            if phone_number in str(ret1):
                sql="DELETE FROM {0} where `手机号码`='{1}'".format(table_name,phone_number) # 删除数据
                cur.execute(sql)
                format = str(',%s' * len(data))[1:]
                cur.execute('insert into {0} values({1})'.format(table_name, format), data)  # 插入数据
            else:
                format = str(',%s' * len(data))[1:]
                cur.execute('insert into {0} values({1})'.format(table_name, format), data)  # 插入数据

            # ret2
            cur.execute("select `resume_id` from {0} where `resume_id`='{1}'".format('fenjianli_id', resume_id))
            ret2 = cur.fetchone()

            if ret2 == None:
                downdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                upload = [resume_id, downdate, '转换', '{"keywords": "转换"}']
                format = str(',%s' * len(upload))[1:]
                cur.execute('insert into {0} values({1})'.format('fenjianli_id', format), upload)  # 插入数据


            # 提交
            db.commit()
            # 关闭指针对象
            cur.close()
            # 关闭连接对象
            db.close()

    # 启动转换程序
    def turn_data_program(self):

        cwd = os.getcwd()
        # 启动文件地址提取和转换程序
        dl.file_name(cwd + '\data-转换')
        if len(dl.url_all) == 0:
            print('请放入转换文件')
            time.sleep(5)
        else:
            # 启动判断简历类型程序
            for i in dl.url_all:
                names = os.path.splitext(i)

                # if names[1] == '.html':
                #     dl.url_fenjianli_1.append(dl.file_coding(i))
                # elif 'doc_cache' in i:
                #     dl.url_fenjianli_2.append(dl.file_coding(i))

                if names[1] == '.html':
                    dl.url_fenjianli_4.append(i)

                elif names[1] == '.doc':
                    dl.url_fenjianli_3.append(i)

            # if len(dl.url_fenjianli_1) != 0:
            #     dl.get_task('纷简历-1', dl.get_url_fenjianli_1, dl.url_fenjianli_1, dl.url_fenjianli_1_title,dl.url_fenjianli_1_datas)

            # if len(dl.url_fenjianli_2) != 0:
            #     dl.get_task('纷简历-2',dl.get_url_fenjianli_2, dl.url_fenjianli_2, dl.url_fenjianli_2_title, dl.url_fenjianli_2_datas)

            if len(dl.url_fenjianli_3) != 0:
                dl.get_task('纷简历-3', dl.get_url_fenjianli_3, dl.url_fenjianli_3, dl.url_fenjianli_3_title,dl.url_fenjianli_3_datas)

            if len(dl.url_fenjianli_4) != 0:
                dl.get_task('纷简历-4', dl.get_url_fenjianli_4, dl.url_fenjianli_4, dl.url_fenjianli_4_title,dl.url_fenjianli_4_datas)

            print()
            print("正确数量：%d | 错误数量：%d | 其他类型：%d" % (dl.conversion_situation['正确简历'], dl.conversion_situation['错误简历'], dl.conversion_situation['其他类型']))
            input("回车结束程序")
            # print()
            # print('五秒后自动结束程序')
            # time.sleep(5)

    '''--------------------下载程序--------------------'''

    #搜索条件模块
    def search_condition(self):
        self.account=input('下载账号：')
        self.data_D_max=int(input('下载数量：'))

        #条件
        dicts = {}
        keywords = input('关键词：')
        if keywords != '':
            dicts.update({'keywords': keywords})

        city = input('城市编号：')
        if city != '':
            dicts.update({'city': int(city)})

        age = input('年龄：')
        if age != '':
            dicts.update({'age': age})

        degree = input('学历编号：')
        if degree != '':
            dicts.update({'degree': int(degree)})

        sex = input('性别：')
        if sex != '':
            dicts.update({'sex': int(sex)})

        update = input('更新日期：')
        if update != '':
            dicts.update({'update': int(update)})

        dicts.update({'hideDownloaded': 1})
        dicts.update({'page': 1})
        self.condition = dicts

    #获得简历ID
    def get_resume_id(self,page):
        url = 'http://www.fenjianli.com/search/list'
        cookies = {'fid': dl.cookie}
        headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '28',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.fenjianli.com',
            'Origin': 'http://www.fenjianli.com',
            'Referer': 'http://www.fenjianli.com/search',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        self.condition['page']=page
        payload=self.condition

        html = requests.post(url, data=payload, cookies=cookies,headers=headers).text
        for i in json.loads(html)['data']['data']:
            if dl.data_D_min < dl.data_D_max:
                dl.search_mysql(i['es_id'])
                # print(i['es_id'])
            else:
                break

    #判断ID是否存在
    def search_mysql(self,resume_id):
        table_name = 'fenjianli_id'  # 数据表名称
        downdate=time.strftime('%Y-%m-%d', time.localtime(time.time()))

        db = pymysql.connect(host="192.168.0.41", user="root", password="", db="it-data", port=3306,charset='utf8mb4')  # 连接数据库
        # cur = db.cursor(cursor=pymysql.cursors.DictCursor)  # 获取一个列表游标
        cur = db.cursor()  # 获取一个游标
        cur.execute("select resume_id from {0} where resume_id='{1}'".format(table_name, resume_id))
        select_id = cur.fetchone()
        # print(select_id)
        if select_id==None:
            # 下载联系方式状态:剩余积分不足/您已经下载过了/success

            exchange = dl.exchange(resume_id)
            if exchange != '剩余积分不足':
                print('未下载简历',resume_id)
                if self.data_D_min != 0:
                    time.sleep(random.randint(10, 50)/10)

                #下载html文件
                dl.down_data(resume_id)
                judge_result=dl.down_judge(resume_id)

                #上传数据库
                if judge_result=='成功':

                    # 下载doc文件
                    dl.download_doc(resume_id)

                    upload = [resume_id, downdate, self.account,str(json.dumps(self.condition,ensure_ascii=False))]
                    # # print(upload)
                    format = str(',%s' * len(upload))[1:]
                    cur.execute('insert into {0} values({1})'.format(table_name, format), upload)  # 插入数据
                    # dl.get_url_fenjianli_4(os.path.getsize(os.path.join('data-下载\html\\', resume_id + '.html'))) #下载并上传数据
                    self.data_D_min+=1
                    self.download_situation['下载成功'] += 1
                else:
                    print('下载失败简历', resume_id)
                    self.download_situation['下载失败'] += 1
            else:
                print('账号积分不足，请上传简历补充积分')
                self.data_D_min = self.data_D_max
        else:
            print('已下载简历',resume_id)


        # 提交
        db.commit()
        # 关闭指针对象
        cur.close()
        # 关闭连接对象
        db.close()

    #下载联系方式
    def exchange(self,resume_id):
        url = 'http://www.fenjianli.com/resume/download'
        cookies = {'fid': dl.cookie}
        headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '31',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.fenjianli.com',
            'Origin': 'http://www.fenjianli.com',
            'Referer': 'http://www.fenjianli.com/resume/resumeTemplate?resumeId=' + resume_id + '&keywords=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        payload={'resumeId':resume_id}
        html = requests.post(url, data=payload, cookies=cookies,headers=headers).text
        htmlf=json.loads(html)['msg']
        # print(htmlf)
        return htmlf

    #下载简历html数据
    def down_data(self,resume_id):
        url = 'http://www.fenjianli.com/resume/resumeTemplate'
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.fenjianli.com',
            'Referer': 'http://www.fenjianli.com/resume/detail?resumeIds='+resume_id+'&keywords=',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        cookies = {'fid': self.cookie}
        payload = {'resumeId': resume_id}
        html = requests.get(url, params=payload, cookies=cookies,headers=headers).text

        # 下载简历
        htmlf = open('data-下载\html\\' + resume_id + '.html', 'w', encoding='UTF-8')
        htmlf.write(html)
        htmlf.close()

    #下载简历doc数据
    def download_doc(self,resume_id):
        url = 'http://www.fenjianli.com/resume/export'
        cookies = {'fid': dl.cookie}
        headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '41',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.fenjianli.com',
            'Origin': 'http://www.fenjianli.com',
            'Referer': 'http://www.fenjianli.com/resume/resumeTemplate?resumeId=' + resume_id + '&keywords=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        payload={'resumeId':resume_id,'type':'word'}
        html = requests.post(url, data=payload, cookies=cookies,headers=headers)
        # print(html)
        with open('data-下载\doc\\' + resume_id + '.doc', 'wb') as code:
            code.write(html.content)

    #判断文件是否成功下载
    def down_judge(self,resume_id):
        size = os.path.getsize(os.path.join('data-下载\html\\', resume_id + '.html'))

        if size == 10271:
            print('----------《登录失效请重新登录账户》----------')
            dl.get_cookies()
            htmlf = open('cookie.txt', 'w', encoding='UTF-8')
            htmlf.write(dl.cookie)
            htmlf.close()
            dl.down_data(resume_id)
            # time.sleep(random.randint(100, 200) / 10)

        cycle_number = 0
        while size == 5298 and cycle_number <= 3:
            time.sleep(30)
            dl.down_data(resume_id)
            size = os.path.getsize(os.path.join('data-下载\html\\', resume_id + '.html'))
            cycle_number += 1

        if size !=5298:
            return '成功'
        else:
            return '失败'

    #启动下载程序
    def down_data_program(self):
        try:
            htmlf = open('cookie.txt', 'r', encoding='UTF-8')
            dl.cookie = htmlf.read()
            htmlf.close()
        except:
            dl.get_cookies()
            htmlf = open('cookie.txt', 'w', encoding='UTF-8')
            htmlf.write(dl.cookie)
            htmlf.close()

        # 确认条件
        while True:
            dl.search_condition()
            confirm = input('是否确定条件（Y/N）')
            if confirm == 'Y' or confirm == 'y':
                break
            print()

        #获得每页ID
        for i in range(1,135):
            # print(i)
            if self.data_D_min <dl.data_D_max:
                try:
                    dl.get_resume_id(i)
                    time.sleep(random.randint(10, 30) /10)
                except:
                    print('----------《登录失效请重新登录账户》----------')
                    dl.get_cookies()
                    htmlf = open('cookie.txt', 'w', encoding='UTF-8')
                    htmlf.write(dl.cookie)
                    htmlf.close()
                    dl.get_resume_id(i)
                    time.sleep(random.randint(10, 30)/10)
            else:
                break

        #下载结果报告
        print("下载成功：%d | 下载失败：%d" % (dl.download_situation['下载成功'], dl.download_situation['下载失败']))
        input("回车结束程序")

    '''--------------------测试程序--------------------'''

    #筛选获得ID_下载页
    def get_ID2(self,page):
        url='http://www.fenjianli.com/resume/lpDownLoadResumeList'
        htmlf = open('cookie.txt', 'r', encoding='UTF-8')
        self.cookie = htmlf.read()
        htmlf.close()
        # url = 'http://www.fenjianli.com/search/list'
        cookies = {'fid': self.cookie}
        payload = {
            'page': page,
            'name': '',
            'job': '',
            'company': '',
            'order': 'desc'
        }

        htmlf = requests.get(url, params=payload, cookies=cookies).text
        soup = BeautifulSoup(htmlf, 'lxml')
        soup=soup.select('div[class="max-width resume-box"] div[class="resume-list"]')
        for i in soup:
            # print(i.get('data-id'))

            if dl.data_D_min<dl.data_D_max:
                dl.search_mysql_id(i.get('data-id'))
            else:
                break

            htmlf = open('urlIDs.txt', 'a', encoding='UTF-8')
            htmlf.write(i.get('data-id') + '\n')
            htmlf.close()

    def search_mysql_id(self,resume_id):
        table_name = 'fenjianli_html'  # 数据表名称

        db = pymysql.connect(host="192.168.0.41", user="root", password="", db="it-data", port=3306,charset='utf8mb4')  # 连接数据库
        # cur = db.cursor(cursor=pymysql.cursors.DictCursor)  # 获取一个列表游标
        cur = db.cursor()  # 获取一个游标
        cur.execute("select 简历编号 from {0} where 简历编号='{1}'".format(table_name, resume_id))
        select_id = cur.fetchone()

        if resume_id == None:
            print('没有',resume_id)
            dl.down_data(resume_id)

        else:
            print('有',resume_id)

        # 提交
        db.commit()
        # 关闭指针对象
        cur.close()
        # 关闭连接对象
        db.close()

if __name__=='__main__':

    dl = downloader()
    print('请选择模式：')
    print('《转换》输入"1" | 《上传》输入"2" | 《下载》输入"3"')
    select=input()
    if select=='1':
        dl.turn_data_program()
    elif select=='2':
        dl.up_data_program()
    elif select=='3':
        dl.down_data_program()
