from tkinter import *
from tkinter import filedialog

def get_file():
    dirname = filedialog.askdirectory(parent=app,
                                      initialdir="/",
                                      title='Please select a directory')
    txt.getvar(dirname)

app = Tk()
app.title('TrajPy')
app.geometry('400x400')
lbl = Label(app, text="TrajPy", font=("Arial Bold", 28))
lbl.grid(column=0, row=0)
txt = Entry(app, width=50)

txt.grid(column=0, row=5)
btn = Button(app, text="Find", command=get_file)
btn.grid(column=1, row=5)


app.mainloop()

