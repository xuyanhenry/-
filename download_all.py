import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from utils.fanqiedownload import change_userid,get_chapter_list,get_text_from_xpath,download_novels
from utils.qimaodownload import get_book_list,get_book_name,qimaodownloadmain
if __name__ == '__main__':
    while True:
        choose_web=input("选择小说网址：1.番茄 2.七猫 （输入1/2, 输入exit退出程序）")
        if choose_web.lower() == 'exit':
            break
        if choose_web=='1':
            while True:
                change_userid()
                book_id = input("Please enter the book ID(输入'exit' 返回选择处): ")
                if book_id.lower() == 'exit':
                    break
                css = '.page-header-info .info-name h1::text'
                item_id_list = get_chapter_list(book_id)
                if item_id_list==[]:
                    print("找不到此书，请检查书的id和网站是否正确")
                    continue
                if item_id_list==None:
                    continue
                text_content = get_text_from_xpath(book_id, css)
                if text_content:
                    book_name = text_content.strip()
                    print("book name:",book_name)
                else:
                    book_name = "Unknown_Book"
                # 获取当前脚本的目录
                current_directory = os.path.dirname(sys.executable)
                output_file = os.path.join(current_directory, f"{book_name}.txt")
                # output_file = f"E:/爬虫/{book_name}.txt"                        #要改
                download_novels(item_id_list, book_name, output_file)
                print(f"All chapters saved to {output_file}")
        if choose_web=='2':
            while True:
                headers = {
                    "app-version": "51110",
                    "platform": "android",
                    "reg": "0",
                    "AUTHORIZATION": "",
                    "application-id": "com.****.reader",
                    "net-env": "1",
                    "channel": "unknown",
                    "qm-params": "",
                }

                sign_key = 'd3dGiJc651gSQ8w1'
                api_url = "https://api-ks.wtzw.com/api/v1/chapter/content"
                book_id = input("Enter the book ID(输入 'exit' 返回选择处): ")
                if book_id.lower() == 'exit':
                    break
                list_data=get_book_list(book_id)
                if list_data==[]:
                    print("找不到id")
                    continue
                if list_data==None:
                    continue
                book_name=get_book_name(book_id,headers)
                print(book_name)
                current_directory = os.path.dirname(sys.executable)
                output_file = os.path.join(current_directory, f"{book_name}.txt")
                # output_file = f"E:/爬虫/{book_name}.txt" 
                qimaodownloadmain(book_id, headers, sign_key, api_url, output_file, list_data)
                print(f"All chapters saved to {output_file}")


