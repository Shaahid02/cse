import requests
import pandas as pd
from datetime import datetime
import os
import json
import csv

# API endpoint
url = "https://www.cse.lk/api/list_by_market_cap"

# Payload as specified
payload = {
    "headers": {
        "normalizedNames": {},
        "lazyUpdate": None
    }
}


def save_data_to_files(data):
    # Format lastTradedTime and add date_scraped to each object
    formatted_data = []
    for obj in data:
        # Format lastTradedTime
        if "lastTradedTime" in obj:
            dt = pd.to_datetime(obj["lastTradedTime"], unit='ms')
            dt = dt + pd.Timedelta(hours=5, minutes=30)
            if pd.notna(dt):
                obj["lastTradedTime"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                obj["lastTradedTime"] = None  # or set to a default string
        # Add date_scraped
        obj["date_scraped"] = datetime.now().strftime("%Y-%m-%d")
        formatted_data.append(obj)

    # Save to JSON
    json_filename = "daily_market_capitalization.json"
    
    # Load existing data if file exists
    existing_data = []
    if os.path.exists(json_filename):
        try:
            with open(json_filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []
    
    # Append new data to existing data
    existing_data.extend(formatted_data)
    
    # Write all data back to file
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to JSON: {json_filename}")

    # Save to CSV
    csv_filename = "daily_market_capitalization.csv"
    
    if formatted_data:
        all_keys = set()
        for obj in formatted_data:
            if isinstance(obj, dict):
                all_keys.update(obj.keys())
    
    with open(csv_filename, 'a', encoding='utf-8', newline='') as f:
        # Use the keys from the first object to preserve original order
        first_keys = list(formatted_data[0].keys()) if formatted_data else []
        writer = csv.DictWriter(f, fieldnames=first_keys)
        
        if not os.path.exists(csv_filename): writer.writeheader()
        
        for obj in formatted_data:
            if isinstance(obj, dict):
                writer.writerow(obj)

        print(f"💾 Saved to CSV: {csv_filename}")
        
    return json_filename, csv_filename


try:
    # Make the API request
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    # Extract data
    data = response.json().get("reqByMarketcap", [])
    
    json_file, csv_file = save_data_to_files(data)
    print(f"📊 Records added: {len(data)}")

except Exception as e:
    print(f"❌ Error: {e}")
    raise
