# -*-coding:utf-8-*-
import re
import time
import sys
import os
import json
import traceback
import requests
from bson import ObjectId
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy.orm import load_only
from datetime import datetime

from dc.conf.settings import get_settings2
from dc.services.mysql_service import MySQLService
from dc.services.redis_service import RedisService
from dc.services.logging_service import LoggingService
from dc.models.model import DCSiteListRule, DCSiteListItem, MPCompanyAntitrust, MPCompanyInfo, DCIntellectualProperty, \
    DCSiteList
from dc.common.alchemy import query2dict
from dc.services.check_analysis import CheckAnalysis
from dc.tests.browser import Browser
from dc.common.webdriver_helper import WebDriverHelper
from dc.conf.settings import get_settings

"""
[功能]：数据采集-文章分析服务
[作者]：lws
[日期]：2022-10-19
"""

mysql = MySQLService()
redisService = RedisService('redis')
client1 = redisService.get_client()

log_service = LoggingService('dc_analysis_html.log')

redis_prefix = 'laravel_database_'
redis_analyse_key = f'{redis_prefix}dc-site-task-analyse'
redis_site_bind_rule = f'{redis_prefix}site_id_bind_rule_id_'
redis_rule_item = f'{redis_prefix}site_rule_info_'
redis_site_mark = f'{redis_prefix}site_source_bind_mark_'
redis_site_name = f'{redis_prefix}site_source_bind_name_'
redis_analysis_key = f'{redis_prefix}-dc-analysis-method-'
save_path = "/uploads/chanquan/"

from jwtools.io_util import *



# 写入主任务队列
def handel():

    zfile = os.path.dirname(__file__) + "/22.html"
    res_body = read_text_from_file(zfile)
    res_url = 'https://finance.sina.com.cn/stock/relnews/us/2024-09-06/doc-incnfpnk4614820.shtml'
    insert_info = analysisChanQuan('rule_item_arr', 'task_id', 'site_id', 'detail_method', 'utf-8', res_url, res_body)
    print(insert_info['image'])
    exit(0)



def get_rule_info(site_id):
    session = mysql.create_session()
    try:
        ret = session.query(DCSiteListRule).filter(DCSiteListRule.siteListId == site_id,
                                                   DCSiteListRule.status == 1).first()
        dc_rule_info = query2dict(ret)
        session.close()
        return dc_rule_info['id']
    except:
        if session is not None:
            session.close()

        log_service.error(f"获取规则信息失败，对应siteId：{site_id}，失败原因：{traceback.format_exc()}")
        return 0


def get_rule_item(rule_id):
    session = mysql.create_session()
    try:
        fields = ['id', 'siteListId', 'siteRuleId', 'columnKey', 'crawlRuleType', 'crawlRule', 'startFlag', 'endFlag',
                  'columnRegex', 'columnDefault']
        ret = session.query(DCSiteListItem).options(load_only(*fields)).filter(DCSiteListItem.siteRuleId == rule_id,
                                                                               DCSiteListItem.status == 1).all()
        dc_rule_item = []
        for info in ret:
            tmp = info.__dict__
            tmp.pop('_sa_instance_state')
            dc_rule_item.append(tmp)

        session.close()
        return dc_rule_item
    except:
        if session is not None:
            session.close()

        log_service.error(f"获取数据项规则失败，对应ruleId：{rule_id}，失败原因：{traceback.format_exc()}")
        return []


def save_es(info, es_index, url='', site_nam='', main_task_id='', task_id='', site_id=''):
    session = mysql.create_session()
    site: DCSiteList = session.query(DCSiteList).filter(DCSiteList.id == site_id).first()
    session.close()
    # 拆分site.tags 并写入es
    tags = site.tags.split(',') if site.tags else []
    info['tags'] = tags
    info['dc_detail_url'] = f"{url}"
    info['dc_site_name'] = f"{site_nam}"
    info['mainTaskId'] = main_task_id
    info['siteListId'] = site_id
    info['taskId'] = task_id
    info['analysis_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    info['version'] = 2

    if es_index == "dc_policy":
        info['area'] = getPolicyInfo(info['title'] + site_nam, 7, 'ner')
        info['industry'] = getPolicyInfo(info['title'] + info['text'], 6, 'ner')
        info['informationtype'] = getInformationType(info['title']) if getInformationType(info['title']) != '其他' else ''

    if es_index == "dc_bianjifagao":
        info['isPublished'] = 0  # 发布状态
        info['isPass'] = 0  # pass
        info['isWaiting'] = 0  # 待定
        info['isDeal'] = 0  # 处理状态
        info['publishID'] = 0  # 发布出去的id
        info['createAt'] = info['analysis_time']
        info['content'] = info['text']
        info['_dc_type'] = 1
        # 删除 info字典 中的 text
        info.pop('text') if 'text' in info else None

    try:
        es = ess.get_connect()
        is_exists = es.indices.exists(index=es_index)
        if is_exists:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "siteListId": site_id
                                }
                            },
                            {
                                "match": {
                                    "dc_detail_url.keyword": url
                                }
                            }
                        ]
                    }
                }
            }
            es.delete_by_query(index=es_index, body=query)

        res = es.index(index=es_index, body=info)
        es.close()
        return res['_id']
    except:
        log_service.error(f"写入es失败原因：{traceback.format_exc()}")
        return ''


def deal_format_date(date_str):
    date_str = date_str.strip()
    date_str = date_str.replace('年', '-')
    date_str = date_str.replace('月', '-')
    date_str = date_str.replace('日', '')
    date_str = date_str.replace('/n', '')
    date_str = date_str.replace('/', '-')
    date_str = date_str.replace('\\', '-')
    date_str = date_str.replace('.', '-')
    date_str = date_str.replace('- ', '-')
    date_str = date_str[0:10]

    if not date_str:
        format_date = '1970-01-01'  # time.strftime("%Y-%m-%d", time.localtime())
        type1 = 2
        return [format_date, type1]

    if datetime.strptime(date_str, "%Y-%m-%d"):
        date_str = datetime.strptime(date_str, "%Y-%m-%d")
        format_date = date_str.strftime("%Y-%m-%d")
        type1 = 1
    elif datetime.strptime(date_str, "%m/%d/%Y"):
        date_str = datetime.strptime(date_str, "%m/%d/%Y")
        format_date = date_str.strftime("%Y-%m-%d")
        type1 = 1
    elif datetime.strptime(date_str, "%A, %B %d, %Y"):
        date_str = datetime.strptime(date_str, "%A, %B %d, %Y")
        format_date = date_str.strftime("%Y-%m-%d")
        type1 = 1
    elif datetime.strptime(date_str, "%B %d %Y"):
        date_str = datetime.strptime(date_str, "%B %d %Y")
        format_date = date_str.strftime("%Y-%m-%d")
        type1 = 1
    elif datetime.strptime(date_str, "%A, %b %d, %Y, %I:%M%p"):
        date_str = datetime.strptime(date_str, "%A, %b %d, %Y, %I:%M%p")
        format_date = date_str.strftime("%Y-%m-%d")
        type1 = 1
    elif datetime.strptime(date_str, "%d %b %Y"):
        date_str = datetime.strptime(date_str, "%d %b %Y")
        format_date = date_str.strftime("%Y-%m-%d")
        type1 = 1
    else:
        format_date = '1970-01-01'  # time.strftime("%Y-%m-%d", time.localtime())
        type1 = 2

    return [format_date, type1]


def analysis(html, items, task_id, site_id, detail_method=2, charset='utf-8', detail_url=''):
    if detail_method == 2:

        f = open(f"./tmp{task_id}.html", 'a', encoding=f"{charset}", errors='ignore')
        f.write(html)
        f.close()

        analysis_method = client1.get(f"{redis_analysis_key}{site_id}")
        asd = int(analysis_method) if analysis_method else 0
        try:
            if asd == 1:
                opt = webdriver.FirefoxOptions()
                opt.add_argument("--headless")
                opt.add_argument('--disable-gpu')
                driver = webdriver.Firefox(options=opt)
                # webdriver_url = get_settings2('webdriver', 'host')  # "http://192.168.1.120:4444"
                # driver = WebDriverHelper.get_remote_webdriver(webdriver_url, Browser.Firefox)
                driver.get(f"{detail_url}")
                driver.implicitly_wait(10)
            else:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-gpu')
                # webdriver_url = get_settings2('webdriver', 'host')  # "http://192.168.1.120:4444"
                # driver = WebDriverHelper.get_remote_webdriver(webdriver_url, Browser.Chrome)
                driver = webdriver.Chrome(options=chrome_options)
                driver.get('file:///' + os.path.abspath(f"tmp{task_id}.html"))
                # driver.set_page_load_timeout()  页面加载超时
                # driver.set_script_timeout()  js加载超时
        except:
            if os.path.isfile(f"tmp{task_id}.html"):
                os.remove(os.path.abspath(f"tmp{task_id}.html"))
            log_service.error(f"子任务id：{task_id}启动浏览器失败")

    info = {}
    false_num = 0
    for item in items:
        str1 = ''
        if detail_method == 2:
            try:
                if item['crawlRuleType'] == 1:
                    xpath = driver.find_elements('xpath', item['crawlRule'])
                    driver.implicitly_wait(10)
                    str1 = CheckAnalysis.deal_text(xpath)
                if item['crawlRuleType'] == 2:
                    css = driver.find_elements('css selector', item['crawlRule'])
                    driver.implicitly_wait(10)
                    str1 = CheckAnalysis.deal_text(css)
                # if item['crawlRuleType'] == 5:
                #     xpath = driver.find_elements('xpath', item['crawlRule'])
                #     driver.implicitly_wait(10)
                #     str1 = CheckAnalysis.deal_attr(xpath, item['attr_value'])
                # if item['crawlRuleType'] == 6:
                #     css = driver.find_elements('css selector', item['crawlRule'])
                #     driver.implicitly_wait(10)
                #     str1 = CheckAnalysis.deal_attr(css, item['attr_value'])

            except:
                str1 = ''
        else:
            html = CheckAnalysis.html_replace_str(html)
            if item['crawlRuleType'] == 1:
                str1 = CheckAnalysis.selector_xpath(html, f"{item['crawlRule']}")
            if item['crawlRuleType'] == 2:
                str1 = CheckAnalysis.selector_css(html, f"{item['crawlRule']}")
            # if item['crawlRuleType'] == 5:
            #     str1 = CheckAnalysis.selector_xpath_attr(html, f"{item['crawlRule']}")
            # if item['crawlRuleType'] == 6:
            #     str1 = CheckAnalysis.selector_css_attr(html, f"{item['crawlRule']}")

        if item['crawlRuleType'] == 3:
            arr = re.search(item['crawlRule'], html)
            if not arr:
                str1 = ''
            else:
                str1 = arr.group()

        if item['crawlRuleType'] == 4:
            begin = html.find(item['startFlag'])
            end = html.rfind(item['endFlag'])
            str1 = html[begin:end]

        if str1:
            str1 = str1.strip()
            str1 = str1.strip("/n")

        if 'columnRegex' in item and item['columnRegex'] and str1:
            arr = re.findall(f"{item['columnRegex']}", str1)
            str1 = arr[0] if arr else str1

        if item['columnKey'] == 'public_time':
            tmp_arr = deal_format_date(str1)
            str1 = tmp_arr[0]
            if tmp_arr[1] == 2:
                false_num += 1

        info[item['columnKey']] = str1
        if len(str1) == 0:
            false_num += 1
            info[item['columnKey']] = item['columnDefault']

    if detail_method == 2:
        try:
            driver.close()
        except:
            log_service.error(f"关闭链接")

        if os.path.isfile(f"tmp{task_id}.html"):
            os.remove(os.path.abspath(f"tmp{task_id}.html"))

    if false_num == 0:
        log_service.dcPullLog(f"子任务id：{task_id}对应数据解析成功")
        analysis_status = 1
    elif false_num == len(items):
        log_service.dcPullLog(f"子任务id：{task_id}对应数据解析失败")
        analysis_status = 2
        info = {}
    else:
        log_service.dcPullLog(f"子任务id：{task_id}对应数据部分解析成功")
        analysis_status = 3

    return {'info': info, 'analysis_status': analysis_status}


def up_site_task(es_id, es_index, task_id, analysis_status=0):
    session = mysql.create_session()

    up_sql = f"update DC_SiteTask set esIndex = '{es_index}', esId = '{es_id}', analysisStatus = {analysis_status} where id = {task_id}"
    try:
        session.execute(up_sql)
        session.commit()
        session.close()
    except:
        if session is not None:
            session.close()
        log_service.error(f"子任务id：{task_id}更新执行状态失败，失败原因：{traceback.format_exc()}")


def saveCompanyAntitrust(info, esId, esIndex, url='', site_nam='', main_task_id='', task_id='', site_id=''):
    mysql1 = MySQLService('mysql_company')
    session1 = mysql1.create_session()
    if info['siteListId'] == 377:
        text1 = info['text']
        arr = text1.split("/n")
        for tmp1 in arr:
            arr1 = tmp1.split("\n")
            if len(arr1) < 2:
                arr1 = tmp1.split()
                if len(arr1) < 2:
                    continue

            if arr1[1] == "案件名称":
                continue

            deal_arr = dealConclusionDate(arr1[3], info['pinjieyong'])
            df = {'title': arr1[1],
                  'source': "反垄断局",
                  'pubTime': "",
                  'conclusionDate': deal_arr[0].strip(),
                  'url': info['dc_detail_url'],
                  'companyInfo': arr1[2],
                  'isUnconditional': 1,
                  'createAt': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  'esId': esId,
                  'year': deal_arr[1],
                  'month': deal_arr[2],
                  'esIndex': esIndex}
            dch = MPCompanyAntitrust(**df)
            session1.add(dch)
        session1.commit()
    elif info['siteListId'] == 378:
        chrome_options1 = Options()
        chrome_options1.add_argument('--headless')
        chrome_options1.add_argument('--no-sandbox')
        chrome_options1.add_argument('--disable-gpu')
        driver3 = webdriver.Chrome(options=chrome_options1)

        info['dc_detail_url'] = f"{url}"
        info['dc_site_name'] = site_nam
        info['mainTaskId'] = main_task_id
        info['siteListId'] = site_id
        info['taskId'] = task_id
        info['analysis_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info['version'] = 2

        driver3.get(url)
        xpath = driver3.find_elements('xpath', "//div[@class='zt_xilan_07']//table//tr[1]/following-sibling::tr")
        driver3.implicitly_wait(10)

        for x in xpath:
            td1 = x.find_element('xpath', './td[1]')
            if td1.text == '序号':
                continue
            td2 = x.find_element('xpath', './td[2]')
            td3 = x.find_element('xpath', './td[3]')
            td4 = x.find_element('xpath', './td[4]')
            conclusionDate2 = td4.text.strip()

            info['title'] = td2.text
            info['content'] = td3.text
            info['public_time'] = deal_format_date(conclusionDate2)[0]

            es = ess.get_connect()
            res = es.index(index=esIndex, body=info)
            es.close()

            df = {'title': td2.text,
                  'source': "反垄断执法二司",
                  'pubTime': "",
                  'conclusionDate': conclusionDate2,
                  'url': url,
                  'companyInfo': td3.text,
                  'isUnconditional': 1,
                  'createAt': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  'esId': res['_id'] if res['_id'] else '',
                  'year': conclusionDate2[0:4],
                  'month': conclusionDate2[5:].split('月')[0].strip('0'),
                  'esIndex': esIndex}
            dch = MPCompanyAntitrust(**df)
            session1.add(dch)
        session1.commit()
        driver3.close()
    else:
        arr_time = info['public_time'].split("-")
        df = {'title': info['title'],
              'source': "反垄断局" if info['siteListId'] == 379 else "反垄断执法二司",
              'pubTime': info['public_time'],
              'conclusionDate': "",
              'url': info['dc_detail_url'],
              'companyInfo': getCompanyName(info['content']),
              'isUnconditional': 2,
              'createAt': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              'esId': esId,
              'year': arr_time[0],
              'month': arr_time[1].strip("0"),
              'esIndex': esIndex}
        dch = MPCompanyAntitrust(**df)
        session1.add(dch)
        session1.commit()


def getCompanyName(body):
    mysql1 = MySQLService('mysql_company')
    session1 = mysql1.create_session()

    companyNames = client1.get("company_name_list")
    # companyDict = client1.get("company_dict")
    if companyNames:
        companyNames = json.loads(companyNames)
        # companyDict = json.loads(companyDict)
    else:
        companyInfos = session1.query(MPCompanyInfo).options(load_only(MPCompanyInfo.id, MPCompanyInfo.name)).all()
        # companyNames = []
        companyDict = {}
        for companyInfo in companyInfos:
            tmp = companyInfo.__dict__
            companyNames.append(tmp['name'])
            # companyDict[tmp['id']] = tmp['name']
        client1.set("company_name_list", json.dumps(companyNames), 86400)
        # client1.set("company_dict", json.dumps(companyDict), 86400)

    arr1 = []
    for companyName in companyNames:
        arr = re.search(companyName, body)
        if arr:
            arr1.append(arr[0])

    return '、'.join(arr1) if arr1 else ''


def dealConclusionDate(date_str, year):
    date_str = date_str.strip()
    date_str = date_str.replace('年', '-')
    date_str = date_str.replace('月', '-')
    date_str = date_str.replace('日', '')

    try:
        if datetime.strptime(date_str, "%Y-%m-%d"):
            date_str1 = datetime.strptime(date_str, "%Y-%m-%d")
            format_date = datetime.strftime(date_str1, "%Y年%#m月%#d日")
            year1 = date_str1.strftime("%Y")
            month1 = date_str1.strftime("%#m")
    except:
        if datetime.strptime(date_str, "%m-%d"):
            date_str1 = datetime.strptime(date_str, "%m-%d")
            format_date1 = datetime.strftime(date_str1, "%#m月%#d日")
            if re.search("\\d{4}", year):
                arr = re.search("\\d{4}", year)
                format_date = str(arr[0]) + "年" + format_date1
                year1 = arr[0]
                month1 = date_str1.strftime("%#m")
        else:
            format_date = '1970年1月1日'
            year1 = 1970
            month1 = 1

    return [format_date, year1, month1]


def analysisChanQuan(rule_item_arr, task_id, site_id, detail_method, charset, detail_url, html):
    ym = time.strftime('%Y%m', time.localtime(time.time())) + "/"
    # analysis_method = client1.get(f"{redis_analysis_key}{site_id}")
    asd = 0  # int(analysis_method) if analysis_method else 0
    try:
        if asd == 1:
            opt = webdriver.FirefoxOptions()
            opt.add_argument("--headless")
            opt.add_argument('--disable-gpu')

            opt.set_preference("browser.download.folderList", 2)
            opt.set_preference("browser.download.manager.showWhenStarting", False)
            opt.set_preference("browser.download.dir", "/data" + save_path)

            driver = webdriver.Firefox(options=opt)
            driver.implicitly_wait(10)
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            prefs = {'profile.default_content_settings.popups': 0,
                     'download.default_directory': "/data" + save_path + ym}
            chrome_options.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(options=chrome_options)

        driver.set_window_size(width=1005, height=500, windowHandle='current')
        # if detail_method == 1:
        #     f = open(f"./tmp{task_id}.html", 'a', encoding=f"{charset}", errors='ignore')
        #     f.write(html)
        #     f.close()
        #
        #     time.sleep(1)
        #
        #     driver.get('file:///' + os.path.abspath(f"tmp{task_id}.html"))
        # else:
        driver.get(detail_url)
    except:
        log_service.error(f"子任务id：{task_id}启动浏览器失败")

    # 处理保存快照,返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    pic_name = save_path + ym + CheckAnalysis.getMd5(detail_url)

    info = {}
    false_num = 0

    # https://finance.sina.com.cn/stock/relnews/us/2024-09-06/doc-incnfpnk4614820.shtml
    # 10693567	1889	4162654	https://news.sina.com.cn	https://finance.sina.com.cn/stock/relnews/us/2024-09-06/doc-incnfpnk4614820.shtml	英特尔考虑出售其自动驾驶子公司股份，昔日智驾芯片巨头已连亏两年	1	2024-09-06 20:14:21	1	200		66daf21c1d1eedc9ca659fcc	1	2024-09-06 20:11:09	2024-09-06 20:14:41	dc_bianjifagao	KWtCx5EBG8DIxTyBDw5j			1878

    rule = {
        'crawlRule': '//div[@class="article"]',
        'path': 'https://finance.sina.com.cn/',
        'pathLevel': '0',
    }

    str1 = CheckAnalysis.getImages(driver, detail_url, rule, 1)

    return {'info': info, 'analysis_status': 'analysis_status','image': str1}


def checkWords(site_id, title):
    session = mysql.create_session()
    try:
        ret = session.query(DCIntellectualProperty).filter(DCIntellectualProperty.siteListId == site_id).first()
        dc_info = query2dict(ret)
        session.close()
        keywords = dc_info['keyWords']
        filter_words = dc_info['filterWords']
        filter_arr = filter_words.split(",") if filter_words else []
        keyword_arr = keywords.split(",") if keywords else []
        for filter_word in filter_arr:
            if re.findall(filter_word, title):
                return 2

        for keyword in keyword_arr:
            if re.findall(keyword, title):
                return 1
            else:
                continue
    except:
        if session is not None:
            session.close()

        log_service.error(f"获取规则信息失败，对应siteId：{site_id}，失败原因：{traceback.format_exc()}")
        return 2

    return 2


# 获取区域、行业
def getPolicyInfo(content, model_id, type1):
    info = []
    params = {"model_id": model_id, "data": content, "type": type1}
    if model_id == 2:
        url = get_settings('getArea')
    elif model_id == 1:
        url = get_settings('getIndustry')

    try:
        res = requests.post(url, json=params)
        res.encoding = "UTF-8"
        if res.status_code != 200:
            return info

        arr = json.loads(res.text)['data']
        for item in arr:
            if item['type'] == 'ORG':
                info.append('全国')
            else:
                info.append(item['span'])

        return list(set(info))[0:3] if info else []
    except:
        return info


# 获取信息类别
def getInformationType(content):
    info = ''
    params = {"model_id": 4, "data": content, "type": "classification"}
    url = get_settings('getInformationType')
    try:
        res = requests.post(url, json=params)
        res.encoding = "UTF-8"
        if res.status_code != 200:
            return info

        info = json.loads(res.text)['data']

        return info
    except:
        return info


handel()
