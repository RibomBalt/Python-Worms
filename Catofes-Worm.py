# -*-encoding: utf-8 -*-
import requests
import re
import os
import sys

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 状态不是200时，抛出HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except requests.HTTPError as e:
        return r.status_code


def postHTML(url, data):
    try:
        r = requests.post(url, data, timeout=100)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except requests.HTTPError as e:
        return r.status_code


if __name__ == '__main__':

    assert os.name == 'nt'
    data = dict()

    print(r'This is a worm to download and rename data of Prof.Wang Jiajun on http://edu.catofes.com')

    data['user'] = input(r'Please input your account(typically your school id):')
    data['pw'] = input(r'Please input your password(your school id again if not changed):')

    url = r'https://edu.catofes.com/education/teacher/ActionUser.do?dispatch=login'


    r1 = requests.post(url, data, timeout=100)
    cookies = r1.cookies
    r5 = requests.get(r'https://edu.catofes.com/education/course/ActionSession.do?dispatch=eduCenter', cookies=cookies,
                      timeout=100)

    addrURL = r'http://edu.catofes.com/education/upload/lesson/16/'


    pattern = r'(\d{13}_\d{1,2}).([a-z]{3})" target="_blank" >([^<]+)'
    # print(r5.text)
    regexResult = re.findall(pattern, r5.text)
    # print(regexResult)
    # list of urlName, kuozhanming, name

    # Only bad passwords leads to empty Regex Result
    if not len(regexResult):
        input('Exception: Bad passwords or accounts! Exit with an enter.')
        sys.exit(0)


    # TODO make directory, download files and rename it



    directory = os.getcwd()+r'\Electronic-Magnetic'
    if not os.path.exists(directory):
        os.mkdir(directory)
    print(r'Download PPT to %s'%directory)

    counting = 0
    for data in regexResult:
        fileURL = ''.join([addrURL, data[0], '.', data[1]])
        with open(''.join([directory, "\\", data[2], '.', data[1]]), 'wb') as f:
            r = requests.get(fileURL, cookies=cookies, timeout=1000)
            for fileData in r.iter_content(chunk_size=100):
                f.write(fileData)
        counting += 1
        print('已完成%d份下载，共有%d份，文件名：%s.%s' % (counting, len(regexResult), data[2], data[1]))

    input('已完成下载，请在%s路径下查看！回车键退出程序！' % directory)
