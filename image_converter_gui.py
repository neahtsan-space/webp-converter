import os
import zipfile
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

class ImageConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Image to WebP Converter with Zip")
        master.geometry("500x500")

        self.label = tk.Label(master, text="Select a folder to convert images to WebP and zip them.")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(master, text="Browse Folder", command=self.select_folder)
        self.browse_button.pack()

        self.file_listbox = tk.Listbox(master, width=60, height=10)
        self.file_listbox.pack(pady=10)

        self.progress = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.convert_button = tk.Button(master, text="Start Conversion", command=self.convert_images)
        self.convert_button.pack(pady=10)

        self.folder_path = ""
        self.image_files = []

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.image_files = []
            self.file_listbox.delete(0, tk.END)

            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.lower().endswith(supported_extensions):
                        full_path = os.path.join(root, file)
                        self.image_files.append(full_path)
                        self.file_listbox.insert(tk.END, os.path.relpath(full_path, self.folder_path))

            if not self.image_files:
                messagebox.showinfo("No Images Found", "No supported image files were found.")

    def convert_images(self):
        if not self.folder_path or not self.image_files:
            messagebox.showwarning("Warning", "Please select a folder with images first.")
            return

        output_folder = os.path.join(self.folder_path, "converted_webp")
        os.makedirs(output_folder, exist_ok=True)

        webp_files = []
        self.progress["maximum"] = len(self.image_files)
        self.progress["value"] = 0
        self.master.update_idletasks()

        for i, img_path in enumerate(self.image_files):
            try:
                img = Image.open(img_path).convert("RGB")
                relative_path = os.path.relpath(img_path, self.folder_path)
                output_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.webp')
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img.save(output_path, 'webp')
                webp_files.append(output_path)
            except Exception as e:
                print(f"Failed to convert {img_path}: {e}")
            self.progress["value"] = i + 1
            self.master.update_idletasks()

        if webp_files:
            zip_path = os.path.join(self.folder_path, "converted_images.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in webp_files:
                    arcname = os.path.relpath(file, self.folder_path)
                    #zipf.write(file, arcname)

            messagebox.showinfo("Done", f"Converted {len(webp_files)} images to WebP and zipped them into:\n{zip_path}")
        else:
            messagebox.showinfo("No Conversion", "No files were successfully converted.")

        # Clear file list and reset progress bar
        self.image_files = []
        self.file_listbox.delete(0, tk.END)
        self.progress["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
