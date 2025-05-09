#  DATA ENGINEERING PIPELINE
## An data engineering pipeline to curate a Speech-To-Text dataset from publicly available lectures on NPTEL, to train speech recognition models.

## Setup Instructions

1.**Clone the Repository:**

```bash
git clone <your-repo-link>
cd <your-repo-folder>
```

2.**Install Python Dependencies:**

In **PowerShell** (or any terminal), run:

pip install -r requirements.txt


Use **Choco (Chocolatey)** to install FFmpeg on Windows:

```powershell
choco install ffmpeg
```

> *Alternative for MacOS/Linux:*
>
> * Mac: `brew install ffmpeg`
> * Ubuntu: `sudo apt-get install ffmpeg`



3. **Set up Grafana :**

Download & install Grafana:

[https://grafana.com/grafana/download}

Install Grafana with Chocolatey(Run on PowerShell as Administrator):

`choco install grafana -y`

Configure a **SQLite data source** to connect to the `dashboard/processed_data.db` file.
`grafana-cli plugins install fr-ser-sqlite-datasource`

And restart the Grafana service:

`Restart-Service grafana`
---

4. ## How to Run the Pipeline

Run everything **sequentially** with a **single command**:

```bash 
python main.py <nptel_course_url>
```

Example:

```bash
python main.py https://nptel.ac.in/courses/106106184

```
##  Project Structure
```
.
├── main.py
├── scraper/
│   └── scrape_data.py
├── downloader/
│   └── download_data.py
├── audio_preprocessor/
│   └── preprocess_audio.sh
|   └── remove_trailing_audio.py
|   └── rename_files.py
├── text_preprocessor/
│   └── preprocess_transcript.py
|   └── rename_files.py
├── train_manifest/
│   └── create_manifest.py
├── dashboard/
│   └── process_data.py
|   └── dashboard_data.db
├── data/
│   └── (Downloaded + Processed Data)
|   └── (transcript and audio links in json file)
├── requirements.txt
├── requirements.in
├── README.md
└── train_manifest.jsonl
```

**What Happens Internally:**

1. **Scraper Folder:**

   * Scrapes all **YouTube links** (audio) & **transcript PDF links** using Selenium.

2. **Downloader Folder:**

   * Downloads **audio files** using `yt-dlp`.
   * Downloads **transcript PDFs** using the scraped links.

3. **Audio Preprocessor Folder:**

   * Converts audio to **WAV (16kHz, mono)** using FFmpeg.
   * Removes the **last 10 seconds** to clean up trailing silence.
   * Renames files for consistency.

4. **Text Preprocessor Folder:**

   * Converts **PDFs to `.txt` files.**
   * Cleans text: lowercase, punctuation removal, numbers to words.
   * Renames files to match audio.

5. **Train Manifest Creator:**

   * Generates a **`train_manifest.jsonl`** with:

     * `audio_filepath`
     * `duration`
     * `text`

6. **Dashboard Folder:**

   * Processes:

     * Audio file path
     * Duration
     * Word count
     * Character count
   * Populates a **SQLite DB** for Grafana.

7. **Data Folder:**
  * Stores all Downloaded and Processed files in different folders and the transcript and audio links in json files

8. **main.py**
  *Runs everything sequentially with a single command




---

## Using the Dashboard 

1️⃣ In Grafana:

* Set up a **SQLite data source** pointing to: `dashboard/dashboard_data.db`.

2️⃣ Import the **dashboard DB** (provided in `/dashboard` ).

3️⃣ Dashboard Insights:

* Total Hours
* Total Utterances
* Vocabulary & Alphabet Size
* Histograms: Duration/File, Words/File, Characters/File
* Alphabet Table

---

## 🔍 Observations & Reflections

1️⃣ **Scraping:**

* **Selenium WebDriver** was essential because the NPTEL site is dynamic.
* Downloading both **YouTube links** and **Drive transcripts** required handling **dynamic elements** and waiting for JavaScript to load.

2️⃣ **Downloading:**

* `yt-dlp` made audio downloads smooth and efficient.
* PDF downloads (from Google Drive) were direct and reliable using requests

3️⃣ **Audio Preprocessing:**

* **FFmpeg** handled audio conversion and trimming seamlessly.
* Removing the last 10 seconds addressed trailing music often present in lectures.
* File renaming was critical to ensure **consistent mapping** between audio & text.

4️⃣ **Text Preprocessing:**

* The PDFs had a clean structure, making text extraction straightforward.
* Additional cleaning (lowercase, punctuation removal, number conversion via `num2words`) standardized transcripts well.

5️⃣ **Manifest File:**

* The manifest format matched the requirements for key value pairs of audio path, duration,transcript text
* Duration was calculated using `soundfile`.

6️⃣ **Dashboard:**

* Building the SQLite DB helped **Grafana** ingest data easily.
* It was insightful to **visualize durations, word counts, character counts**, and ensure data balance.

#### **Outcome:**

* Successfully built a reusable pipeline for collecting lecture audio and transcript data from NPTEL courses.
* Cleaned and uniformly formatted WAV audio files ready for further processing.
* Scripts support automation, scalability, and easy reuse for new datasets.


