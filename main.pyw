import os  # Add this line
import time
import requests
from plyer import notification
import tkinter as tk
from threading import Thread

class WebsiteMonitor:
    def __init__(self, url_file='url.txt', interval=15):
        self.url_file = url_file
        self.interval = interval
        self.site_was_up = None
        self.running = False

    def read_url(self):
        with open(self.url_file, 'r') as file:
            return file.read().strip()

    def write_url(self, url):
        with open(self.url_file, 'w') as file:
            file.write(url)

    def check_website(self):
        url = self.read_url()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False

    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=8
        )

    def monitor(self):
        while self.running:
            site_is_up = self.check_website()
            if site_is_up:
                self.send_notification("The website is Available", "The website page is now accessible!")
                self.site_was_up = True
            elif not site_is_up and self.site_was_up is not False:
                self.send_notification("The website is Unavailable", "The website page is not accessible!")
                self.site_was_up = False
            time.sleep(self.interval)

    def start(self):
        self.running = True
        thread = Thread(target=self.monitor)
        thread.start()

    def stop(self):
        self.running = False

class GUI:
    def __init__(self, master):
        self.master = master
        self.monitor = WebsiteMonitor()
        
        if not os.path.exists('url.txt'):
            self.monitor.write_url("http://127.0.0.1:8000/")

        self.start_button = tk.Button(master, text="Start", command=self.start_monitoring, width=20, height=2, bg="green", fg="white")
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_monitoring, state=tk.DISABLED, width=20, height=2, bg="red", fg="white")
        self.stop_button.pack(pady=20)

        self.settings_button = tk.Button(master, text="Settings", command=self.open_settings, width=20, height=2, bg="blue", fg="white")
        self.settings_button.pack(pady=20)

    def start_monitoring(self):
        self.monitor.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_monitoring(self):
        self.monitor.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def check_internet(self):
        try:
            requests.head('https://www.google.com', timeout=1)
            return True
        except requests.ConnectionError:
            return False

    def monitor_internet(self):
        while True:
            if not self.check_internet():
                self.send_notification("Internet Connection Lost", "Your internet connection is not working!")
            time.sleep(5)

    def start_internet_monitoring(self):
        thread = Thread(target=self.monitor_internet)
        thread.start()

    def open_settings(self):
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")
        self.settings_window.geometry("350x150")

        self.url_label = tk.Label(self.settings_window, text="Enter URL:")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(self.settings_window, width=50)
        self.url_entry.insert(0, self.monitor.read_url())
        self.url_entry.pack(pady=10)

        self.save_button = tk.Button(self.settings_window, text="Save", command=self.save_settings, width=20, height=2, bg="green", fg="white")
        self.save_button.pack(pady=10)

    def save_settings(self):
        new_url = self.url_entry.get()
        self.monitor.write_url(new_url)
        self.settings_window.destroy()

root = tk.Tk()
root.title("Website Monitor")
root.geometry("300x250")
gui = GUI(root)
gui.start_internet_monitoring()
root.mainloop()
