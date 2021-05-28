from tkinter import *
from tkinter import ttk
from functools import partial
from kernel import *
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Work_area_Window(Frame):
    def __init__(self, parent, file=None):

        Frame.__init__(self, parent)
        self.index=1
        self.project_label=StringVar()
        self.project_label.set("")
        self.file_path = file.file_path
        self.file = file
        self.grid(row=0, column=0, sticky=N + S + E + W, pady=10, padx=10)

        # Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.menu_bar_infos()
        # Grid.columnconfigure(self, 1, weight=1)
        statusbar = Label(self, textvariable=self.project_label, bd=1, relief=SUNKEN, anchor=W).grid(row=2,column=0,sticky=E+W)
        #menu.pack()
        self.affichage = Frame(self)
        self.affichage.grid(row=1, column=0, sticky=N + S + E + W)
        self.graph_frame = ScrollFrame(self.affichage)
        #Grid.rowconfigure(self.graph_frame.frame, 0, weight=1)
        #Grid.columnconfigure(self.graph_frame.frame, 0, weight=1)
        #self.graph_frame.grid(row=1, column=0, sticky=N + S + E + W)

    def menu_bar_infos(self):

        frame = Frame(self)
        Label(frame, text="File Path:  ").grid(column=0, row=0, padx=1, pady=5)
        Label(frame, text=self.file_path, bg="white", fg="black").grid(column=1, row=0, padx=1, pady=5)
        menu = ttk.Menubutton(frame, text="Générer tour optimal", compound=LEFT)
        menu.menu = Menu(menu, tearoff="false")
        menu.config(menu=menu.menu, )
        #menu.menu.add_command(label="test")
        affichage_menu = Menu(menu.menu, tearoff="false")
        affichage_menu_heur_spec = Menu(menu.menu, tearoff="false")
        menu.menu.add_cascade(label="Méthode exacte", menu=affichage_menu, )
        menu.menu.add_cascade(label="heuristiques spécifiques", menu=affichage_menu_heur_spec, )

        plot = Menu(affichage_menu, tearoff="false", )
        affichage_menu.add_cascade(label="Plot", menu=plot)
        affichage_menu_heur_spec.add_command(label="Plus proche voisin (PPV)",command=self.show_ppv)
        plot.add_command(label="Programmation dynamique", command=self.show_programmation_dynamique)
        plot.add_command(label="Bunch and bound", command=self.show_bunch_and_bound)
        plot.add_command(label="Bunch and bound amélioré", command=self.show_bunch_and_bound_am)

        menu.grid(row=0, column=2, padx=15, pady=5)


        menu2 = ttk.Menubutton(frame, text="Comparer entre méthodes", compound=LEFT)
        menu2.menu = Menu(menu2, tearoff="false")
        menu2.config(menu=menu2.menu, )
        #menu.menu.add_command(label="test")
        compare_menu = Menu(menu2.menu, tearoff="false")
        menu2.menu.add_cascade(label="Méthodes exactes", menu=compare_menu, )
        #plot = Menu(affichage_menu, tearoff="false", )
        #affichage_menu.add_cascade(label="Plot", menu=plot)
        compare_menu.add_command(label="Temps d'éxecution", command=self.compare_methode_exactes)
        menu2.grid(row=0, column=3, padx=15, pady=5)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

    def show_ppv(self):
             None
    def show_programmation_dynamique(self):

        tour,cout,time=Programation_dynamique(self.file.distances,self.file.nb_villes)
        plotcylce_img = "test"
        fig = plotcycle(self.file.points,tour,cout,plotcylce_img,"Programmation dynamque",time*60)
        frame=self.graph_frame.frame
        #self.img = ImageTk.PhotoImage(Image.open(plotcylce_img+".png").resize((770, 320), Image.ANTIALIAS))
        #self.image_id = self.canvas.create_image(20, 20, anchor=NW, image=self.img)
        #self.canvas.pack()
        fig_tk =FigureCanvasTkAgg(fig, frame).get_tk_widget()
        fig_tk.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W,padx=15, pady=5)
        Grid.rowconfigure(fig_tk, 0, weight=1)
        Grid.columnconfigure(fig_tk, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        #frame.pack()
        self.index=self.index+1
        self.graph_frame.update()

    def show_bunch_and_bound(self):
        cout, tour, nb_noeud, temps=branchAndBoundAmeliore(self.file.distances, False ,self.file.points)
        plotcylce_img = "test"
        fig = plotcycle(self.file.points,tour,cout,plotcylce_img,"Bunch and bound classique",temps)
        frame=self.graph_frame.frame
        fig_tk =FigureCanvasTkAgg(fig, frame).get_tk_widget()
        fig_tk.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W,padx=15, pady=5)
        Grid.rowconfigure(fig_tk, 0, weight=1)
        Grid.columnconfigure(fig_tk, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        self.index=self.index+1
        self.graph_frame.update()

    def show_bunch_and_bound_am(self):
        cout, tour, nb_noeud, temps=branchAndBoundAmeliore(self.file.distances, True ,self.file.points)
        plotcylce_img = "test"
        fig = plotcycle(self.file.points,tour,cout,plotcylce_img,"Bunch and bound amélioré",temps)
        frame=self.graph_frame.frame
        fig_tk =FigureCanvasTkAgg(fig, frame).get_tk_widget()
        fig_tk.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W,padx=15, pady=5)
        Grid.rowconfigure(fig_tk, 0, weight=1)
        Grid.columnconfigure(fig_tk, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        self.index=self.index+1
        self.graph_frame.update()
    def compare_methode_exactes(self):
        frame = self.graph_frame.frame
        fig_temp_exec = courbes_methodes_exactes(self.file.distances, self.file.nb_villes,self.file.points)
        fig_temp_exec_tk =FigureCanvasTkAgg(fig_temp_exec, self.graph_frame.frame).get_tk_widget()
        fig_temp_exec_tk.grid(column=0, columnspan=1, row=2, sticky=N + S + E + W,padx=15, pady=5)
        self.index = self.index + 1
        self.graph_frame.update()


class AutoScrollbar(Scrollbar):
    # A scrollbar that hides itself if it's not needed.
    # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise TclError("cannot use place with this widget")


class ScrollFrame:

    def __init__(self, master):

        self.vscrollbar = AutoScrollbar(master)
        self.vscrollbar.grid(row=0, column=1, sticky=N + S)
        self.hscrollbar = AutoScrollbar(master, orient=HORIZONTAL)
        self.hscrollbar.grid(row=1, column=0, sticky=E + W)
        self.canvas = Canvas(master, yscrollcommand=self.vscrollbar.set,
                             xscrollcommand=self.hscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        # make the canvas expandable
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # create frame inside canvas
        self.frame = Frame(self.canvas)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.bind("<Configure>", self.reset_scrollregion)

    def reset_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update(self):
        self.canvas.create_window(0, 0, anchor="nw", window=self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.frame.winfo_reqwidth())
        if self.frame.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canvas.config(height=self.frame.winfo_reqheight())

