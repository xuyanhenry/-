import requests
import json
import re
import os
from parsel import Selector
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
# from lxml import etree
from tqdm import tqdm
import time
import logging

# 配置日志记录
logging.basicConfig(filename='error.txt', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

id = 7357767624615331386
flag=0

dic_data = {
    "58344": "D","58345": "在","58346": "主","58347": "特","58348": "家","58349": "军",
    "58350": "然","58351": "表","58352": "场","58353": "4","58354": "要","58355": "只",
    "58356": "v","58357": "和","58358": "?","58359": "6","58360": "别","58361": "还",
    "58362": "g","58363": "现","58364": "儿","58365": "岁","58366": "?","58367": "?",
    "58368": "此","58369": "象","58370": "月", "58371": "3","58372": "出","58373": "战",
    "58374": "工","58375": "相","58376": "o","58377": "男","58378": "直","58379": "失",
    "58380": "世","58381": "F","58382": "都","58383": "平","58384": "文","58385": "什",
    "58386": "V","58387": "O","58388": "将","58389": "真","58390": "工","58391": "那",
    "58392": "当","58393": "?","58394": "会","58395": "立","58396": "些","58397": "u",
    "58398": "是","58399": "十","58400": "张","58401": "学","58402": "气","58403": "大",
    "58404": "爱","58405": "两","58406": "命","58407": "全","58408": "后","58409": "东",
    "58410": "性","58411": "通","58412": "被","58413": "1","58414": "它","58415": "乐",
    "58416": "接","58417": "而","58418": "感","58419": "车","58420": "山","58421": "公",
    "58422": "了","58423": "常","58424": "以","58425": "何","58426": "可","58427": "话",
    "58428": "先","58429": "p","58430": "i","58431": "叫","58432": "轻","58433": "M",
    "58434": "士","58435": "w","58436": "着","58437": "变","58438": "尔","58439": "快",
    "58440": "l","58441": "个","58442": "说","58443": "少","58444": "色","58445": "里",
    "58446": "安","58447": "花","58448": "远","58449": "7","58450": "难","58451": "师",
    "58452": "放","58453": "t","58454": "报","58455": "认","58456": "面","58457": "道",
    "58458": "S","58459": "?","58460": "克","58461": "地","58462": "度","58463": "I",
    "58464": "好","58465": "机","58466": "U","58467": "民","58468": "写","58469": "把",
    "58470": "万","58471": "同","58472": "水","58473": "新","58474": "没","58475": "书",
    "58476": "电","58477": "吃","58478": "像","58479": "斯","58480": "5","58481": "为",
    "58482": "y","58483": "白","58484": "几","58485": "日","58486": "教","58487": "看",
    "58488": "但","58489": "第","58490": "加","58491": "候","58492": "作","58493": "上",
    "58494": "拉","58495": "住","58496": "有","58497": "法","58498": "r","58499": "事",
    "58500": "应","58501": "位","58502": "利","58503": "你","58504": "声","58505": "身",
    "58506": "国","58507": "问","58508": "马","58509": "女","58510": "他","58511": "Y",
    "58512": "比","58513": "父","58514": "x","58515": "A","58516": "H","58517": "N",
    "58518": "s","58519": "X","58520": "边","58521": "美","58522": "对","58523": "所",
    "58524": "金","58525": "活","58526": "回","58527": "意","58528": "到","58529": "z",
    "58530": "从","58531": "j","58532": "知","58533": "又","58534": "内","58535": "因",
    "58536": "点","58537": "Q","58538": "三","58539": "定","58540": "8","58541": "R",
    "58542": "b","58543": "正","58544": "或","58545": "夫","58546": "向","58547": "德",
    "58548": "听","58549": "更","58550": "?","58551": "得","58552": "告","58553": "并",
    "58554": "本","58555": "q","58556": "过","58557": "记","58558": "L","58559": "让" ,
    "58560": "打","58561": "f","58562": "人","58563": "就","58564": "者","58565": "去",
    "58566": "原" ,"58567": "满","58568": "体","58569": "做","58570": "经","58571": "K",
    "58572": "走","58573": "如" ,"58574": "孩","58575": "c","58576": "G","58577": "给",
    "58578": "使","58579": "物","58580": "?","58581": "最","58582": "笑","58583": "部",
    "58584": "?","58585": "员","58586": "等","58587": "受","58588": "k","58589": "行",
    "58590": "一","58591": "条","58592": "果","58593": "动","58594": "光","58595": "门",
    "58596": "头","58597": "见", "58598": "往","58599": "自","58600": "解","58601": "成",
    "58602": "处","58603": "天","58604": "能","58605": "于","58606": "名","58607": "其",
    "58608": "发","58609": "总","58610": "母","58611": "的","58612": "死","58613": "手",
    "58614": "入","58615": "路","58616": "进","58617": "心","58618": "来","58619": "h",
    "58620": "时","58621": "力","58622": "多","58623": "开","58624": "已","58625": "许",
    "58626": "d","58627": "至","58628": "由","58629": "很","58630": "界","58631": "n",
    "58632": "小","58633": "与","58634": "Z","58635": "想","58636": "代","58637": "么",
    "58638": "分","58639": "生","58640": "口","58641": "再","58642": "妈","58643": "望",
    "58644": "次","58645": "西","58646": "风","58647": "种","58648": "带","58649": "J",
    "58650": "?","58651": "实","58652": "情","58653": "才","58654": "这","58655": "?",
    "58656": "E","58657": "我","58658": "神","58659": "格","58660": "长","58661": "觉",
    "58662": "间","58663": "年","58664": "眼","58665": "无","58666": "不","58667": "亲",
    "58668": "关","58669": "结","58670": "0", "58671": "友","58672": "信","58673": "下",
    "58674": "却","58675": "重","58676": "己","58677": "老","58678": "2","58679": "音",
    "58680": "字","58681": "m","58682": "呢","58683": "明", "58684": "之","58685": "前",
    "58686": "高","58687": "P","58688": "B","58689": "目","58690": "太","58691": "e",
    "58692": "9","58693": "起","58694": "稜","58695": "她","58696": "也","58697": "W",
    "58698": "用","58699": "方","58700": "子","58701": "英","58702": "每","58703": "理",
    "58704": "便","58705": "四","58706": "数","58707": "期","58708": "中","58709": "C",
    "58710": "外","58711": "样","58712": "a","58713": "海","58714": "们","58715": "任"
}


def get_text_from_xpath(book_id, css):
    url = f"https://fanqienovel.com/page/{book_id}"
    response = requests.get(url)
    if response.status_code == 200:
        selector = Selector(response.text)
        elements = selector.css(css).get()         #书名
        if elements:
            print("elements",elements)
            return elements
    return None


def change_testid(oldid):
    testid_list=[7281289297792074302,7283085298735514175,7287418859806540350,7309126386378080830,7318806175602967102,7081540607377673253,7081540642454637575,
                 6603267294128767501,6603267294393008648,6603267295189926414,6840273276552348168,6845672413309436430,7141323055267217957,7146910344860926464]
    try:
        # 查找oldid在列表中的位置
        index = testid_list.index(oldid)
        
        # 返回列表中下一个数字，如果存在
        if index < len(testid_list) - 1:
            return testid_list[index + 1]
        else:
            # print("在列表最后")
            return testid_list[0]
    
    except ValueError:
        # print("不在列表")
        return testid_list[0]



def change_userid():
    global id
    testid = 7281289297792074302
    useid=id
    time_out=1
    while True:
        test_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
            'sec-ch-ua':'"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'cookie' : f'novel_web_id={useid}'
        }
        
        try:
            # # 发送请求并处理数据
            # res = requests.get(f'https://fanqienovel.com/api/reader/full?itemId={testid}', headers=test_headers)
            # data = json.loads(res.text)['data']
            # # print("data",data)
            # if data=={}:
            #     testid=change_testid(testid)
            #     print("改变testid",testid)
            #     continue
            # content = data['chapterData']['content']
            # print(content)
            res = requests.get(f'https://fanqienovel.com/reader/{testid}', headers=test_headers)
            html_content = res.content
            soup = BeautifulSoup(html_content, 'html.parser')
            div_content = soup.find('div', class_='muye-reader-content noselect')
            # if div_content:
            #     print(div_content.text)  # 提取div中的文本内容
            # else:
            #     print("未找到指定的div元素")
            html_text = str(soup)

            # 定义需要查找的两段字符
            string1 = "扫码下载APP免费读，SVIP网页畅读"
            string2 = "扫码下载「番茄小说APP」可免费阅读全本小说，购买SVIP还可享受网页畅读权益"
            if not string1 in html_text and not string2 in html_text:
                print("成功的id", useid)
                id=useid
                return

            # if len(div_content.text) > 1000:
            #     print("成功的id", useid)
            #     id=useid
            #     return
        except Exception as e:
            print(f"请求失败，ID={useid}, 次数：{time_out},错误: {e}")
            # logging.error("change_userid发生错误: %s", str(e))

            time.sleep(1)  # 等待1秒再重试
            time_out=time_out+1
            if time_out>5:
                useid += 1
                time_out=0

            continue

        useid += 1
        

def get_context_from_fanqie(item_id,retries=5):
    global id,flag

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'sec-ch-ua':'"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cookie':f'novel_web_id={id}'
    }
    try:
        # 发送请求并处理数据
        while True:
            if flag==1:
                time.sleep(1)
                continue
            res = requests.get(f'https://fanqienovel.com/reader/{item_id}', headers=headers)

            if res.status_code == 200:
                # return res.content  # 返回成功的响应内容
                html_content = res.content
                soup = BeautifulSoup(html_content, 'html.parser')
                div_content = soup.find('div', class_='muye-reader-content noselect')
                if div_content is None:
                    print("未找到指定的 div 元素")
                    print(res.text)
                    print("网页逻辑变化，请汇报错误，谢谢")
                    input("按任意键退出...")
                    exit()
                if div_content.text=="" and retries>0:
                    retries=retries-1
                    time.sleep(1)
                    print("重试")
                    continue
                if retries<=0:
                    id+=1
                    if flag==1:
                        retries+=1
                        continue
                    print("切换id")
                    logging.error("改变id: %s", str(res.text))
                    flag=1
                    change_userid()
                    flag=0
                    retries=5
                    continue
                # if div_content:
                #     print(div_content.text)  # 提取div中的文本内容
                # if len(div_content.text)>120 and len(div_content.text)<1000 :
                #     print("切换id")
                #     change_userid()
                #     continue
                # if len(div_content.text)>1000 or len(div_content.text)<120:
                #     break
                html_text = str(soup)

                # 定义需要查找的两段字符
                string1 = "扫码下载APP免费读，SVIP网页畅读"
                string2 = "扫码下载「番茄小说APP」可免费阅读全本小说，购买SVIP还可享受网页畅读权益"
                if string1 in html_text and string2 in html_text:
                    print("切换id")
                    logging.error("改变id: %s", str(res.text))
                    change_userid()
                    continue
                else:
                    break

            else:
                print("http状况",res.status_code)
                
                print("http请求错误，重试")
                if(res.status_code==444):
                    print(res.text)
                    time.sleep(2)
                continue


        #     response = requests.get(f'https://fanqienovel.com/api/reader/full?itemId={item_id}', headers=headers)
        #     # print("response",response.text)
        #     if response.text=="" and retries>0:
        #         retries=retries-1
        #         time.sleep(1)
        #         print("重试")
        #         continue
        #     if retries<=0:
        #         id+=1
        #         if flag==1:
        #             retries+=1
        #             continue
        #         print("切换id")
        #         flag=1
        #         change_userid()
        #         flag=0
        #         retries=5
        #         continue
        #     data = json.loads(response.text)['data']
        #     if 'chapterData' in data:
        #         break
        #     elif retries>0:
        #         retries=retries-1
        #         time.sleep(1)

        #         # return get_context_from_fanqie(item_id,retries)

        # content = data['chapterData']['content']
        # # print("content",content)
        # content = div_content.text
        if div_content:
            # 遍历所有元素，保留<p>标签并提取文本
            for tag in div_content.find_all(True):  # 查找所有标签
                if tag.name != 'p':  # 如果不是<p>标签
                    tag.unwrap()  # 移除标签，仅保留标签内的内容

            # 输出处理后的HTML，保留<p>标签和文本
            content = str(div_content)
            # print(content)
        return content



    except Exception as e:
        try:
            response_content = json.loads(res.text)
        except (ValueError, AttributeError) as json_error:
            response_content = "无法解析JSON或response为空"
        logging.error("get_context_from_fanqie发生错误: %s, 响应内容: %s", str(e), response_content)
        # logging.error("get_context_from_fanqie发生错误: %s,%s", str(e),json.loads(response.text))
        print(f"请求失败，错误: {e}",json.loads(res.text))
        return "无法解析"



def remove_p_tags(content):
    content=content.replace('\r', '')
    content = re.sub(r'^(.*?)<p', '<p', content, flags=re.DOTALL)
    content = re.sub(r'<p[^>]*>', '<p>', content)
    content = re.sub(r'<p>', '', content)
    content = re.sub(r'</p>', '\n', content)
    content = re.sub(r'<[^>]+>', '', content)
    return content

def fetch_content(item):
    item_id = item['ID']
    chapter_name = item['title']
    retry_count = 0
    max_retries = 2

    # while retry_count <= max_retries:
    content = get_context_from_fanqie(item_id)
    # content = get_content_from_fanqienovel(item_id)
    # if content == "无法解析":
    #     content = get_content_from_dushuge(book_name, chapter_name)
    
    if content != "无法解析":
        content = remove_p_tags(content)
        processed_content = f"{chapter_name}\n\n"
        for index in content:
            try:
                word = dic_data[str(ord(index))]
                processed_content += word
            except KeyError:
                processed_content += index
        processed_content += '\n\n'
        return item, processed_content
    else:
        # retry_count += 1
        # if retry_count > max_retries:
            # id+=1
            # change_userid()
            # retry_count=0
            return item, f"Failed to fetch content for {chapter_name} after {max_retries + 1} attempts.\n"

def download_novels(item_id_list, book_name, output_file):
    total_chapters = len(item_id_list)
    with open(output_file, 'w', encoding='utf-8') as file, tqdm(total=total_chapters, desc="Progress", unit="chapter") as pbar:
        all_contents = []
        with ThreadPoolExecutor(max_workers=2) as executor:                             #可以更改线程数
            futures = {executor.submit(fetch_content, item): item for item in item_id_list}
            for future in as_completed(futures):
                item, chapter_content = future.result()
                index = item_id_list.index(item)
                all_contents.append((index, chapter_content))
                pbar.update(1)
                
                if len(all_contents) >= 20:                                        # 每20章保存一次
                    all_contents.sort(key=lambda x: x[0])
                    for _, content in all_contents:
                        file.write(content)
                    all_contents.clear()

        # 保存剩余内容
        if all_contents:
            all_contents.sort(key=lambda x: x[0])
            for _, content in all_contents:
                file.write(content)

def get_chapter_list(book_id):
    url = f"https://fanqienovel.com/api/reader/directory/detail?bookId={book_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        chapter_list_with_volume = data.get('data', {}).get('chapterListWithVolume', [])
        
        item_id_list = []
        for volume in chapter_list_with_volume:
            for chapter in volume:
                item_id = chapter.get('itemId')
                title = chapter.get('title')
                if item_id and title:
                    item_id_list.append({"ID": item_id, "title": title})
        
        return item_id_list
    else:
        print("Failed to fetch data，please try again")
        return None
    

    



if __name__ == '__main__':
    # Main execution
    while True:
        change_userid()
        book_id = input("Please enter the book ID: ")
        css = '.page-header-info .info-name h1::text'
        item_id_list = get_chapter_list(book_id)
        text_content = get_text_from_xpath(book_id, css)
        if text_content:
            book_name = text_content.strip()
            print("book name:",book_name)
        else:
            book_name = "Unknown_Book"
        # 获取当前脚本的目录
        # current_directory = os.path.dirname(os.path.abspath(__file__))
        # output_file = os.path.join(current_directory, f"{book_name}.txt")
        output_file = f"E:/爬虫/{book_name}.txt"                        #要改

        download_novels(item_id_list, book_name, output_file)
        print(f"All chapters saved to {output_file}")