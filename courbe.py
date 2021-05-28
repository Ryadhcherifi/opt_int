import numpy as np
import matplotlib.pyplot as plt
import sys
import copy
import time


def load_points_1(file_name):
    file = open(file_name, 'r')
    Name = file.readline().strip().split()[1]
    FileType = file.readline().strip().split()[1]
    Comment = file.readline().strip().split()[1]
    Dimension = file.readline().strip().split()[1]
    EdgeWeightType = file.readline().strip().split()[1]
    print(Name)
    print(EdgeWeightType)
    test=file.readline().strip()
    print(test)
    print(test == "EDGE_WEIGHT_FORMAT: FUNCTION")
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
    return distances







def villes_candidates(ensemble_e):
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
    t1 = time.time()
    for i in range(nb_villes - 1):
        (tableau_dynamique[0])[i] = (Graphe[i, nb_villes - 1], i)

    for i in range((2 ** (nb_villes - 1)) - 1):
        ensemble = i + 1
        complement_ensemble = ~ ensemble
        tableau_dynamique.append({})
        villes_candidates_complement_ensemble = villes_candidates(complement_ensemble)
        villes_candidates_complement_ensemble.append(nb_villes - 1)
        for ville in villes_candidates_complement_ensemble:
            minimum = 100000
            dernier2 = nb_villes - 1
            for sommet in villes_candidates(ensemble):
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

    #chemin_hamiltionien.append(chemin_hamiltionien[0])
    return chemin_hamiltionien, cpt



def courbe(Graphe, nb_villes):
    liste_p = [] #programmation d
    liste_b = [] # b&b
    x = []
    liste_b.insert(0,0)
    liste_p.insert(0,0)
    x.insert(0,0)
    for i in range(2, nb_villes+1):
        print("i = ", i)

        #Programmation dynamique
        time1 = time.time()
        Programation_dynamique(Graphe, i)
        time2 = time.time()
        liste_p.insert(i, (time2-time1)/60)


        #Branch and Bound
        time1 = time.time()
        ## Appel B&B
        time2 = time.time()
        liste_b.insert(i, (time2 - time1) / 60)


        x.insert(i,i)

    print(liste_p)
    Y1 = np.asarray(liste_p)
    Y2= np.asarray(liste_b)
    X = np.asarray(x)
    fig,ax = plt.subplots()
    ax.plot(X,Y1, label='Programmation dynamique')
    ax.plot(X,Y2, label='Branch and Bound')
    fig.legend()
    ax.set_ylabel('temps d\'exécution')
    ax.set_xlabel('nombre de villes')
    plt.savefig('courbe.png')

    plt.show()  # affiche la figure a l'ecran




file_name = 'burma14.tsp'
points, N = load_points_1(file_name)
distances = load_distances_1(points, N)
np.savetxt("distances.txt", distances)
nb_villes = N
Graphe = distances
courbe(Graphe, nb_villes)




#a, b = Programation_dynamique(Graphe, nb_villes)
