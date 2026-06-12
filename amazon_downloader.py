import os
import json
import csv
import requests
import shutil
from tqdm import tqdm

# Setup the workspace directory
output_dir = "amazon_reviews_50k"
os.makedirs(output_dir, exist_ok=True)

# Complete list of categories from your folder structure
categories = [
    "All_Beauty", "Amazon_Fashion", "Appliances", "Arts_Crafts_and_Sewing", "Automotive",
    "Baby_Products", "Beauty_and_Personal_Care", "Books", "CDs_and_Vinyl", "Cell_Phones_and_Accessories",
    "Clothing_Shoes_and_Jewelry", "Digital_Music", "Electronics", "Gift_Cards", "Grocery_and_Gourmet_Food",
    "Handmade_Products", "Health_and_Household", "Health_and_Personal_Care", "Home_and_Kitchen",
    "Industrial_and_Scientific", "Kindle_Store", "Magazine_Subscriptions", "Movies_and_TV",
    "Musical_Instruments", "Office_Products", "Patio_Lawn_and_Garden", "Pet_Supplies", "Software",
    "Sports_and_Outdoors", "Subscription_Boxes", "Tools_and_Home_Improvement", "Toys_and_Games",
    "Unknown", "Video_Games"
]

TARGET_USER_COUNT = 50000

print("--- Starting Network-Optimized JSONL Stream ---")

for category in categories:
    print(f"\nStreaming Category: {category}")
    
    # Construct the raw download endpoint for the JSONL files
    url = f"https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/raw/review_categories/{category}.jsonl"
    csv_file_path = os.path.join(output_dir, f"amazon_2023_{category}_50k_users.csv")
    
    seen_users = set()
    writer = None
    file_handle = None
    
    try:
        # stream=True opens the connection without downloading the file payload completely
        with requests.get(url, stream=True, timeout=30) as r:
            if r.status_code == 404:
                print(f"  Skipping {category}: Received 404 Not Found from Hugging Face.")
                continue
                
            r.raise_for_status()
            
            # Create a progress bar that goes up to 50,000 unique users
            pbar = tqdm(total=TARGET_USER_COUNT, desc=f"  Extracting {category}")
            
            # Read line-by-line over the web connection
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                    
                try:
                    review_data = json.loads(line)
                    user_id = review_data.get("user_id")
                    
                    # Deduplicate: only capture the review if we haven't tracked this user yet
                    if user_id and user_id not in seen_users:
                        seen_users.add(user_id)
                        
                        # Lazily initialize the CSV writer on the first valid line to extract schema keys dynamically
                        if writer is None:
                            file_handle = open(csv_file_path, mode='w', newline='', encoding='utf-8')
                            fieldnames = list(review_data.keys())
                            writer = csv.DictWriter(file_handle, fieldnames=fieldnames, extrasaction='ignore')
                            writer.writeheader()
                        
                        writer.writerow(review_data)
                        pbar.update(1)
                        
                    # Stop fetching from the web the exact moment our quota is filled
                    if len(seen_users) >= TARGET_USER_COUNT:
                        break
                        
                except json.JSONDecodeError:
                    continue
            
            pbar.close()
            
    except Exception as e:
        print(f"  Error processing category {category}: {e}")
    finally:
        # Securely close the disk file stream if it was opened
        if file_handle:
            file_handle.close()
            print(f"  -> Successfully saved 50,000 unique user rows to {csv_file_path}")

# --- ZIP ARCHIVE STEP ---
print("\n--- Compressing All Files into a Single Zip Archive ---")
zip_archive_name = "amazon_reviews_50k_dataset"
shutil.make_archive(zip_archive_name, 'zip', output_dir)
print(f"Success! Master archive created: {zip_archive_name}.zip")
print("You can download the zip file directly from your Google Colab file explorer panel on the left side menu.")
