import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_selenium_task():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.google.com")
    # Perform other Selenium actions here
    driver.quit()

root = tk.Tk()
root.title("Selenium GUI")

run_button = tk.Button(root, text="Run Selenium", command=run_selenium_task)
run_button.pack()

root.mainloop()