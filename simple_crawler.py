# -*- coding: gbk -*-
__author__ = 'Psinary'
"""

�����а湦�ܣ�
    ʹ��ǰ�������ع����ļ�������ʾ�Ƿ���У���һ��ʹ��ֱ��y

        1��������
            1��ȫ�Զ�����
            2���Զ�������

        2����ȡ�б�����


        3���Զ�ץȡ�б�

��������ѡ�
����Զ�������ҳ��**************
��ҳ����  *************************
ʹ�÷��ص��б�д��һ�������б� ***********************
����������������ͼ *****************************
 pass ��������ͷ urlib��֧�����
 pass �Ƿ���Ӵ�������ʹ��class���ֲ�����ʽ
 pass дһ��һ��д���ַ��һ�����ص�������

ҳ����Ŀ���㺯��**************************
    ��ȡ����ҳ�溯��
    ���㵥��ҳ����ͼƬ��Ŀ

���غ��� *****************
    1����ȡ�ı���ַ���� **********************
    2�����غ���������ؽ�������
        �Ż�������
        IOError: [Errno socket error] [Errno 10060] ������������������
        ���ӶϿ�����������
        sleep()

��飬�����ļ���
��װexe�����exe
�ֻ��˲��ԣ�linux��mac����
��������ļ�˵��������
˵���ĵ���д
    �ֵ䣬�Լ�˵��
������Ƶ����


"""
import urllib
import re
import os

"""�����Ŀ¼��Ҫ��url_codes��images��convert_url_list��images_url��4���ļ��У������洢��ʱ����"""


def get_content_url(url):
    """��ȡ��ҳ���룬��д���ļ�"""
    response = urllib.urlopen(url)

    print "��ҳ״̬�룺%d" % response.getcode()
    print "��ʼ��ȡ������ҳ�ļ�������"

    content = response.read()
    print "��ȡ�ļ���ϣ���ʼд���ļ�������"
    file_page1 = open("url_codes\\page1.txt","a+")
    file_page1.write("\n"+ content)
    file_page1.close()
    print "д���ļ����"
    response.close()

    return content

def get_images_url(url_content):
    """��ȡ��ҳͼƬ��ַ����������images_url\image_url.txt"""
    regex = r'class="directlink largeimg" href="(.+?\.jpg)"'
    print "��ʼ��ȡͼƬ��ַ������"
    pat = re.compile(regex)
    images_code_list = re.findall(pat,url_content)
    print "��ȡͼƬ��ַ��ϣ���ʼ���档����"
    images_url_file = open("images_url\\image_url.txt","a+")

    images_url_file.write(str(images_code_list))
    images_url_file.close()
    image_num = len(images_code_list)
    print "�ѱ���%d��ͼƬ��ַ" % image_num
    return images_code_list,image_num


def get_images(download_url_list):
    """����ͼƬ��images�ļ���"""
    num = 0
    for image_url in download_url_list:
        print "��%d��ͼƬ�����С�����" % num
        print image_url

        urllib.urlretrieve(image_url,"images\\%d.jpg" % num)
        num += 1
    print "����ͼƬ������ɣ���"

def convert_list_url(images_list):
    """����ȡ�����ĵ�ַ�б�ת��Ϊ���е�txt�ı��洢��convert_url_list�ļ����µ�list.txt"""
    convert_list_file = open("convert_url_list\\list.txt","a+")
    convert_list_file.write("\n")
    # convert_list_file.writelines(images_list) # ���еĵ�ַ������һ�𲻷������
    for url in images_list:
        convert_list_file.write(url)
        convert_list_file.write("\n")
        # print "д��һ��"
    convert_list_file.close()


def simple_set_page(start_page,end_page,keyword):
    """������ʼҳ�ͽ���ҳ�Լ��ؼ��ʷ��ض�Ӧ�ؼ��ʵĶ�ҳurl�б�"""

    end_page += 1
    url_all = []
    for page in range(start_page,end_page):
        url = "https://yande.re/post?page=%d&tags=%s" % (page,keyword)
        # print url # ���Դ�ӡ��ȡ��ַ
        url_all.append(url)

    return url_all

def get_download_url(start_page,end_page,keyword): # ��������Ϊ�ַ���
    """��ȡ���ص�ַ�б�ת��Ϊ���������������������ʹ�õ��ı��ļ�"""
    page = 1
    numbers = 0
    for url in simple_set_page(start_page,end_page,keyword):
        code_content = get_content_url(url)
        return_list = get_images_url(code_content)
        images_url_list = return_list[0]
        image_num = return_list[1]
        numbers = numbers + image_num
        convert_list_url(images_url_list)
        print "###########��%dҳ��ַд�����###########" % page
        page += 1
    print "��%d��ͼƬ��ַ��ȡ��ɣ���" % numbers

def read_images_url(list_file_address):
    """��ȡ�ı��е����ص�ַ�����������ص�ַ�б�"""
    images_urlfile = open(list_file_address,"r")
    url = images_urlfile.read()
    url_list = url.split("\n")
    # print ('' in url_list) # ����Ƿ��п��ַ�
    null_num = url_list.count('')
    for num in range(0,null_num):
        url_list.remove('')

    images_urlfile.close()
    print "��%d��ͼƬ��ַ��ɾ��%d�����ַ�" % (len(url_list),null_num)
    return url_list

def download(file_address):
    """��ȡ��ַ��ʼ����"""
    url_list = read_images_url(file_address)
    get_images(url_list)
    print "�����������"

def read_page(url):
    """��ȡ��ҳ���ݲ�����"""
    response = urllib.urlopen(url)

    print "��ҳ״̬�룺%d" % response.getcode()
    print "��ʼ��ȡ������ҳ�ļ�������"

    content = response.read()
    response.close()
    return content

def check_image(url_content):
    """����Ƿ���ͼƬ�����ؽ��"""
    regex = r'class="directlink largeimg" href="(.+?\.jpg)"'
    print "��ʼ��ȡͼƬ��ַ������"
    pat = re.compile(regex)
    images_code_list = re.findall(pat,url_content)
    image_num = len(images_code_list)

    """���ļ�������ص�ַת��Ϊ�������������ع��߿���ʹ�õĵ�ַ"""
    convert_list_url(images_code_list)

    if image_num == 0:
        return False
    else:
        return True


def check_page_num(keyw):
    """��ѯ�ж���ͼƬ������ͼƬҳ��"""
    page = 1
    while True:
        url = "https://yande.re/post?page=%d&tags=%s" % (page,keyw)
        print "############��%dҳ############" % page
        content = read_page(url)
        have_pic_result = check_image(content)
        print "���ͼƬ"
        if have_pic_result:
            page += 1
        else:
            print "����%dҳͼƬ" % (page - 1)
            return page
            break

def MainProgram():
    """��������"""
    check_file1()
    check_file2()
    check_file3()
    check_file4()
    print "�������򽫻�����֮ǰ�Ļ������ݣ��Ƿ�������<y/n>"
    if raw_input("> ") == 'y':
        clear_date()
        print """
Name: Yande crawler text v1.00

    ��������yande.reͼվ��ץȡ���档֧�ֱ�ǩ���Զ���ҳ�������������б���ȡ�����������б�֧�ֵ���
�������������أ���Ѹ�ף���IDM�ȣ�

ʹ����֪��

1�������Ŀ¼��Ҫ��url_codes��images��convert_url_list��images_url��4���ļ��У������洢��ʱ����,
���û�и��ļ��У����ֶ���������������޷��������ݡ�
2���ó������ѧϰ�о�ʹ�ã�����ʹ���߽��д�����ȡ����������ķ������⣬����ʹ���߱��˳е�������
�����߸Ų�����
3����ʹ�ñ����򣬽�Ĭ��ͬ���������
        """
        print "##########--<  Yande crawler text v1.00  >--##########"
        print "1.������ ��1 \n2.��ȡ�б����� ��2 \n3.�Զ�ץȡ�б� ��3"
        select_mode = raw_input("��������ģʽ����:> ")
        while True:
            if select_mode == '1':
                print "##########������##########"
                new_download()
                break
            elif select_mode == '2':
                print "##########��ȡ�б�����###########"
                continue_download()
                break
            elif select_mode == '3':
                print "##########�Զ�ץȡ�б�##########"
                key_word = raw_input("������Ҫ����ͼƬ�Ĺؼ��ʣ�> ")
                num = check_page_num(key_word)
                print "�ؼ���%s��%dҳͼƬ" % (key_word,num - 1)
                read_images_url("convert_url_list\\list.txt")
                print "�б�ץȡ��ϣ���"
                break
            else:
                print "##########��������##########"
            print "1.������ ��1 \n2.��ȡ�б����� ��2 \n3.�˳� ��3"
            select_mode = raw_input("��������ģʽ����:> ")
    else:
        print "ת�����ݺ�����������"

def new_download():
    """�µ�����ģ��"""
    print "1.ȫ�Զ����� ��1 \n2.�Զ������� ��2\n"
    while True:
        select = raw_input("��ѡ��ģʽ��> ")
        if select == '1':
            print "###########ȫ�Զ�����###########"
            key_word = raw_input("������Ҫ����ͼƬ�Ĺؼ��ʣ�> ")
            num = check_page_num(key_word)
            print "�ؼ���%s��%dҳͼƬ" % (key_word,num - 1)

            print "###########��ʼ����###########"
            download("convert_url_list\\list.txt")
            break
        elif select == '2':
            print "###########�Զ�������###########"
            key_word = raw_input("������Ҫ����ͼƬ�Ĺؼ��ʣ�> ")
            start_page = raw_input("��������ʼҳ�룺>")
            end_page = raw_input("���������ҳ�룺> ")
            start_page = int(start_page)
            end_page = int(end_page)
            url_list = simple_set_page(start_page,end_page,key_word)
            for url in url_list:
                code_content = get_content_url(url)
                piclist_num = get_images_url(code_content)
                convert_list_url(piclist_num[0])
                print "###########��%dҳ %d��ͼƬ��ַд�����###########" % (start_page,piclist_num[1])
                start_page += 1
            download("convert_url_list\\list.txt")
            break
        else:
            print "###########�������############"
    print "1.ȫ�Զ����� ��1 \n2.�Զ������� ��2\n"

def continue_download():
    """�����ļ�·����֧�����·��������ȡ�ļ���ʼ����"""
    imagelist = raw_input("�������ļ�·����>  ")
    print "��ʼ����"
    download(imagelist)

def clear_date():
    """�����ǰ�Ļ�������"""
    if os.path.exists("url_codes\page1.txt"):
        os.remove("url_codes\page1.txt")
    if os.path.exists("images_url\image_url.txt"):
        os.remove("images_url\image_url.txt")
    if os.path.exists("convert_url_list\list.txt"):
        os.remove("convert_url_list\list.txt")

def check_file1():
    """��鴴��convert_url_list�ļ���"""
    if os.path.exists("/convert_url_list"):
        pass
    else:
        os.makedirs("convert_url_list")

def check_file2():
    """��鴴��image�ļ���"""
    if os.path.exists("/images"):
        pass
    else:
        os.makedirs("images")

def check_file3():
    """��鴴��images_url�ļ���"""
    if os.path.exists("/images_url"):
        pass
    else:
        os.makedirs("images_url")

def check_file4():
    """��鴴��url_codes�ļ���"""
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
#     print "###########��%dҳ��ַд�����###########" % page
#     page += 1

# url = "https://yande.re/post?page=2&tags=yuzu-soft"
# code_content = get_content_url(url)
# images_url_list = get_images_url(code_content)
# convert_list_url(images_url_list)
#get_images(images_url_list)
