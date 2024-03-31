import json
import time
import requests
import sys

def main():
    print("欢迎使用九歌诗歌生成器！\n")
    print("如有侵权请删除本软件！\n")
    print("仅供学习使用，请勿用于商业用途！\n")
    while True:
        # 获取用户输入
        user_input = input("请输入诗句或关键词：")
        
        # 第一步：向/getpoem 发送POST请求并获取celery_id
        headers_getpoem = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
        }
        data_getpoem = {
            'inputs': user_input,
            'predict_lower': 'predict_lower'  
        }
        response_getpoem = requests.post('https://jiuge.thunlp.org/getpoem', headers=headers_getpoem, data=data_getpoem)
        response_json = response_getpoem.json()

        if response_getpoem.status_code == 200 and 'celery_id' in response_json:
            celery_id = response_json['celery_id']
            print(f"获取诗歌任务ID成功，任务ID为：{celery_id}")

            # 第二步：使用获取到的celery_id 向/sendpoem 发送POST请求
            for i in range(3, 0, -1):
                print(f"等待{i}秒...")
                time.sleep(1)
            print("开始获取结果...\n")

            url = "https://jiuge.thunlp.org/sendpoem"
            payload={'celery_id': celery_id}
            files=[]
            headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
               'Accept': '*/*',
               'Host': 'jiuge.thunlp.org',
               'Connection': 'keep-alive'
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = json.loads(response.text)

            # 直接输出中文
            try:
                print("对联诗句:")
                for couplet_line in data["couplet"]:
                    print(couplet_line)

                print("\n来源诗句:")
                print(data["source"])

                print("\n状态:")
                print(data["status"])
            except KeyError:
                print("未能成功获取诗歌生成结果，请检查API接口或稍后重试。")

        else:
            print(f"获取诗歌任务ID失败，状态码为：{response_getpoem.status_code}")

        # 等待用户按键，按任意键则重新开始，按下'q'则退出程序
        next_action = input("\n按回车键重新开始，或输入q退出程序：")
        if next_action.lower() == 'q':
            break

if __name__ == "__main__":
    main()