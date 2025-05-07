#  DATA ENGINEERING PIPELINE
## Created a data engineering pipeline to curate a Speech-To-Text dataset from publicly available lectures on NPTEL, to train speech recognition models.

### **Audio Processing Pipeline: Execution Guide**

**Task 1 – Downloading Audio:**
Run `main.py` with nptel course link as parameter to scrape YouTube links and download audio 
        (e.g., `python main.py "https://nptel.ac.in/courses/106106184"`)

**Task 2 – Preprocessing Audio:**
Run `preprocess_audio.sh` with 3 args: input folder, output folder, and CPU count 
        (e.g., `./audio_preprocessor/preprocess_audio.sh data/audio_downloads data/audio_processed 4`).
Run remove_trailing_audio.py script to trim the trailing audio in order to detect and trim silence or unwanted parts at the end(last 10 secs of video).
        (e.g., `python3 ./audio_preprocessor/remove_trailing_audio.py /data/audio_processed /data/audio_final`)


**Prerequisites:**
Ensure packages inside requirements.txt are installed (`sudo apt install ffmpeg parallel`).


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

#### **Code Structure:**

* `main.py`: Pipeline controller
* `scraper/scrape_data.py`: Scrapes links
* `downloader/download_data.py`: Downloads audio and PDFs



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



#### **Outcome:**

* Successfully built a reusable pipeline for collecting lecture audio and transcript data from NPTEL courses.
* Cleaned and uniformly formatted WAV audio files ready for further processing.
* Scripts support automation, scalability, and easy reuse for new datasets.

