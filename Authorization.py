# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:52:40 2021

@author: lenovo
"""

import time
import hmac
import hashlib
import urllib.parse
import sys
import webbrowser

appid = "1305000518"
bucket = "pic-1305000518"
secretid = "AKIDoY4oQoj2n12nKdOdnkV5nFTTTFmCdHYb"
secretkey = "JRJNI4U4Ter7fy73rQkYv3v3wlNmIcjd"
#content_length = sys.argv[1]
#content_md5 = sys.argv[2]
#UriPathname = '/' + sys.argv[3]

#这是测试代码
content_length = str(218367)
content_md5 = 'de6c2e6d66424c9c0eba9c5b7a109dcd'
UriPathname = '/' + '我已经彻底成功了.jpg'

#这里是将content_length的值转换为字符串形式
while content_length.find(',') != -1:
	content_length = content_length.replace(',','')

#这里是将通过sys导入的32位的十六进制字符转化为一个128位的二进制字符，具体原理就是读取每一位的十六进制字符然后将字符转化为十进制，再转化为二进制的字符串，将字符串叠加
content_md5 = content_md5.upper()
i = 0
var = ''
while i < len(content_md5):
    temp = bin(int(content_md5[i],16))
    temp = temp[2:]
    while len(temp) < 4:
        temp = '0' + temp
    var = var + temp
    i = i + 1
content_md5 = var

#这里是将生成的128位二进制字符串每六位取为一个单元进行编码，转化为base64编码后的字符串
content_md5 = content_md5 + '0000'
refer = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
refer = refer + refer.lower() + '0123456789+/'
n = 1
var = ''
while n < 23:
    temp = content_md5[6*(n-1):6*n]
    temp = int(temp,2)
    var = var + refer[temp]
    n = n + 1 
content_md5 = var + '=='
MD5 = content_md5

#这里给出了将字符串特殊化urlencode的函数
def str_urlencode(strtoencode):
    "strtoencode是需要被编码的序列"
    strtoencode = urllib.parse.quote(strtoencode)
    strtoencode = strtoencode.translate(str.maketrans({'/':'%2F','=':'%3D','+':'%2B'}))
    return strtoencode

content_md5 = str_urlencode(content_md5)

#这是测试代码
#print(content_md5)
#print('\n')

content_type = str_urlencode('image/jpeg')

#这是测试代码
#print(content_type)
#print('\n')

"""
这是先前的实现方式，现舍弃不用
#这里是将content-type进行特殊化的urlencode编码，除了一般的urlencode编码外，还有一部分特殊符号如/需要编码，具体请见网址：https://cloud.tencent.com/document/product/436/7778#.E4.B8.8A.E4.BC.A0.E5.AF.B9.E8.B1.A1
#由于content-type只涉及到一项需要编码的内容，这里偷懒取巧了，正确的做法是遍历整个content-type后替换所有特殊字符
content_type = urllib.parse.quote('image/jpeg')
if '/' in content_type:
    n = content_type.find('/')
    content_type = content_type[:n] + '%2F' + content_type[n+1:]

#这里是将content-md5进行特殊化的urlencode编码，具体内容如上段
content_md5 = urllib.parse.quote(content_md5)
if '/' in content_md5:
    n = content_md5.find('/')
    content_md5 = content_md5[:n] + '%2F' +content_md5[n+1:]
"""  

#生成时间戳
#EndTimestamp = int(time.time() + 600)
#StartTimestamp = int(time.time())
#KeyTime = "{StartTimestamp};{EndTimestamp}"
#KeyTime = KeyTime.format_map(vars())

#以下为测试代码
KeyTime = "1614430371;1614433971"

#生成SignKey
SignKey = hmac.new(secretkey.encode('utf-8'),KeyTime.encode('utf-8'),hashlib.sha1).hexdigest()

#步骤3中要求生成HttpParameters，但是实际测试结果发现一般情况下该字段为空，故省去

#生成HttpHeaders：上传图片的请求头有content-md5,content-type,host，这里的写法是很取巧的，实际上应该遍历整个请求头，将key和value值都进行urlencode编码等处理
#HttpHeaders是否要包括content-length，现在还不是很清楚，需要测试一下
HttpHeaders = "content-length={content_length}&content-md5={content_md5}&content-type=image%2Fjpeg&host=pic-1305000518.cos.ap-shanghai.myqcloud.com"
HttpHeaders = HttpHeaders.format_map(vars())

#生成HttpString
HttpString = "put\n{UriPathname}\n\n{HttpHeaders}\n"
HttpString = HttpString.format_map(vars())

#这是测试代码
print(HttpString)
print('\n')
httpstring_encode = HttpString.encode('utf-8')
print(httpstring_encode)
print('\n')

#生成StringToSign
sha1_http_string = hashlib.sha1(HttpString.encode('utf-8')).hexdigest()
StringToSign = "sha1\n{KeyTime}\n{sha1_http_string}\n"
StringToSign = StringToSign.format_map(vars())

#这是测试代码
#print(StringToSign)
#print('\n')
#print(sha1_http_string)
#print('\n')

#生成Signature
Signature = hmac.new(SignKey.encode('utf-8'),StringToSign.encode('utf-8'),hashlib.sha1).hexdigest()

#这是测试代码
#print(Signature)
#print('\n')

#生成签名
s = "q-sign-algorithm=sha1&q-ak={secretid}&q-sign-time={KeyTime}&q-key-time={KeyTime}&q-header-list=content-md5;content-type;host&q-url-param-list=&q-signature={Signature}" 
s = s.format_map(vars())

#这是测试代码
#print(s + '\n')

#生成x-callback-url码传递参数到腾讯云图床二
url = sys.argv[-1] + "?{s}" + "&MD5={MD5}" + "&len={content_length}"
url = url.format_map(vars())

#这是测试代码
#print(url)

#webbrowser.get('safari').open(url)
