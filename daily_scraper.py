from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import time

# Set up headless Chrome with correct binary
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser"

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Go to the CSE market capitalization page
url = "https://www.cse.lk/pages/market-capitalization/market-capitalization.html"
driver.get(url)

# Let page load
time.sleep(5)

# Find the correct table by heading text
tables = driver.find_elements("tag name", "table")
target_table = None
for table in tables:
    if "DAILY SHARE TRADING STATISTICS (SUMMARY)" in table.text:
        target_table = table
        break

if not target_table:
    driver.quit()
    raise Exception("Target table not found on the page")

# Extract table HTML and convert to DataFrame
html = target_table.get_attribute("outerHTML")
df = pd.read_html(html)[0]

# Save DataFrame to CSV with proper file name
today_str = datetime.now().strftime("%Y-%m-%d")
filename = f"{today_str}_daily_share_trading_statistics.csv"
df.to_csv(filename, index=False)

print(f"✅ Saved: {filename}")
driver.quit()
