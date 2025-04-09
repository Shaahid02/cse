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
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    
    # Convert directly to DataFrame
    # This will preserve all columns from the API response
    df = pd.DataFrame(data)
    
    # Add date column for reference
    df['date_scraped'] = datetime.now().strftime('%Y-%m-%d')
    
    # Save to CSV with fixed filename
    filename = "daily_market_capitalization.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    
    # Print column names to verify
    print("\nColumns in the dataset:")
    print(df.columns.tolist())
    
    # Print first few rows to verify
    print("\nFirst 3 rows of the data:")
    print(df.head(3))

except Exception as e:
    print(f"❌ Error: {e}")
    raise