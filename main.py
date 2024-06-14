import tkinter as tk
from PIL import Image, ImageTk
import fitz  # PyMuPDF


class PDFViewer:
    def __init__(self, root, pdf_path):
        self.root = root
        self.root.title("PDF Viewer")
        self.pdf_document = None

        # Open the PDF file
        self.open_pdf(pdf_path)

        # Create a frame for the canvas and scrollbar
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=1)

        # Create a canvas to display the PDF pages with fixed width
        self.canvas_width = 480  # Fixed canvas width
        self.canvas = tk.Canvas(self.frame, width=self.canvas_width)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create an internal frame to hold the PDF pages
        self.internal_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.internal_frame, anchor="nw")

        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind canvas resize event
        self.canvas.bind('<Configure>', self.on_canvas_resize)

        self.display_pdf()

    def on_canvas_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.yview_moveto(0)

    def display_pdf(self):
        for widget in self.internal_frame.winfo_children():
            widget.destroy()

        if self.pdf_document:
            for page_num in range(len(self.pdf_document)):
                page = self.pdf_document.load_page(page_num)
                # Remove margins by cropping
                pix = self.get_cropped_pixmap(page)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                photo = ImageTk.PhotoImage(image=img)

                label = tk.Label(self.internal_frame, image=photo)
                label.image = photo  # Keep a reference to the image to prevent garbage collection
                label.pack()

            # Update the canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
            self.canvas.yview_moveto(0)

    def get_cropped_pixmap(self, page):
        """ Crop the PDF page by 2.5 cm from each side and return a pixmap. """
        crop_margin = 60.87  # in points

        rect = page.rect
        cropped_rect = fitz.Rect(rect.x0 + crop_margin, rect.y0 + crop_margin, rect.x1 - crop_margin,
                                 rect.y1 - crop_margin)
        page.set_cropbox(cropped_rect)
        pix = page.get_pixmap()
        return pix

    def open_pdf(self, file_path):
        self.pdf_document = fitz.open(file_path)

    def run(self):
        self.root.mainloop()

pdf_path = 'C:\\Users\\Admin\\Documents\\Notariat\\umowa sprzedaży zabudowanej nieruchomości\\28.03.2024 sprzedaż zabudowanej Łygas.pdf'
root = tk.Tk()
pdf_viewer = PDFViewer(root, pdf_path)
root.mainloop()
