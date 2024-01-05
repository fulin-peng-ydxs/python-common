import urllib.request
import urllib.parse
import sys
import json
from lxml import etree


def get_data(year):
    # 结果集
    result = {
        "xiu": [],
        "ban": []
    }
    #
    for month in range(1, 13):
        q = str(year) + "-" + str(month)
        month_result = send_request(q)
        if month_result is not None:
            result.get("xiu").extend(month_result.get("xiu"))
            result.get("ban").extend(month_result.get("ban"))
    return result


def send_request(month):
    # 基础请求地址：万年历
    base_url = 'https://wannianrili.bmcx.com/ajax/?'
    # 请求参数：month指定年月 xxxx-xx
    data = {
        'q': month,
        'v': '22121303'
    }
    # 请求头
    headers = {
    }
    # 完整请求地址
    url = base_url + urllib.parse.urlencode(data)
    # 请求对象
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)  # 发送请求
    content = response.read().decode('utf-8')  # 解析响应：html数据
    # 解析html
    tree = etree.HTML(content)
    xiu_list = tree.xpath('//div[@class="wnrl_riqi"]//a[@class="wnrl_riqi_xiu"]/span[@class="wnrl_td_gl"]/text()')
    ban_list = tree.xpath('//div[@class="wnrl_riqi"]//a[@class="wnrl_riqi_ban"]/span[@class="wnrl_td_gl"]/text()')
    if len(xiu_list) == 0 and len(ban_list) == 0:
        return
    result = {
        "xiu": [],
        "ban": []
    }
    for xiu in xiu_list:
        result.get("xiu").append(month + "-" + xiu)
    for ban in ban_list:
        result.get("ban").append(month + "-" + ban)
    return result


# 程序入口
if __name__ == '__main__':
    # 获取数据
    result = get_data(sys.argv[1])
    download_result = {
        "法定节假日": result.get("xiu"),
        "法定补班日": result.get("ban")
    }
    # 下载数据
    with open(sys.argv[2], 'w') as file:
        json.dump(download_result, file, ensure_ascii=False)
