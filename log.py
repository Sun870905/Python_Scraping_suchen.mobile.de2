from datetime import datetime
from colorama import init, Fore
class Log:
    def __init__(self, log=True, logfile="error-logs.html"):
        init(autoreset=True)
        self.log = log
        self.logfile = logfile

    def get_time(self):
        date = datetime.now()
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def green_text(self, text):
        return Fore.LIGHTGREEN_EX + str(text) + Fore.RESET

    def blue_text(self, text):
        return Fore.LIGHTBLUE_EX + str(text) + Fore.RESET

    def red_text(self, text):
        return Fore.LIGHTRED_EX + str(text) + Fore.RESET

    def yellow_text(self, text):
        return Fore.LIGHTYELLOW_EX + str(text) + Fore.RESET

    def __get_bot_badge(self):
        return Fore.LIGHTBLUE_EX + "  BOT  " + Fore.RESET

    def __get_browser_badge(self):
        return Fore.YELLOW + "BROWSER" + Fore.RESET

    def write_log(self, badge="bot", msg=" "):
        if badge.upper() == "BOT":
            bot_log = f"[ {self.get_time()} ]"
            print(f"{bot_log} [{self.__get_bot_badge()}] {msg}")
            with open(self.logfile, "a") as log:
                log.write(f"<p>{bot_log} [  BOT  ] {msg}</p>")
        elif badge.upper() == "BROWSER":
            browser_log = f"[ {self.get_time()} ]"
            print(f"{browser_log} [{self.__get_browser_badge()}] {msg}")
            with open(self.logfile, "a") as log:
                log.write(f"<p>{browser_log} [  BROWSER  ] {msg}</p>")

    def error_log(self, error_msg):
        if self.log:
            with open(self.logfile, "a") as log:
                error_msg_line = f'[ {self.get_time()} ] [  ERROR  ] {str(error_msg)}'
                log.write(f"<p>{error_msg_line}</p>")