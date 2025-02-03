import os
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import tarfile
import gzip
from pathlib import Path


class NanoHub:
    def __init__(self, root):
        self.root = root
        self.root.title("NanoHub - File Compressor/Decompressor")

        self.compress_button = tk.Button(
            root, text="Compress File", command=self.compress_file
        )
        self.compress_button.pack(pady=10)

        self.decompress_button = tk.Button(
            root, text="Decompress File", command=self.decompress_file
        )
        self.decompress_button.pack(pady=10)

    def compress_file(self):
        file_path = filedialog.askopenfilename(title="Select a File to Compress")
        if not file_path:
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Compressed File As", defaultextension=".zip"
        )
        if not save_path:
            return

        try:
            if save_path.endswith(".zip"):
                with zipfile.ZipFile(save_path, "w") as zf:
                    zf.write(file_path, os.path.basename(file_path))
            elif save_path.endswith(".tar.gz"):
                with tarfile.open(save_path, "w:gz") as tar:
                    tar.add(file_path, arcname=os.path.basename(file_path))
            elif save_path.endswith(".gz"):
                with open(file_path, "rb") as f_in:
                    with gzip.open(save_path, "wb") as f_out:
                        f_out.writelines(f_in)
            else:
                messagebox.showerror("Error", "Unsupported compression format")
                return

            messagebox.showinfo("Success", "File Compressed Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed: {e}")

    def decompress_file(self):
        file_path = filedialog.askopenfilename(title="Select a File to Decompress")
        if not file_path:
            return

        save_dir = filedialog.askdirectory(title="Select Directory to Extract Files")
        if not save_dir:
            return

        try:
            if file_path.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zf:
                    zf.extractall(save_dir)
            elif file_path.endswith(".tar.gz"):
                with tarfile.open(file_path, "r:gz") as tar:
                    tar.extractall(save_dir)
            elif file_path.endswith(".gz"):
                with gzip.open(file_path, "rb") as f_in:
                    out_file_path = Path(save_dir) / Path(file_path).stem
                    with open(out_file_path, "wb") as f_out:
                        f_out.write(f_in.read())
            else:
                messagebox.showerror("Error", "Unsupported decompression format")
                return

            messagebox.showinfo("Success", "File Decompressed Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Decompression failed: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NanoHub(root)
    root.mainloop()