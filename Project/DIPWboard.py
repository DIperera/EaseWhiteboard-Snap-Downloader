import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab

class Whiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🖊️ DIPWboard byIshiraPerera")
        self.root.geometry("800x600")
        self.root.config(bg="white")

        # Frame with black border to contain the canvas
        self.border_frame = tk.Frame(self.root, bg="black", padx=2, pady=2)
        self.border_frame.pack(pady=10)

        # Canvas inside the frame
        self.canvas = tk.Canvas(self.border_frame, bg="white", width=780, height=500, highlightthickness=0)
        self.canvas.pack()

        # Download button
        download_btn = tk.Button(self.root, text="Download Drawing 🖼️", command=self.download)
        download_btn.pack(pady=10)

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Drawing state
        self.old_x = None
        self.old_y = None

    def draw(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=3, fill='black', capstyle=tk.ROUND, smooth=True)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def download(self):
        # Get canvas location and dimensions
        x = self.root.winfo_rootx() + self.canvas.winfo_rootx()
        y = self.root.winfo_rooty() + self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        # Grab only the canvas area (inside the black border)
        image = ImageGrab.grab(bbox=(x, y, x1, y1))

        # Save dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
                                                 title="Save Drawing")
        if file_path:
            image.save(file_path)
            print("Drawing saved as:", file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = Whiteboard(root)
    root.mainloop()
