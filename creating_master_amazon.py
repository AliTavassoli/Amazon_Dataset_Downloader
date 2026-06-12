import os
import pandas as pd
from tqdm import tqdm
import shutil

# Directories and file paths
input_dir = "amazon_reviews_50k"
master_csv_path = "amazon_reviews_master_combined.csv"
master_zip_path = "amazon_reviews_master_combined"

# Reset the master file if it already exists from a previous run
if os.path.exists(master_csv_path):
    os.remove(master_csv_path)

# Gather all the CSV files you just downloaded
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
print(f"--- Found {len(csv_files)} CSV files to merge ---")

# Process each file sequentially to keep RAM near 0%
for file_name in tqdm(csv_files, desc="Merging Categories"):
    file_path = os.path.join(input_dir, file_name)
    
    # Clean up the file name to extract a clean category name
    category_name = file_name.replace("amazon_2023_", "").replace("_50k_users.csv", "")
    
    try:
        # Load just this single category file
        df = pd.read_csv(file_path)
        
        # Add a tracker column so you know exactly which category a review came from
        df['category'] = category_name
        
        # Only write the header row for the absolute first file created
        header_needed = not os.path.exists(master_csv_path)
        
        # Append directly to the master file on the disk
        df.to_csv(master_csv_path, mode='a', index=False, header=header_needed)
        
        # Clear the memory instantly
        del df
        
    except Exception as e:
        print(f"  Error processing {file_name}: {e}")

print(f"\n--> Master CSV successfully created at: {master_csv_path}")

# --- BONUS: ZIP THE MASTER FILE FOR EASY DOWNLOAD ---
print("\n--- Compressing Master File into a ZIP Archive ---")
# Temporary folder to hold the master file for clean zipping
temp_dir = "master_zip_holder"
os.makedirs(temp_dir, exist_ok=True)
shutil.copy(master_csv_path, os.path.join(temp_dir, os.path.basename(master_csv_path)))

# Zip the master file folder
shutil.make_archive(master_zip_path, 'zip', temp_dir)

# Clean up the temporary folder
shutil.rmtree(temp_dir)

print(f"Success! Compressed Master Archive created: {master_zip_path}.zip")
print("You can find 'amazon_reviews_master_combined.zip' in your Colab files panel, ready for download.")
