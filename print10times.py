import urllib.request
import urllib.parse
import subprocess
import tempfile

etherpad_base_url = 'https://pad.riseup.net/p'
pad_id = 'pptpabf-keep'
# pad_id = 'pptrytxt-tmp'


# Encode the pad_id to handle non-ASCII characters
encoded_pad_id = urllib.parse.quote(pad_id, safe="")
etherpad_text_url = f'{etherpad_base_url}/{encoded_pad_id}/export/txt'

# Fetch the plain text content using urllib
def fetch_etherpad_text(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8') 
    except Exception as e:
        print(f"Error fetching Etherpad text content: {e}")
        return None

# Directly print content without creating temporary files
def print_to_printer_directly(content):
    try:
        # Use `lp` command with stdin to avoid temporary files
        process = subprocess.Popen(["lp", "-d", "Star_MCP31__STR_001_"], stdin=subprocess.PIPE)
        process.communicate(input=content.encode('utf-8'))
        if process.returncode != 0:
            print(f"Error printing: Return code {process.returncode}")
    except Exception as e:
        print(f"Error printing to printer: {e}")

if __name__ == "__main__":
    print("Fetching Etherpad content...")
    content = fetch_etherpad_text(etherpad_text_url)
    if content:
        for _ in range(10):  # Print 10 times
            print_to_printer_directly(content)
    else:
        print("Failed to fetch content from Etherpad.")