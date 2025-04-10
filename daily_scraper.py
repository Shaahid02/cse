import requests
import pandas as pd
from datetime import datetime
import os

# API endpoint
url = "https://www.cse.lk/api/list_by_market_cap"

# Payload as specified
payload = {
    "headers": {
        "normalizedNames": {},
        "lazyUpdate": None
    }
}

# Output CSV file
filename = "daily_market_capitalization.csv"

try:
    # Make the API request
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    # Extract data
    data = response.json().get("reqByMarketcap", [])
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add timestamp column in yyyy-MM-dd format
    df["date_scraped"] = datetime.now().strftime("%Y-%m-%d")
    
    # Determine whether to write the header
    write_header = not os.path.exists(filename)
    
    # Save to CSV (append mode)
    df.to_csv(filename, mode='a', header=write_header, index=False)
    
    print(f"✅ Successfully appended to: {filename}")
    print(f"📊 Records added: {len(df)}")

except Exception as e:
    print(f"❌ Error: {e}")
    raise
