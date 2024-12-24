import asyncio
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import subprocess

# GoogleサンタのURL
URL = "https://santatracker.google.com/"
OUTPUT_DIR = "screenshots"

def setup_driver():
    """Selenium用のChromeDriverをセットアップする"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
   # タイムゾーンを東京に設定
    options.add_experimental_option("prefs", {
        "intl.accept_languages": "ja",  # 言語を日本語に設定
    })
    options.add_argument("--lang=ja")
    options.add_argument("--disable-dev-shm-usage")  # デバッグ環境でのリソース問題を軽減

    # タイムゾーンを東京にするための追加設定
    options.add_argument("--blink-settings=timezone=Asia/Tokyo")
    return webdriver.Chrome(options=options)

async def take_screenshot(driver, output_dir, count):
    """非同期でスクリーンショットを取得する"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, f"screenshot_{count:04d}.png")
    driver.save_screenshot(filename)
    print(f"Saved screenshot {filename}")

def create_video(output_dir):
    # 現在の日時を動画ファイル名に追加
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_name = f"output_{timestamp}.av1"
    """スクリーンショットをAV1動画に変換する"""
    command = [
        "ffmpeg", "-y", "-framerate", "30", "-i",
        os.path.join(output_dir, "screenshot_%04d.png"),
        "-c:v", "libsvtav1", video_name
    ]
    subprocess.run(command)

async def monitor_time(driver, start_time, duration):
    """非同期に時間を監視し、30秒ごとに非同期でスクリーンショットを撮影"""
    count = 0
    end_time = start_time + duration
    while datetime.now() < end_time:
        now = datetime.now()
        # 30秒のタイミングでスクリーンショットを非同期で撮影
        if now.second % 30 == 0 and now.microsecond < 500000:
            asyncio.create_task(take_screenshot(driver, OUTPUT_DIR, count))
            count += 1
            # 次の撮影タイミングまで待機
            await asyncio.sleep(30 - now.second % 30)
        await asyncio.sleep(0.5)  # 500ミリ秒ごとに監視

async def main():
    # 開始時刻を設定（次の00分から開始）
    now = datetime.now()
    start_time = now.replace(second=0, microsecond=0)
    if now.second != 15:
        start_time += timedelta(minutes=1)
    
    # 撮影時間（3時間）
    duration = timedelta(minutes=3)

    driver = setup_driver()
  
    # 開始時刻まで待機
    wait_time = (start_time - datetime.now()).total_seconds()
    if wait_time > 0:
        print(f"開始時刻まで {wait_time:.1f} 秒待機します...")
        await asyncio.sleep(wait_time)

    driver.get(URL)

    try:
        await monitor_time(driver, start_time, duration)
    finally:
        driver.quit()

    # 撮影終了後に動画を生成
    create_video(OUTPUT_DIR)

if __name__ == "__main__":
    asyncio.run(main())
