# circle2.py
import tkinter
tk = tkinter.Tk()
tk.title("Circle")
def spin():    
    strvar.set(3.14159*(float(intvar.get()))**2)
intvar = tkinter.IntVar()
strvar = tkinter.StringVar()
label=tkinter.Label(tk, textvariable=strvar).grid(
                    row=0,column=0, padx=10,pady=10)
spinbox=tkinter.Spinbox(tk, textvariable=intvar, from_=0, to=100, 
                        command=spin).grid(row=1,column=0, padx=10,pady=10)
tk.mainloop()




























