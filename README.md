# Link Downloader

A simple Python application that allows users to fetch and download files from a specified webpage. This application utilizes the BeautifulSoup library to parse HTML content and identify downloadable links based on specified file extensions.

## Features

- Input a URL to fetch downloadable content.
- Display a list of downloadable files in a user-friendly interface.
- Select and download one or more files at a time.
- Option to select all downloadable files quickly.

## Requirements

- Python 3.x
- Required Python packages:
    - requests
    - beautifulsoup4
    - tkinter (usually comes pre-installed with Python)

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/robinpatzak/link-downloader
```

2. Navigate into the directory

```bash
cd link-downloader
```

3. Install the required packages (Setting up a virtual environment first is highly recommended):
```bash
pip install requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Usage

1. Enter the webpage URL from which you want to download files in the provided input field.
2. Click on "Fetch Downloadable Content" to retrieve the list of downloadable files.
3. Select the files you want to download from the list.
4. Click on "Download Selected Files" to download the chosen files.
5. Use the "Select All" button to quickly select all files in the list.
