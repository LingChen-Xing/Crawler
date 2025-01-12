import requests
from lxml import etree
import os
from tkinter import simpledialog
import tkinter as tk
import time
import webbrowser

# 爬虫函数
def crawler(url, name, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    try:
        resp = requests.get(url=url, headers=headers, timeout=10)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        html_doc = resp.text
        html = etree.HTML(html_doc)

        with open("url_list.txt", "a+", encoding="utf-8") as f:
            f.write(url+"\n")
        with open("name_list.txt", "a+", encoding="utf-8") as f:
            f.write(name+"\n")
        with open("path_list.txt", "a+", encoding="utf-8") as f:
            f.write(path+"\n")

        extracted_list = html.xpath(path)
        if not extracted_list:
            print(f"未提取到内容，路径可能有误: {path}")
            return []

        file_name = f"{name}.txt"
        # 删除多余换行符并确保保留两个换行符
        clean_content = []
        for item in extracted_list:
            item = item.strip()  # 去掉前后空白和换行
            if item:  # 确保非空
                clean_content.append(item)
        clean_content = "\n".join(clean_content) + "\n"  # 每行加入一个换行符，并确保文件以两个换行结尾
        with open(file_name, "w+", encoding="utf-8") as f:
            f.write(f"开始爬行的 URL: {url}\n----------\n\n")
            f.write(clean_content)
        print(f"爬取完成，结果已保存到 {file_name}")
        return extracted_list

    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
        return []

def crawler_new(url, name, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    try:
        resp = requests.get(url=url, headers=headers, timeout=10)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        html_doc = resp.text
        html = etree.HTML(html_doc)

        extracted_list = html.xpath(path)
        if not extracted_list:
            print(f"未提取到内容，路径可能有误: {path}")
            return []

        clean_content = []
        for item in extracted_list:
            item = item.strip()  # 去掉前后空白和换行
            if item:  # 确保非空
                clean_content.append(item)
        return clean_content

    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
        return []

def inspect(file_name, content):
    """
    检查内容是否存在于文件中。
    返回:
        bool: True 表示写入了新内容，False 表示内容已存在。
    """
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"{content}\n")
        return True

    with open(file_name, "r", encoding="utf-8") as file:
        existing_contents = file.readlines()
        if content + '\n' in existing_contents:
            return False

    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"{content}\n")
    return True
# 这个检查函数每次只能检查一次


def All_inspect():
    while True:
        j = 1
        k = 0
        new = ""
        with open("url_list.txt", "r", encoding="utf-8") as file:
            url_list= file.read().splitlines()
            print(url_list)
        with open("name_list.txt", "r", encoding="utf-8") as file:
            name_list = file.read().splitlines()
        with open("path_list.txt", "r", encoding="utf-8") as file:
            past_lixt = file.read().splitlines()
        for url,name,path in zip(url_list,name_list,past_lixt):
            k = k+1
            print("现在爬取到了"+name+",url为"+url+"，path为："+path+"第"+str(k)+"个")
            all=""
            extracted_content = crawler_new(url,name,path)
            new_list = []
            lj_list = []
            with open('lj.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    cleaned_content = line.strip()  # 去除每行的前后空白字符
                    lj_list.append(cleaned_content)
            for content in extracted_content:
                cleaned_content = content.strip()
                if cleaned_content and inspect(f"{name}.txt", cleaned_content):  # 检查非空内容
                    new_list.append(f"发现新内容：{cleaned_content}")
                    j = 1
                    for i in lj_list:
                        if(cleaned_content.split("\r\n")[0] == i):
                            print("j = 0")
                            j=0
                            break
                    if(j==1):
                        print("j = 1")
                        all=all+f"{cleaned_content}\n"
                    #问题结束
            if(all!=""):
                new=new+f"{name}----{url}下发现新内容：\n{all}\n\n\n"
            if new_list:
                print(new_list)
            else:
                if(j==1):
                    j=0;
        finally_show_html(new)
        time.sleep(1800)

def crawl_new_url():
    """
    提示用户输入新的 URL、Path 和 Name 并调用 crawler 函数。
    """
    # 弹出输入对话框
    url = simpledialog.askstring("输入 URL", "请输入新的 URL：")
    path = simpledialog.askstring("输入路径", "请输入 XPath 表达式：")
    name = simpledialog.askstring("输入名称", "请输入文件名：")

    if url and path and name:
        print(f"开始爬行 URL: {url}, Path: {path}, Name: {name}")
        extracted_content = crawler(url, name, path)
        if extracted_content:
            print(f"爬行完成，提取到 {len(extracted_content)} 条内容")
            finally_show_html(f"爬行完成，提取到 {len(extracted_content)} 条内容")
        else:
            print("未提取到内容或爬行失败")
            finally_show_html("未提取到内容或爬行失败")

def finally_show_html(content):
    """
    将内容写入 HTML 文件并在浏览器中打开
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crawler</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Crawler_For_Xing_Station</h1>
            <h2>程序将在半小时后再次检查</h2>
            <p>{content.replace('\n', '<br>')}</p>
        </div>
    </body>
    </html>
    """
    file_path = "Crawler.html"

    # 将内容写入 HTML 文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 在浏览器中打开
    webbrowser.open(file_path)

def main():

    with open("li.txt","a+") as f:
        f.write("")
    # 创建主窗口
    root = tk.Tk()
    root.title("爬虫控制面板")

    # 设置窗口大小
    root.geometry("300x150")

    # 添加按钮
    check_button = tk.Button(root, text="检查", command=All_inspect)
    check_button.pack(pady=10)

    crawl_button = tk.Button(root, text="爬行", command=crawl_new_url)
    crawl_button.pack(pady=10)

    # 运行主循环
    root.mainloop()
    pass

if __name__ =="__main__":
    main()