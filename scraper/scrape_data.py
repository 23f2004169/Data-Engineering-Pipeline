import os
import time
import json
import subprocess
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse


def setup_driver():
    options = Options()
    #get course url from command line argument
    parser = argparse.ArgumentParser(description="NPTEL YouTube Audio Scraper/Downloader.")
    parser.add_argument("course_url", type=str, help="The NPTEL course URL to scrape.")
    args = parser.parse_args()
    global COURSE_URL
    COURSE_URL = args.course_url
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def get_week_elements(driver, json_path):
    wait = WebDriverWait(driver, 10)
    driver.get(COURSE_URL)
    print("📘 Loading course page...")
    time.sleep(3)

    week_spans = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Week')]"))
    )
    print(f"🔎 Found {len(week_spans)} week spans.")

    data = []

    for i in range(len(week_spans)):
        week_spans = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Week')]"))
        )
        week = week_spans[i]
        week_text = week.text.strip()
        print(f"\n📂 Opening {week_text}...")
        driver.execute_script("arguments[0].scrollIntoView(true);", week)
        week.click()
        time.sleep(2)
        try:
            lesson_items = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lessons-list li"))
            )

            for j in range(len(lesson_items)):
                lesson_items = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lessons-list li"))
                )
                li = lesson_items[j]
                lesson_title = li.text.strip()
                if not lesson_title:
                    continue
                print(f"🎥 Lesson: {lesson_title}")
                try:
                    li.click()
                    # time.sleep(2)
                    iframe = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "iframe[src*='youtube.com']")
                        )
                    )
                    driver.switch_to.frame(iframe)
                    youtube_link = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "a[href*='youtube.com/watch']"))
                    ).get_attribute("href")
                    print(f"✅ YouTube Link: {youtube_link}")
                    data.append({"lesson_title": lesson_title, "youtube_link": youtube_link})
                except Exception as e:
                    print(f"⚠️ Skipped: {e}")
                finally:
                    driver.switch_to.default_content()
        except Exception as e:
            print(f"❌ No lessons found in {week_text}: {e}")

    driver.quit()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved {len(data)} entries to {json_path}")



 

def get_transcript_links(course_url):
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(course_url)

    print("📘 Opening course page...")
    time.sleep(3)

    # Click on the Downloads tab
    print("🧭 Looking for 'Downloads' tab...")
    tabs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tab")))
    for tab in tabs:
        if tab.text.strip().lower() == "downloads":
            tab.click()
            print("✅ Clicked on Downloads tab.")
            break
    else:
        print("❌ 'Downloads' tab not found.")
        driver.quit()
        return

    time.sleep(2)

    # Click on the Transcripts section
    try:
        transcripts_header = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[text()='Transcripts']"))
        )
        # driver.execute_script("arguments[0].scrollIntoView(true);", transcripts_header)
        transcripts_header.click()
        print("📂 Opened Transcripts section.")
    except Exception as e:
        print(f"❌ Transcripts section not found: {e}")
        driver.quit()
        return

    time.sleep(2)

    # Process all transcript entries
    data_divs = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.d-data"))
    )
    print(f"📥 Found {len(data_divs)} transcript entries.\n")

    results = []

    for idx, div in enumerate(data_divs, start=1):
        print(f"➡️ Processing transcript {idx}")
        entry = {}

        try:
            # Optional: get course or week title from <span class="c-name">
            try:
                title_span = div.find_element(By.CSS_SELECTOR, "span.c-name")
                entry["title"] = title_span.text.strip()
            except:
                entry["title"] = f"Transcript {idx}"
            time.sleep(1)
            # Click language dropdown
            dropdown = div.find_element(By.CSS_SELECTOR, ".pseudo-input")
            # driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
            dropdown.click()
            time.sleep(1)

            # Click "english-Verified"
            options = div.find_elements(By.CSS_SELECTOR, "ul.pseudo-options li")
            clicked = False
            for opt in options:
                if "english-verified" in opt.text.strip().lower():
                    opt.click()
                    print("✅ Selected 'english-Verified'")
                    clicked = True
                    time.sleep(1)
                    break

            if not clicked:
                print("⚠️ 'english-Verified' option not found.")
                continue

            # Now look for the drive link anchor
            try:
                link = div.find_element(By.CSS_SELECTOR, "a[href*='drive.google.com']")
                href = link.get_attribute("href")
                print(f"🔗 Transcript link: {href}\n")
                entry["link"] = href
                results.append(entry)
            except Exception as e:
                print("⚠️ Google Drive link not found.\n")

        except Exception as e:
            print(f"⚠️ Error processing transcript {idx}: {e}\n")

    driver.quit()

    # Save results to JSON
    if results:
        with open("data/transcripts.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved {len(results)} transcript links to transcripts.json")
    else:
        print("❌ No transcript links found to save.")





    
    
