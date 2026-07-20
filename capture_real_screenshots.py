import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # New headless mode for Chrome 109+
chrome_options.add_argument("--window-size=1280,900")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("Initializing Chrome Webdriver...")
driver = webdriver.Chrome(options=chrome_options)
try:
    print("Page 1: Navigating to Dashboard Overview Hub...")
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)
    os.makedirs("static/images", exist_ok=True)
    driver.save_screenshot("static/images/01_overview.png")
    print("01_overview.png is generated successfully!")

    print("Page 2: Navigating to Step 1. Market Radar...")
    market_tab = driver.find_element(By.CSS_SELECTOR, "li[data-page='market']")
    market_tab.click()
    time.sleep(0.5)
    
    # Enter search term
    input_box = driver.find_element(By.ID, "market-input")
    input_box.clear()
    input_box.send_keys("비비크림")
    
    # Click Submit
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#market-form button[type='submit']")
    submit_btn.click()
    
    # Wait for preset results to load
    time.sleep(2)
    driver.save_screenshot("static/images/02_market_radar.png")
    print("02_market_radar.png is generated successfully!")

    print("Page 3: Navigating to Step 2. VOC Insights...")
    voc_tab = driver.find_element(By.CSS_SELECTOR, "li[data-page='voc']")
    voc_tab.click()
    time.sleep(0.5)
    
    # Input review body
    voc_textarea = driver.find_element(By.ID, "voc-text-input")
    voc_textarea.clear()
    txt = """제형이 너무 무거워서 화장 전 메이크업 밀림이 엄청 나네요. 평점 2점 줍니다.
밀리지 않는 발림성은 좋은데 저한테는 다크닝 현상이 와서 오후 되면 칙칙해요. 평점 3점.
홍조는 정말 잘 가려주는데 튜브형 용기에서 내용물이 나올 때 너무 뻑뻑해서 짜기 어려워요. 평점 3점."""
    voc_textarea.send_keys(txt)
    
    # Click Analyse
    voc_btn = driver.find_element(By.ID, "voc-analyze-pasted-btn")
    voc_btn.click()
    
    # Wait for analyse results parsing
    time.sleep(2.5)
    driver.save_screenshot("static/images/03_voc_insights.png")
    print("03_voc_insights.png is generated successfully!")

    print("Page 4: Navigating to Step 3. Copywriter...")
    # Click the first Selling Point card item
    first_sp = driver.find_element(By.CSS_SELECTOR, "#voc-sp-list .sp-item-card")
    first_sp.click()
    time.sleep(1)
    
    # Click Step 3 submit button to actually generate copy!
    gen_btn = driver.find_element(By.CSS_SELECTOR, "#generator-form button[type='submit']")
    gen_btn.click()
    
    # Wait for the copywriting results to load
    time.sleep(2.5)
    driver.save_screenshot("static/images/04_copywriter.png")
    print("04_copywriter.png is generated successfully!")
    
    print("All real screenshots captured and saved successfully inside static/images/!")

except Exception as e:
    print(f"Error occurred during screenshot capture: {e}")
finally:
    driver.quit()
