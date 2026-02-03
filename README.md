# Punjabi Toxic Comment Detection

## Setup & Configuration

1. **Install dependencies**:

   All required Python packages are listed in `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

2. **API key configuration (`config.py`)**:

   This project uses the YouTube Data API v3, which requires an API key.

   Create a file at: `crawler/config.py`

   and add your API key:

   ```bash
    API_KEY = "YOUR_YOUTUBE_API_KEY"
   ```

   You can create an API key by following the official documentation: https://developers.google.com/youtube/v3/getting-started

   > **Note**: `config.py` is intentionally not visible in the repository because it is listed in `.gitignore`.
   > This is done to prevent accidentally exposing sensitive API keys.

3. **Running the crawler**:

   Once dependencies are installed and `config.py` is set up, you can run the crawler:

   ```bash
    python crawler/yt_crawler.py
   ```

   Collected comments will be saved to: `data/raw_comments.csv`

   > **Note**: `raw_comments.csv` is intentionally not visible in the repository because it is listed in `.gitignore`.
   > This is done because it is too big (~500k records).
