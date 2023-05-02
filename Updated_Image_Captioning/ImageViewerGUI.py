from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
from model import *
import os

def open_img():

    global filename

    filename = filedialog.askopenfilename(title='open', filetypes=[("Image Files", "*.png *.jpeg *.jpg")])

    text.configure(state="normal")
    text.delete(1.0, END)
    text.insert(END, filename.split("/")[-1])
    text.configure(state="disabled")

    img = Image.open(filename)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    panel = Label(root, image=img)
    panel.image = img
    panel.grid(row=1, column=0, columnspan=2)

def out(results, type):

    if type == "Captioning":
        return "Top 3 captions\n\n" + "\n".join(results)

    elif type == "Classification":
        return "Top 3 classes\n\n" + "\n".join(["{}: {} %".format( it[1], float(it[0])*100 ) for it in results])

def _process():

    global filename

    option = clicked.get()
    if option == "Captioning":
        _model = ImageCaptioningModel()

    elif option == "Classification":
        _model = ImageClassificationModel()

    try:
        result = out(_model(filename), option)

        text_panel.config(text="")
        text_panel.config(text=result)

    except NameError:
        messagebox.showerror("Error", "Select a File!")

if __name__ == "__main__":

    root = Tk()
    root.title("Image Processor")

    options = ["Captioning", "Classification"]
    clicked = StringVar()
    clicked.set(options[0])

    drop = OptionMenu(root, clicked, *options)
    drop.grid(row=0, column=2)

    process = Button(root, text="Process", command=_process)
    process.grid(row=0, column=3)

    text = Text(root, bg="white", height=1, width=32)
    text.configure(state="disabled")
    text.grid(row=0, column=0)

    text_panel = Label(root)
    text_panel.grid(row=1, column=2, columnspan=2)

    btn = Button(root, text='Open', command=open_img).grid(row=0, column=1)

    root.mainloop()
