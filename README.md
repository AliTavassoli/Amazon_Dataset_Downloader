# 🚀 Amazon Reviews 2023 Downloader & Merger

A memory-optimized, network-streamed Python pipeline designed to extract and merge clean user review subsets from the massive **Amazon Reviews 2023 dataset (McAuley Lab)** on Hugging Face without blowing up your local machine or Google Colab RAM.

---

## 🛠️ How It Works (In a Nutshell)

Instead of downloading massive **20GB+** files and crashing your environment, this pipeline uses **smart streaming**.

1. **Line-by-Line Network Streaming**: It opens a live data stream to Hugging Face, reading reviews one single line at a time.
2. **On-the-Fly Deduplication**: It keeps track of users dynamically and dumps the data straight to your hard drive the split second a new unique user is found.
3. **Flat Memory Footprint**: Once the strict cap is met, it immediately hangs up the phone on the server, keeping your RAM usage close to 0%.

---

## 📂 Script Breakdown

### 1. `amazon_downloader.py`

This script handles the heavy lifting of fetching the data safely over the network.

* **What it does**: Streams all 34 product categories sequentially from the Hugging Face JSONL endpoints.
* **The Goal**: Stops fetching the exact moment it hits **50,000 unique users** per category.
* **Output**: Saves 34 individual, clean CSV files into the `amazon_reviews_50k/` directory and compresses them into a single, easy-to-download `.zip` archive.

### 2. `creating_master_amazon.py`

This script takes all those freshly downloaded category sheets and brings them together.

* **What it does**: Reads the individual 50k CSV files chunk-by-chunk.
* **The Goal**: Injects a fresh `category` tracking column into each row and appends them sequentially into a single file.
* **Output**: Generates a grand master file (`amazon_reviews_master_combined.csv`) containing roughly **1.7 million rows** of rich review text, safely zipped and ready for your machine learning models or analysis.

---

## 📊 Output Structure

```text
├── amazon_reviews_50k_dataset.zip         # Compressed archive of raw categories
├── amazon_reviews_master_combined.zip      # Compressed master merged sheet (~1.7M rows)
└── amazon_reviews_50k/                    # Standalone working directory
    ├── amazon_2023_All_Beauty_50k_users.csv
    ├── amazon_2023_Books_50k_users.csv
    └── ... (remaining 32 category sheets)

```
