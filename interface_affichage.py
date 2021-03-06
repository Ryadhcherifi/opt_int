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
            "depart": 1
        }
        self.paramaters["ppv"]=ppv
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



