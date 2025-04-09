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
    
    # Flatten the data if it's nested
    # This is a common approach when dealing with JSON APIs
    processed_data = []
    
    # Assuming data is a list of dictionaries at the top level
    # If it's nested differently, you'll need to adjust this section
    for item in data:
        # Extract only the fields we want for the CSV
        processed_item = {
            'Company': item.get('companyName', ''),
            'Symbol': item.get('symbol', ''),
            'Sector': item.get('sectorDescription', ''),
            'Market_Cap_LKR': item.get('marketCap', 0),
            'Last_Traded_Price': item.get('lastTradedPrice', 0),
            'Price_Change': item.get('change', 0),
            'Price_Change_Percentage': item.get('changePercentage', 0),
            'Date': datetime.now().strftime('%Y-%m-%d')
        }
        processed_data.append(processed_item)
    
    # Convert to DataFrame
    df = pd.DataFrame(processed_data)
    
    # Save to CSV with fixed filename
    filename = "daily_market_capitalization.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    
    # Print first few rows to verify
    print("\nFirst 5 rows of the data:")
    print(df.head())

except Exception as e:
    print(f"❌ Error: {e}")
    raise