# Punjabi Toxic Comment Detection

## Setup & Configuration

1. **Setup a virtual enviornment**

   Create a python 3.11 or below virtual enviornment for this project. Some dependencies like `fastText` do not yet offer full, stable support or pre-built wheels for Python 3.13. It can be setup with the following:

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   All required Python packages are listed in `requirements.txt`. Install them using:

   ```bash
   pip install -r requirements.txt
   ```

   This project uses `lid.176.bin` which is a pre-trained fastText model used for language identification in Python. Download it using:

   ```bash
   wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
   ```

   and put the downloaded model in `models/`

   > **Note**: `lid.176.bin` is intentionally not visible in the repository because it is listed in `.gitignore`.

   The `fasttext` Python library may have compatibility issues with newer versions of `NumPy` due to the original library no longer being actively maintained by Meta. This often results in an error when loading the `lid.176.bin` model. Install a compatible version of numpy using:

   ```bash
   pip uninstall numpy -y
   pip install "numpy<2.0"
   ```   

3. **API key configuration (`config.py`)**:

   This project uses the YouTube Data API v3, which requires an API key. Create a file at `crawler/config.py` and add your API key:

   ```bash
    API_KEY = "YOUR_YOUTUBE_API_KEY"
   ```

   You can create an API key by following the official documentation: https://developers.google.com/youtube/v3/getting-started

   > **Note**: `config.py` is intentionally not visible in the repository because it is listed in `.gitignore`. This is done to prevent accidentally exposing sensitive API keys.

4. **Running the crawler**:

   Once dependencies are installed and `config.py` is set up, you can run the crawler:

   ```bash
    python crawler/yt_crawler.py
   ```

   This fetchs comments using the YouTube Data API. Collected comments will be saved to: `data/raw_comments.csv`

5. **Cleaning the raw data**:

   Before any language detection is performed, the raw comments need to be cleaned and normalized using:

   ```bash
   python preprocessing/cleaning.py
   ```

   Cleaned comments will be saved to: `data/clean_comments.csv`

   > **Note**: `raw_comments.csv` and `clean_comments.csv` are intentionally not visible in the repository because it is listed in `.gitignore`. This is done because they are too big (~500k records).

6. **Detect punjabi comments**

   Punjabi comments are detected using a hybrid approach that combines:

   * Gurmukhi Unicode detection
   * Roman Punjabi lexicon matching
   * fastText language identification

   Run the detection script:

   ```bash
   python preprocessing/detectPunjabi.py
   ```

   Detected punjabi comments will be saved to: `data/punjabi_comments.csv`
