import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def time_span(interval, iterations, callback):
    """
    指定した間隔(interval)で指定回数(iterations)処理を実行する。
    callback: 実行する関数。
    """
    base_time = time.perf_counter()

    for _ in range(iterations):
        now = time.perf_counter()
        elapsed_time = now - base_time
        remainder = elapsed_time % interval

        # コールバック関数を実行
        callback()

        # 次の間隔まで待機
        time.sleep(interval - remainder)

# スクリーンショット保存先フォルダ
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

# Chromeドライバーの設定
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=ja-JP")
options.add_argument("--window-size=1920,1419")
options.add_argument("TZ=Asia/Tokyo")
options.add_experimental_option("prefs", {
        "intl.accept_languages": "ja",  # 言語を日本語に設定
    })
options.add_argument("--lang=ja")

# ドライバーの起動
driver = webdriver.Chrome(options=options)

# GoogleサンタページのURL
url = "https://santatracker.google.com/"
driver.get(url)  # ページを一度だけロード
print("Waiting for completely loading the page...")
time.sleep(20)
print("Page loaded successfully.")

# 00分まで待機
now = datetime.now()
seconds_to_wait = (60 - now.minute) * 60 - now.second
print(f"Waiting {seconds_to_wait} seconds until 00:00...")
time.sleep(seconds_to_wait)

# スクリーンショット撮影のコールバック関数
screenshot_counter = 0  # 撮影した枚数をカウントする
def take_screenshot():
    global screenshot_counter
    filename = os.path.join(output_dir, f"santa_{screenshot_counter:04d}.png")
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")
    screenshot_counter += 1

# 10秒間隔で360枚のスクリーンショットを撮影
time_span(5, 720, take_screenshot)

# ドライバーを終了
driver.quit()
