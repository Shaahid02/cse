import requests
import pandas as pd
import json
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
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    
    # Convert to a pandas DataFrame
    # Assuming the response has the data in the root level
    # You might need to adjust this depending on the actual response structure
    df = pd.DataFrame(data)
    
    # Save to CSV with fixed filename
    filename = "daily_market_capitalization.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")

except Exception as e:
    print(f"❌ Error: {e}")
    raise