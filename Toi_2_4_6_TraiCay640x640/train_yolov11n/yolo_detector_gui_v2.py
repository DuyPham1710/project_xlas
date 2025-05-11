import	tkinter	as	tk
from tkinter.filedialog import Open
from PIL import Image, ImageTk
import numpy as np
import cv2


from ultralytics import YOLO
from ultralytics.utils import plotting
import supervision as sv

import shutil
import os

class	App(tk.Tk):
    def	__init__(self):
        super().__init__()
        self.imgin = None
        self.model = YOLO('yolov8n_trai_cay.pt',task="detect")
        #self.model = YOLO('best.pt',task="detect")
        self.resizable(False, False)


        self.title('Phát hiện trái cây dùng yolo11')
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open Image", command = self.mnu_open_image_click)
        file_menu.add_command(label="Predict", command = self.mnu_predict_click)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu)


        self.cvs_image = tk.Canvas(self, relief = tk.SUNKEN, border = 1, 
                                   width = 640, height = 640)
        
        self.cvs_image.grid(row = 0, column = 0, padx = 5, pady = 5)

    def mnu_open_image_click(self):
        ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png')]
        dlg = Open(self, filetypes = ftypes)
        filename = dlg.show()
        if filename != '':
            image = Image.open(filename).convert('RGB')
            self.imgin = np.array(image)[:, :, ::-1].copy()
            self.image_tk = ImageTk.PhotoImage(image)
            self.cvs_image.create_image(0, 0, anchor = tk.NW, image = self.image_tk)


    def mnu_predict_click(self):
        results = self.model.predict(source=self.imgin,conf= 0.5)
        plotting.plot_images()
        img = self.imgin.copy()
        for result in results:
            boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy format
            for box in boxes:  # Iterate over boxes
                r = box.xyxy[0].astype(int)  # Get corner points as int
                class_id = int(box.cls[0])  # Get class ID
                class_name = self.model.names[class_id]  # Get class name using the class ID
                print(f"Class: {class_name}, Box: {r}")  # Print class name and box coordinates
                cv2.rectangle(img, r[:2], r[2:], (0, 255, 0), 2)  # Draw boxes on the image
        cv2.imshow("ImageOut",img)


if	__name__	==	"__main__":
    app	=	App()
    app.mainloop()
