from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
from io import StringIO

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser"

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the page
url = "https://www.cse.lk/pages/market-capitalization/market-capitalization.html"
driver.get(url)

try:
    # Wait for the table with ID 'DataTables_Table_0' to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "DataTables_Table_0"))
    )

    # Extract the table HTML
    table_element = driver.find_element(By.ID, "DataTables_Table_0")
    html = table_element.get_attribute("outerHTML")

    # Parse with pandas using StringIO and lxml
    df = pd.read_html(StringIO(html), flavor="lxml")[0]

    # Generate filename
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_str}_daily_share_trading_statistics.csv"

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")

except Exception as e:
    print(f"❌ Error: {e}")
    raise

finally:
    driver.quit()
