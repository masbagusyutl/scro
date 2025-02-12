import requests
import time
import random
from datetime import datetime, timedelta

# Function to read cookies from data.txt
def read_cookies():
    with open('data.txt', 'r') as file:
        cookies = file.readlines()
    return cookies

# Function to make POST requests
def make_post_request(url, cookies, payload=None):
    headers = {
        'Cookie': cookies,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

# Function to display countdown with moving time
def display_countdown(duration):
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        remaining = end_time - datetime.now()
        print(f"Countdown: {remaining}", end='\r')
        time.sleep(1)
    print("\nCountdown: Time's up!")

# Function to claim farming
def claim_farming(cookies):
    status_code = make_post_request('https://game.scroo-g.com/api/miner:claim', cookies)
    return status_code == 200

# Function to check farming status
def check_farming_status(cookies):
    status_code = make_post_request('https://game.scroo-g.com/api/miner:list', cookies)
    return status_code == 200

# Function to crack eggs with a time limit
def crack_eggs(cookies, account_index, total_accounts, time_limit_minutes):
    game_id = 347063
    total_points = 0
    actions_list = ["tap"] * 3 + ["tap-x2"]  # Majority are "tap" (3 times more likely)
    end_time = datetime.now() + timedelta(minutes=time_limit_minutes)

    while datetime.now() < end_time:
        action = random.choice(actions_list)
        points = 1 if action == "tap" else 2
        payload = {
            "game_id": game_id,
            "actions": [action]
        }
        status_code = make_post_request('https://game.scroo-g.com/api/game:failing-eggs:action', cookies, payload)
        if status_code == 200:
            total_points += points
        print(f"Account {account_index}/{total_accounts}: Crack eggs action: {action}, Points: {total_points}, Status code: {status_code}")
        time.sleep(random.uniform(0.5, 2))  # Random delay between actions

# Main function to process accounts
def process_accounts():
    cookies_list = read_cookies()
    num_accounts = len(cookies_list)
    print(f"Total accounts found: {num_accounts}")

    time_limit_minutes = 30  # 30-minute time limit per account

    for idx, cookies in enumerate(cookies_list, start=1):
        cookies = cookies.strip()
        print(f"Processing account {idx}/{num_accounts}")

        # Claim farming
        farming_claimed = claim_farming(cookies)
        if farming_claimed:
            print(f"Account {idx}/{num_accounts}: Farming reward claimed.")
        else:
            print(f"Account {idx}/{num_accounts}: Failed to claim farming reward or already claimed.")

        # Crack eggs within the time limit
        crack_eggs(cookies, idx, num_accounts, time_limit_minutes)

        # Adding 5-second delay between account switches
        if idx < num_accounts:
            time.sleep(5)

    # Check if farming task is completed
    farming_status = check_farming_status(cookies_list[0].strip())
    if farming_status:
        print("Farming task is already completed for today.")
    else:
        print("Farming task is not completed yet. Proceeding to claim farming reward.")
        claim_farming(cookies_list[0].strip())

    # Start 1-hour countdown timer
    print("All accounts processed. Starting 1-hour countdown.")
    display_countdown(3600)  # 3600 seconds = 1 hour

    # Restart the process
    print("Restarting the process...")
    process_accounts()

# Starting the process
process_accounts()
