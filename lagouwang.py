import pymongo
from pyquery import PyQuery as pq
from selenium import webdriver
import os
import pymongo
import requests
from time import sleep
from lxml import etree
from urllib import request
import sys
import io
import json
from datetime import datetime
from bs4 import BeautifulSoup
#心得：for循环里边的一定要是url再进行browser.get()

#存入mongo库
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['node_club_dev']
collection = mydb.topics


browser = webdriver.Chrome()
firsturl = 'https://www.lagou.com/gongsi/184-0-24-0'
browser.get(firsturl)
#下面是得到每个公司的列表
company_list = browser.find_elements_by_css_selector('.top a')#存在两个相同的url
secondurl_list  = []
secondurl_list1=[]
for one in company_list:
    secondurl = one.get_attribute('href')
    secondurl_list.append(secondurl)
#去重
for i in secondurl_list:
    if i not in secondurl_list1:
        secondurl_list1.append(i)
#print(secondurl_list1)no problem
for secondurl in secondurl_list1:
    browser = webdriver.Chrome()
    browser.get(secondurl)#每个公司的url

    company_content = browser.find_element_by_css_selector('.company_content').text
    #print('公司介绍')
    #print(company_content)

    third_url1 = browser.find_element_by_css_selector('.company_navs_wrap')
    third_url2 = third_url1.find_elements_by_css_selector('li')[1]
    third_url3 = third_url2.find_element_by_css_selector('a')
    third_url = third_url3.get_attribute('href')  # 得到公司页面的招聘页面url
    #print(third_url)

    #校招的招聘页面为third_url后加上?schoolJob=true，所以
    xiaozhao_url = third_url+'?schoolJob=true'

    ######################################################
    #此为非校招的招聘内容
    browser.get(third_url)
    company = browser.find_element_by_css_selector("[class='hovertips']").text  # 公司名称
    #print(company)
    #点击'产品'这个分类
    button = browser.find_elements_by_css_selector(".con_filter_li.no_select")[2]
    #print(button)
    button.click()
    #得到详细页面
    xiangxi_list = []
    job_urls = browser.find_elements_by_css_selector(".item_title_date a")
    for i in job_urls:
        xiangxiyemian_url  = i.get_attribute('href')
        xiangxi_list.append(xiangxiyemian_url)
    #print(xiangxi_list)# 招聘工作的列表

    #详细页面解析
    job_name_list = []
    job_list = []
    for k in xiangxi_list:
        detail_content = browser.get(k)
        jobname = browser.find_element_by_css_selector('.name').text
        #print(jobname)
        #job_name_list.append(jobname)
        job_describe = browser.find_element_by_css_selector('.job-detail').text
        #print(job_describe)
        #print('工作地址')
        work_address = browser.find_element_by_css_selector('.work_addr').text
        lianxifangshi = browser.find_element_by_css_selector('.hr_portrait').get_attribute('value')
        lianxiren = browser.find_element_by_css_selector('.publisher_name a').get_attribute('title')
        #print(work_address)
        job = {'jobname':jobname,
               'job_describe':job_describe,
               'job_address':work_address,
               'lianxiren': lianxiren,
               'lianxifangshi':lianxifangshi
               }
        job_list.append(job)

        #print(lianxifangshi)
    company_job = {'company_name':company,
                   'company_content':company_content,
                   'job_list':job_list}
    print(company_job)
    # topic = {
    #     'author_id': ObjectId("id"),
    #     'content': company_all
    #     'abstract': company_job,
    #     'cover_url': imgsrc,
    #     'deleted': False,
    #     'title': datet,
    #     'create_at': datetime.datetime.utcnow(),
    #     'update_at': datetime.datetime.utcnow(),
    #     'last_reply_at': datetime.datetime.utcnow(),
    #     "lock": False,
    #     "good": False,
    #     "top": False,
    #     "__v": 0}

    ###############################################
    #此为校招的招聘内容
    try:
        browser.get(xiaozhao_url)
        xiaozhao_company = browser.find_element_by_css_selector("[class='hovertips']").text  # 公司名称
        #print(xiaozhao_company)
        # 点击'产品'这个分类
        xiaozhao_button = browser.find_elements_by_css_selector(".con_filter_li.no_select")[2]
        # print(button)
        xiaozhao_button.click()
        # 得到详细页面
        xiaozhao_xiangxi_list = []
        xiaozhao_job_urls = browser.find_elements_by_css_selector(".item_title_date a")
        for i in xiaozhao_job_urls:
            xiaozhao_xiangxiyemian_url = i.get_attribute('href')
            xiaozhao_xiangxi_list.append(xiaozhao_xiangxiyemian_url)
        # print(xiangxi_list)# 招聘工作的列表

        # 详细页面解析
        xiaozhao_job_name_list = []
        xiaozhao_job_list = []
        for k in xiaozhao_xiangxi_list:
            xiaozhao_detail_content = browser.get(k)
            xiaozhao_jobname = browser.find_element_by_css_selector('.name').text
        #print(xiaozhao_jobname)
        # job_name_list.append(jobname)
        xiaozhao_job_describe = browser.find_element_by_css_selector('.job-detail').text
        #print(xiaozhao_job_describe)
        #print('工作地址')
        xiaozhao_work_address = browser.find_element_by_css_selector('.work_addr').text
        #print(xiaozhao_work_address)
        xiaozhao_lianxifangshi = browser.find_element_by_css_selector('.hr_portrait').get_attribute('value')
        xiaozhao_lianxiren =browser.find_element_by_css_selector('.publisher_name a').get_attribute('title')
        xiaozhao_job = {'xiaozhao_jobname': xiaozhao_jobname,
               'xiaozhao_job_describe': xiaozhao_job_describe,
               'xiaozhao_job_address': xiaozhao_work_address,
                'xiaozhao_lianxiren': xiaozhao_lianxiren,
               'xiaozhao_lianxifangshi': lianxifangshi
               }
        job_list.append(xiaozhao_job)
        xiaozhao_company_job = {'company_name': xiaozhao_company,
                       'company_content': company_content,
                       'job_list': xiaozhao_job_list}
        print(xiaozhao_company_job)
        # xiaozhao_topic = {
        #     'author_id': ObjectId("id"),
        #     'content': company_all
        #     'abstract': xiaozhao_company_job,
        #     'cover_url': imgsrc,
        #     'deleted': False,
        #     'title': datet,
        #     'create_at': datetime.datetime.utcnow(),
        #     'update_at': datetime.datetime.utcnow(),
        #     'last_reply_at': datetime.datetime.utcnow(),
        #     "lock": False,
        #     "good": False,
        #     "top": False,
        #     "__v": 0
    except:
        pass


    """
    job1 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[0]
    jobname1 = job1.get_attribute('data-positionname')
    #print(jobname1)
    xiangxiyemian1 = job1.find_element_by_css_selector('.item_title_date')
    xiangxiyemian2 = xiangxiyemian1.find_element_by_css_selector('a')
    xiangxiyemian3 = xiangxiyemian2.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian3)
    xiangxi_list.append(xiangxiyemian3)

    job2 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[1]
    jobname2 = job2.get_attribute('data-positionname')
    #print(jobname2)
    xiangxiyemian4 = job2.find_element_by_css_selector('.item_title_date')
    xiangxiyemian5 = xiangxiyemian4.find_element_by_css_selector('a')
    xiangxiyemian6 = xiangxiyemian5.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian6)
    xiangxi_list.append(xiangxiyemian6)

    job3 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[2]
    jobname3 = job3.get_attribute('data-positionname')
    #print(jobname3)
    xiangxiyemian7 = job3.find_element_by_css_selector('.item_title_date')
    xiangxiyemian8 = xiangxiyemian7.find_element_by_css_selector('a')
    xiangxiyemian9 = xiangxiyemian8.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian9)
    xiangxi_list.append(xiangxiyemian9)

    job4 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[3]
    jobname4 = job4.get_attribute('data-positionname')
    #print(jobname4)
    xiangxiyemian10 = job4.find_element_by_css_selector('.item_title_date')
    xiangxiyemian11= xiangxiyemian10.find_element_by_css_selector('a')
    xiangxiyemian12 = xiangxiyemian11.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian12)
    xiangxi_list.append(xiangxiyemian12)

    job5 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[4]
    jobname5 = job5.get_attribute('data-positionname')
    #print(jobname5)
    xiangxiyemian13 = job5.find_element_by_css_selector('.item_title_date')
    xiangxiyemian14 = xiangxiyemian13.find_element_by_css_selector('a')
    xiangxiyemian15 = xiangxiyemian14.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian15)
    xiangxi_list.append(xiangxiyemian15)

    job6 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[5]
    jobname6 = job6.get_attribute('data-positionname')
    #print(jobname6)
    xiangxiyemian16 = job6.find_element_by_css_selector('.item_title_date')
    xiangxiyemian17 = xiangxiyemian16.find_element_by_css_selector('a')
    xiangxiyemian18 = xiangxiyemian17.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian18)
    xiangxi_list.append(xiangxiyemian18)

    job7 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[6]
    jobname7 = job7.get_attribute('data-positionname')
    #print(jobname7)
    xiangxiyemian19 = job7.find_element_by_css_selector('.item_title_date')
    xiangxiyemian20 = xiangxiyemian19.find_element_by_css_selector('a')
    xiangxiyemian21 = xiangxiyemian20.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian21)
    xiangxi_list.append(xiangxiyemian21)

    job8 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[7]
    jobname8 = job8.get_attribute('data-positionname')
    #print(jobname8)
    xiangxiyemian22 = job8.find_element_by_css_selector('.item_title_date')
    xiangxiyemian23 = xiangxiyemian22.find_element_by_css_selector('a')
    xiangxiyemian24 = xiangxiyemian23.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian24)
    xiangxi_list.append(xiangxiyemian24)

    job9 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[8]
    jobname9 = job9.get_attribute('data-positionname')
    #print(jobname9)
    xiangxiyemian25 = job9.find_element_by_css_selector('.item_title_date')
    xiangxiyemian26 = xiangxiyemian25.find_element_by_css_selector('a')
    xiangxiyemian27 = xiangxiyemian26.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian27)
    xiangxi_list.append(xiangxiyemian27)

    job10 = browser.find_elements_by_css_selector("[class='con_list_item default_list']")[9]
    jobname10 = job10.get_attribute('data-positionname')
    #print(jobname10)
    xiangxiyemian28 = job10.find_element_by_css_selector('.item_title_date')
    xiangxiyemian29 = xiangxiyemian28.find_element_by_css_selector('a')
    xiangxiyemian30 = xiangxiyemian29.get_attribute('href')  # 得到详细页面的url
    #print('详细页面')
    #print(xiangxiyemian30)
    xiangxi_list.append(xiangxiyemian30)
    browser.close()

    job_describes = []
    job_place = []
    for xiangxiyemian in xiangxi_list:
        browser = webdriver.Chrome()
        browser.get(xiangxiyemian)
        job_describe = browser.find_element_by_css_selector('.job-detail').text
        job_describes.append(job_describe)
        jobplace1 = browser.find_element_by_css_selector('.work_addr')
        jobplace2 = jobplace1.find_element_by_css_selector('a').text
        job_place.append(jobplace2)
        browser.close()

    job_1 = {'jobname' : jobname1,
             'jobcontent' : job_describes[0],
             'workplace' : job_place[0],
             'detailed_url' : xiangxi_list[0]}

    job_2 = {'jobname': jobname2,
            'jobcontent': job_describes[1],
            'workplace': job_place[1],
            'detailed_url': xiangxi_list[1]}

    job_3 = {'jobname': jobname3,
            'jobcontent': job_describes[2],
            'workplace': job_place[2],
            'detailed_url': xiangxi_list[2]}

    job_4 = {'jobname': jobname4,
            'jobcontent': job_describes[3],
            'workplace': job_place[3],
            'detailed_url': xiangxi_list[3]}

    job_5 = {'jobname': jobname5,
            'jobcontent': job_describes[4],
            'workplace': job_place[4],
            'detailed_url': xiangxi_list[4]}

    job_6 = {'jobname': jobname6,
            'jobcontent': job_describes[5],
            'workplace': job_place[5],
            'detailed_url': xiangxi_list[5]}

    job_7 = {'jobname': jobname7,
             'jobcontent': job_describes[6],
             'workplace': job_place[6],
             'detailed_url': xiangxi_list[6]}

    job_8 = {'jobname': jobname8,
             'jobcontent': job_describes[7],
             'workplace': job_place[7],
             'detailed_url': xiangxi_list[7]}

    job_9 = {'jobname': jobname9,
             'jobcontent': job_describes[8],
             'workplace': job_place[8],
             'detailed_url': xiangxi_list[8]}

    job_10 = {'jobname': jobname10,
             'jobcontent': job_describes[9],
             'workplace': job_place[9],
             'detailed_url': xiangxi_list[9]}


    company_all = {'jobone' : job_1,
                   'jobtwo': job_2,
                   'jobthree':job_3,
                   'jobforth':job_4,
                   'jobfifth':job_5,
                   'jobsixth':job_6,
                   'jobsenventh':job_7,
                   'jobeighth':job_8,
                   'jobnighth':job_9,
                   'jobtenth':job_10}
    print(company_all)
    print(job_place)
    """
    """
    topic = {
        'author_id': ObjectId("id"),
        'content': company_all
        'abstract': text,
        'cover_url': imgsrc,
        'deleted': False,
        'title': datet,
        'create_at': datetime.datetime.utcnow(),
        'update_at': datetime.datetime.utcnow(),
        'last_reply_at': datetime.datetime.utcnow(),
        "lock": False,
        "good": False,
        "top": False,
        "__v": 0

    }
    collection.insert(topic)
    """




















    # for j in jobname()
    #     browser = webdriver.Chrome()
    #     browser.get(third_url4)
    #     print(j)
    #     jobname = j.get_attribute('data-positionname')  # 有一个翻页的问题  工作名称
    #     print(jobname)
    #     xiangxiyemian1 = j.find_element_by_css_selector('.item_title_date')
    #     xiangxiyemian2 = xiangxiyemian1.find_element_by_css_selector('a')
    #     xiangxiyemian3 = xiangxiyemian2.get_attribute('href')  # 得到详细页面的url
    #     print('详细页面')
    #     print(xiangxiyemian3)
    #     browser.close()
    #     browser = webdriver.Chrome()
    #     browser.get(xiangxiyemian3)
    #     adress_name = browser.find_element_by_css_selector('.address').text
    #     print(adress_name)
    #     adress = browser.find_element_by_css_selector('.work_addr').text
    #     # adress2 = adress.find_element_by_css_selector('a').text
    #     print(adress)
    #     browser.close()

    #   print(company)
    #     print(jobname)
    #     print('*************************')
    #     jobrequests = browser.find_element_by_css_selector("[class='job_request']")
    #     jobrequest = jobrequests.text
    #     print(jobrequest)
    #     print('************************')
    #     jobdetails = browser.find_element_by_css_selector("[class='job_detail']")
    #     jobdetail = jobdetails.text
    #     print(jobdetail)
    #     try:
    #         os.makedirs(os.getcwd() + '\\wuhan')
    #     except:
    #         pass
    #     with open(os.getcwd() + '\\wuhan\\' + jobname + '.txt', 'w', encoding='utf-8') as f:
    #         f.write(company)
    #         f.write('\n')
    #         f.write(jobname)
    #         f.write('\n')
    #         f.write(jobrequest)
    #         f.write('\n')
    #         f.write(jobdetail)
    #
    #     browser.close()

#browser.close()

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
# url = 'https://www.lagou.com/jobs/list_?px=default&gx=&isSchoolJob=1&city=武汉#filterBox'
# req = request.Request(url)
# cookie_str = r'JSESSIONID=ABAAABAAAGGABCB92EA53F670A9C4BBBE749C70537112C9; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1555583311; _ga=GA1.2.678791697.1555583311; _gat=1; user_trace_token=20190418182829-b52c781d-61c4-11e9-93c6-5254005c3644; LGSID=20190418182829-b52c79d3-61c4-11e9-93c6-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F184-0-24-0; LGUID=20190418182829-b52c7b5c-61c4-11e9-93c6-5254005c3644; _gid=GA1.2.71042631.1555583311; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a300168762d3-0eb73ded48cf6d-3f674706-1327104-16a300168772b%22%2C%22%24device_id%22%3A%2216a300168762d3-0eb73ded48cf6d-3f674706-1327104-16a300168772b%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=027e2f80f1a53a35b63b571167a2fdae1bbc2fc5b4e211a91c580f642d3dbe16; _putrc=4EF66433F6F6C3B8123F89F2B170EADC; login=true; unick=%E6%9D%8E%E7%82%9C%E9%BA%92; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=2fea5aaea9a3c6f172a7b376bd95a645a19b72c968fb8a6458dba450042e774f; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=b17fc9e84801762b4853855551377c166cd3d92441; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1555583587; LGRID=20190418183304-59823a9c-61c5-11e9-93c6-5254005c3644'
# req.add_header('cookie', cookie_str)
# req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
#
# resp = request.urlopen(req)
#
# print(resp.read().decode('utf-8'))


# class Login(object):
#     def __init__(self):
#         self.headers = {
#             'Referer': 'https://www.lagou.com/',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#
#             'Host': 'passport.lagou.com'
#         }
#         self.login_url = 'https://passport.lagou.com/login/login.html?signature=7B1FBD57CE0A7E65E0087030148379A8&service=http%253A%252F%252Fwww.lagou.com%252Flogin&action=login&serviceId=lagou&ts=1555409928072'
#         self.post_url = 'https://passport.lagou.com/login/login.html?signature=7B1FBD57CE0A7E65E0087030148379A8&service=http%253A%252F%252Fwww.lagou.com%252Flogin&action=login&serviceId=lagou&ts=1555409928072'
#         # self.logined_url = 'https://www.shixiseng.com/settings/profile'
#         self.session = requests.Session()
#
#     # def token(self):
#     #         response = self.session.get(self.login_url, headers=self.headers)
#     #         selector = etree.HTML(response.text)
#     #         token = selector.xpath('//div//input[2]/@value')
#     #         return token
#
#     def login(self, phonenumber, password,isValidate,):
#         post_data = {
#             'isValidate': isValidate,
#             'username': phonenumber,
#             'password': password,
#             'request_form_verifyCode':'',
#             'submit':'',
#             #'challenge':challenge
#         }
#         response = self.session.post(self.post_url, data=post_data, headers=self.headers)
#         #print(response)
#
#         if response.status_code == 200:
#             html = 'https://www.lagou.com/gongsi/184-0-24-0'
#             self.dynamics(html)
#             # print(response.text)
#
#         # response = self.session.get(self.logined_url, headers=self.headers)
#         # if response.status_code == 200:
#         #         self.profile(response.text)
#
#     def dynamics(self, html):
#         browser = webdriver.Chrome()
#         browser.get(html)
#         #print(browser.page_source)
#         input_one = browser.find_elements_by_css_selector('.top')#有翻页
#
#         #print(input_one)
#         for i in input_one:
#             one = i.find_element_by_css_selector('p')
#             two = one.find_element_by_css_selector('a')
#             second_url = two.get_attribute('href')#得到公司页面url
#             #print(second_url)
#             browser.get(second_url)
#
#             third_url1 = browser.find_element_by_css_selector('.company_navs_wrap')
#             third_url2 = third_url1.find_elements_by_css_selector('li')[1]
#             third_url3 = third_url2.find_element_by_css_selector('a')
#             third_url4 = third_url3.get_attribute('href')#得到公司页面的招聘页面url
#             #print(third_url4)
#             browser.get(third_url4)
#
#             company = browser.find_element_by_css_selector("[class='hovertips']").text#公司名称
#             print(company)
#
#             jobnames = browser.find_elements_by_css_selector("[class='con_list_item default_list']")#招聘工作的列表
#             for j in jobnames:
#                 jobname = j.get_attribute('data-positionname')#有一个翻页的问题  工作名称
#                 print(jobname)
#                 xiangxiyemian1 = j.find_element_by_css_selector('.item_title_date')
#                 xiangxiyemian2 = xiangxiyemian1.find_element_by_css_selector('a')
#                 xiangxiyemian3 = xiangxiyemian2.get_attribute('href')#得到详细页面的url
#                 print('详细页面')
#                 print(xiangxiyemian3)
#                 browser.get(xiangxiyemian3)
#                 adress_name = browser.find_element_by_css_selector('.address').text
#                 print(adress_name)
#                 adress = browser.find_element_by_css_selector('.work_addr').text
#                 #adress2 = adress.find_element_by_css_selector('a').text
#                 print(adress)
#                 #browser.close()
#
#         #   print(company)
#         #     print(jobname)
#         #     print('*************************')
#         #     jobrequests = browser.find_element_by_css_selector("[class='job_request']")
#         #     jobrequest = jobrequests.text
#         #     print(jobrequest)
#         #     print('************************')
#         #     jobdetails = browser.find_element_by_css_selector("[class='job_detail']")
#         #     jobdetail = jobdetails.text
#         #     print(jobdetail)
#         #     try:
#         #         os.makedirs(os.getcwd() + '\\wuhan')
#         #     except:
#         #         pass
#         #     with open(os.getcwd() + '\\wuhan\\' + jobname + '.txt', 'w', encoding='utf-8') as f:
#         #         f.write(company)
#         #         f.write('\n')
#         #         f.write(jobname)
#         #         f.write('\n')
#         #         f.write(jobrequest)
#         #         f.write('\n')
#         #         f.write(jobdetail)
#         #
#         #     browser.close()
#
#         browser.close()
#         sleep(5)
#
# if __name__ == "__main__":
#         login = Login()
#         login.login(phonenumber='18344238907', password='ca71f341bd8d847d79b958d2c40b4532',isValidate='ture')


