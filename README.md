#  DATA ENGINEERING PIPELINE
## An data engineering pipeline to curate a Speech-To-Text dataset from publicly available lectures on NPTEL, to train speech recognition models.

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

1. **Scraper Folder:**

   * Scrapes all **YouTube links** (audio) & **transcript PDF links** using Selenium.

2. **Downloader Folder:**

   * Downloads **audio files** using `yt-dlp`.
   * Downloads **transcript PDFs** from the scraped links.

3. **Audio Preprocessor Folder:**

   * Converts audio to **WAV (16kHz, mono)** using ffmpeg.
   * Removes the **last 10 seconds** to clean up ending music.
   * Renames files for consistency.

4. **Text Preprocessor Folder:**

   * Converts **PDFs to `.txt` files.**
   * Cleans text: lowercase, punctuation removal, numbers to words
   * Removes unspoken text segments in the lecture video from transcript
   * Renames files to match audio.

5. **Train Manifest Creator:**

   * Generates a **`train_manifest.jsonl`** with:

     * `audio_filepath`
     * `duration`
     * `text`

6. **Dashboard Folder:**
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

7. **Data Folder:**
  * Stores all Downloaded and Processed files in different folders and the transcript and audio links in json files

8. **main.py**  (`python main.py "https://nptel.ac.in/courses/106106184`)
  *Runs everything sequentially with a single command


---
**Process to Set up Grafana :**

Download & install Grafana:

[https://grafana.com/grafana/download}

Install Grafana with Chocolatey(Run on PowerShell as Administrator):

`choco install grafana -y`

Configure a **SQLite data source** to connect to the `dashboard/dashboard_data.db` file.

`grafana-cli plugins install fr-ser-sqlite-datasource`

And restart the Grafana service:

`Restart-Service grafana`

## Using the Dashboard 

Import the **dashboard DB** (provided in `/dashboard` ).

Dashboard Insights:

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


### **To run Step Wise: Execution Guide**

**Step 1 – Downloading Audio:**
Run `main.py` with nptel course link as parameter to scrape YouTube links and download audio 
        (e.g., `python main.py "https://nptel.ac.in/courses/106106184"`)

**Step 2 – Preprocessing Audio:**
Run `preprocess_audio.sh` with 3 args: input folder, output folder, and CPU count 
        (e.g., `./audio_preprocessor/preprocess_audio.sh data/audio_downloads data/audio_processed 4`).
Run remove_trailing_audio.py script to trim the trailing audio in order to detect and trim silence or unwanted parts at the end(last 10 secs of video).
        (e.g., `python3 ./audio_preprocessor/remove_trailing_audio.py /data/audio_processed /data/audio_final`)

**Step 3 - Preprocessing transcript files:**



**Prerequisites:**
Ensure packages inside requirements.txt are installed (`pip install requirements.txt`).


### **Task 1 : Scrape and Download the Data**

Automate the collection of audio lectures and their transcripts to build a speech-to-text dataset.

#### **Methodology:**

* **Lecture Audio Download:**

  * Used Selenium to navigate to the **Course Details** tab.
  * Scraped YouTube video links from iframe tags under each weekly lecture.
  * Downloaded audio using `yt-dlp` into `data/audio_downloads/`.

* **Transcript Download:**

  * Navigated to the **Downloads** tab and expanded the **Transcripts** section.
  * Extracted Google Drive links and used `requests` to download PDFs.
  * Saved files to `data/transcript_downloads/`.

---


### **Task 2: Preprocessing Audio **

To prepare the downloaded audio files for further analysis, we performed the following preprocessing steps:

#### **1. Audio Conversion using Bash Script**

* A bash script (`preprocess_audio.sh`) was created to:

  * Convert audio files to `.wav` format using `ffmpeg`.
  * Set the sampling rate to **16 kHz** and convert audio to **mono channel**.
* The script accepts three user inputs:

  * Path to input audio directory
  * Path to output directory
  * Number of CPUs for parallel execution
* Audio processing is parallelized using `GNU parallel` to handle large-scale datasets (\~1M files).

#### **2. Additional Cleaning: Trimming End-of-Lecture Noise**

* Many lectures contain non-instructional audio in the last \~10 seconds (e.g., platform credits).
* A Python script (`remove_trailing_audio.py`) was developed using `pydub` to:

  * Trim the last 10 seconds of each WAV file.
  * Save the cleaned audio to a final output directory.





This repository builds a complete data engineering pipeline to curate a **speech-to-text dataset** from NPTEL lecture videos, **preprocess the data**, and **visualize key statistics** using Grafana.
