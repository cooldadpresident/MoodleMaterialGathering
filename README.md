Of course. Here is a comprehensive `README.md` file for the script. You can save this text directly into a file named `README.md` in the same folder as your script.

---

# Moodle Course Document Downloader

A simple Python script to automatically download all linked documents, such as presentations, slides, and other resources, from a saved Moodle course page. This tool is designed to help you quickly gather all course materials for offline access, note-taking in apps like Obsidian, or for feeding into AI models.

## Features

-   **Parses Local HTML**: Works with a saved HTML file of your course page, so it doesn't scrape the live site repeatedly.
-   **Authenticated Downloads**: Uses your browser's session cookie to securely download files that require you to be logged in.
-   **Organized Output**: Saves all downloaded files into a dedicated folder (`downloaded_materials`).
-   **Smart Filenaming**: Attempts to retrieve the original filename from the server, falling back to a sanitized version of the link text.
-   **Handles Common Resources**: Downloads both direct file links (`modtype_resource`) and URL links (`modtype_url`) which often point to documents.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3**: This script is written for Python 3. You can download it from [python.org](https://www.python.org/).
2.  **Required Python Libraries**: You'll need `requests` and `beautifulsoup4`. You can install them using pip:

    ```bash
    pip install requests beautifulsoup4
    ```

## How to Use

Follow these steps to download your course materials.

### Step 1: Save the Course Webpage

1.  Log in to your Moodle e-learning portal (`elearning.jcu.cz`).
2.  Navigate to the main page of the course you want to download materials from.
3.  Right-click anywhere on the page and select **"Save As..."** (the wording may vary depending on your browser).
4.  In the save dialog, make sure the format is set to **"Webpage, Complete"**. This ensures all necessary parts of the page are saved.
5.  Save the file as `course_page.html` in the same directory where you will place the `download_docs.py` script.

### Step 2: Find Your Session Cookie

To download protected files, the script needs to authenticate as you. You can do this by providing your session cookie.

1.  Stay logged into your Moodle e-learning portal.
2.  Open the browser's developer tools (usually by pressing **F12** or **Ctrl+Shift+I**).
3.  Go to the **Application** tab (in Chrome) or **Storage** tab (in Firefox).
4.  On the left-hand menu, find the **Cookies** section and select the URL of your e-learning site (e.g., `https://elearning.jcu.cz`).
5.  Find the cookie named `MoodleSession`.
6.  Click on it and copy its entire **Cookie Value**. It will be a long string of letters and numbers.



### Step 3: Configure the Script

Open the `download_docs.py` file in a text editor and update the following variables:

1.  `HTML_FILE_PATH`: Ensure this matches the name of the HTML file you saved in Step 1 (the default is `'course_page.html'`).
2.  `MOODLE_SESSION_COOKIE`: **This is the most important step.** Paste the cookie value you copied in Step 2, replacing `'YOUR_MOODLE_SESSION_COOKIE_VALUE'`.

```python
# The name of the HTML file you saved from your browser.
HTML_FILE_PATH = 'course_page.html' 

# The session cookie needed for authentication.
# IMPORTANT: Replace 'YOUR_MOODLE_SESSION_COOKIE_VALUE' with the actual cookie value.
```

### Step 4: Run the Script

1.  Open a terminal or command prompt.
2.  Navigate to the directory where you saved the script and the HTML file.
3.  Run the script using the following command:

    ```bash
    python download_docs.py
    ```

The script will create a folder named `downloaded_materials` and begin downloading the files. You will see progress messages in the terminal.

## Troubleshooting

-   **`[ERROR] The file 'course_page.html' was not found.`**
    -   Make sure the HTML file is saved in the same folder as the script and that the `HTML_FILE_PATH` variable in the script matches its name.

-   **`[ERROR] Failed to download... Reason: 403 Forbidden`**
    -   This almost always means your `MOODLE_SESSION_COOKIE` is incorrect or has expired. Your session cookie expires when you log out or after a period of inactivity.
    -   **Solution**: Log back into Moodle, get the new session cookie value (Step 2), and update the script.

-   **"No downloadable documents found..."**
    -   Ensure you saved the webpage as **"Webpage, Complete"** and not "HTML Only".
    -   The script might not be able to find the links if the course page has a very unusual structure.

## Disclaimer

This script is intended for personal use to make it easier to access course materials you are already entitled to view. Please use it responsibly and respect the terms of service of your university's e-learning platform.

---
