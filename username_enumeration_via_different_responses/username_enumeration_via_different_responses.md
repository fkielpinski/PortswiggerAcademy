## Identify vulnerability
export TARGET="https://<random-url>.web-security-academy.net"

To interact with a login form programmatically, we first need to identify the name attributes of the username and password input fields. These attributes tell us what parameters to send in our requests.

We can use curl to fetch the raw HTML of the login page and extract the relevant form elements:

```
curl -s $TARGET/login | grep -E "<form|<input"
```
Even when submitting incorrect credentials, the server might always return a 200 OK status. However, differences in the response body can still reveal whether a username is valid. To analyze these variations, we can compare responses using `curl` and `diff`.

```
diff <(echo "$(curl -s -X POST "$TARGET/login" -d "username=test&password=test")") \
     <(echo "$(curl -s "$TARGET/login")")
```

<                         <p class=is-warning>Invalid username</p>

This response suggests that application might give different response if we use correct username. We can automate the process with Python. 


