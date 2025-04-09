from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import os
import time

# Get today's date
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"{date_str}_daily_share_trading_statistics.csv"

# Setup Selenium Chrome in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Start driver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.cse.lk/pages/market-capitalization/market-capitalization.html")

# Wait for content to load
time.sleep(5)

# Read all tables
tables = pd.read_html(driver.page_source)

# Close browser
driver.quit()

# Pick correct table (you may need to adjust index depending on page structure)
daily_stats_table = tables[1]

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Save CSV
output_path = f"output/{filename}"
daily_stats_table.to_csv(output_path, index=False)

print(f"Saved: {output_path}")
