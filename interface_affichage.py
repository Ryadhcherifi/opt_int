from tkinter import *
from tkinter import ttk
from functools import partial
from kernel import *
import time as time
from tabou import ITS,recherche_tabou_2opt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Work_area_Window(Frame):
    def __init__(self, parent, file=None):

        Frame.__init__(self, parent)
        self.paramaters={}
        self.default_params_init()
        self.index=0
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
        affichage_menu_heur_spec.add_command(label="Moindre cout",command=self.show_moindre_cout)
        affichage_menu_heur_spec.add_command(label="2-OPT",command=self.show_2opt)
        affichage_menu_heur_spec.add_command(label="3-OPT",command=self.show_3opt)
        affichage_menu_heur_spec.add_command(label="Ant Colony Optimizaion", command=self.show_aco)

        # Debut recherche tabou

        tabou = Menu(menu.menu, tearoff="false", )
        menu.menu.add_cascade(label="Recherche tabou", menu=tabou)
        # tabou.add_command(label="Tabou simple", command=self.show_tabou_simple_parametrer)
        tabou.add_command(label="Tabou hybride", command=self.show_tabou_simple_parametrer)
        tabou.add_command(label="ITS", command=self.show_ITS_parametrer)

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

    #fonctions RT

    def show_ITS_parametrer(self):
        frame = self.graph_frame.frame
        frame_tabou_simple = Frame(frame)
        frame_tabou_simple.grid(column=0, columnspan=1, row=self.index, sticky=N + S + E + W, padx=15, pady=5)
        self.index += 1
        Grid.rowconfigure(frame_tabou_simple, 0, weight=1)
        Grid.columnconfigure(frame_tabou_simple, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)

        frame1 = Frame(frame_tabou_simple)
        frame1.pack(anchor="w")


        Label(frame1, text="Le nombre d'iterations ITS :").grid(column=0, columnspan=1, row=0, padx=10)
        nb_iteration_ITS = IntVar()
        nb_iteration_ITS.set(10)
        Entry(frame1, textvariable=nb_iteration_ITS).grid(column=1, columnspan=1, row=0, padx=10)


        Label(frame1, text="Le nombre d'iterations de la RT :").grid(column=0, columnspan=1, row=7, padx=10)
        nb_iteration = IntVar()
        nb_iteration.set(800)
        Entry(frame1, textvariable=nb_iteration).grid(column=1, columnspan=1, row=7, padx=10)


        Label(frame1, text="Pas d'augmentation :").grid(column=0, columnspan=1, row=2, padx=10)
        pas_aug = StringVar()
        pas_aug.set("0.75")
        Entry(frame1, textvariable=pas_aug).grid(column=1, columnspan=1, row=2, padx=10)

        Label(frame1, text="Pas de diminution :").grid(column=2, columnspan=1, row=2, padx=10)
        pas_dim = StringVar()
        pas_dim.set("1.0")
        Entry(frame1, textvariable=pas_dim).grid(column=3, columnspan=1, row=2, padx=10)

        Label(frame1, text="Taille de la liste tabou :").grid(column=0, columnspan=1, row=4, padx=10)
        taille_liste_tabou = IntVar()
        taille_liste_tabou.set(80)
        Entry(frame1, textvariable=taille_liste_tabou).grid(column=1, columnspan=1, row=4, padx=10)

        Label(frame1, text="Taille min voisinage :").grid(column=0, columnspan=1, row=3, padx=10)
        taille_v_min = IntVar()
        taille_v_min.set(15)
        Entry(frame1, textvariable=taille_v_min).grid(column=1, columnspan=1, row=3, padx=10)

        Label(frame1, text="Taille max voisinage :").grid(column=2, columnspan=1, row=3, padx=10)
        taille_v_max = IntVar()
        taille_v_max.set(25)
        Entry(frame1, textvariable=taille_v_max).grid(column=3, columnspan=1, row=3, padx=10)

        Label(frame1, text="Taille initiale voisinage :").grid(column=4, columnspan=1, row=3, padx=10)
        taille_v_i = IntVar()
        taille_v_i.set(20)
        Entry(frame1, textvariable=taille_v_i).grid(column=5, columnspan=1, row=3, padx=10)


        Label(frame1, text="Mu :").grid(column=0, columnspan=1, row=5, padx=10)
        mu = IntVar()
        mu.set(150)
        Entry(frame1, textvariable=mu).grid(column=1, columnspan=1, row=5, padx=10)

        print("row7")
        Button(frame1, text="ok default ", command=partial(self.show_ITS_default, frame1)).grid(column=0, columnspan=1, row=8, padx=10)
        Button(frame1, text="calculer", command=partial(self.show_ITS_param, nb_iteration, frame1,nb_iteration_ITS,pas_dim,pas_aug,taille_liste_tabou,taille_v_min,taille_v_max,taille_v_i,mu)).grid(column=1, columnspan=1, row=8, padx=10)



        self.graph_frame.update()


        return None

    def show_ITS_default(self, frame1):


        points, N = self.file.points,self.file.nb_villes
        instance = self.file.file_path.split('/')[-1]
        #distances = load_distances(points, N)
        distances = self.file.distances
        #np.savetxt("distances.txt", distances)
        tour, cout, time = ITS(distances, 0)
        parametre="0"
        fichier_save("./stats_file.csv", "rc_its", instance, parametre, cout, tour, time, time)
        print("temps dexecution recherche_tabou_2opt ", time, "cout opt", cout)
        Label(frame1, text="Cout du cycle obtenu :").grid(column=0, columnspan=1, row=10, padx=10)
        cout_string = StringVar()
        cout_string.set(str(cout))
        Label(frame1, textvariable=cout_string).grid(column=1, columnspan=1, row=10, padx=10)
        Label(frame1, text="Temps d\'éxecution :").grid(column=2, columnspan=1, row=10, padx=10)
        temps_string = StringVar()
        temps_string.set(str(time))
        Label(frame1, textvariable=temps_string).grid(column=3, columnspan=1, row=10, padx=10)



        #label.pack()

        return None

    def show_ITS_param(self, nb_iteration, frame1, nb_iteration_ITS,pas_dim,pas_aug,taille_liste_tabou,taille_v_min,taille_v_max,taille_v_i,mu):
        """print("nb _it wesh", nb_iteration.get())
        print("la solution de depart ", sol_depart.get())
        print("le reste ",float(pas_dim.get()),float(pas_aug.get()),taille_liste_tabou.get(),taille_v_min.get(),taille_v_max.get(),taille_v_i.get(),mu.get(),"\nok")
        print("HELOOO maj",self.file_path)"""


        #points, N = load_points(self.file_path)
        points, N = self.file.points,self.file.nb_villes
        #distances = load_distances(points, N)
        distances = self.file.distances
        instance = self.file.file_path.split('/')[-1]
        #distances = load_distances(points, N)
        #np.savetxt("distances.txt", distances)
        tour, cout, time = ITS(distances, 0 ,NB_IT_ITS=nb_iteration_ITS.get(),TAILLE_LISTE_TABOU_MAX=taille_liste_tabou.get(),mu=mu.get(),PAS_AUGMENTATION=float(pas_aug.get()),PAS_DIMINUTION=float(pas_dim.get()),MAX_ITERATION=nb_iteration.get(),taille_voisinage=taille_v_i.get(), TAILLE_VOISINAGE_MIN=taille_v_min.get(), TAILLE_VOISINAGE_MAX=taille_v_max.get(),)
        parametre=str(0)+","+str(nb_iteration_ITS.get())+","+str(taille_liste_tabou.get())+","+str(mu.get())+","+str(float(pas_aug.get()))+","+ str(float(pas_dim.get()))+","+str(nb_iteration.get())+","+str(taille_v_i.get())+","+str(taille_v_min.get())+","+str(taille_v_max.get())
        fichier_save("./stats_file.csv", "rc_its", instance, parametre, cout, tour, time, time)
        print("temps dexecution recherche_tabou_2opt ", time, "cout opt", cout)

        Label(frame1, text="Cout du cycle obtenu :").grid(column=0, columnspan=1, row=10, padx=10)
        cout_string = StringVar()
        cout_string.set(str(cout))
        Label(frame1, textvariable=cout_string).grid(column=1, columnspan=1, row=10, padx=10)
        Label(frame1, text="Temps d\'éxecution :").grid(column=2, columnspan=1, row=10, padx=10)
        temps_string = StringVar()
        temps_string.set(str(time))
        Label(frame1, textvariable=temps_string).grid(column=3, columnspan=1, row=10, padx=10)



        #label.pack()

        return None



    def show_tabou_simple_parametrer(self ):
        frame = self.graph_frame.frame
        frame_tabou_simple = Frame(frame)
        frame_tabou_simple.grid(column=0, columnspan=1, row=self.index, sticky=N + S + E + W, padx=15, pady=5)
        self.index += 1
        Grid.rowconfigure(frame_tabou_simple, 0, weight=1)
        Grid.columnconfigure(frame_tabou_simple, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)

        frame1 = Frame(frame_tabou_simple)
        frame1.pack(anchor="w")


        Label(frame1, text="Le nombre d'iteration :").grid(column=0, columnspan=1, row=0, padx=10)
        nb_iteration = IntVar()
        nb_iteration.set(18000)
        Entry(frame1, textvariable=nb_iteration).grid(column=1, columnspan=1, row=0, padx=10)

        Label(frame1, text="La solution de depart :").grid(column=0, columnspan=1, row=1, padx=10)
        sol_depart = ["opt", "ppv", "mc", "ppv1"]
        liste_soldepart = ttk.Combobox(frame1, values=sol_depart)
        liste_soldepart.current(0)
        liste_soldepart.grid(column=1, columnspan=1, row=1, padx=10)

        Label(frame1, text="Pas d'augmentation :").grid(column=0, columnspan=1, row=2, padx=10)
        pas_aug = StringVar()
        pas_aug.set("0.75")
        Entry(frame1, textvariable=pas_aug).grid(column=1, columnspan=1, row=2, padx=10)

        Label(frame1, text="Pas de diminution :").grid(column=2, columnspan=1, row=2, padx=10)
        pas_dim = StringVar()
        pas_dim.set("1.0")
        Entry(frame1, textvariable=pas_dim).grid(column=3, columnspan=1, row=2, padx=10)

        Label(frame1, text="Taille de la liste tabou :").grid(column=0, columnspan=1, row=4, padx=10)
        taille_liste_tabou = IntVar()
        taille_liste_tabou.set(80)
        Entry(frame1, textvariable=taille_liste_tabou).grid(column=1, columnspan=1, row=4, padx=10)

        Label(frame1, text="Taille min voisinage :").grid(column=0, columnspan=1, row=3, padx=10)
        taille_v_min = IntVar()
        taille_v_min.set(15)
        Entry(frame1, textvariable=taille_v_min).grid(column=1, columnspan=1, row=3, padx=10)

        Label(frame1, text="Taille max voisinage :").grid(column=2, columnspan=1, row=3, padx=10)
        taille_v_max = IntVar()
        taille_v_max.set(25)
        Entry(frame1, textvariable=taille_v_max).grid(column=3, columnspan=1, row=3, padx=10)

        Label(frame1, text="Taille initiale voisinage :").grid(column=4, columnspan=1, row=3, padx=10)
        taille_v_i = IntVar()
        taille_v_i.set(20)
        Entry(frame1, textvariable=taille_v_i).grid(column=5, columnspan=1, row=3, padx=10)


        Label(frame1, text="Mu :").grid(column=0, columnspan=1, row=5, padx=10)
        mu = IntVar()
        mu.set(100)
        Entry(frame1, textvariable=mu).grid(column=1, columnspan=1, row=5, padx=10)

        print("row7")
        Button(frame1, text="ok default ", command=partial(self.show_tabou_simple, nb_iteration.get(), frame1)).grid(column=0, columnspan=1, row=8, padx=10)
        Button(frame1, text="calculer", command=partial(self.show_tabou_simple_param, nb_iteration, frame1,liste_soldepart,pas_dim,pas_aug,taille_liste_tabou,taille_v_min,taille_v_max,taille_v_i,mu)).grid(column=1, columnspan=1, row=8, padx=10)



        self.graph_frame.update()


        return None

    def show_tabou_simple(self, nb_iteration, frame1):
        """print("nb _it", nb_iteration.get())
        print("HELOOO maj",self.file_path)"""
        #points, N = load_points(self.file_path)

        #distances = load_distances(points, N)
        points, N = self.file.points,self.file.nb_villes
        distances = self.file.distances
        #np.savetxt("distances.txt", distances)

        tour, cout, amelioration, time = recherche_tabou_2opt(distances, 0)
        instance = self.file.file_path.split('/')[-1]
        parametre="0"
        fichier_save("./stats_file.csv", "rc_2opt", instance, parametre, cout, tour, time, time)
        print("temps dexecution recherche_tabou_2opt ", time, "cout opt", cout)

        Label(frame1, text="Cout du cycle obtenu :").grid(column=0, columnspan=1, row=10, padx=10)
        cout_string = StringVar()
        cout_string.set(str(cout))
        Label(frame1, textvariable=cout_string).grid(column=1, columnspan=1, row=10, padx=10)
        Label(frame1, text="Temps d\'éxecution :").grid(column=2, columnspan=1, row=10, padx=10)
        temps_string = StringVar()
        temps_string.set(str(time))
        Label(frame1, textvariable=temps_string).grid(column=3, columnspan=1, row=10, padx=10)

        #label.pack()

        return None

    def show_tabou_simple_param(self, nb_iteration, frame1, sol_depart,pas_dim,pas_aug,taille_liste_tabou,taille_v_min,taille_v_max,taille_v_i,mu):
        """print("nb _it wesh", nb_iteration.get())
        print("la solution de depart ", sol_depart.get())
        print("le reste ",float(pas_dim.get()),float(pas_aug.get()),taille_liste_tabou.get(),taille_v_min.get(),taille_v_max.get(),taille_v_i.get(),mu.get(),"\nok")
        print("HELOOO maj",self.file_path)"""

        print("sol depart interface ", sol_depart.get())

        #points, N = load_points(self.file_path)

        #distances = load_distances(points, N)
        distances = self.file.distances
        #np.savetxt("distances.txt", distances)

        tour, cout, amelioration, time = recherche_tabou_2opt(distances, 0,depart=sol_depart.get(),TAILLE_LISTE_TABOU_MAX=taille_liste_tabou.get(),mu=mu.get(),PAS_AUGMENTATION=float(pas_aug.get()),PAS_DIMINUTION=float(pas_dim.get()),MAX_ITERATION=nb_iteration.get(),taille_voisinage=taille_v_i.get(), TAILLE_VOISINAGE_MIN=taille_v_min.get(), TAILLE_VOISINAGE_MAX=taille_v_max.get(),)
        instance = self.file.file_path.split('/')[-1]
        parametre=str(0)+","+str(sol_depart.get())+","+str(taille_liste_tabou.get())+","+str(mu.get())+","+str(float(pas_aug.get()))+","+ str(float(pas_dim.get()))+","+str(nb_iteration.get())+","+str(taille_v_i.get())+","+str(taille_v_min.get())+","+str(taille_v_max.get())
        fichier_save("./stats_file.csv", "rc_2opt", instance, parametre, cout, tour, time, time)
        print("temps dexecution recherche_tabou_2opt ", time, "cout opt", cout)

        Label(frame1, text="Cout du cycle obtenu :").grid(column=0, columnspan=1, row=10, padx=10)
        cout_string = StringVar()
        cout_string.set(str(cout))
        Label(frame1, textvariable=cout_string).grid(column=1, columnspan=1, row=10, padx=10)
        Label(frame1, text="Temps d\'éxecution :").grid(column=2, columnspan=1, row=10, padx=10)
        temps_string = StringVar()
        temps_string.set(str(time))
        Label(frame1, textvariable=temps_string).grid(column=3, columnspan=1, row=10, padx=10)



        #label.pack()

        return None



    def default_params_init(self):

        ppv = {
            "depart": 1
        }
        self.paramaters["ppv"]=ppv
        aco = {
            "depart": 0,
            "Q": 50,
            "alpha": 1,
            "beta": 1,
            "l": 40,
            "it": 30,
            "ro": 0.5
        }
        self.paramaters["aco"] = aco
        #print(self.paramaters)







    def get_params(self,methode):
        if (methode == "ppv"):
            params = self.paramaters.get("ppv")
            None

    def show_moindre_cout(self):
        frame = self.graph_frame.frame
        frame_mc = Frame(frame)
        frame_mc.grid(column=0, columnspan=1, row=self.index, sticky=N + S + E + W, padx=15, pady=5)
        self.index += 1
        Grid.rowconfigure(frame_mc, 0, weight=1)
        Grid.columnconfigure(frame_mc, 0, weight=1)
        Grid.rowconfigure(frame_mc, 0, weight=1)
        Grid.columnconfigure(frame_mc, 0, weight=1)
        frame_mc_result = Frame(frame_mc)
        frame_mc_result.pack(anchor="w")
        cout, time, route = moindre_cout(self.file.distances)
        Label(frame_mc_result,text="\n*** Avec la méthode moindre cout ***").grid(column=0, columnspan=1, row=0,padx=10,pady=10, sticky="nw")
        Label(frame_mc_result,text="    Cout de la solution généré:"+str(cout)).grid(column=0, columnspan=1, row=1,padx=10,pady=10, sticky="nw")
        Label(frame_mc_result,text="    Temps d'éxecution:"+str(time)).grid(column=0, columnspan=1, row=2,padx=10,pady=10, sticky="nw")
        self.graph_frame.update()

    def show_ppv(self):
        frame = self.graph_frame.frame
        frame_ppv = Frame(frame)
        frame_ppv.grid(column=0, columnspan=1, row=self.index, sticky=N + S + E + W, padx=15, pady=5)
        self.index += 1
        Grid.rowconfigure(frame_ppv, 0, weight=1)
        Grid.columnconfigure(frame_ppv, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)

        depart =  self.paramaters["ppv"]["depart"]
        depart_tk=IntVar()
        depart_tk.set(depart)
        frame_ppv_params = Frame(frame_ppv)
        frame_ppv_params.pack(anchor="w")
        Label(frame_ppv_params,text="Ville de départ:").grid(column=0, columnspan=1, row=0,padx=10)
        Entry(frame_ppv_params,textvariable=depart_tk).grid(column=1, columnspan=1, row=0,padx=10)
        Button(frame_ppv_params, text="Calculer", command=partial(self.show_ppv_result,depart_tk,frame_ppv)).grid(column=2, columnspan=1, row=0,padx=10)
        Button(frame_ppv_params, text="PPV Généralisée", command=partial(self.show_ppv_gen_result,frame_ppv)).grid(column=3, columnspan=1, row=0,padx=10)
        self.graph_frame.update()

    def show_ppv_gen_result(self,frame_ppv):
        frame_ppv_result = Frame(frame_ppv)
        frame_ppv_result.pack(anchor="w")
        tour_optimal, cout, time, stats=ppv_gen(self.file.distances,stats = True)
        Label(frame_ppv_result,text="\n***Le plus proche voisin avec toutes les villes comme ville de départ***").grid(column=0, columnspan=1, row=0,padx=10,pady=10, sticky="nw")
        Label(frame_ppv_result,text="       Cout de la solution: "+str(cout)).grid(column=0, columnspan=1, row=1,padx=10,pady=10, sticky="nw")
        Label(frame_ppv_result,text="       Temps d'éxecution de l'algorithme': "+str(time)+" s").grid(column=0, columnspan=1, row=2,padx=10,pady=10, sticky="nw")
        frame_plot = Frame(frame_ppv)
        fig = plot_ppv_gen(len(tour_optimal), stats)
        fig_tk =FigureCanvasTkAgg(fig, frame_plot).get_tk_widget()
        fig_tk.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W,padx=15, pady=5)
        frame_plot.pack(anchor="w")
    def show_ppv_result(self,depart_tk,frame_ppv):
        print("Depart="+str(depart_tk.get()))
        debut = depart_tk.get()
        print(self.file.distances)
        visite, cout, time =ppv(debut,self.file.distances,temps=True)
        frame_ppv_result = Frame(frame_ppv)
        frame_ppv_result.pack(anchor="w")
        Label(frame_ppv_result,text="\n***Le plus proche voisin avec "+str(debut)+" comme ville de départ donne:***").grid(column=0, columnspan=1, row=0,padx=10,pady=10, sticky="nw")
        Label(frame_ppv_result,text="       Cout de la solution: "+str(cout)).grid(column=0, columnspan=1, row=1,padx=10,pady=10, sticky="nw")
        Label(frame_ppv_result,text="       Temps d'éxecution de l'algorithme: "+str(time)+" s").grid(column=0, columnspan=1, row=2,padx=10,pady=10, sticky="nw")

    def show_2opt(self):
        frame = self.graph_frame.frame
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        Label(frame, text="Veuillez choisir l'algorithme pour l'instance de depart !").grid(column=0, columnspan=1, row=0,padx=10)

        listemethodes = ["sequetielle","Random", "ppv","ppv generalisé" ,"moindre cout"]
        listeCombo = ttk.Combobox(frame,state="readonly", values=listemethodes)
        listeCombo.grid(column=1, columnspan=1, row=0,padx=10)
        listeCombo.bind('<<ComboboxSelected>>', self.choix_box_2opt)
        listeCombo.current(0)
        # frame.pack()
        self.index = self.index + 1
        self.graph_frame.update()

    def choix_box_2opt(self,event):
        methode=event.widget.get()
        distances = self.file.distances
        instance = self.file.file_path.split('/')[-1]

        print(methode)
        if methode=="Random":
            resu2=Rand(0,np.size(distances,0)-1,distances)
            cout_methode=resu2[0]
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "2-OPT", instance, resu2[2])
            if cout_2opt == None:
                print("hhh")
                resu = two_opt2(resu2[2], distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(resu[2]) + float(resu2[1])
                fichier_save("./stats_file.csv", "2-OPT", instance, str(resu2[2]), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)



        elif methode=="sequetielle":
            li=[]
            for i in range (np.size(distances,0) ) :
                li.append(i)
            li.append(0)
            cout_methode = cost(distances,np.array(li))
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "2-OPT", instance,li)
            if cout_2opt == None:
                print("hhh")
                resu = two_opt2(li, distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt)
                fichier_save("./stats_file.csv", "2-OPT", instance, str(li), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)

        elif methode == "ppv generalisé":
            cout_methode, tour_optimal, temps, temps_cum = get_results("./stats_file.csv", "ppv_gen", instance, "/")
            if cout_methode == None:
                resu2 = ppv_gen(distances)
                cout_methode = resu2[1]
                fichier_save("./stats_file.csv", "ppv_gen", instance, "/", resu2[1], str(resu2[0]), resu2[2], resu2[2])
                print("hhh")
            else:
                resu2 = [tour_optimal, cout_methode, temps]

            print(resu2)
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "2-OPT", instance,resu2[0])
            if cout_2opt == None:
                print("hhh")
                resu = two_opt2(list(np.array(resu2[0]) - 1), distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt) + float(resu2[2])
                fichier_save("./stats_file.csv", "2-OPT", instance, str(resu2[0]), str(cout_2opt), str(resu[1]),temps_2opt, temps_cumule)

        elif methode=="ppv":
            cout_methode, tour_optimal, temps, temps_cum = get_results("./stats_file.csv", "ppv", instance,1)
            if cout_methode==None:
                resu2=ppv(1,distances,True)
                cout_methode = resu2[1]
                fichier_save("./stats_file.csv", "ppv", instance, str(1), resu2[1], str(resu2[0]), resu2[2],resu2[2])
                print("hhh")
            else:
                print("fff")
                resu2=[tour_optimal,cout_methode,temps]

            print(resu2)
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "2-OPT", instance,resu2[0])
            if cout_2opt==None:
                print("hhh")
                resu=two_opt2(list(np.array(resu2[0])-1),distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt) + float(resu2[2])
                fichier_save("./stats_file.csv","2-OPT",instance,str(resu2[0]),str(cout_2opt),str(resu[1]),temps_2opt,temps_cumule)
        else:

            cout_methode, tour_optimal, temps, temps_cum = get_results("./stats_file.csv", "mc", instance, "/")
            if cout_methode == None:
                resu2=moindre_cout(distances)
                cout_methode = resu2[0]
                fichier_save("./stats_file.csv", "mc", instance, "/", resu2[0], str(resu2[2]), resu2[1], resu2[1])
                print("hhh")
            else:
                print("fff")
                resu2=[cout_methode,temps,tour_optimal]
            print(resu2)
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "2-OPT", instance,resu2[2])
            if cout_2opt == None:
                print("hhh")
                resu = two_opt2(resu2[2], distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt) + float(resu2[1])
                fichier_save("./stats_file.csv", "2-OPT", instance, str(resu2[2]), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)

        frame =self.graph_frame.frame
        frame_opt = Frame(frame)
        frame_opt.grid(columnspan=2,row=self.index, sticky=N + S + E + W, padx=15, pady=5)
        self.index=self.index+1
        Grid.rowconfigure(frame_opt, 0, weight=1)
        Grid.columnconfigure(frame_opt, 0, weight=1)
        #frame_ppv=Frame(frame2)
        #frame_ppv.pack()
        Label(frame_opt, text="Cout de l'heuristique 2-OPT avec : "+ methode,font=("Courier", 18)).grid(column=0, columnspan=1, row=1,padx=10,pady=10)
        Label(frame_opt, text=str(cout_2opt),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=1,padx=10,pady=10)

        Label(frame_opt, text="Cout de la methode " + methode + ": ",font=("Courier", 18)).grid(column=0, columnspan=1, row=2,padx=10,pady=10)
        Label(frame_opt, text=str(cout_methode),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=2,padx=10,pady=10)
        Label(frame_opt, text="Temps d'execution 2-OPT: ",font=("Courier", 18)).grid(column=0, columnspan=1, row=3,padx=10,pady=10)
        Label(frame_opt, text=str(temps_2opt),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=3,padx=10,pady=10)

        Label(frame_opt, text="Temps cumulé des deux methodes: " ,font=("Courier", 18)).grid(column=0, columnspan=1, row=4,padx=10,pady=10)
        Label(frame_opt, text=str(temps_cumule),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=4,padx=10,pady=10)

        Label(frame_opt,text="Gain en cout de la solution 2-OPT: ",font=("Courier", 18)).grid(column=0, columnspan=1, row=5,padx=10,pady=10)
        Label(frame_opt, text=str(100*(cout_2opt - cout_methode) / cout_methode)+"%",font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=5,padx=10,pady=10)

    def show_3opt(self):
        frame = self.graph_frame.frame
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        Label(frame, text="Veuillez choisir l'algorithme pour l'instance de depart !").grid(column=0, columnspan=1, row=0,padx=10)

        listemethodes = ["sequetielle","Random", "ppv","ppv generalisé", "moindre cout"]
        listeCombo = ttk.Combobox(frame, values=listemethodes)
        listeCombo.grid(column=1, columnspan=1, row=0,padx=10)

        listeCombo.bind('<<ComboboxSelected>>', self.choix_box_3opt)
        listeCombo.current(0)
        # frame.pack()
        self.index = self.index + 1
        self.graph_frame.update()

    def choix_box_3opt(self,event):
        methode = event.widget.get()
        distances = self.file.distances
        instance = self.file.file_path.split('/')[-1]

        print(methode)
        if methode == "Random":
            resu2 = Rand(0, np.size(distances, 0) - 1, distances)
            cout_methode = resu2[0]
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "3-OPT", instance,
                                                                            resu2[2])
            if cout_2opt == None:
                print("hhh")
                resu = three_opt(resu2[2],distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(resu[2]) + float(resu2[1])
                fichier_save("./stats_file.csv", "3-OPT", instance, str(resu2[2]), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)

        elif methode == "sequetielle":
            li = []
            for i in range(np.size(distances, 0)):
                li.append(i)
            li.append(0)
            cout_methode = cost(distances, np.array(li))
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "3-OPT", instance, li)
            if cout_2opt == None:
                print("hhh")
                resu = three_opt(li, distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt)
                fichier_save("./stats_file.csv", "3-OPT", instance, str(li), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)

        elif methode == "ppv generalisé":
            cout_methode, tour_optimal, temps, temps_cum = get_results("./stats_file.csv", "ppv_gen", instance, "/")
            if cout_methode == None:
                resu2 = ppv_gen(distances)
                cout_methode = resu2[1]
                fichier_save("./stats_file.csv", "ppv_gen", instance, "/", resu2[1], str(resu2[0]), resu2[2], resu2[2])
                print("hhh")
            else:
                resu2 = [tour_optimal, cout_methode, temps]

            print(resu2)
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "3-OPT", instance,
                                                                            resu2[0])
            if cout_2opt == None:
                print("hhh")
                resu = three_opt(list(np.array(resu2[0]) - 1), distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt) + float(resu2[2])
                fichier_save("./stats_file.csv", "3-OPT", instance, str(resu2[0]), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)

        elif methode == "ppv":
            cout_methode, tour_optimal, temps, temps_cum = get_results("./stats_file.csv", "ppv", instance, 1)
            if cout_methode == None:
                resu2 = ppv(1, distances, True)
                cout_methode = resu2[1]
                fichier_save("./stats_file.csv", "ppv", instance, str(1), resu2[1], str(resu2[0]), resu2[2], resu2[2])
                print("hhh")
            else:
                print("fff")
                resu2 = [tour_optimal, cout_methode, temps]

            print(resu2)
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "3-OPT", instance,
                                                                            resu2[0])
            if cout_2opt == None:
                print("hhh")
                resu = three_opt(list(np.array(resu2[0]) - 1), distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt) + float(resu2[2])
                fichier_save("./stats_file.csv", "3-OPT", instance, str(resu2[0]), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)
        else:

            cout_methode, tour_optimal, temps, temps_cum = get_results("./stats_file.csv", "mc", instance, "/")
            if cout_methode == None:
                resu2 = moindre_cout(distances)
                cout_methode = resu2[0]
                fichier_save("./stats_file.csv", "mc", instance, "/", resu2[0], str(resu2[2]), resu2[1], resu2[1])
                print("hhh")
            else:
                print("fff")
                resu2 = [cout_methode, temps, tour_optimal]
            print(resu2)
            cout_2opt, tour_optimal, temps_2opt, temps_cumule = get_results("./stats_file.csv", "3-OPT", instance,
                                                                            resu2[2])
            if cout_2opt == None:
                print("hhh")
                resu = three_opt(resu2[2], distances)
                cout_2opt = resu[0]
                temps_2opt = resu[2]
                temps_cumule = float(temps_2opt) + float(resu2[1])
                fichier_save("./stats_file.csv", "3-OPT", instance, str(resu2[2]), str(cout_2opt), str(resu[1]),
                             temps_2opt, temps_cumule)

        frame =self.graph_frame.frame
        frame_opt = Frame(frame)
        frame_opt.grid(columnspan=2,row=self.index, sticky=N + S + E + W, padx=15, pady=5)
        self.index=self.index+1
        Grid.rowconfigure(frame_opt, 0, weight=1)
        Grid.columnconfigure(frame_opt, 0, weight=1)

        Label(frame_opt, text="Cout de l'heuristique 3-OPT avec : "+methode,font=("Courier", 18)).grid(column=0, columnspan=1, row=1,padx=10,pady=10)
        Label(frame_opt, text=str(cout_2opt),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=1,padx=10,pady=10)

        Label(frame_opt, text="Cout de la methode " + methode + ": ",font=("Courier", 18)).grid(column=0, columnspan=1, row=2,padx=10,pady=10)
        Label(frame_opt, text=str(cout_methode),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=2,padx=10,pady=10)
        Label(frame_opt, text="Temps d'execution 3-OPT: ",font=("Courier", 18)).grid(column=0, columnspan=1, row=3,padx=10,pady=10)
        Label(frame_opt, text=str(temps_2opt),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=3,padx=10,pady=10)

        Label(frame_opt, text="Temps cumulé des deux methodes: " ,font=("Courier", 18)).grid(column=0, columnspan=1, row=4,padx=10,pady=10)
        Label(frame_opt, text=str(temps_cumule),font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=4,padx=10,pady=10)

        Label(frame_opt,text="Gain en cout de la solution 3-OPT: ",font=("Courier", 18)).grid(column=0, columnspan=1, row=5,padx=10,pady=10)
        Label(frame_opt, text=str(100*(cout_2opt - cout_methode) / cout_methode)+"%",font=("Courier", 18),fg="#0000FF").grid(column=1, columnspan=1, row=5,padx=10,pady=10)

    def show_aco(self):
        frame = self.graph_frame.frame
        frame_aco = Frame(frame)
        frame_aco.grid(column=0, columnspan=1, row=0, sticky=N + S + E + W, padx=15, pady=5)
        Grid.rowconfigure(frame_aco, 0, weight=1)
        Grid.columnconfigure(frame_aco, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        depart = self.paramaters["aco"]["depart"]
        print(self.paramaters["aco"]["Q"])
        Qu = self.paramaters["aco"]["Q"]
        alpha = self.paramaters["aco"]["alpha"]
        beta = self.paramaters["aco"]["beta"]
        l = self.paramaters["aco"]["l"]
        it = self.paramaters["aco"]["it"]
        ro = self.paramaters["aco"]["ro"]

        depart_tk = IntVar()
        depart_tk.set(depart)
        Q_tk = IntVar()
        Q_tk.set(Qu)
        alpha_tk = IntVar()
        alpha_tk.set(alpha)
        beta_tk = IntVar()
        beta_tk.set(beta)
        l_tk = IntVar()
        l_tk.set(l)
        it_tk = IntVar()
        it_tk.set(it)

        ro_tk = StringVar()
        ro_tk.set(ro)

        frame_aco_params = Frame(frame_aco)
        frame_aco_params.pack()
        Label(frame_aco_params, text="Ville de départ:").grid(column=0, columnspan=1, row=0, padx=10)
        Entry(frame_aco_params, textvariable=depart_tk).grid(column=1, columnspan=1, row=0, padx=10)
        Label(frame_aco_params, text="Nombre de fourmis").grid(column=0, columnspan=1, row=1, padx=10)
        Entry(frame_aco_params, textvariable=l_tk).grid(column=1, columnspan=1, row=1, padx=10)
        Label(frame_aco_params, text="Nombre de tours").grid(column=0, columnspan=1, row=2, padx=10)
        Entry(frame_aco_params, textvariable=it_tk).grid(column=1, columnspan=1, row=2, padx=10)
        Label(frame_aco_params, text="Taux d'évaporation").grid(column=0, columnspan=1, row=3, padx=10)
        Entry(frame_aco_params, textvariable=ro_tk).grid(column=1, columnspan=1, row=3, padx=10)
        Label(frame_aco_params, text="Coefficient de maj des phéromones Q").grid(column=0, columnspan=1, row=4, padx=10)
        Entry(frame_aco_params, textvariable=Q_tk).grid(column=1, columnspan=1, row=4, padx=10)
        Label(frame_aco_params, text="Coefficient des phéromones").grid(column=0, columnspan=1, row=5, padx=10)
        Entry(frame_aco_params, textvariable=alpha_tk).grid(column=1, columnspan=1, row=5, padx=10)
        Label(frame_aco_params, text="Coefficient de la visibilité").grid(column=0, columnspan=1, row=6, padx=10)
        Entry(frame_aco_params, textvariable=beta_tk).grid(column=1, columnspan=1, row=6, padx=10)
        self.graph_frame.update()
        Button(frame_aco_params, text="Calculer",
               command=partial(self.show_aco_result, depart_tk, l_tk, it_tk, ro_tk, Q_tk, alpha_tk, beta_tk,
                               frame_aco_params)).grid(column=2, columnspan=1, row=0, padx=10)

    def show_aco_result(self, depart_tk, l_tk, it_tk, ro_tk, Q_tk, alpha_tk, beta_tk, frame_aco_params):
        depart = depart_tk.get()
        Qu = Q_tk.get()
        alpha = alpha_tk.get()
        beta = beta_tk.get()
        l = l_tk.get()
        it = it_tk.get()
        ro = 1 - float(ro_tk.get())

        distances = self.file.distances
        points, N = self.file.points,self.file.nb_villes
        #distances = self.load_distances(points, N)
        print(N)
        visibility = np.zeros((N, N), "double")
        P = np.zeros((N, N), "double")
        for i in range(N):
            for j in range(N):
                if (distances[i][j] != 0):
                    visibility[i][j] = 1 / distances[i][j]

        pheromone = [[1 / 100 for i in range(N)] for j in range(N)]
        pheromone2 = [[1 / 100 for i in range(N)] for j in range(N)]
        for a in range(N):
            pheromone[a][a] = 0
            pheromone2[a][a] = 0
        t1 = time.time()

        for t in range(it):
            for k in range(l):
                allowed = [i for i in range(N)]
                # i=np.random.randint(100)
                i = 0
                allowed.pop(allowed.index(i))
                for a in range(N - 1):
                    c = int(self.pk(i, allowed, pheromone, alpha, beta, visibility))
                    allowed.pop(allowed.index(c))
                    pheromone2[i][c] = pheromone[i][c] * ro + Qu / distances[i][c]
                    pheromone2[c][i] = pheromone2[i][c]

                    i = c
            for a in range(N):
                for b in range(N):
                    pheromone[a][b] = pheromone2[a][b]

        chemin = [0 for i in range(N)]
        i = 0
        cout = 0

        for a in range(N):
            ind = np.max(pheromone[i])
            j = pheromone[i].index(ind)
            for b in range(N):
                pheromone[b][i] = 0
            chemin[a] = j
            cout = cout + distances[i][j]
            i = j
        chemin[N - 1] = 0
        cout = cout + distances[i][0]
        t2 = time.time()
        Label(frame_aco_params, text="Cout : " + str(cout)).grid(column=0, columnspan=1, row=8, padx=10)
        Label(frame_aco_params, text="Temps : " + str(t2 - t1)).grid(column=0, columnspan=1, row=9, padx=10)
        instance = self.file.file_path.split('/')[-1]
        parametre=str(depart)+","+str(Qu)+","+str(alpha)+","+str(beta)+","+str(l)+","+str(it)+","+str(ro)
        temps = t2 - t1
        fichier_save("./stats_file.csv", "aco", instance, parametre, cout, chemin, temps, temps)
        print(chemin)
        print(cout)

    def pk(self, i, allowed, pheromone, alpha, beta, visibility):
        somme = 0
        for j in range(len(allowed)):
            somme = somme + (pheromone[i][allowed[j]] ** alpha) * (visibility[i][allowed[j]] ** beta)
        prob = [0 for j in range(len(allowed))]
        for j in range(len(allowed)):
            prob[j] = ((pheromone[i][allowed[j]] ** alpha) * (visibility[i][allowed[j]] ** beta)) / somme
        return np.random.choice(
            allowed,
            1,
            p=prob)

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



