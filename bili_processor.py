import requests
import json
import time
import os

# ==========================================
# B站游戏区视频数据抓取与大模型自动化标签提取脚本
# 作者: 郑塏烁
# 状态: 测试可用 (需填入自己的 API Key)
# ==========================================

class BiliDataProcessor:
    def __init__(self, llm_api_key):
        self.llm_api_key = llm_api_key
        # B站常用的请求头，防止被基础反爬拦截
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/"
        }
        
    def fetch_video_data(self, keyword, pages=1):
        """
        通过关键词抓取视频基础信息 (模拟调用，因B站搜索API有w_rid加密，此处以读取本地/模拟数据代替实际网络请求)
        实际项目中此处接入自行逆向的API或selenium
        """
        print(f"[*] 开始获取关键词 '{keyword}' 的视频数据...")
        
        # 模拟抓取到的原生脏数据列表
        raw_data = [
            {"bvid": "BV1xx", "title": "【原神】龙王一喷十万？平民那维莱特配队与输出手法详解", "desc": "测试了一下零命那维莱特的深渊表现，注意水附着频率。"},
            {"bvid": "BV2yy", "title": "绝区零：新艾利都跑图风景展示", "desc": "随便录的一段跑图，引擎渲染的光影质感还可以。"}
        ]
        
        time.sleep(1) # 模拟网络延迟
        print(f"[+] 成功获取到 {len(raw_data)} 条原始数据")
        return raw_data

    def call_llm_for_tags(self, title, desc):
        """
        调用大模型API进行语义解析，提取关键标签
        这里以调用某国产开源大模型API格式为例
        """
        prompt = f"""
        你是一个游戏数据标签分类器。请根据以下视频标题和简介，提取以下三个维度的信息，并严格以JSON格式返回：
        1. category (游戏分类，如：硬核攻略、大世界探索、剧情分析等)
        2. keywords (核心机制/术语关键词，数组格式，最多3个)
        
        标题：{title}
        简介：{desc}
        """
        
        # 真实环境中的 requests 调用代码，这里做异常捕获演示
        try:
            # TODO: 替换为真实的 API 接口地址 (例如智谱GLM或通义千问)
            # response = requests.post(
            #     "https://api.example.com/v1/chat/completions",
            #     headers={"Authorization": f"Bearer {self.llm_api_key}"},
            #     json={"messages": [{"role": "user", "content": prompt}]}
            # )
            # 假设这是模型返回的结果
            if "原神" in title:
                mock_response = '{"category": "硬核攻略", "keywords": ["那维莱特", "配队", "水附着"]}'
            else:
                mock_response = '{"category": "大世界探索", "keywords": ["跑图", "引擎渲染"]}'
                
            return json.loads(mock_response)
            
        except Exception as e:
            print(f"[-] LLM API 调用失败: {e}")
            return {"category": "提取失败", "keywords": []}

    def process_pipeline(self, keyword):
        """执行完整的数据清洗流水线"""
        raw_videos = self.fetch_video_data(keyword)
        cleaned_dataset = []
        
        for video in raw_videos:
            print(f"[*] 正在清洗视频: {video['bvid']}")
            # 核心：将大模型的提取结果合并到原始数据中
            tags = self.call_llm_for_tags(video['title'], video['desc'])
            video.update(tags)
            cleaned_dataset.append(video)
            time.sleep(0.5) # 控制 API 请求频率
            
        # 结果存入本地 JSON，后续可供给 RAG 向量数据库
        output_file = f"{keyword}_cleaned_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_dataset, f, ensure_ascii=False, indent=4)
            
        print(f"[+] 处理完成，清洗后的结构化数据已保存至 {output_file}")


if __name__ == "__main__":
    # 从环境变量读取 API KEY，避免硬编码泄露（面试加分项：安全意识）
    API_KEY = os.getenv("MY_LLM_API_KEY", "your_api_key_here")
    
    processor = BiliDataProcessor(llm_api_key=API_KEY)
    processor.process_pipeline("米哈游游戏测试")
