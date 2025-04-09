from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import time
import os

# Get today's date in yyyy-MM-dd format
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"{date_str}_daily_share_trading_statistics.csv"

# Set up Chrome options for headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Path to chromedriver in GitHub Actions environment
options.binary_location = "/usr/bin/chromium-browser"

# Start WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://www.cse.lk/pages/market-capitalization/market-capitalization.html")

# Wait for dynamic content to load
time.sleep(5)

# Parse tables using pandas
tables = pd.read_html(driver.page_source)

# Close the driver
driver.quit()

# Pick the correct table (check index if needed)
daily_stats_table = tables[1]

# Save the table with formatted filename
os.makedirs("output", exist_ok=True)
daily_stats_table.to_csv(f"output/{filename}", index=False)

print(f"Saved: output/{filename}")
