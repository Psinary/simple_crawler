# simple_crawler
yande  images crawler/spider  
一个yande.re 图站的爬虫，支持tag和自定义页数下载  

## 原理
用python写的简单的yande图站的爬虫，主要使用urllib模块下载读取网页，正则表达式提取图片下载地址并写入convert_url_list\list.txt，支持其他第三方工具（迅雷，IDM等）读取下载。

## 使用须知
程序根目录需要有url_codes,images,convert_url_list和images_url共4个文件夹，用来存储临时数据,如果没有该文件夹，请手动创建，否则程序无法下载数据。  
程序有封装为exe的版本，可以下载到win系统直接使用  
使用windows系统的命令行执行脚本时，把文件编码改为gbk，否则，会出现乱码。

## 使用方法、
根据提示使用即可，关键字可以使用英文，或罗马音
