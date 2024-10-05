import os
import requests
from urllib.parse import urljoin, unquote, urlparse
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END

class FileDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Downloader")
        self.download_links = []

        self.url_label = tk.Label(root, text="Enter Page URL:")
        self.url_label.pack(padx=10, pady=5)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(padx=10, pady=5)

        self.fetch_button = tk.Button(root, text="Fetch Downloadable Content", command=self.on_fetch_click)
        self.fetch_button.pack(padx=10, pady=5)

        self.listbox_frame = tk.Frame(root)
        self.listbox_frame.pack(padx=10, pady=5)

        self.scrollbar = Scrollbar(self.listbox_frame, orient="vertical")
        self.listbox = Listbox(self.listbox_frame, selectmode="multiple", yscrollcommand=self.scrollbar.set, width=80, height=15)

        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)

        self.download_button = tk.Button(root, text="Download Selected Files", command=self.on_download_click)
        self.download_button.pack(padx=10, pady=10)

        self.select_all_button = tk.Button(root, text="Select All", command=self.on_select_all_click)
        self.select_all_button.pack(padx=10, pady=5)

    def fetch_downloadable_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            download_links = []
            for link in soup.find_all('a', href=True):
                file_url = link['href']
                full_file_url = urljoin(url, file_url)
                if full_file_url.endswith(('.zip', '.pdf', '.exe', '.mp3', '.mp4', '.jpg')):
                    parsed_url = urlparse(full_file_url)
                    filename = os.path.basename(parsed_url.path)
                    decoded_filename = unquote(filename)
                    download_links.append((decoded_filename, full_file_url))
            
            return download_links
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch content: {e}")
            return None

    def on_fetch_click(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        
        self.download_links = self.fetch_downloadable_content(url)
        
        if self.download_links:
            self.listbox.delete(0, END)
            for display_name, _ in self.download_links:
                self.listbox.insert(END, display_name)
        else:
            messagebox.showinfo("Info", "No downloadable content found.")

    def download_selected_files(self, selected_links, folder='downloads'):
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        for link in selected_links:
            try:
                filename = os.path.basename(urlparse(link).path)
                if not filename:
                    filename = 'downloaded_file'
                
                filepath = os.path.join(folder, filename)
                response = requests.get(link, stream=True)
                response.raise_for_status()

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"Downloaded: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download {link}: {e}")

    def on_download_click(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one file to download.")
            return
        
        selected_links = [self.download_links[i][1] for i in selected_indices]
        self.download_selected_files(selected_links)
        messagebox.showinfo("Success", "Selected files have been downloaded.")

    def on_select_all_click(self):
        self.listbox.select_set(0, END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileDownloaderApp(root)
    root.mainloop()
