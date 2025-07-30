# Check Image Size Nutriclub

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-passed-brightgreen)](requirements.txt)
[![Last Commit](https://img.shields.io/github/last-commit/maazway/check-image-size-nutriclub)](https://github.com/maazway/check-image-size-nutriclub/commits/main)

---

## Project Description

This project simplifies the process of checking image sizes in Nutriclub articles.

---

## Features

* Retrieves image dimensions (width and height)
* Image URL
* Aspect ratio
* Check status
* Supports various common image formats (e.g., JPG, PNG, GIF)

---

## Installation

To run this project in your local environment, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/maazway/check-image-size-nutriclub
    cd check-image-size-nutriclub
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv

    # On Windows:
    venv\Scripts\activate

    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

*(There are 2 scripts: one for mobile version and one for desktop version)*

**To run:**

```bash
# To run the mobile script:
python scripts/check_size_image_banner_mobile.py
# Check output:
output/result_checking_size_banner_mobile.csv

# To run the desktop script:
python scripts/check_size_image_banner_desktop.py
# Check output:
output/result_checking_size_banner_desktop.csv
