import os
import requests
import re
from bs4 import BeautifulSoup

# --- CONFIGURATION ---

# The name of the HTML file you saved from your browser.
HTML_FILE_PATH = 'course_page.html' 

# The session cookie needed for authentication.
# IMPORTANT: Replace 'YOUR_MOODLE_SESSION_COOKIE_VALUE' with the actual cookie value.
# Example: 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'
MOODLE_SESSION_COOKIE = ''

# The folder where the downloaded files will be saved.
DOWNLOAD_FOLDER = 'downloaded_materials'

# --- END OF CONFIGURATION ---


def sanitize_filename(name):
    """Removes invalid characters from a string to make it a valid filename."""
    # Remove the hidden "Soubor" or "URL" span text
    name = name.replace('Soubor', '').replace('URL', '').strip()
    # Remove invalid file system characters
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_file(session, url, folder, filename_prefix):
    """Downloads a file from a given URL into a specified folder."""
    try:
        response = session.get(url, allow_redirects=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Try to get the filename from the Content-Disposition header
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            # Extracts filename from header, e.g., "attachment; filename*=UTF-8''Algoritmy.pdf"
            filenames = re.findall('filename\*?=([^;]+)', content_disposition, flags=re.IGNORECASE)
            if filenames:
                filename = requests.utils.unquote(filenames[0].strip().strip("'\""))
                # Clean up UTF-8'' prefix if it exists
                if filename.lower().startswith("utf-8''"):
                    filename = filename[7:]
            else: # Fallback if filename is not found
                filename = url.split('/')[-1] or f"{filename_prefix}.pdf"
        else:
            # Fallback: create a filename from the prefix and assume PDF
            print(f"  [Warning] Could not determine filename from headers. Saving as PDF.")
            filename = f"{filename_prefix}.pdf"
        
        # Sanitize the final filename
        sanitized_filename = sanitize_filename(filename)
        filepath = os.path.join(folder, sanitized_filename)

        print(f"  -> Downloading '{sanitized_filename}'...")
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"  -> Saved to '{filepath}'")

    except requests.exceptions.RequestException as e:
        print(f"  [Error] Failed to download {url}. Reason: {e}")


def main():
    """Main function to parse HTML and download documents."""
    if MOODLE_SESSION_COOKIE == 'YOUR_MOODLE_SESSION_COOKIE_VALUE':
        print("[ERROR] Please update the 'MOODLE_SESSION_COOKIE' variable in the script with your actual session cookie.")
        return

    # Check if the HTML file exists
    if not os.path.exists(HTML_FILE_PATH):
        print(f"[ERROR] The file '{HTML_FILE_PATH}' was not found.")
        print("Please save the course webpage as a complete HTML file in the same directory as this script.")
        return

    # Create the download folder if it doesn't exist
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
        print(f"Created directory: '{DOWNLOAD_FOLDER}'")

    # Read the local HTML file
    with open(HTML_FILE_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Set up a session with the necessary cookie for authentication
    session = requests.Session()
    session.cookies.set('MoodleSession', MOODLE_SESSION_COOKIE)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })


    # Find all activity list items that are resources (files) or URLs
    # 'modtype_resource' is typically a file, 'modtype_url' can also link to documents
    activities = soup.find_all('li', class_=lambda c: c and ('modtype_resource' in c or 'modtype_url' in c))

    if not activities:
        print("No downloadable documents found on the page. Check if the HTML file is correct.")
        return
        
    print(f"Found {len(activities)} potential documents. Starting download...")

    for activity in activities:
        link_tag = activity.find('a', class_='aalink')
        if link_tag and link_tag.has_attr('href'):
            url = link_tag['href']
            # Get the name from the 'instancename' span inside the link
            instance_name_tag = link_tag.find('span', class_='instancename')
            if instance_name_tag:
                doc_name = sanitize_filename(instance_name_tag.get_text(strip=True))
                print(f"\nProcessing '{doc_name}'...")
                download_file(session, url, DOWNLOAD_FOLDER, doc_name)

    print("\nScript finished. All documents have been downloaded.")


if __name__ == '__main__':
    main()
