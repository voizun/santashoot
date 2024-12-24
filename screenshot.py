import os
import signal
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

# スクリーンショット撮影カウンター
screenshot_count = 0
max_screenshots = 10  # 最大360枚撮影


def capture_screenshot(signum, frame):
    global screenshot_count

    # 撮影が完了した場合、ドライバーを終了して終了
    if screenshot_count >= max_screenshots:
        print("Screenshot capture complete.")
        driver.quit()
        exit(0)

    # スクリーンショットを保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"santa_{screenshot_count:04d}.png")
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")

    # カウンターを増加
    screenshot_count += 1


if __name__ == "__main__":
    # 最初にURLを1回開く
    driver.get(url)
    print("Waiting for completely loading the page...")
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located)
    print("Page loaded successfully.")
    
    # 00分まで待機
    now = datetime.now()
    seconds_to_wait = (60 - now.minute) * 60 - now.second
    print(f"Waiting {seconds_to_wait} seconds until 00:00...")
    time.sleep(seconds_to_wait)

    # タイマー設定: 初回遅延なし、10秒間隔で実行
    signal.signal(signal.SIGALRM, capture_screenshot)
    signal.setitimer(signal.ITIMER_REAL, 0, 10)  # 10秒間隔で実行

    # メインスレッドを待機させる
    while True:
        time.sleep(60)
