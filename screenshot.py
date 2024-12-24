import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pillow_avif

# スクリーンショット保存先フォルダ
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

# Chromeドライバーの設定
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=ja-JP")
options.add_argument("--window-size=3840,2160")
options.add_argument("TZ=Asia/Tokyo")

# ドライバーの起動
driver = webdriver.Chrome(options=options)

# GoogleサンタページのURL
url = "https://santatracker.google.com/"

# 360回のループ (30秒ごと、約3時間)
for i in range(5):
    # 現在時刻を取得し次の30秒まで待機
    now = datetime.now()
    seconds_to_wait = 30 - (now.second % 30)
    time.sleep(seconds_to_wait)

    # ページを開く
    driver.get(url)
    time.sleep(3)

    # スクリーンショットをPNG形式で保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = os.path.join(output_dir, f"santa_{timestamp}.png")
    driver.save_screenshot(png_path)
    print(f"PNG Screenshot saved: {png_path}")

    # PNGをAVIFに変換して保存
    avif_path = os.path.join(output_dir, f"santa_{timestamp}.avif")
    with Image.open(png_path) as img:
        img.save(avif_path, format="AVIF")
    print(f"AVIF Screenshot saved: {avif_path}")

    # 変換後にPNGを削除
    os.remove(png_path)
    print(f"Deleted PNG file: {png_path}")

# ドライバーを終了
driver.quit()
