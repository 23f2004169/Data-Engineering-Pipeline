#  DATA ENGINEERING PIPELINE
## This repository builds a complete data engineering pipeline to curate a **Speech-To-Text dataset** NPTEL lecture videos, **preprocess the data** to train speech recognition models.

The above code was tested on the courses: 
NOC:Deep Learning, IIT Ropar (`https://nptel.ac.in/courses/106106184`)  and 
NOC:Aircraft Maintenance, IIT Kanpur (`https://nptel.ac.in/courses/101104071`)

**Visualize LIVE Key Statistics** using Grafana : 
      http://localhost:3000/public-dashboards/c238776f31774a8dbd9343c20de32e38

## Setup Instructions

1.**Clone the Repository:**

```bash
git clone <repo-link>
cd <repo-folder>
```

2.**Install Python Dependencies:**

In **PowerShell** (or any terminal), run:

```powershell
pip install -r requirements.txt
```

Use **Choco (Chocolatey)** to install FFmpeg on Windows:

```powershell
choco install ffmpeg
```

> *Alternative for MacOS/Linux:*
>
> * Mac: `brew install ffmpeg`
> * Ubuntu: `sudo apt-get install ffmpeg`

---

3. ## How to Run the Pipeline

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
│   └── audio_downloads
│   └── audio_wav
│   └── audio_processed
│   └── transcript_downloads
│   └── transcript_processed
|   └── transcripts.json
│   └── video_links.json
├── requirements.txt
├── requirements.in
├── README.md
└── train_manifest.jsonl
```

**What Happens Internally:**

1. **Scraper Folder:** (`python scraper/scrape_data.py https://nptel.ac.in/courses/106106184`)

   * Scrapes all **YouTube links** (audio) & **transcript PDF links** using Selenium.

2. **Downloader Folder:** (`python downloader/download_data.py https://nptel.ac.in/courses/106106184`)

   * Downloads **audio files** using `yt-dlp`.
   * Downloads **transcript PDFs** from the scraped links.

3. **Audio Preprocessor Folder:**

   * Converts audio to **WAV (16kHz, mono)** using ffmpeg (`./audio_preprocessor/preprocess_audio.sh data/audio_downloads data/audio_wav 4`)
   * Removes the **last 10 seconds** to clean up ending music using pydub (`python ./audio_preprocessor/remove_trailing_audio.py /data/audio_wav /data/audio_processed`)
   * Renames files for consistency (`python audio_preprocessor/rename_files.py`)

4. **Text Preprocessor Folder:**

   * Converts **PDFs to `.txt` files.** (`python text_preprocessor/preprocess_transcript.py`)
     * Cleans text: lowercase, punctuation removal, numbers to words 
     * Removes unspoken text segments in the lecture video from transcript 
   * Renames files to match audio. (`python text_preprocessor/rename_files.py`)

5. **Train Manifest Creator:** (`python train_manifest/create_manifest.py`)
   * Generates a **`train_manifest.jsonl`** with:
     * `audio_filepath`
     * `duration`
     * `text`

6. **Dashboard Folder:**  (`python dashboard/process_data.py `)
  * From process_data.py
   * Processes:
     * Audio file path
     * Duration per file
     * Word count per file
     * Character count per file
   * Finds:
     * Total number of hours
     * Total number of utterances
     * Vocabulary Size
     * Alphabet Size
  * Populates a **SQLite DB** for Grafana.

7. **Data Folder:** (data)
  * Stores all Downloaded and Processed files in different folders and the transcript and audio links in json files

8. **main.py**  (`python main.py https://nptel.ac.in/courses/106106184`)
  * Runs everything sequentially with a single command


---
## Process to Set up Grafana :

Download & install Grafana:

[https://grafana.com/grafana/download}

Install Grafana with Chocolatey(Run on PowerShell as Administrator):

`choco install grafana -y`

Configure a **SQLite data source** to connect to the `dashboard/dashboard_data.db` file.

`grafana-cli plugins install fr-ser-sqlite-datasource`

And restart the Grafana service:

`Restart-Service grafana`

### Using the Dashboard 

Import the **dashboard DB** (provided in `/dashboard` ).

Dashboard Insights:

* Total Hours
* Total Utterances
* Vocabulary & Alphabet Size
* Histograms: Duration/File, Words/File, Characters/File
* Alphabet Table

---

## Observations & Reflections

1️. **Scraping:**

* **Selenium WebDriver** was essential because the NPTEL site is dynamic.
* Downloading both **YouTube links** and **Drive transcripts** required handling **dynamic elements** and waiting for JavaScript to load.

2️. **Downloading:**

* `yt-dlp` made audio downloads smooth and efficient.
* PDF downloads (from Google Drive) were direct and reliable using requests

3. **Audio Preprocessing:**

* **FFmpeg** handled audio conversion and trimming seamlessly.
* Removing the last 10 seconds addressed trailing music often present in lectures.
* File renaming was critical to ensure **consistent mapping** between audio & text.

4️. **Text Preprocessing:**

* The PDFs had a clean structure, making text extraction straightforward.
* Additional cleaning (lowercase, punctuation removal, number conversion via `num2words`) standardized transcripts well.

5️. **Manifest File:**

* The manifest format matched the requirements for key value pairs of audio path, duration,transcript text
* Duration was calculated using `soundfile`.

6️. **Dashboard:**

* Building the SQLite DB helped **Grafana** ingest data easily.
* It was insightful to **visualize durations, word counts, character counts**, and ensure data balance.

---

## **Outcome:**

* Developed a **modular, reusable pipeline** to collect and preprocess lecture audio and transcripts from NPTEL courses, scalable to any course via URL input.

* Automated **audio download and processing**:
  * Converted audio to **16kHz mono WAV format**.
  * Removed trailing non-informative segments for cleaner data.

* Automated **transcript extraction and cleaning**:
  * Converted PDFs to `.txt`, lowercased text, removed punctuation,converted digits to spoken form and removed unspoken text segments.

* Generated a **training manifest (`train_manifest.jsonl`)** compatible with ASR frameworks like NVIDIA NeMo.

* Created a **SQLite database** for dataset stats (duration, word & character counts) and built a **Grafana dashboard** for visualization.

* Implemented **parallel processing** for efficiency and ensured **cross-platform compatibility** (tested on Windows with PowerShell).

* The entire pipeline is **fully automated** and can be executed with:
  ```bash
  python main.py <course_url>
  ```
