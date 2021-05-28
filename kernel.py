import numpy as np
import matplotlib.pyplot as plt
import sys
import copy
import time
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class File:

        def __init__(self, file_path=None):
           self.file_path=file_path
           self.points,self.nb_villes=load_points_1(self.file_path)
           self.distances=load_distances_1(self.points,self.nb_villes)

def load_points_1(file_name):
    file = open(file_name, 'r')
    Name = file.readline().strip().split()[1]
    FileType = file.readline().strip().split()[1]
    Comment = file.readline().strip().split()[1]
    Dimension = file.readline().strip().split()[1]
    EdgeWeightType = file.readline().strip().split()[1]
    #print(Name)
    #print(EdgeWeightType)
    test=file.readline().strip()
    #print(test)
    #print(test == "EDGE_WEIGHT_FORMAT: FUNCTION")
    while test != "NODE_COORD_SECTION":
        test = file.readline().strip()
        #print(test)

    points = []
    N = int(Dimension)
    pi = 3.141592
    for i in range(0, int(Dimension)):
        x, y = file.readline().strip().split()[1:]
        degx = int(float(x))
        minx = float(x) - degx
        radx = pi * (degx + 5.0 * minx / 3.0) / 180.0

        degy = int(float(y))
        miny = float(y) - degy
        rady = pi * (degy + 5.0 * miny / 3.0) / 180.0

        points.append([radx, rady])
    file.close()
    return points, N


def load_distances_1(points, N):

    distances = np.full(shape=(N, N),fill_value=-1,dtype=int)
    mini = 10000
    rrr = 6378.388
    pi = 3.141592

    q1 = 0
    q2 = 0
    q3 = 0

    for i in range(N):
        for j in range(N):
            if (i != j):
                q1 = np.cos(points[i][1] - points[j][1])
                q2 = np.cos(points[i][0] - points[j][0])
                q3 = np.cos(points[i][0] + points[j][0])
                distances[i, j] = (int)(rrr * np.arccos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
                # distances[i, j] = np.sqrt(
                # np.square(points[i][0] - points[j][0]) + np.square(points[i][1] - points[j][1]))
                if mini > distances[i, j]:
                    mini = distances[i, j]
    print("************************************ max = ", mini)
    #print(distances)
    return distances







def villes_candidates(ensemble_e,nb_villes):
    v_candidates = []
    for k in range(nb_villes - 1):
        if 1 & ensemble_e:
            v_candidates.append(k)
        ensemble_e = ensemble_e >> 1
    # print("les villes candidates sont"), v_candidates
    return v_candidates


def calculer_cout(solution, distances):
    nb_villes = len(solution)
    cout = 0

    for i in range(nb_villes - 1):
        cout = cout + distances[solution[i]][solution[i + 1]]

    return cout


def exclure_sommet(sommet_s, ensemble_e):
    a = 1 << sommet_s
    masque = ~ a
    return ensemble_e & masque



def Programation_dynamique(Graphe, nb_villes):

    tableau_dynamique = [{}]
    time1 = time.time()
    for i in range(nb_villes - 1):
        (tableau_dynamique[0])[i] = (Graphe[i, nb_villes - 1], i)

    for i in range((2 ** (nb_villes - 1)) - 1):
        ensemble = i + 1
        complement_ensemble = ~ ensemble
        tableau_dynamique.append({})
        villes_candidates_complement_ensemble = villes_candidates(complement_ensemble,nb_villes)
        villes_candidates_complement_ensemble.append(nb_villes - 1)
        for ville in villes_candidates_complement_ensemble:
            minimum = 100000
            dernier2 = nb_villes - 1
            for sommet in villes_candidates(ensemble,nb_villes):
                ensemble_reduit = exclure_sommet(sommet, ensemble)
                a, b = (tableau_dynamique[ensemble_reduit])[sommet]
                if Graphe[ville, sommet] + a < minimum:
                    minimum = Graphe[ville, sommet] + a
                    dernier2 = sommet
            (tableau_dynamique[ensemble])[ville] = (minimum, dernier2)
    time2 = time.time()



    m = (2 ** (nb_villes - 1)) - 1
    (c, d) = tableau_dynamique[m][nb_villes - 1]
    chemin_hamiltionien = [nb_villes - 1]
    indice_tab = (2 ** (nb_villes - 1)) - 1
    for i in reversed(range(nb_villes - 1)):
        x, y = (tableau_dynamique[indice_tab])[chemin_hamiltionien[nb_villes - 2 - i]]
        chemin_hamiltionien.append(y)
        indice_tab = exclure_sommet(y, indice_tab)

    cpt = Graphe[chemin_hamiltionien[0], chemin_hamiltionien[nb_villes - 1]]

    for i in range(nb_villes - 1):
        cpt = cpt + Graphe[chemin_hamiltionien[i], chemin_hamiltionien[i + 1]]

    chemin_hamiltionien.append(chemin_hamiltionien[0])
    print(chemin_hamiltionien)
    return chemin_hamiltionien, cpt,(time2 - time1) / 60



def courbes_methodes_exactes(Graphe, nb_villes,points):
    liste_p = [] #programmation d
    liste_b = [] # b&b
    liste_b_ameliore = []  # b&b
    x = []
    liste_b.insert(0,0)
    liste_p.insert(0, 0)
    liste_b_ameliore.insert(0, 0)
    x.insert(0,0)
    for i in range(2, 21):
        #print("i = ", i)
        copie = np.full(shape=(i, i), fill_value=-1, dtype=int)
        for a in range(i):
            for b in range(i):
                copie[a][b] = Graphe[a][b]

        #Programmation dynamique
        time1 = time.time()
        Programation_dynamique(Graphe, i)
        time2 = time.time()
        liste_p.insert(i, (time2-time1)/60)

        # Branch and Bound amélioré
        cout, circuit, nb_noeud, temps = branchAndBoundAmeliore(copie, True,points)
        liste_b_ameliore.insert(i, (temps) / 60)

        # Branch and Bound
        cout, circuit, nb_noeud, temps = branchAndBoundAmeliore(copie, False,points)
        liste_b.insert(i, (temps) / 60)

        x.insert(i, i)

    #print(liste_p)
    Y1 = np.asarray(liste_p)
    Y2 = np.asarray(liste_b)
    Y3 = np.asarray(liste_b_ameliore)
    X = np.asarray(x)
    fig,ax = plt.subplots(figsize=(12, 6))
    ax.plot(X,Y1, label='Programmation dynamique')
    ax.plot(X,Y2, label='Branch and Bound')
    ax.plot(X, Y3, label = 'Branch and Bound amelioré')
    fig.legend()
    ax.set_ylabel('temps d\'exécution')
    ax.set_xlabel('nombre de villes')
    return fig
    #plt.show()  # affiche la figure a l'ecran

def eliminerSousTournee(ens_aretes, matrice):
    for i in range(0, matrice.shape[0]):
        for j in range(0, matrice.shape[1]):
            if matrice[i, j] > -1:
                for k in range(len(ens_aretes)):
                    depart, arrive = ens_aretes[k]
                    if j in depart and i in arrive:
                        matrice[i, j] = -1


def ajouterArete(ens_aretes1, de, ar, coordonnees_points, ameliore):
    if len(ens_aretes1) == 0:
        ens_aretes1.append(([de], [ar]))
        return False
    else:
        indice = -1
        i = 0
        ajout = False
        if ameliore:
            x_de = coordonnees_points[de][0]
            y_de = coordonnees_points[de][1]
            x_ar = coordonnees_points[ar][0]
            y_ar = coordonnees_points[ar][1]
        while i < len(ens_aretes1):
            depart, arrive = ens_aretes1[i]
            if ameliore:
                j = 0
                while j < len(depart):
                    x_depart = coordonnees_points[depart[j]][0]
                    y_depart = coordonnees_points[depart[j]][1]
                    x_arrive = coordonnees_points[arrive[j]][0]
                    y_arrive = coordonnees_points[arrive[j]][1]
                    q1 = (x_depart - x_de) * (y_ar - y_de) - (y_depart - y_de) * (x_ar - x_de)
                    q2 = (y_ar - y_de) * (x_arrive - x_de) - (y_arrive - y_de) * (x_ar - x_de)
                    q3 = (x_de - x_depart) * (y_arrive - y_depart) - (y_de - y_depart) * (x_arrive - x_depart)
                    q4 = (x_ar - x_depart) * (y_arrive - y_depart) - (y_ar - y_depart) * (x_arrive - x_depart)
                    if q1 * q2 < 0 and q3 * q4 < 0:
                        return True
                    j = j + 1
            if de in arrive or ar in depart:
                ajout = True
                if indice == -1:
                    depart.append(de)
                    arrive.append(ar)
                    indice = i
                else:
                    depart2, arrive2 = ens_aretes1[indice]
                    while depart:
                        depart2.append(depart.pop())
                        arrive2.append(arrive.pop())
                    del ens_aretes1[i]
            i = i + 1
        if not ajout:
            ens_aretes1.append(([de], [ar]))
            return False



def reductionMatrice(matrice):
    m_l = []
    for i in range(0, matrice.shape[0]):
        mini = sys.maxsize
        for j in range(0, matrice.shape[1]):
            if 0 <= matrice[i, j] < mini:
                mini = matrice[i, j]
        if mini == sys.maxsize:
            m_l.append(0)
        else:
            m_l.append(mini)
    min_lignes = np.array(m_l)
    evaluation = np.sum(min_lignes)
    for j in range(0, matrice.shape[1]):
        matrice[:, j] = matrice[:, j] - min_lignes
    m_c = []
    for i in range(0, matrice.shape[1]):
        mini = sys.maxsize
        for j in range(0, matrice.shape[0]):
            if 0 <= matrice[j, i] < mini:
                mini = matrice[j, i]
        if mini == sys.maxsize:
            m_c.append(0)
        else:
            m_c.append(mini)
    min_colonnes = np.array(m_c)
    evaluation = evaluation + np.sum(min_colonnes)
    for i in range(0, matrice.shape[0]):
        matrice[i, :] = matrice[i, :] - min_colonnes
    return evaluation


def calculerRegretMax(matrice):
    cases_nulles = []
    regrets = []
    obligation = False
    coordonees_regret_max = (32, 32)
    for i in range(0, matrice.shape[0]):
        for j in range(0, matrice.shape[1]):
            if matrice[i, j] == 0:
                ligne = np.copy(matrice[i, :])
                ligne[j] = -1
                colonne = np.copy(matrice[:, j])
                colonne[i] = -1
                if ligne[ligne >= 0].size != 0:
                    min_ligne = ligne[ligne >= 0].min()
                else:
                    min_ligne = 0
                    obligation = True
                    regret_max = 0
                    coordonees_regret_max = (i, j)
                if colonne[colonne >= 0].size != 0:
                    min_colonne = colonne[colonne >= 0].min()
                else:
                    min_colonne = 0
                    obligation = True
                    regret_max = 0
                    coordonees_regret_max = (i, j)
                cases_nulles.append((i, j))
                regrets.append(min_ligne + min_colonne)
    if not obligation:
        regret_max = -1
        indice_regret_max = 0
        for index, regret in enumerate(regrets):
            if regret > regret_max:
                regret_max = regret
                indice_regret_max = index
        coordonees_regret_max = cases_nulles[indice_regret_max]

    return regret_max, coordonees_regret_max, obligation


def enelverLigneColonne(matrice, ligne, colonne):
    for i in range(matrice.shape[0]):
        matrice[ligne, i] = -1
        matrice[i, colonne] = -1


def visiterNoeud(matrice_a, ens_aretes, nb_sommets, cout, solution_opt, nb_noeud, cp, ameliore):
    nb_noeud[0] = nb_noeud[0] + 1
    matrice = matrice_a.copy()
    evaluation = reductionMatrice(matrice)
    evaluation = evaluation + cout
    if evaluation < solution_opt[0]:
        if matrice.shape[0] - nb_sommets > 2:
            regret_max, coordonees_regret_max, obligation = calculerRegretMax(matrice)
            i, j = coordonees_regret_max
            new_ens_aretes = copy.deepcopy(ens_aretes)
            new_nb_sommets = nb_sommets + 1
            coupe = ajouterArete(new_ens_aretes, i, j, cp, ameliore)
            if not coupe or not ameliore:
                new_matrice = matrice.copy()
                enelverLigneColonne(new_matrice, i, j)
                eliminerSousTournee(new_ens_aretes, new_matrice)
                new_cout = evaluation
                visiterNoeud(new_matrice,new_ens_aretes,new_nb_sommets,new_cout,solution_opt,nb_noeud,cp, ameliore)
            new_cout2 = evaluation + regret_max
            if new_cout2 < solution_opt[0] and not obligation:
                new_matrice2 = matrice.copy()
                new_matrice2[i, j] = -1
                ens_aretes2 = copy.deepcopy(ens_aretes)
                visiterNoeud(new_matrice2, ens_aretes2, nb_sommets, evaluation, solution_opt, nb_noeud, cp, ameliore)

        else:
            for i in range(matrice.shape[0]):
                for j in range(matrice.shape[0]):
                    if matrice[i, j] >= 0:
                        evaluation = evaluation + matrice[i, j]
                        ajouterArete(ens_aretes, i, j, cp, False)


            temp = solution_opt[0]
            if evaluation < temp:
                solution_opt[0] = evaluation
                if len(solution_opt)==1:
                    solution_opt.append(ens_aretes)
                else:
                    solution_opt[1] = ens_aretes


def branchAndBoundAmeliore(Graphe, ameliore,points):
    solution = [Graphe[Graphe.shape[0] - 1, 0]]
    circuit_base1 = []
    circuit_base2 = []
    for i in range(Graphe.shape[0] - 1):
        solution[0] = solution[0] + Graphe[i, i + 1]
        circuit_base1.append(i)
        circuit_base2.append(i+1)
    circuit_base1.append(Graphe.shape[0]-1)
    circuit_base2.append(0)
    solution.append([(circuit_base1, circuit_base2)])
    nb_noeud = [0]
    ens = []
    t1 = time.time()
    #print(solution)
    visiterNoeud(Graphe, ens, 0, 0, solution, nb_noeud, points, ameliore)
    t2 = time.time()

    cout = solution[0]
    depart, arrive = (solution[1])[0]
    circuit = [0]
    index_actu = depart.index(0)
    for i in range(Graphe.shape[0]-1):
        prochain = arrive[index_actu]
        circuit.append(prochain)
        index_actu = depart.index(prochain)
    circuit.append(0)
    temps = t2-t1
    #print("Cout=",cout)
    #print("tour=",circuit)
    #print("temps=",temps)
    return cout, circuit, nb_noeud[0], temps

def plotcycle(points, route, cout, file_path,algo,texec):
    print(route)
    font1 = {'family': 'serif', 'color': 'blue', 'size': 16}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    custom_line = [Line2D([0], [0], color='blue', lw=4)]
    #axx = plt.figure(1, figsize=(10, 10))



    sorted_list1 = []
    for i in range(len(route)):
        sorted_list1.append([points[route[i]][0], points[route[i]][1]])
    print(sorted_list1)
    x = list(list(zip(*sorted_list1))[0])
    y = list(list(zip(*sorted_list1))[1])
    print(x)
    print(y)
    fig, axx = plt.subplots(figsize=(12, 6))
    axx.plot(x, y, '-p', color='blue',
                   markersize=4, linewidth=2,
                   markerfacecolor='white',
                   markeredgecolor='red',
                   markeredgewidth=2)
    phrase = "Cout total du cycle:" + str(cout)
    temps_dexec = "Temps d'éxuction avec "+str(algo)+" "+str(texec)
    fig.legend(custom_line, [phrase], prop={'size': 12}, loc="upper left")
    fig.legend(custom_line,[temps_dexec],prop={'size': 12},loc="upper right")
    axx.set_title("Graphe du cycle des villes visitées", fontdict=font1)
    axx.set_ylabel('ordonnées des villes', fontdict=font2)
    axx.set_xlabel('abscisses des villes', fontdict=font2)
    i = 0
    for elem in points:
        axx.annotate(str(i), (elem[0], elem[1]),size=15)
        i = i + 1
    #plt.savefig(file_path + '.png')
    return fig