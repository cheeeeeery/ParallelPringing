import urllib.request
import urllib.parse
import subprocess
import tempfile
import textwrap
import time
import os  # this is for the beepboop

etherpad_base_url = 'https://pad.riseup.net/p'
pad_id = 'pptpabf-keep'

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

# Format the content by wrapping lines for readability (optional)
def format_content(content):
    wrapped_lines = []
    for line in content.splitlines():
        wrapped_lines.extend(textwrap.wrap(line, width=40))
    formatted_content = "\n".join(wrapped_lines)
    return formatted_content

# Print content to the printer
def print_to_printer(content):
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name
    try:
        play_sound()  # beepboop
        print("COUNTDOWN")
        countdown(5)  # 5 seconds
        subprocess.run(["lp", "-d", "Star_MCP31__STR_001_", temp_file_path], check=True) #change printer here
    except subprocess.CalledProcessError as e:
        print(f"Error printing to printer: {e}")
    finally:
        subprocess.run(["rm", temp_file_path])

# Countdown function (countdown from given number of seconds)
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{i}!!!")
        play_sound()  # Play sound during 54321
        time.sleep(1)  # 1 sec break inbetweem
    print("Printing now!!!!!!!!!!!!!!!!AHHHHHHHHHHHHHHHHHHHHH!!!")


# Beep boop beep boop printing beep boop
def play_sound():
    if os.name == 'posix':  # For Linux/macOS
        try:
            if 'Darwin' in os.uname().sysname:  # macOS
                os.system('osascript -e "beep"')  # Beep once on macOS
            else:  
                os.system("aplay /usr/share/sounds/alsa/Front_Center.wav")  
        except Exception as e:
            print(f"Error playing sound: {e}")

# print every 10 minutes
def periodic_print():
    while True:
        print("Getting the etherpad data")
        content = fetch_etherpad_text(etherpad_text_url)
        
        if content:
            formatted_content = format_content(content)
            
            print_to_printer(formatted_content)
        else:
            print("Failed to fetch content from Etherpad.")
        
        # 10 min = 600 sec
        print("10 min Break for our printers:3")
        time.sleep(600)

if __name__ == "__main__":
    periodic_print()
