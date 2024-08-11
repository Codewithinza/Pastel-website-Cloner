import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")

def save_html(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def apply_pastel_theme(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Adding pastel CSS theme
    pastel_css = """
    <style>
        body {
            background-color: #f5f5f5;
            color: #333;
            font-family: Arial, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #f48fb1;
        }
        a {
            color: #81c784;
        }
        a:hover {
            color: #66bb6a;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        img {
            border-radius: 8px;
        }
    </style>
    """

    # Insert pastel CSS into the head of the HTML
    if soup.head:
        soup.head.append(BeautifulSoup(pastel_css, 'html.parser'))
    else:
        new_head = soup.new_tag("head")
        soup.html.insert(0, new_head)
        new_head.append(BeautifulSoup(pastel_css, 'html.parser'))
    
    return str(soup)

def clone_page(url, save_path):
    html_content = fetch_page(url)
    themed_html = apply_pastel_theme(html_content)
    save_html(themed_html, save_path)
    messagebox.showinfo("Success", f"Page cloned and saved as {save_path} with pastel theme.")

def on_clone_button_click():
    url = url_entry.get()
    if url:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if save_path:
            try:
                clone_page(url, save_path)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Save Error", "No file selected.")
    else:
        messagebox.showwarning("Input Error", "Please enter a URL.")

# Create GUI
root = tk.Tk()
root.title("Pastel Webpage Cloner")

tk.Label(root, text="Enter the URL of the webpage to clone:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

clone_button = tk.Button(root, text="Clone Page", command=on_clone_button_click)
clone_button.pack(pady=20)

root.mainloop()
