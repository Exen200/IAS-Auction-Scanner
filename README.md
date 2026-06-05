# KAS Auction Monitor (Katowice, Poznań, Wrocław, Opole)

A lightweight, automated desktop application written in Python to monitor administrative auction notices from the Chambers of Tax Administration (IAS / KAS) in **Katowice, Wrocław, Poznań, and Opole**. The application scrapes official websites, filters notices for movable property (e.g., vehicles, machinery, electronics), detects new listings, and saves them to text files.

## 🌟 Key Features
* **Multi-Region Tracking:** Monitors pages for Katowice, Wrocław, Poznań, and Opole simultaneously.
* **Smart Filtering:** Categorizes listings using keywords to automatically include movables (`GOOD` keywords like cars, computers, equipment) and exclude real estate (`BAD` keywords like apartments, plots of land).
* **Incremental Scraping:** Tracks previously seen auctions using a local database (`seen_links.json`) to prevent duplicate entries and only flag genuinely new announcements.
* **User-Friendly Desktop GUI:** Built with Python's Tkinter, featuring a dark-themed interface, asynchronous execution via threading (prevents freezing during web requests), a visual progress bar, and a real-time activity log.
* **Organized Output:** Saves newly discovered listings in structured text files organized inside a daily snapshot folder (`WYNIKI/YYYY-MM-DD.txt`).

---

## 🛠️ Requirements & Installation

The project runs on **Python 3.x** and requires standard web-scraping dependencies.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/kas-auction-monitor.git
   cd kas-auction-monitor
   ```

2. **Install requirements:**
   Make sure you have `pip` installed, then run:
   ```bash
   pip install requests beautifulsoup4
   ```
   *(Note: `tkinter`, `json`, `os`, and `threading` are built into standard Python installations).*

---

## 🚀 How to Use

1. Launch the application by executing the script:
   ```bash
   python main.py
   ```
2. **Interface Controls:**
   * **SPRAWDŹ TERAZ (Check Now):** Starts the scraping worker thread. It iterates through all regions, processes up to 15 pages per source, and fetches new records.
   * **OTWÓRZ WYNIKI (Open Results):** Quickly opens the system file explorer directly inside the output results directory (`WYNIKI`).
   * **ZAMKNIJ (Close):** Exits the application safely.

---

## 📁 File Structure & Data Workflow

* `main.py` — Core script containing the Web Scraper, filtering logic, and the Tkinter GUI.
* `seen_links.json` — Local database registry generated automatically to keep track of already scraped URL links.
* `WYNIKI/` — Destination directory for output logs. Each time new auctions are detected, a file named after the current date (e.g., `2026-06-05.txt`) is generated.

### Output Text Format
```text
[Katowice]
Obwieszczenie o licytacji pojazdu osobowego Skoda Octavia
https://www.gov.pl/web/ias-katowice/obwieszczenia-o-licytacjach/...

[Wroclaw]
Licytacja publiczna - sprzęt komputerowy oraz elektronika
https://www.gov.pl/web/ias-wroclaw/obwieszczenia-o-licytacjach/...
```

---

## ⚙️ Custom Filtering Logic
You can fine-tune what kind of items the application looks for by modifying the keyword arrays directly inside `main.py`:
```python
BAD = ['nieruchomo', 'dzialka', 'lokal', 'mieszkan', 'grunt', 'udzial']
GOOD = ['samoch', 'pojazd', 'ruchomo', 'motocy', 'maszyn', 'sprzet', 'komputer', 'bmw', 'audi', 'opel']
```

---

## 🔒 Disclaimer
This project was developed strictly for educational and personal automation purposes. The application relies on parsing publicly accessible static HTML elements on Polish government platforms. The author is not responsible for any changes made to the structure of the target websites that could disrupt the script's scraping capabilities.
