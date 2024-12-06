#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, font
from datetime import datetime
import os
import math
import threading
import yt_dlp

class SmartText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Return>', self.smart_newline)
        self.bind('<Shift-Return>', self.normal_newline)

    def smart_newline(self, event):
        # Check if the current line starts with a bullet point
        current_line = self.get("insert linestart", "insert lineend")
        if current_line.strip().startswith('•'):
            # Insert a new bullet point on the next line
            self.insert(tk.INSERT, '\n• ')
            return 'break'  # Prevent default newline behavior
        return None

    def normal_newline(self, event):
        # Allow normal newline without bullet point
        self.insert(tk.INSERT, '\n')
        return 'break'

class CLIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dev Companion: Notes & Tools")
        self.geometry("800x700")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill='both')
        
        # Create tabs
        self.textpad_frame = ttk.Frame(self.notebook)
        self.ytdl_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.textpad_frame, text="Text Pad")
        self.notebook.add(self.ytdl_frame, text="Media Downloader")
        
        self.setup_textpad_tab()
        self.setup_ytdl_tab()

    def setup_ytdl_tab(self):
        # Media Downloader Layout
        ytdl_frame = ttk.Frame(self.ytdl_frame)
        ytdl_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Title
        title_label = ttk.Label(ytdl_frame, text="Media Downloader", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # URL Input Frame
        url_frame = ttk.Frame(ytdl_frame)
        url_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(url_frame, text="Video/Audio URL:", font=('Helvetica', 10)).pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50, font=('Helvetica', 10))
        self.url_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=10)

        # Platform Detection
        platform_frame = ttk.Frame(ytdl_frame)
        platform_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(platform_frame, text="Platform:").pack(side=tk.LEFT, padx=(0,10))
        self.platform_var = tk.StringVar(value="Auto Detect")
        platform_options = [
            "Auto Detect", 
            "YouTube", 
            "Vimeo", 
            "Facebook", 
            "Instagram", 
            "TikTok",
            "Other Video Sites"
        ]
        self.platform_dropdown = ttk.Combobox(platform_frame, textvariable=self.platform_var, values=platform_options, width=20)
        self.platform_dropdown.pack(side=tk.LEFT)

        # Options Frame
        options_frame = ttk.LabelFrame(ytdl_frame, text="Download Options", padding=(10, 5))
        options_frame.pack(fill='x', padx=10, pady=5)

        # Playlist/Multiple Media Options
        ttk.Label(options_frame, text="Media Limit:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.playlist_var = tk.StringVar(value="First 5 Items")
        playlist_options = [
            "First 5 Items", 
            "First 10 Items",
            "First 20 Items",
            "Entire Playlist/Collection", 
            "Single Item Only"
        ]
        self.playlist_dropdown = ttk.Combobox(options_frame, textvariable=self.playlist_var, values=playlist_options, width=20)
        self.playlist_dropdown.grid(row=0, column=1, padx=5, pady=2)

        # Download Type
        ttk.Label(options_frame, text="Download Type:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.download_type_var = tk.StringVar(value="Video + Audio")
        download_type_options = [
            "Video + Audio", 
            "Video Only (Highest Quality)", 
            "Audio Only (MP3)", 
            "Audio Only (WAV)",
            "Thumbnail/Cover"
        ]
        self.download_type_dropdown = ttk.Combobox(options_frame, textvariable=self.download_type_var, values=download_type_options, width=20)
        self.download_type_dropdown.grid(row=1, column=1, padx=5, pady=2)

        # Quality Options
        ttk.Label(options_frame, text="Video Quality:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.quality_var = tk.StringVar(value="Best Available")
        quality_options = [
            "Best Available", 
            "4K", 
            "1080p", 
            "720p", 
            "480p", 
            "360p"
        ]
        self.quality_dropdown = ttk.Combobox(options_frame, textvariable=self.quality_var, values=quality_options, width=20)
        self.quality_dropdown.grid(row=2, column=1, padx=5, pady=2)

        # Download Location
        ttk.Label(options_frame, text="Save Location:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.download_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads", "Media Downloads"))
        path_entry = ttk.Entry(options_frame, textvariable=self.download_path, width=30)
        path_entry.grid(row=3, column=1, padx=5, pady=2)
        ttk.Button(options_frame, text="Browse", command=self.browse_download_path).grid(row=3, column=2, padx=5, pady=2)

        # Subfolder Options
        ttk.Label(options_frame, text="Organize by:").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        self.subfolder_var = tk.StringVar(value="Platform")
        subfolder_options = [
            "Platform", 
            "Date", 
            "Content Type",
            "No Subfolders"
        ]
        self.subfolder_dropdown = ttk.Combobox(options_frame, textvariable=self.subfolder_var, values=subfolder_options, width=20)
        self.subfolder_dropdown.grid(row=4, column=1, padx=5, pady=2)

        # Download Button
        download_button = ttk.Button(ytdl_frame, text="Start Download", command=self.start_download, style='Accent.TButton')
        download_button.pack(pady=10)

        # Progress Frame
        progress_frame = ttk.LabelFrame(ytdl_frame, text="Download Progress", padding=(10, 5))
        progress_frame.pack(fill='x', padx=10, pady=5, expand=True)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=100, mode='determinate')
        self.progress_bar.pack(fill='x', padx=5, pady=5)

        # Status Label
        self.status_var = tk.StringVar(value="Ready to download")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, wraplength=500)
        status_label.pack(pady=5)

    def browse_download_path(self):
        path = filedialog.askdirectory()
        if path:
            # Ensure a Media Downloads folder
            media_path = os.path.join(path, "Media Downloads")
            os.makedirs(media_path, exist_ok=True)
            self.download_path.set(media_path)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video/audio URL")
            return

        # Reset progress
        self.progress_bar['value'] = 0
        self.status_var.set("Preparing download...")

        # Disable download button
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

    def download_video(self):
        try:
            url = self.url_entry.get().strip()
            download_path = self.download_path.get()
            platform = self.platform_var.get()
            playlist_choice = self.playlist_var.get()
            download_type = self.download_type_var.get()
            quality = self.quality_var.get()
            subfolder_option = self.subfolder_var.get()

            # Prepare yt-dlp options with more flexible output template
            if subfolder_option == "Platform":
                output_template = os.path.join(download_path, '%(extractor_key)s', '%(title)s.%(ext)s')
            elif subfolder_option == "Date":
                output_template = os.path.join(download_path, '%(upload_date>%Y-%m-%d)s', '%(title)s.%(ext)s')
            elif subfolder_option == "Content Type":
                output_template = os.path.join(download_path, '%(content_type)s', '%(title)s.%(ext)s')
            else:
                output_template = os.path.join(download_path, '%(title)s.%(ext)s')

            ydl_opts = {
                'outtmpl': output_template,
                'progress_hooks': [self.progress_hook],
                'no_color': True,
            }

            # Playlist/Collection handling
            if playlist_choice == "First 5 Items":
                ydl_opts['playlist_items'] = '1-5'
            elif playlist_choice == "First 10 Items":
                ydl_opts['playlist_items'] = '1-10'
            elif playlist_choice == "First 20 Items":
                ydl_opts['playlist_items'] = '1-20'
            elif playlist_choice == "Single Item Only":
                ydl_opts['noplaylist'] = True

            # Format and quality selection
            if download_type == "Video Only (Highest Quality)":
                ydl_opts['format'] = 'bestvideo'
            elif download_type == "Audio Only (MP3)":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                })
            elif download_type == "Audio Only (WAV)":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                    }]
                })
            elif download_type == "Thumbnail/Cover":
                ydl_opts.update({
                    'format': 'thumbnail',
                    'skip_download': True,
                })
            else:  # Video + Audio
                ydl_opts['format'] = 'bestvideo+bestaudio/best'

            # Quality filtering
            if quality != "Best Available":
                ydl_opts['format'] += f'[height<={quality[:-1]}]'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                
                # Determine number of items downloaded
                if 'entries' in info_dict:
                    downloaded_count = len(info_dict['entries'])
                    self.after(0, lambda: self.status_var.set(f"Downloaded {downloaded_count} item(s)"))
                else:
                    self.after(0, lambda: self.status_var.set("Downloaded 1 item"))

            self.after(0, self.download_complete)
        except Exception as e:
            self.after(0, lambda: self.download_error(str(e)))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%', '')
            try:
                progress = float(p)
                self.after(0, lambda: self.progress_bar.config(value=progress))
            except ValueError:
                pass
            
            downloaded = d.get('_downloaded_bytes_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            progress_msg = f"Downloading: {p}% | Downloaded: {downloaded} | Speed: {speed} | ETA: {eta}"
            self.after(0, lambda: self.status_var.set(progress_msg))

    def download_complete(self):
        self.progress_bar['value'] = 100
        self.status_var.set("Download completed successfully!")
        messagebox.showinfo("Success", "Media downloaded successfully!")

    def download_error(self, error):
        self.progress_bar['value'] = 0
        self.status_var.set("Download failed!")
        messagebox.showerror("Download Error", error)

    def setup_textpad_tab(self):
        # Textpad layout
        textpad_header = ttk.Frame(self.textpad_frame)
        textpad_header.pack(pady=5, padx=10, fill='x')

        # Header with title and buttons
        ttk.Label(textpad_header, text="Dev Thoughts Pad", font=('Helvetica', 14, 'bold')).pack(side=tk.LEFT)
        
        # Buttons frame
        textpad_buttons = ttk.Frame(self.textpad_frame)
        textpad_buttons.pack(pady=5, padx=10, fill='x')

        # Textpad buttons
        ttk.Button(textpad_buttons, text="Save Note", command=self.save_textpad_note).grid(row=0, column=0, padx=5)
        ttk.Button(textpad_buttons, text="Clear", command=self.clear_textpad).grid(row=0, column=1, padx=5)
        ttk.Button(textpad_buttons, text="Add Bullet", command=self.add_textpad_bullet).grid(row=0, column=2, padx=5)
        ttk.Button(textpad_buttons, text="Add Timestamp", command=self.add_textpad_timestamp).grid(row=0, column=3, padx=5)

        # Text area with custom Text widget for smart bullet points
        self.textpad = SmartText(self.textpad_frame, wrap=tk.WORD, height=20, width=80, 
                                 font=('Consolas', 11), 
                                 insertbackground='blue',  # Cursor color
                                 selectbackground='lightblue')
        self.textpad.pack(pady=10, padx=10, expand=True, fill='both')

        # Scrollbar for text area
        textpad_scrollbar = ttk.Scrollbar(self.textpad_frame, orient=tk.VERTICAL, command=self.textpad.yview)
        textpad_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.textpad.configure(yscrollcommand=textpad_scrollbar.set)

        # Saved notes list
        ttk.Label(self.textpad_frame, text="Saved Text Notes", font=('Helvetica', 12)).pack(pady=5)
        
        self.textpad_notes_list = tk.Listbox(self.textpad_frame, height=5, width=50)
        self.textpad_notes_list.pack(pady=5, padx=10, fill='x')
        
        # Load existing notes
        self.load_textpad_notes()

    def save_textpad_note(self):
        note_content = self.textpad.get("1.0", tk.END).strip()
        
        if not note_content:
            messagebox.showwarning("Warning", "Note is empty!")
            return

        # Create notes directory if it doesn't exist
        notes_dir = os.path.join(os.path.expanduser("~"), "DevThoughtsPad")
        os.makedirs(notes_dir, exist_ok=True)

        # Prompt for note name
        note_name = simpledialog.askstring("Save Note", "Enter a name for your note:", parent=self)
        if not note_name:
            note_name = "dev_thought"

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(notes_dir, f"{note_name}_{timestamp}.txt")

        # Save note
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(note_content)

        # Update notes list
        self.textpad_notes_list.insert(tk.END, f"{note_name}_{timestamp}.txt")
        
        messagebox.showinfo("Success", f"Note saved as {note_name}_{timestamp}.txt")

    def clear_textpad(self):
        self.textpad.delete("1.0", tk.END)

    def add_textpad_bullet(self):
        self.textpad.insert(tk.END, "• ")

    def add_textpad_timestamp(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.textpad.insert(tk.END, f"\n--- {timestamp} ---\n")

    def load_textpad_notes(self):
        notes_dir = os.path.join(os.path.expanduser("~"), "DevThoughtsPad")
        
        # Create directory if it doesn't exist
        os.makedirs(notes_dir, exist_ok=True)

        # List notes
        try:
            notes = os.listdir(notes_dir)
            for note in notes:
                self.textpad_notes_list.insert(tk.END, note)
        except Exception as e:
            print(f"Error loading notes: {e}")

def main():
    app = CLIApp()
    app.mainloop()

if __name__ == '__main__':
    main()
