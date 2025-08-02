from fileinput import filename
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog as fd
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfile
root = tk.Tk()
root.title('Brain tumor')
canvas= tk.Canvas(root, width=600, height=500)
canvas.grid(columnspan=3, rowspan=3)

instruction=tk.Label(root, text="Enter image for prediction",font=('Helvetica', 20))
instruction.grid(columnspan=3,column=0, row=0)

def select_file():
    filetypes = (
        ('Images', '*.jpg'),
        ('Images', '*.png'),
    )
    global imagePath

    imagePath = fd.askopenfilename(
        title='Open a file',
        initialdir='./pred',
        filetypes=filetypes)

    if imagePath == "":
        showerror(
            title='Error Image',
            message="Please Choose an image"
        )
        select_file()
    else:
        img = Image.open(imagePath)
        width, height = img.size
        img = img.resize((round(250/height*width) , round(300)))
        # img=ImageTk.PhotoImage(Image.open(filename).resize((round(680/height*width) , round(680))))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(image=img)
        label.img=img
        label.grid(column=1, row=1)        

def scanImage():
    try:
        imagePath
        import cv2
        from keras.models import load_model
        from PIL import Image
        import numpy as np

        model = load_model('BrainTumor10Epochs.h5')
        image = cv2.imread(filename=imagePath)
        img = Image.fromarray(image)
        img = img.resize((64,64))
        img = np.array(img)
        input_img = np.expand_dims(img, axis=0)

        result = (model.predict(input_img) > 0.5).astype("int32")
        
        if(result[0] == 0):
            showinfo(
                title='Result',
                message="No"
            )
        else:
            showinfo(
                title='Result',
                message="Yes"
            )
    except NameError:
        showerror(
            title='Error Image',
            message="Please Choose an image"
        )
        select_file()
    


browse_button = tk.Button(root, text='browse', command=select_file, font=('Helvetica', 15), width=15, height=2, bg='light green')
browse_button.grid(column=0, row=2)        

browse_button = tk.Button(root, text='scan', command=scanImage, font=('Helvetica', 15), width=15, height=2, bg='light grey')
browse_button.grid(column=1, row=2)        

button = tk.Button(root, text='Exit', command=root.destroy, font=('Helvetica', 15), width=15, height=2, bg='light blue')
button.grid(column=2, row=2)

canvas= tk.Canvas(root, width=200, height=30)
canvas.grid(columnspan=4)

root.mainloop()