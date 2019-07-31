# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: config.py
# @time: 19-7-17 上午11:48

from urllib import parse
from easydict import EasyDict as edict


# initial the edict object
__C = edict()
# customer can call by cfg variabel
cfg = __C

# ############################### db params ############################### #
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

# keywords info
# ############################### common info ############################### #
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
# ACCTPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,images/webp,images/apng,*/*;q=0.8,application/signed-exchange;v=b3'
ACCTPT = 'text/html,application/xhtml+xml,*/*;q=0.8'

# url params
"""
1. type:
    only can choise in [1, 12, 2, 3, 32, 4, 6, 8, 17]
2. keywords:
3. time:
    only can choise in [1, 7, 30, 90, 180]
3. page:
    range is from 1 to 50
4. diqu:
    diqu id of huabei: range(1, 6)
    diqu id of huanan: [19, 20, 21, 33, 34]
    diqu id of huadong: range(9, 16)
    diqu id of huazhong: range(16, 19)
    diqu id of xibei: range(27, 32)
    diqu id of xinan: range(22, 27)
    diqu id of dongbei: range(6, 9)
"""

REFERER = 'https://www.bidcenter.com.cn/'
FILTER_TYPE = '1,2,4'

# without index of 32
REGION = list(range(1, 35))
REGION.remove(32)

# ---------------- time params select ------------------- #
# 1: time = 1
TIME = 7
PAGE = range(1, 51)

# 1: time = 30
# TIME = 30
# PAGE = range(1, 10)

# 2: time = 30
# TIME = 30
# PAGE = range(1, 51)
# ---------------- time params select ------------------- #


"""
:keyword
医院、病理、玻片、玻片影像、切片影像、玻片扫描、切片扫描、数字切片、数字玻片、试剂、耗材

test_url = https://search.bidcenter.com.cn/search?keywords=%E7%97%85%E7%90%86&diqu=1&time=30&type=1,2,4&page=1
"""

# ############################### keywords of 医院 ############################### #
__C.params_dict = edict()
__C.params_dict.TMPCookie = 'bidguidnew=182cee5a-68c5-4c9b-821b-0b7be1486d03; bidguid=e8f1e7f7-c039-43e1-8166-ea10fe87dc68; _uab_collina=156326605289189350882046; _umdata=G8CEF84EB50A2847C96804BAECAFB7B7073D65E; BAIDU_SSP_lcr=https://www.baidu.com/link?url=Fo0o6Ck8dwwmNAKMuEqYiif4Tq0779NYRvmVAJ3MIXBS6ZeV5sQyIXpVM8C-B49a&wd=&eqid=83ed08230006b9d4000000065d2d9643; UM_distinctid=16bfacdf55f1f3-0e0154f208ca5a-3b654406-240800-16bfacdf5602e5; BIDCTER_USERNAME=UserName=13169614817; aspcn=id=3844287&name=13169614817&vip=1&company=%e5%8c%97%e4%ba%ac%e7%99%be%e5%ba%a6%e7%bd%91%e8%ae%af%e7%a7%91%e6%8a%80%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8(%e9%87%8d%e5%a4%8d)&lianxiren=%e6%9e%97%e5%b0%8f%e5%ba%a6&tel=010-8813528&email=linjinquan14@163.com&diqu=&Token=FE346093871731730777F11AC9A32972CCC16DE1F2DD26943EB6AFDF0F14C767AE3BB998D85F5039243748D8512BF652; PASSKEY=Token=FE346093871731730777F11AC9A32972CCC16DE1F2DD26943EB6AFDF0F14C767AE3BB998D85F5039243748D8512BF652; keywords==; Hm_lpvt_9954aa2d605277c3e24cb76809e2f856={}'
# header params
__C.params_dict.headers = edict()
__C.params_dict.headers.Accept = ACCTPT
__C.params_dict.headers.Referer = REFERER
__C.params_dict.headers.Cookie = ''

# request params
__C.params_dict.params = edict()
# __C.params_dict.params.keywords = parse.quote('医院')
__C.params_dict.params.type = FILTER_TYPE
__C.params_dict.params.time = TIME
__C.params_dict.params.diqu = REGION
__C.params_dict.params.page = PAGE


