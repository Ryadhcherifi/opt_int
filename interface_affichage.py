from tkinter import *
from tkinter import ttk
from functools import partial
from kernel import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Work_area_Window(Frame):
    def __init__(self, parent, file=None):

        Frame.__init__(self, parent)
        self.paramaters={}
        self.default_params_init()
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
        affichage_menu_heur_spec.add_command(label="2-OPT",command=self.show_2opt)
        affichage_menu_heur_spec.add_command(label="Ant Colony Optimizaion",command=self.show_aco)


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


    def default_params_init(self):

        ppv = {
            "depart": 0
        }
        self.paramaters["ppv"]=ppv
        aco = {
            "depart": 0,
            "Q":50,
            "alpha":1,
            "beta":1,
            "l":40,
            "it":30,
            "ro":0.5
        }
        self.paramaters["aco"]=aco
        #print(self.paramaters)

    def get_params(self,methode):
        if (methode == "ppv"):
            params = self.paramaters.get("ppv")
            None

    def show_ppv(self):
        frame = self.graph_frame.frame
        frame_ppv = Frame(frame)
        frame_ppv.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W, padx=15, pady=5)
        Grid.rowconfigure(frame_ppv, 0, weight=1)
        Grid.columnconfigure(frame_ppv, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        print(self.paramaters)
        depart =  self.paramaters["ppv"]["depart"]
        depart_tk=IntVar(depart)
        frame_ppv_params = Frame(frame_ppv)
        frame_ppv_params.pack()
        Label(frame_ppv_params,text="Ville de départ:").grid(column=0, columnspan=1, row=0,padx=10)
        Entry(frame_ppv_params,textvariable=depart_tk).grid(column=1, columnspan=1, row=0,padx=10)
        self.graph_frame.update()
        Button(frame_ppv_params, text="Calculer", command=partial(self.show_ppv_result,depart_tk)).grid(column=2, columnspan=1, row=0,padx=10)
        Button(frame_ppv_params, text="PPV Généralisée", command=None).grid(column=3, columnspan=1, row=0,padx=10)


    def show_ppv_result(self,depart_tk):
                 print("Depart="+str(depart_tk.get()))
    def show_2opt(self):
        frame = self.graph_frame.frame
        labelChoix = Label(frame, text="Veuillez choisir l'algorithme pour l'instance de depart !")

        labelChoix.pack()
        listemethodes = ["sequetielle","Random", "plus proche voisin", "moindre cout"]
        listeCombo = ttk.Combobox(frame, values=listemethodes)
        listeCombo.bind('<<ComboboxSelected>>', self.choix_box_2opt)
        listeCombo.current(0)

        listeCombo.pack()


        # frame.pack()
        self.index = self.index + 1
        self.graph_frame.update()

    def choix_box_2opt(self,event):
        methode=event.widget.get()
        distances = self.file.distances
        cout_methode=0
        cout_2opt=0
        temps_2opt=0
        temps_cumule=0

        if methode=="Random":
            resu2=Rand(0,np.size(distances,0)-1,distances)
            resu = two_opt2(resu2[2], distances)
            cout_methode=resu2[0]
            cout_2opt=resu[0]
            temps_2opt=resu[2]
            temps_cumule=temps_2opt+resu2[1]

        elif methode=="sequetielle":
            li=[]
            for i in range (np.size(distances,0) ) :
                li.append(i)
            li.append(0)
            resu=two_opt2(li,distances)
            cout_methode = cost(distances,np.array(li))
            cout_2opt = resu[0]
            temps_2opt = resu[2]
            temps_cumule = temps_2opt

        elif methode=="plus proche voisin":
            resu2=ppv(1,distances)
            resu=two_opt2(list(np.array(resu2[0])-1),distances)

        else:
            resu2=moindre_cout(distances)
            print(resu2[2])
            resu=two_opt2(resu2[2],distances)
            cout_methode = resu2[0]
            cout_2opt = resu[0]
            temps_2opt = resu[2]
            temps_cumule = temps_2opt + resu2[1]
        lst=[("Cout 2-opt",cout_2opt),("Cout methode generatrice",cout_methode)]
        #Table(self.graph_frame.frame,2,2)

    def show_3opt(self):
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

    def show_aco(self):
        frame = self.graph_frame.frame
        frame_aco = Frame(frame)
        frame_aco.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W, padx=15, pady=5)
        Grid.rowconfigure(frame_aco, 0, weight=1)
        Grid.columnconfigure(frame_aco, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        depart =  self.paramaters["aco"]["depart"]
        print(self.paramaters["aco"]["Q"])
        Qu =  self.paramaters["aco"]["Q"]
        alpha =  self.paramaters["aco"]["alpha"]
        beta =  self.paramaters["aco"]["beta"]
        l =  self.paramaters["aco"]["l"]
        it =  self.paramaters["aco"]["it"]
        ro =  self.paramaters["aco"]["ro"]

        depart_tk=IntVar()
        depart_tk.set(depart)
        Q_tk=IntVar()
        Q_tk.set(Qu)
        alpha_tk=IntVar()
        alpha_tk.set(alpha)
        beta_tk=IntVar()
        beta_tk.set(beta)
        l_tk=IntVar()
        l_tk.set(l)
        it_tk=IntVar()
        it_tk.set(it)
        
        ro_tk=StringVar()
        ro_tk.set(ro)

        frame_aco_params = Frame(frame_aco)
        frame_aco_params.pack()
        Label(frame_aco_params,text="Ville de départ:").grid(column=0, columnspan=1, row=0,padx=10)
        Entry(frame_aco_params,textvariable=depart_tk).grid(column=1, columnspan=1, row=0,padx=10)
        Label(frame_aco_params,text="Nombre de fourmis").grid(column=0, columnspan=1, row=1,padx=10)
        Entry(frame_aco_params,textvariable=l_tk).grid(column=1, columnspan=1, row=1,padx=10)
        Label(frame_aco_params,text="Nombre de tours").grid(column=0, columnspan=1, row=2,padx=10)
        Entry(frame_aco_params,textvariable=it_tk).grid(column=1, columnspan=1, row=2,padx=10)
        Label(frame_aco_params,text="Taux d'évaporation").grid(column=0, columnspan=1, row=3,padx=10)
        Entry(frame_aco_params,textvariable=ro_tk).grid(column=1, columnspan=1, row=3,padx=10)
        Label(frame_aco_params,text="Coefficient de maj des phéromones Q").grid(column=0, columnspan=1, row=4,padx=10)
        Entry(frame_aco_params,textvariable=Q_tk).grid(column=1, columnspan=1, row=4,padx=10)
        Label(frame_aco_params,text="Coefficient des phéromones").grid(column=0, columnspan=1, row=5,padx=10)
        Entry(frame_aco_params,textvariable=alpha_tk).grid(column=1, columnspan=1, row=5,padx=10)
        Label(frame_aco_params,text="Coefficient de la visibilité").grid(column=0, columnspan=1, row=6,padx=10)
        Entry(frame_aco_params,textvariable=beta_tk).grid(column=1, columnspan=1, row=6,padx=10)
        self.graph_frame.update()
        Button(frame_aco_params, text="Calculer", command=partial(self.show_aco_result,depart_tk,l_tk,it_tk,ro_tk,Q_tk,alpha_tk,beta_tk,frame_aco_params)).grid(column=2, columnspan=1, row=0,padx=10)
        


    def show_aco_result(self,depart_tk,l_tk,it_tk,ro_tk,Q_tk,alpha_tk,beta_tk,frame_aco_params):
        depart =  depart_tk.get()
        Qu = Q_tk.get()
        alpha =  alpha_tk.get()
        beta = beta_tk.get()
        l =  l_tk.get()
        it = it_tk.get()
        ro =  1-float(ro_tk.get())
        
        distances = self.file.distances
        points,N=self.load_points(self.file_path)
        distances=self.load_distances(points,N)
        print(N)
        visibility=np.zeros((N,N),"double")
        P=np.zeros((N,N),"double")
        for i in range(N) : 
            for j in range(N) :
                if(distances[i][j]!=0):
                    visibility[i][j]=1/distances[i][j]

        pheromone=[[1/100 for i in range(N)] for j in range(N)]
        pheromone2=[[1/100 for i in range(N)] for j in range(N)]
        for a in range(N):
            pheromone[a][a]=0
            pheromone2[a][a]=0
        for t in range(it) :    
            for k in range(l) :
                allowed=[i for i in range(N)]
                #i=np.random.randint(100)
                i=0
                allowed.pop(allowed.index(i))
                for a in range(N-1) :
                    c=int(self.pk(i,allowed,pheromone,alpha,beta,visibility))
                    allowed.pop(allowed.index(c))
                    pheromone2[i][c]= pheromone[i][c]*ro + Qu/distances[i][c]
                    pheromone2[c][i]=pheromone2[i][c]
                    
                    i=c
            for a in range(N):
                for b in range(N):
                    pheromone[a][b]=pheromone2[a][b]  

        chemin=[0 for i in range(N)]
        i=0
        cout=0        
            
        for a in range(N):
            ind=np.max(pheromone[i])
            j=pheromone[i].index(ind)
            for b in range(N):
                pheromone[b][i]=0
            chemin[a]=j
            cout=cout+distances[i][j]
            i=j
        chemin[N-1]=0
        cout=cout+distances[i][0]
        Label(frame_aco_params,text="Chemin : "+str(chemin)).grid(column=0, columnspan=10, row=8,padx=10)
        Label(frame_aco_params,text="Cout : "+str(cout)).grid(column=0, columnspan=1, row=9,padx=10)

        print(chemin)
        print(cout)

    def pk(self,i,allowed,pheromone,alpha,beta,visibility):
        somme=0
        for j in range(len(allowed)):
            somme = somme + (pheromone[i][allowed[j]]**alpha)*(visibility[i][allowed[j]]**beta)
        prob=[0 for j in range(len(allowed))]
        for j in range(len(allowed)):
            prob[j]=((pheromone[i][allowed[j]]**alpha)*(visibility[i][allowed[j]]**beta))/somme
        return np.random.choice(
        allowed, 
        1,
        p=prob)

    def load_points(self,file_name):
        file = open(file_name, 'r')
        Name = file.readline().strip().split()[1]
        FileType = file.readline().strip().split()[1] 
        Comment = file.readline().strip().split()[1] 
        Dimension = file.readline().strip().split()[1]
        EdgeWeightType = file.readline().strip().split()[1]  
        file.readline()
        points = []
        N = int(Dimension)
        for i in range(0, int(Dimension)):
            x,y = file.readline().strip().split()[1:]
            points.append([float(x), float(y)])
        file.close()
        return points,N
    
    def load_distances(self,points,N):
        distances = np.zeros((N,N),"double")
        for i in range(N) : 
            for j in range(N) :
                if (i != j):
                    distances[i,j]=np.sqrt(np.square(points[i][0]-points[j][0])+np.square(points[i][1]-points[j][1]))
        return distances

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



