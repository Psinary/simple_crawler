# -*- coding: gbk -*-
__author__ = 'Psinary'
"""

命令行版功能：
    使用前清理下载过的文件，并提示是否进行，第一次使用直接y

        1、新下载
            1，全自动下载
            2，自定义下载

        2、读取列表下载


        3、自动抓取列表

开发功能选项：
添加自定义下载页数**************
多页下载  *************************
使用返回的列表写入一个下载列表 ***********************
计数器：共多少张图 *****************************
 pass 添加浏览器头 urlib不支持这个
 pass 是否添加代理，考虑使用class那种参数形式
 pass 写一个一边写入地址，一边下载的下载器

页面数目计算函数**************************
    读取单个页面函数
    计算单个页面中图片数目

下载函数 *****************
    1、读取文本地址函数 **********************
    2、下载函数添加下载进度条，
        优化下载器
        IOError: [Errno socket error] [Errno 10060] 问题解决方法。。。。
        链接断开后重新链接
        sleep()

检查，创建文件夹
封装exe，打包exe
手机端测试，linux，mac测试
添加启动文件说明，名字
说明文档编写
    字典，以及说明
功能视频制作


"""
import urllib
import re
import os

"""程序根目录需要有url_codes、images、convert_url_list和images_url共4个文件夹，用来存储临时数据"""


def get_content_url(url):
    """获取网页代码，并写入文件"""
    response = urllib.urlopen(url)

    print "网页状态码：%d" % response.getcode()
    print "开始读取下载网页文件。。。"

    content = response.read()
    print "读取文件完毕，开始写入文件。。。"
    file_page1 = open("url_codes\\page1.txt","a+")
    file_page1.write("\n"+ content)
    file_page1.close()
    print "写入文件完毕"
    response.close()

    return content

def get_images_url(url_content):
    """提取网页图片地址，并保存在images_url\image_url.txt"""
    regex = r'class="directlink largeimg" href="(.+?\.jpg)"'
    print "开始提取图片地址。。。"
    pat = re.compile(regex)
    images_code_list = re.findall(pat,url_content)
    print "提取图片地址完毕，开始保存。。。"
    images_url_file = open("images_url\\image_url.txt","a+")

    images_url_file.write(str(images_code_list))
    images_url_file.close()
    image_num = len(images_code_list)
    print "已保存%d张图片地址" % image_num
    return images_code_list,image_num


def get_images(download_url_list):
    """下载图片到images文件夹"""
    num = 0
    for image_url in download_url_list:
        print "第%d张图片下载中。。。" % num
        print image_url

        urllib.urlretrieve(image_url,"images\\%d.jpg" % num)
        num += 1
    print "所有图片下载完成！！"

def convert_list_url(images_list):
    """把提取出来的地址列表转换为单行的txt文本存储到convert_url_list文件夹下的list.txt"""
    convert_list_file = open("convert_url_list\\list.txt","a+")
    convert_list_file.write("\n")
    # convert_list_file.writelines(images_list) # 所有的地址都连在一起不方便调用
    for url in images_list:
        convert_list_file.write(url)
        convert_list_file.write("\n")
        # print "写入一行"
    convert_list_file.close()


def simple_set_page(start_page,end_page,keyword):
    """输入起始页和结束页以及关键词返回对应关键词的多页url列表"""

    end_page += 1
    url_all = []
    for page in range(start_page,end_page):
        url = "https://yande.re/post?page=%d&tags=%s" % (page,keyword)
        # print url # 测试打印提取地址
        url_all.append(url)

    return url_all

def get_download_url(start_page,end_page,keyword): # 第三参数为字符串
    """获取下载地址列表转换为其他第三方下载软件可以使用的文本文件"""
    page = 1
    numbers = 0
    for url in simple_set_page(start_page,end_page,keyword):
        code_content = get_content_url(url)
        return_list = get_images_url(code_content)
        images_url_list = return_list[0]
        image_num = return_list[1]
        numbers = numbers + image_num
        convert_list_url(images_url_list)
        print "###########第%d页地址写入完成###########" % page
        page += 1
    print "共%d张图片地址提取完成！！" % numbers

def read_images_url(list_file_address):
    """读取文本中的下载地址，并返回下载地址列表"""
    images_urlfile = open(list_file_address,"r")
    url = images_urlfile.read()
    url_list = url.split("\n")
    # print ('' in url_list) # 检查是否还有空字符
    null_num = url_list.count('')
    for num in range(0,null_num):
        url_list.remove('')

    images_urlfile.close()
    print "共%d张图片地址，删除%d个空字符" % (len(url_list),null_num)
    return url_list

def download(file_address):
    """读取地址开始下载"""
    url_list = read_images_url(file_address)
    get_images(url_list)
    print "程序结束！！"

def read_page(url):
    """读取网页内容并返回"""
    response = urllib.urlopen(url)

    print "网页状态码：%d" % response.getcode()
    print "开始读取下载网页文件。。。"

    content = response.read()
    response.close()
    return content

def check_image(url_content):
    """检查是否有图片，返回结果"""
    regex = r'class="directlink largeimg" href="(.+?\.jpg)"'
    print "开始提取图片地址。。。"
    pat = re.compile(regex)
    images_code_list = re.findall(pat,url_content)
    image_num = len(images_code_list)

    """把文件里的下载地址转换为其他第三方下载工具可以使用的地址"""
    convert_list_url(images_code_list)

    if image_num == 0:
        return False
    else:
        return True


def check_page_num(keyw):
    """查询有多少图片，返回图片页数"""
    page = 1
    while True:
        url = "https://yande.re/post?page=%d&tags=%s" % (page,keyw)
        print "############第%d页############" % page
        content = read_page(url)
        have_pic_result = check_image(content)
        print "检查图片"
        if have_pic_result:
            page += 1
        else:
            print "共有%d页图片" % (page - 1)
            return page
            break

def MainProgram():
    """程序主体"""
    check_file1()
    check_file2()
    check_file3()
    check_file4()
    print "启动程序将会清理之前的缓冲数据，是否启动？<y/n>"
    if raw_input("> ") == 'y':
        clear_date()
        print """
Name: Yande crawler text v1.00

    该爬虫是yande.re图站的抓取爬虫。支持标签，自定义页数及导出下载列表爬取。其中下载列表支持第三
方工具批量下载（如迅雷，和IDM等）

使用须知：

1、程序根目录需要有url_codes、images、convert_url_list和images_url共4个文件夹，用来存储临时数据,
如果没有该文件夹，请手动创建，否则程序无法下载数据。
2、该程序仅供学习研究使用，如由使用者进行大量爬取下载所引起的法律问题，将由使用者本人承担。本程
序作者概不负责。
3、如使用本程序，将默认同意以上条款。
        """
        print "##########--<  Yande crawler text v1.00  >--##########"
        print "1.新下载 按1 \n2.读取列表下载 按2 \n3.自动抓取列表 按3"
        select_mode = raw_input("输入下载模式代号:> ")
        while True:
            if select_mode == '1':
                print "##########新下载##########"
                new_download()
                break
            elif select_mode == '2':
                print "##########读取列表下载###########"
                continue_download()
                break
            elif select_mode == '3':
                print "##########自动抓取列表##########"
                key_word = raw_input("请输入要下载图片的关键词：> ")
                num = check_page_num(key_word)
                print "关键词%s有%d页图片" % (key_word,num - 1)
                read_images_url("convert_url_list\\list.txt")
                print "列表抓取完毕！！"
                break
            else:
                print "##########错误输入##########"
            print "1.新下载 按1 \n2.读取列表下载 按2 \n3.退出 按3"
            select_mode = raw_input("输入下载模式代号:> ")
    else:
        print "转移数据后再启动程序。"

def new_download():
    """新的下载模块"""
    print "1.全自动下载 按1 \n2.自定义下载 按2\n"
    while True:
        select = raw_input("请选择模式：> ")
        if select == '1':
            print "###########全自动下载###########"
            key_word = raw_input("请输入要下载图片的关键词：> ")
            num = check_page_num(key_word)
            print "关键词%s有%d页图片" % (key_word,num - 1)

            print "###########开始下载###########"
            download("convert_url_list\\list.txt")
            break
        elif select == '2':
            print "###########自定义下载###########"
            key_word = raw_input("请输入要下载图片的关键词：> ")
            start_page = raw_input("请输入起始页码：>")
            end_page = raw_input("请输入结束页码：> ")
            start_page = int(start_page)
            end_page = int(end_page)
            url_list = simple_set_page(start_page,end_page,key_word)
            for url in url_list:
                code_content = get_content_url(url)
                piclist_num = get_images_url(code_content)
                convert_list_url(piclist_num[0])
                print "###########第%d页 %d张图片地址写入完成###########" % (start_page,piclist_num[1])
                start_page += 1
            download("convert_url_list\\list.txt")
            break
        else:
            print "###########输入错误############"
    print "1.全自动下载 按1 \n2.自定义下载 按2\n"

def continue_download():
    """输入文件路径（支持相对路径），读取文件开始下载"""
    imagelist = raw_input("请输入文件路径：>  ")
    print "开始下载"
    download(imagelist)

def clear_date():
    """清除以前的缓冲数据"""
    if os.path.exists("url_codes\page1.txt"):
        os.remove("url_codes\page1.txt")
    if os.path.exists("images_url\image_url.txt"):
        os.remove("images_url\image_url.txt")
    if os.path.exists("convert_url_list\list.txt"):
        os.remove("convert_url_list\list.txt")

def check_file1():
    """检查创建convert_url_list文件夹"""
    if os.path.exists("/convert_url_list"):
        pass
    else:
        os.makedirs("convert_url_list")

def check_file2():
    """检查创建image文件夹"""
    if os.path.exists("/images"):
        pass
    else:
        os.makedirs("images")

def check_file3():
    """检查创建images_url文件夹"""
    if os.path.exists("/images_url"):
        pass
    else:
        os.makedirs("images_url")

def check_file4():
    """检查创建url_codes文件夹"""
    if os.path.exists("/url_codes"):
        pass
    else:
        os.makedirs("url_codes")

if __name__ == "__main__":
    MainProgram()



# new_download()
# MainProgram()
# clear_date()
# test E:\CS\Python\codes\convert_url_list\list.txt
#print check_page_num("kanan")

# url = "https://yande.re/post?page=1&tags=yuzu-soft"
# content = read_page(url)
# print check_image(content)

# get_download_url(1,2,"clip_craft")
# read_images_url("convert_url_list\\list.txt")
# download("convert_url_list\\list.txt")

# page = 1
# for url in simple_set_page():
#     code_content = get_content_url(url)
#     images_url_list = get_images_url(code_content)
#     convert_list_url(images_url_list)
#     print "###########第%d页地址写入完成###########" % page
#     page += 1

# url = "https://yande.re/post?page=2&tags=yuzu-soft"
# code_content = get_content_url(url)
# images_url_list = get_images_url(code_content)
# convert_list_url(images_url_list)
#get_images(images_url_list)
