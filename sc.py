import requests
import time
from datetime import datetime, timedelta

# Function to read cookies from data.txt
def read_cookies():
    with open('data.txt', 'r') as file:
        cookies = file.readlines()
    return cookies

# Function to make POST requests
def make_post_request(url, cookies):
    headers = {
        'Cookie': cookies,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    return response.status_code

# Function to display countdown with moving time
def display_countdown(duration):
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        remaining = end_time - datetime.now()
        print(f"Countdown: {remaining}", end='\r')
        time.sleep(1)
    print("Countdown: Time's up!")

# Main function to process accounts
def process_accounts():
    cookies_list = read_cookies()
    num_accounts = len(cookies_list)
    print(f"Total accounts found: {num_accounts}")

    for idx, cookies in enumerate(cookies_list, start=1):
        print(f"Processing account {idx}/{num_accounts}")
        status_code1 = make_post_request('https://game.scroo-g.com/api/game:reward', cookies.strip())
        status_code2 = make_post_request('https://game.scroo-g.com/api/miner:reward', cookies.strip())

        print(f"Status codes: URL1 - {status_code1}, URL2 - {status_code2}")
        
        # Adding 5-second delay between account switches
        if idx < num_accounts:
            time.sleep(5)

    # Start 1-hour countdown timer
    print("All accounts processed. Starting 1-hour countdown.")
    display_countdown(3600)  # 3600 seconds = 1 hour

    # Restart the process
    print("Restarting the process...")
    process_accounts()

# Starting the process
process_accounts()
