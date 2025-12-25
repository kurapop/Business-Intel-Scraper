import os
import time
import json # 追加: JSONデータを扱うため
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

# --- 設定読み込み ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("【Error】APIキーが見つかりません。.envを確認してください。")
    exit()

# ★ライブラリを使わず、直接URLを指定する
# ここを変えれば将来どんなモデルでも使える
MODEL_NAME = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

def search_web(keyword, max_results=3):
    """DuckDuckGoで検索"""
    print(f"🔍 Searching for: {keyword} (Region: JP)...")
    results = []
    try:
        ddgs = DDGS()
        # 検索実行
        search_results = ddgs.text(keyword, region='jp-jp', max_results=max_results)
        
        if search_results:
            for res in search_results:
                results.append({"title": res['title'], "url": res['href']})
    except Exception as e:
        print(f"Search Warning: {e}")

    # エラー時のデモデータ
    if not results:
        print("⚠️ Search returned 0 results or Error. Switching to [Demo Mode].")
        results = [
            {
                "title": "【Demo】生成AI (Wikipedia)",
                "url": "https://ja.wikipedia.org/wiki/%E7%94%9F%E6%88%90%E7%9A%84%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD"
            }
        ]
    return results

def scrape_content(url):
    print(f"🌐 Scraping: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding 
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = " ".join([p.text for p in soup.find_all('p')])
            return text[:4000] 
        else:
            print(f"Failed to access: {response.status_code}")
            return None
    except Exception as e:
        print(f"Scrape Error: {e}")
        return None

def analyze_with_gemini(text):
    """ライブラリを使わず直接APIを叩く"""
    print(f"🤖 Analyzing with {MODEL_NAME} (Direct REST API)...")
    
    # プロンプトの作成
    prompt_text = f"""
    以下のテキストはWeb記事の内容です。
    ビジネスマン向けに、以下の3点を日本語で簡潔にまとめてください。
    
    1. 記事の要約（3行以内）
    2. 重要なポイント
    3. 今後の展望や課題

    --- テキスト ---
    {text}
    """

    # 通信データ（JSON）の作成
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    headers = {'Content-Type': 'application/json'}

    try:
        # 直接POST送信
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # 結果の解析
        if response.status_code == 200:
            result = response.json()
            # 階層深い場所にあるテキストを取り出す
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"API Error Code: {response.status_code}")
            print(f"Error Message: {response.text}")
            return None

    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def main():
    target_keyword = "生成AI 活用事例 日本企業 2025"
    
    print(f"=== Mission Start: Business Intel Scraper (Direct Mode) ===")
    
    # 1. 検索
    articles = search_web(target_keyword, max_results=2)
    
    # 2. 分析
    final_report = f"# AI Report: {target_keyword}\nModel: {MODEL_NAME}\n\n"
    
    for i, article in enumerate(articles):
        print(f"\n--- Processing {i+1}/{len(articles)}: {article['title']} ---")
        
        content = scrape_content(article['url'])
        
        if content and len(content) > 50:
            analysis = analyze_with_gemini(content)
            
            if analysis:
                report_section = f"## {i+1}. {article['title']}\n**URL:** {article['url']}\n\n{analysis}\n\n---\n"
                final_report += report_section
                print("✅ Analysis Complete.")
            else:
                print("⚠️ AI Analysis Failed.")
        else:
            print("❌ Content too short or scraped failed.")
        
        time.sleep(1)

    # 3. 保存
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print("\n=== Mission Complete! Check 'report.md' ===")

if __name__ == "__main__":
    main()