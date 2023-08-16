import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random


class TextImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Image Generator")

        self.text_entry = tk.Text(root, width=40, height=5)
        self.text_entry.pack()

        self.generate_button = tk.Button(root, text="Generate Image", command=self.generate_image)
        self.generate_button.pack()

        self.watermark_entry = tk.Entry(root)
        self.watermark_entry.pack()

        self.add_watermark_button = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack()

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.watermarks = []
        self.dense_watermark_percent = tk.DoubleVar()
        self.dense_watermark_percent.set(10.0)

        self.text_size_var = tk.IntVar()
        self.text_size_var.set(30)  # Default text size

        self.dense_label = tk.Label(root, text="Dense Watermark Percentage:")
        self.dense_label.pack()

        self.dense_slider = tk.Scale(root, from_=0.0, to=100.0, variable=self.dense_watermark_percent,
                                     orient=tk.HORIZONTAL)
        self.dense_slider.pack()

        self.text_size_label = tk.Label(root, text="Text Size:")
        self.text_size_label.pack()

        self.text_size_slider = tk.Scale(root, from_=10, to=100, variable=self.text_size_var, orient=tk.HORIZONTAL)
        self.text_size_slider.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack(fill=tk.BOTH, expand=True)  # Fill the available space

        self.root.bind("<Configure>", self.on_window_resize)  # Bind the window resize event

    def generate_image(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        text_size = self.text_size_var.get()

        image = Image.new("RGB", (500, 800), "white")
        draw = ImageDraw.Draw(image)

        font_path = "simsun.ttc"
        font = ImageFont.truetype(font_path, text_size)
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (image.width - text_width) // 2
        text_y = (image.height - text_height) // 2
        draw.text((text_x, text_y), text, fill="black", font=font)

        watermark_font = ImageFont.truetype(font_path, 20)
        watermark_spacing = int((100 - self.dense_watermark_percent.get()) / 100 * 100)
        for watermark_text in self.watermarks:
            text_width, text_height = draw.textsize(watermark_text, font=watermark_font)
            for x in range(0, image.width, text_width + watermark_spacing):
                for y in range(0, image.height, text_height + watermark_spacing):
                    angle = random.randint(-30, 30)
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    watermark_image = Image.new("RGBA", (text_width, text_height))
                    watermark_draw = ImageDraw.Draw(watermark_image)
                    watermark_draw.text((0, 0), watermark_text, fill=color, font=watermark_font)
                    rotated_watermark = watermark_image.rotate(angle, expand=1)
                    image.paste(rotated_watermark, (x, y), rotated_watermark)

        self.generated_image = image

        self.show_image(image)

    def save_image(self):
        if hasattr(self, "generated_image"):
            self.generated_image.save("generated_image.png")

    def reset(self):
        if hasattr(self, "generated_image"):
            delattr(self, "generated_image")
        self.watermarks = []
        self.text_entry.delete("1.0", tk.END)
        self.watermark_entry.delete(0, tk.END)
        self.show_blank_image()

    def add_watermark(self):
        watermark_text = self.watermark_entry.get()
        if watermark_text:
            self.watermarks.append(watermark_text)
            self.generate_image()

    def on_window_resize(self, event):
        if hasattr(self, "image"):
            self.show_image(self.generated_image)

    def show_image(self, image):
        width, height = self.image_label.winfo_width(), self.image_label.winfo_height()
        resized_image = image.resize((width, height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image=resized_image)
        self.image_label.configure(image=self.photo)
        self.image_label.image = self.photo  # Keep a reference to avoid garbage collection

    def show_blank_image(self):
        blank_image = Image.new("RGB", (500, 800), "white")
        self.show_image(blank_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = TextImageGenerator(root)
    app.show_blank_image()
    root.mainloop()
