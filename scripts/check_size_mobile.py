import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import pandas as pd
import os
import csv
from urllib.parse import urljoin

# Konfigurasi
INPUT_CSV = "data/url_artikel.csv"
OUTPUT_CSV = "output/result_checking_mobile.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive"
}

image_check_cache = {}

def get_image_size(image_url):
    if image_url in image_check_cache:
        return image_check_cache[image_url]
    
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=10)
        img = Image.open(BytesIO(response.content))
        img.load()
        width, height = img.size
        ratio = round(width / height, 2)
        result = (width, height, ratio)
        image_check_cache[image_url] = result
        return result
    except:
        return None, None, None

def extract_mobile_image_url(soup, base_url):
    hero_div = soup.find("div", class_="article-detail__hero")
    if not hero_div:
        return None

    picture = hero_div.find("picture")
    if picture:
        # Cari source dengan media khusus mobile
        mobile_source = picture.find("source", attrs={"media": "(max-width: 767px)"})
        if mobile_source and mobile_source.get("srcset"):
            return urljoin(base_url, mobile_source["srcset"])

        # Fallback ke source terakhir jika mobile tidak ada
        sources = picture.find_all("source")
        for source in reversed(sources):
            if source.get("srcset"):
                return urljoin(base_url, source["srcset"])

        # Fallback terakhir ke <img>
        img = picture.find("img")
        if img and img.get("src"):
            return urljoin(base_url, img["src"])

    # Fallback lain: <img> di dalam hero
    img = hero_div.find("img")
    if img and img.get("src"):
        return urljoin(base_url, img["src"])

    return None

def process_urls_streaming(urls, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["url", "image_url", "width", "height", "aspect_ratio", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for index, url in enumerate(urls, 1):
            print(f"[{index}/{len(urls)}] Mengecek: {url}")
            image_url, width, height, ratio = "", "", "", ""
            status = ""

            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                if response.status_code != 200:
                    status = f"Halaman gagal ({response.status_code})"
                    raise Exception()

                soup = BeautifulSoup(response.text, "html.parser")
                img_url = extract_mobile_image_url(soup, url)
                if img_url:
                    w, h, r = get_image_size(img_url)
                    if w and h:
                        image_url, width, height, ratio = img_url, w, h, r
                        status = "OK"
                        print(f"    Gambar ditemukan: {w}x{h}, rasio: {r}")
                    else:
                        status = "Gagal membaca gambar"
                        print(f"    Gagal membaca gambar: {img_url}")
                else:
                    status = "Gambar tidak ditemukan"
                    print("    Gambar tidak ditemukan di div.hero")
            except:
                if not status:
                    status = "Halaman gagal"
                print(f"    {status}")

            writer.writerow({
                "url": url,
                "image_url": image_url,
                "width": width,
                "height": height,
                "aspect_ratio": ratio,
                "status": status
            })
            f.flush()

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"File tidak ditemukan: {INPUT_CSV}")
        return

    df_urls = pd.read_csv(INPUT_CSV)
    urls = df_urls['url'].dropna().astype(str).str.strip().tolist()

    process_urls_streaming(urls, OUTPUT_CSV)

    print(f"\nSelesai. Hasil disimpan di: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
