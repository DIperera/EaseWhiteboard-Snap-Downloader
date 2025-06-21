import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab

class Whiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard 🖊️")
        self.root.geometry("800x600")
        self.root.config(bg="white")

        # Frame with black border for canvas
        self.border_frame = tk.Frame(self.root, bg="black", padx=2, pady=2)
        self.border_frame.pack(pady=10)

        # Canvas inside the border
        self.canvas = tk.Canvas(self.border_frame, bg="white", width=780, height=500, highlightthickness=0)
        self.canvas.pack()

        # Controls frame
        controls = tk.Frame(self.root, bg="white")
        controls.pack(pady=10)

        # Download button
        download_btn = tk.Button(controls, text="Download Drawing 🖼️", command=self.download)
        download_btn.pack(side=tk.LEFT, padx=10)

        # Eraser button
        self.eraser_btn = tk.Button(controls, text="Eraser 🩹", command=self.toggle_eraser)
        self.eraser_btn.pack(side=tk.LEFT, padx=10)

        # Mouse events
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Drawing state
        self.old_x = None
        self.old_y = None
        self.eraser_on = False

    def toggle_eraser(self):
        self.eraser_on = not self.eraser_on
        if self.eraser_on:
            self.eraser_btn.config(bg="gray")
        else:
            self.eraser_btn.config(bg=self.root.cget("bg"))  # reset to normal background

    def draw(self, event):
        if self.old_x and self.old_y:
            color = 'white' if self.eraser_on else 'black'
            width = 20 if self.eraser_on else 3
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=width, fill=color, capstyle=tk.ROUND, smooth=True)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def download(self):
        # Get canvas position
        x = self.root.winfo_rootx() + self.canvas.winfo_rootx()
        y = self.root.winfo_rooty() + self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        # Grab image and save
        image = ImageGrab.grab(bbox=(x, y, x1, y1))
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
