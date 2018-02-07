import requests

url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'

form_data = {
    'first': 'false',
    'pn': '1',
    'kd': '产品经理',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86?labelWords=&fromSearch=true&suginput='
}

rep = requests.post(url=url, data=form_data, headers=headers)
print(rep.text)

