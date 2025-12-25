import os
import requests
from dotenv import load_dotenv

# 設定読み込み
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: API Key not found in .env")
    exit()

# モデルリスト取得（REST API直叩き）
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print("=== 📡 Radar Sweep: Scanning Available Models ===")
try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Connection: OK ({response.status_code})")
        print("Available Models for this Key:")
        print("-" * 40)
        
        found_any = False
        if 'models' in data:
            for m in data['models']:
                # "generateContent"（文章生成）に対応しているものだけ表示
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    print(f"✅ {m['name']}")
                    found_any = True
        
        if not found_any:
            print("❌ No text-generation models found.")
            print("Raw Data:", data)
    else:
        print(f"❌ Connection Failed: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Critical Error: {e}")

print("-" * 40)