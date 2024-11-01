import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from urllib.parse import urlencode
import json
from tqdm import tqdm
import threading
import queue
import base64
from parsel import Selector
import time
import random
import re


def get_book_name(id,headers):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    #     'cookie':'acw_tc=1a0c399617293366986786817e00b5bd210730f1cde9556e33d0c8bc558697; acw_sc__v2=6713957a678736ed1c0fa330ee64dc6c9d8cca56'
    # }
    #old
    #response = requests.get(f'https://www.qimao.com/shuku/{id}/',headers=headers)
    # print("response",response)
    response = requests.get(f"https://api-bc.wtzw.com/api/v1/reader/detail?id={id}", #proxies=proxies,
                        timeout=12)
    if response.status_code == 200:
        data=response.json()
        #print(data)
        filename=data['data']['title']
        filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
        return filename
        #old
        #selector = Selector(response.text)
        #elements = selector.css('span.txt::text').get()  
        # print(elements)
        #if elements:
            # print("elements",elements)
            #return elements
        
    else:
        print("Failed to fetch data，please try again")
        return None
    


def get_headers(book_id):

    version_list = [
        '73720', '73700',
        '73620', '73600',
        '73500',
        '73420', '73400',
        '73328', '73325', '73320', '73300',
        '73220', '73200',
        '73100', '73000', '72900',
        '72820', '72800',
        '70720', '62010', '62112',
    ]

    random.seed(book_id)

    version = random.choice(version_list)

    headers = {
        "AUTHORIZATION": "",
        "app-version": f"{version}",
        "application-id": "com.****.reader",
        "channel": "unknown",
        "net-env": "1",
        "platform": "android",
        "qm-params": "",
        "reg": "0",
    }

    # 获取 headers 的所有键并排序
    keys = sorted(headers.keys())

    # 生成待签名的字符串
    sign_str = ''.join([k + '=' + str(headers[k]) for k in keys]) + sign_key

    # 生成签名
    headers['sign'] = hashlib.md5(sign_str.encode()).hexdigest()

    return headers


def sign_url_params(params):

    keys = sorted(params.keys())

    # 生成待签名的字符串
    sign_str = ''.join([k + '=' + str(params[k]) for k in keys]) + sign_key

    # 使用MD5哈希生成签名
    signature = hashlib.md5(sign_str.encode()).hexdigest()

    # 将签名添加到参数字典中
    params['sign'] = signature

    return params

def get_book_list(id):
    #old
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    #     'cookie':'acw_tc=1a0c380d17293326944078983e00f31fb03eeeae8bb23df7722825188305c3; acw_sc__v2=671385d6f25d1066ad65805bff4e5dc99d6bf954'
    # }
    # session = requests.Session()
    # response = session.get(f'https://www.qimao.com/api/book/chapter-list?book_id={id}',headers=header)
    # try:
    #     if response.status_code == 200:
    #         # print("response",response.text)
    #         data = response.json()
            
    #         if 'data' in data and 'chapters' in data['data']:
    #             list = data['data']['chapters']
    #             list_data = [{'id': chapter['id'], 'title': chapter['title']} for chapter in list]
    #             return list_data
    #         elif 'errors' in data:
    #             list=[]
    #             return list
    #         else:
    #             print("Unexpected response format")
    #             # Handle unexpected format
    #             return None
    #     else:
    #         print("Failed to fetch data，please try again")
    #         return None
    # except Exception as e:
    #     # print(response.text)
    #     print("Error:", e)
    params = {
        "id": id,
        #"chapterId": chapter_id,
    }
    response = requests.get("https://api-ks.wtzw.com/api/v1/chapter/chapter-list",
                            params=sign_url_params(params),
                            headers=get_headers(id),
                            #proxies=proxies,
                            timeout=12)
    try:
        if response.status_code == 200:
            # print("response",response.text)
            data = response.json()
            #print("response",data)
            
            if 'data' in data and 'chapter_lists' in data['data']:
                list = data['data']['chapter_lists']
                list_data = [{'id': chapter['id'], 'title': chapter['title']} for chapter in list]
                #print("list_data",list_data)
                return list_data
            elif 'errors' in data:
                list=[]
                return list
            else:
                print("Unexpected response format")
                # Handle unexpected format
                return None
        else:
            print("Failed to fetch data，please try again")
            return None
    except Exception as e:
        # print(response.text)
        print("Error:", e)
    
    
        
def md5(data):
    return hashlib.md5(data.encode()).hexdigest()


def utf8_encode(string):
    return string.encode('utf-8')

def add_params_and_sign(params, sign_key):
    sorted_params = sorted(params.items())
    sign_string = "".join(f"{key}={value}" for key, value in sorted_params)
    return md5(sign_string + sign_key)


def decode(api_response):
    content = api_response['data']['content']
    # 解码Base64，这里假设内容已经是Base64字符串
    data = base64.b64decode(content)
    # print(data)
    # 提取IV和加密数据
    iv = data[:16]  # 假设IV为前16字节
    encrypted_data = data[16:]
    # 解密数据
    decrypted_content = decrypt(encrypted_data, iv)
    # 将解密后的内容中的 '<br>' 替换为 '\n'
    # decrypted_content.replace('\n', '\n\n')
    context=decrypted_content.replace('\n', '\n\n')
    # print("decode 中的context",context)
    return context.replace('<br>', '\n')

def decrypt(encrypted_data, iv):
    key_hex = '32343263636238323330643730396531'
    key = bytes.fromhex(key_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    try:
        # 尝试解码为UTF-8文本
        return decrypted.decode('utf-8')
    except UnicodeDecodeError:
        # 如果不是有效的UTF-8数据，则返回原始字节数据（适用于非文本内容）
        return decrypted


# def fetch_chapter_content(params, headers, sign_key, url):
#     params['sign'] = add_params_and_sign(params, sign_key)
#     headers['sign'] = add_params_and_sign(headers, sign_key)
#     response = requests.get(url, params=params, headers=headers)
#     if response.status_code == 200:
#         # data = response.json()
#         return response.json()
#     else:
#         print("fetch报错")
#         return None


def fetch_chapter_content(params, headers, sign_key, url):
    retry_attempts = 5
    for attempt in range(retry_attempts):
        params['sign'] = add_params_and_sign(params, sign_key)
        headers['sign'] = add_params_and_sign(headers, sign_key)
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Attempt {attempt + 1}: Failed to fetch data, retrying...")
            time.sleep(0.5)  # Wait for 0.5 seconds before retrying
    print("Failed after 5 retries")
    return None
        


# def fetch_and_save_chapter_content(book_id, chapter, headers, sign_key, api_url, output_file):
#     with open(output_file, 'a', encoding='utf-8') as file:  # 使用追加模式打开文件
        
#             headers = {
#                 "app-version": "51110",
#                 "platform": "android",
#                 "reg": "0",
#                 "AUTHORIZATION": "",
#                 "application-id": "com.****.reader",
#                 "net-env": "1",
#                 "channel": "unknown",
#                 "qm-params": "",
#             }
#             params = {
#                 "id": book_id,
#                 "chapterId": chapter['id']
#             }
#             try:
#                 response_data = fetch_chapter_content(params, headers, sign_key, api_url)
#                 findata = decode(response_data)
#                 # print(findata)
#                 file.write(chapter['title']+"\n\n")
#                 file.write(findata + "\n\n\n\n")  # 追加读取的数据并在每章后添加两个换行
#             except Exception as e:
#                 print(f"Error fetching or writing chapter {chapter['id']}: {e}")


def worker(book_id, headers, sign_key, api_url, results, q, pbar):
    while not q.empty():
        chapter_index, chapter = q.get()
        headers = {                                #莫名其妙有上面传的就会报错
                "app-version": "51110", 
                "platform": "android",
                "reg": "0",
                "AUTHORIZATION": "",
                "application-id": "com.****.reader",
                "net-env": "1",
                "channel": "unknown",
                "qm-params": "",
            }
        params = {
                "id": book_id,
                "chapterId": chapter['id']
            }
        try:
            
            chapter_content = fetch_chapter_content(params, headers, sign_key, api_url)
            if chapter_content is not None:
                chapter_data = decode(chapter_content)
                results[chapter_index] = (chapter['title'], chapter_data)
            # chapter_data = decode(chapter_content)
            # # 存储结果，使用章节索引确保顺序
            # results[chapter_index] = (chapter['title'], chapter_data)
            # q.task_done()  # 标记任务完成
        except Exception as e:
            print(f"Error fetching or writing chapter {chapter['id']}: {e}")
            results[chapter_index] = (chapter['title'], "Failed to download this chapter.")
        finally:
            q.task_done()  # 标记任务完成
            pbar.update(1)  # 安全更新进度条

def qimaodownloadmain(book_id, headers, sign_key, api_url, output_file, chapters):
    # 创建队列并加入任务
    chapter_queue = queue.Queue()
    for index, chapter in enumerate(chapters):
        chapter_queue.put((index, chapter))

    # 结果列表初始化为None，长度与章节数相同
    results = [None] * len(chapters)

    # 创建线程列表
    threads = []
    num_threads = 5  # 定义线程数

    pbar = tqdm(total=len(chapters), desc="下载章节")

    # 启动线程
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(book_id, headers, sign_key, api_url, results, chapter_queue, pbar))
        thread.start()
        threads.append(thread)

    # 等待所有任务完成
    chapter_queue.join()

    # 等待所有线程结束
    for thread in threads:
        thread.join()

    pbar.close()  # 关闭进度条

    # 所有章节下载完成后，统一写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for title, content in results:
            file.write(title + "\n\n" + content + "\n\n\n\n")

    print("所有章节下载并保存完成！")





# Asking user for input
# chapter_id = input("Enter the chapter ID: ")
headers = {
    "app-version": "51110",
    "platform": "android",
    "reg": "0",
    "AUTHORIZATION": "",
    "application-id": "com.****.reader",
    "net-env": "1",
    "channel": "unknown",
    "qm-params": "",
    'cookie':'acw_tc=1a0c39d217277476440312099e014bae6d3c86d827374186a868661b863abd; acw_sc__v2=66fb563c08cadcacd6f78280eee34924ab0c5c4b'
}

sign_key = 'd3dGiJc651gSQ8w1'
api_url = "https://api-ks.wtzw.com/api/v1/chapter/content"

# fetch_and_save_chapters_multithreaded(book_id, list_data, headers, sign_key, api_url, output_file)
if __name__ == '__main__':
    book_id = input("Enter the book ID: ")
    list_data=get_book_list(book_id)
    book_name=get_book_name(book_id,headers)
    print(book_name)
    output_file = f"E:/爬虫/{book_name}.txt" 
    qimaodownloadmain(book_id, headers, sign_key, api_url, output_file, list_data)
# for chapter in tqdm(list_data, desc="下载章节"):
#     fetch_and_save_chapter_content(book_id, chapter, headers, sign_key, api_url, output_file)

# for chapter in list_data:
    # headers = {
    #     "app-version": "51110",
    #     "platform": "android",
    #     "reg": "0",
    #     "AUTHORIZATION": "",
    #     "application-id": "com.****.reader",
    #     "net-env": "1",
    #     "channel": "unknown",
    #     "qm-params": "",
    # }
    # params = {
    #             "id": book_id,
    #             "chapterId": chapter['id']
    #         }
    # response_data = fetch_chapter_content(params, headers, sign_key, api_url)
    # print(response_data)
    # findata=decode(response_data)
    # print(findata)



