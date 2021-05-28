from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Style
from functools import partial
from CustomNotebook import CustomNotebook
from interface_affichage import *
from kernel import *


class App(Frame):
    def __init__(self, master=None):
        combostyle = Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings={'TCombobox':
                                              {'configure':
                                                   {'selectbackground': 'white',
                                                    'fieldbackground': 'white',
                                                    'lightcolor': 'black',
                                                    'selectforeground': 'black',
                                                    'bordercolor': 'white',
                                                    }}}
                                )
        # ATTENTION: this applies the new style 'combostyle' to all tCombobox
        combostyle.theme_use('combostyle')
        Frame.__init__(self, master)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.files = {}
        self.notebook_frames = {}
        self.lastworkarea = 0
        self.top = None
        self.master.title("Blablacar")
        self.master.geometry("1000x700")
        menu = Menu(self)
        self.master.config(menu=menu)
        fichier_menu = Menu(menu, tearoff="false")
        menu.add_cascade(label="Fichier", menu=fichier_menu, )
        importer = Menu(fichier_menu, tearoff="false")
        importer.add_command(label="Fichier TSP", command=self.open_file_instance)
        # fichier_menu.add_command(label="Importer",command=None)
        fichier_menu.add_cascade(label="Importer", menu=importer, )
        fichier_menu.add_command(label="Exit", command=self.master.quit)

        workarea_menu = Menu(menu, tearoff="false")
        menu.add_cascade(label="workarea", menu=workarea_menu)
        workarea_add = Menu(workarea_menu, tearoff="false")
        self.workarea_add_menu = workarea_add
        workarea_menu.add_cascade(label="Add workarea", menu=workarea_add)
        self.notebook = CustomNotebook(self.master)
        self.notebook.pack(side="top", fill="both", expand=True)

    def workarea_add_file(self, menu, file_path):
        # for file_path in self.files.keys():
        # menu.insert_command(label=file_path,command=partial(self.workarea_add,file_path))
        menu.add_command(label=file_path, command=partial(self.workarea_add, file_path))

    def workarea_add(self, file_path):

        frame = Work_area_Window(self.notebook,file=self.files[file_path])
        self.lastworkarea = self.lastworkarea + 1
        self.notebook_frames["Work Area " + str(self.lastworkarea)] = frame
        self.notebook.add(frame, text="Work Area " + str(self.lastworkarea))
        self.notebook.select(frame)
        None

    def open_file_instance(self):
        file_path = filedialog.askopenfilename(title="Selectioner un Fichier")
        print(file_path)
        self.files[file_path]=File(file_path)
        self.workarea_add_file(self.workarea_add_menu, file_path)
        self.workarea_add(file_path)



def main():
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    app = App(master=root)
    app.pack(fill="both", expand="true")
    root.mainloop()


if __name__ == '__main__':
    main()
