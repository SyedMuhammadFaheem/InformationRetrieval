from tkinter import *
from tkinter import messagebox
import Queries

'''This module is responsible for the GUI through which the user can input his/her query and get the 
desired output. The design is very minimal and user friendly. It consists of an entry box to write 
the query and 'Search' button to execute it'''

root = Tk()

# handles the relevant function callings to load the dictionary terms and positional index and to execute the query
def getResult():
    QueryObj = Queries.Queries()
    QueryObj.printPositionalIndex()
    QueryObj.loadPositionalIndex()
    if questionField.get() != '':
        result = 'Result Set: ' + str(QueryObj.queryInput(questionField.get()))
        resultLabel.config(text=result, font=('arial', 14, 'bold'))
    else:
        messagebox.showerror('Error', 'There is nothing to be searched')


root.geometry('900x200')
root.title('Boolean Retrieval Model')
root.config(bg='black')
root.resizable(0, 0)
queryLabel = Label(root, text='Enter Query: ',
                   font=('arial', 14, 'bold'), bg='black')
queryLabel.place(x=30, y=20)
questionField = Entry(root, width=50, font=(
    'arial', 14, 'bold'))
questionField.place(x=125, y=18)
resultLabel = Label(root, bg='black')
resultLabel.place(x=30, y=80)
submit_button = Button(root, text="Search", bd=0, bg='black',
                       relief=RAISED, command=getResult).place(x=550, y=20)
root.mainloop()
