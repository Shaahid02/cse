import requests
import pandas as pd
from datetime import datetime

# API endpoint
url = "https://www.cse.lk/api/list_by_market_cap"

# Payload as specified
payload = {
    "headers": {
        "normalizedNames": {},
        "lazyUpdate": None
    }
}

try:
    # Make the API request
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise error if request fails
    
    # Extract the relevant data (assuming response contains "reqByMarketcap")
    data = response.json().get("reqByMarketcap", [])
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add a timestamp column
    df["date_scraped"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to CSV file
    filename = "daily_market_capitalization.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Successfully saved to: {filename}")
    print(f"📊 Total records saved: {len(df)}")

except Exception as e:
    print(f"❌ Error: {e}")
    raise