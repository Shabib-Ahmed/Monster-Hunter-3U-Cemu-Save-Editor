from fileEditAPI.saveEditorAPI import *
import fileEditAPI.saveEditorAPI as api
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from tkinter import Toplevel, Label, Button

itemListUI = []
equipmentListUI = []

class saveEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MH3U Save File Editor')
        self.geometry("500x300")
        self.minsize(500,300)
        self.fileMenu = fileMenu(self)
        self.notebook = notebook(self)
        self.mainloop()
    
class fileMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        fileMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='File', menu=fileMenu) 
        fileMenu.add_command(label='Open File', command=self.openFile) 
        fileMenu.add_command(label='Save File', command=self.saveFile) 
        fileMenu.add_command(label='Save As...', command=self.saveFileAs) 
        parent.config(menu=self)
        
    def openFile(self):
        global itemListUI, equipmentListUI
        filePath = tk.filedialog.askopenfilename(title="Select Save File")
        if filePath:
            openSaveFile(filePath)
            itemListUI = getItemList(0)
            equipmentListUI = getEquipmentList(0)
            self.parent.notebook.updatePlayerTab()
            self.parent.notebook.updateListboxTree()
            self.parent.notebook.updateEquipmentBoxTree()
        
    def saveFile(self):
        if api.currentFilePath:
            saveSaveFile(api.currentFilePath)
            tk.messagebox.showinfo("Success", "Save file updated successfully!")
        else:
            self.saveFileAs()

    def saveFileAs(self):
        filePath = tk.filedialog.asksaveasfilename(title="Save As...")
        if filePath:
            saveSaveFile(filePath)
            api.currentFilePath = filePath
            tk.messagebox.showinfo("Success", "New save file written successfully!")
        
        
class notebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.playerInfotab = playerInfoTab(self)
        self.itemBoxListTab = itemBoxListTab(self)
        self.equipmentBoxListTab = equipmentBoxListTab(self)
        self.pack(expand=1, fill="both")
        
    def updatePlayerTab(self):
        self.playerInfotab.updatePlayerTab()
    
    def updateListboxTree(self):
        self.itemBoxListTab.updateListboxTree()
    
    def updateEquipmentBoxTree(self):
        self.equipmentBoxListTab.updateEquipmentBoxTree()
        
class playerInfoTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label1 = Label(self, text='Player Name')
        self.label2 = Label(self, text='Zenny Amount')
        self.playerNameEntry = tk.Entry(self)
        self.zennyEntry = tk.Entry(self)
        self.label1.grid(row=0, column=0, pady=2)
        self.label2.grid(row=1, column=0, pady=2)
        self.playerNameEntry.grid(row=0, column=1, pady=2)
        self.zennyEntry.grid(row=1, column=1, pady=2)
        self.submitButton = Button(self, text="Change", command=self.changePlayerInfo)
        self.submitButton.grid(row=2, column=0)
        parent.add(self, text='Player Info')
    
    def updatePlayerTab(self):
        self.playerNameEntry.delete(0, tk.END)
        self.playerNameEntry.insert(0, getPlayerName())
        self.zennyEntry.delete(0, tk.END)
        self.zennyEntry.insert(0, str(getZennyAmount()))
    
    def changePlayerInfo(self):
        changePlayerName(str(self.playerNameEntry.get()))
        changeZennyAmount(int(self.zennyEntry.get()))
        tk.messagebox.showinfo("Success", "Player changes applied to buffer!")

class itemBoxListTab(ttk.Frame):
    boxPageNumber = 0
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.itemBoxTree = ttk.Treeview(self, column=('c1','c2','c3'), show='headings', height=5)
        self.itemBoxTree.pack(expand=1, fill="both")
        self.itemBoxTree.column("c1", anchor=tk.CENTER, width=80)
        self.itemBoxTree.heading("c1", text="Item Number")
        self.itemBoxTree.column("c2", anchor=tk.W, width=80)
        self.itemBoxTree.heading("c2", text="Item")
        self.itemBoxTree.column("c3", anchor=tk.W, width=80)
        self.itemBoxTree.heading("c3", text="Quantity")
        
        self.boxNumber = ttk.Combobox(self, values=list(range(1,11)))
        self.boxNumber.current(self.boxPageNumber)
        self.boxNumber.pack()
        self.boxNumber.bind('<<ComboboxSelected>>', self.changePage)
        self.itemBoxTree.bind('<Double-Button-1>', self.modifyItem)

        parent.add(self, text='Item Box List')
        
    def changePage(self, a):
        global itemListUI
        self.boxPageNumber = self.boxNumber.current()
        itemListUI = getItemList(self.boxPageNumber)
        self.updateListboxTree()
        
    def updateListboxTree(self):
        for i in self.itemBoxTree.get_children():
            self.itemBoxTree.delete(i)
        index = 1 + (self.boxPageNumber * 100)
        for i in itemListUI:
            self.itemBoxTree.insert('', 'end', values=(index, i[0], i[1]))
            index = index + 1
    
    def modifyItem(self, a):
        self.top = Toplevel(self.parent.parent)
        self.top.geometry("+%d+%d" % (self.parent.parent.winfo_x()+100, self.parent.parent.winfo_y()+100))
        self.curItem = self.itemBoxTree.focus()
        if not self.curItem: return
        
        self.label1 = Label(self.top, text='Choose Item')
        self.label2 = Label(self.top, text='Choose Quantity')
        self.label1.grid(row=0, column=0, pady=2)
        self.label2.grid(row=1, column=0, pady=2)

        self.itemEntry = ttk.Combobox(self.top, values=getItemListNames())
        try:
            self.itemEntry.current(getItemListNames().index(self.itemBoxTree.item(self.curItem)['values'][1]))
        except ValueError:
            self.itemEntry.current(0)
        self.itemEntry.grid(row=0, column=1, pady=2)

        self.quantityEntry = ttk.Combobox(self.top, values=list(range(100)))
        self.quantityEntry.current(int(self.itemBoxTree.item(self.curItem)['values'][2]))
        self.quantityEntry.grid(row=1, column=1, pady=2)

        self.button = Button(self.top, text="Ok", command=lambda: self.itemBoxSubmit(self.top, self.quantityEntry, self.itemEntry, self.curItem))
        self.button.grid(row=2, column=1, pady=2)
    
    def itemBoxSubmit(self, top, quantityEntry, itemEntry, curItem):
        self.index = self.itemBoxTree.item(curItem)['values'][0]-1
        chosenItem = getItemListNames()[self.itemEntry.current()]
        chosenQuantity = int(self.quantityEntry.current())
        
        self.itemBoxTree.item(self.curItem, values=(self.itemBoxTree.item(self.curItem)['values'][0], chosenItem, chosenQuantity))
        itemListUI[self.index % 100] = (chosenItem, chosenQuantity)
        changeItem(self.index, chosenItem, chosenQuantity)
        self.top.destroy()
    
class equipmentBoxListTab(ttk.Frame):
    boxPageNumber = 0
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.equipmentBoxTree = ttk.Treeview(self, column=('c1','c2'), show='headings', height=5)
        self.equipmentBoxTree.pack(expand=1, fill="both")
        self.equipmentBoxTree.column("c1", anchor=tk.CENTER, width=80)
        self.equipmentBoxTree.heading("c1", text="Equipment Number")
        self.equipmentBoxTree.column("c2", anchor=tk.W, width=80)
        self.equipmentBoxTree.heading("c2", text="Equipment")
        
        self.boxNumber = ttk.Combobox(self, values=list(range(1,11)))
        self.boxNumber.current(self.boxPageNumber)
        self.boxNumber.pack()
        self.boxNumber.bind('<<ComboboxSelected>>', self.changePage)

        parent.add(self, text='Equipment Box List')
        
    def changePage(self, a):
        global equipmentListUI
        self.boxPageNumber = self.boxNumber.current()
        equipmentListUI = getEquipmentList(self.boxPageNumber)
        self.updateEquipmentBoxTree()
        
    def updateEquipmentBoxTree(self):
        for i in self.equipmentBoxTree.get_children():
            self.equipmentBoxTree.delete(i)
        index = 1 + (self.boxPageNumber * 100)
        for i in equipmentListUI:
            self.equipmentBoxTree.insert('', 'end', values=(index, i))
            index = index + 1
        
saveEditor()