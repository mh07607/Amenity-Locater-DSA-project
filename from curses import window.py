from tkinter import *
import Project

    
def clickbank(amenity='bank'):
    output.delete(0.0, END)
    result = Project.main(amenity, 2000)
    output.insert(INSERT, result)

def clickhospital(amenity='hospital'):
    output.delete(0.0, END)
    result = Project.main(amenity, 2000)
    output.insert(INSERT, result)

def clickworship(amenity='place_of_worship'):
    output.delete(0.0, END)
    result = Project.main(amenity, 2000)
    output.insert(INSERT, result)

def clickatm(amenity='atm'):
    output.delete(0.0, END)
    result = Project.main(amenity, 2000)
    output.insert(INSERT, result)

def Exit():
    window.destroy()
    exit()

window = Tk()
window.title("Nearest Amenity Finder")

Label(window, text = "Nearest Amenity finder", fg = 'black', font='none 20 bold').grid(row=1, column=0, sticky=N)
Label(window, text = "Select Amenity", fg = 'black', font='none 12 bold').grid(row=3, column=0, sticky=W)

Button(window, text='Banks', width = 6, command = clickbank).grid(row=4, column = 0, sticky = W)
Button(window, text='Atms', width = 6, command = clickatm).grid(row=5, column = 0, sticky = W)
Button(window, text='Masjids', width = 6, command = clickworship).grid(row=6, column = 0, sticky = W)
Button(window, text='Hospitals', width = 6, command = clickhospital).grid(row=7, column = 0, sticky = W)

output = Text(window, width=60, height=4, wrap = WORD, background = 'white')
output.grid(row=8, column = 0, columnspan = 2, sticky = W)

Label(window, text = "", fg = 'white', font='none 12 bold').grid(row=9, column=0, sticky=W)
Button(window, text='Exit', width = 6, command = Exit).grid(row=10, column = 0, sticky = W)

window.mainloop()
