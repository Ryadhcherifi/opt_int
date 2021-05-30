from timeit import default_timer as timer
from moindre_cout import cycle, transform, degre, tolist, moindre_cout
from twoopt import two_opt2
from voisinage import generer_voisinage1, calculer_cout, generer_voisinage_opt, generer_voisinage
import pandas as pd
import numpy as np
import math
from random import randint
import time
from random import shuffle

file_name = 'pr439.tsp'


def load_points(file_name):
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
        x, y = file.readline().strip().split()[1:]
        points.append([float(x), float(y)])
    file.close()
    return points, N


def load_distances(points, N):
    distances = np.zeros((N, N), "double")
    for i in range(N):
        for j in range(N):
            if (i != j):
                distances[i, j] = np.sqrt(
                    np.square(points[i][0] - points[j][0]) + np.square(points[i][1] - points[j][1]))
    return distances


def ppv1(ville_initiale, distances):
    cycle = []
    j = ville_initiale
    # cycle.append(j)
    prec = j
    cout = 0
    nb_villes = distances.shape[0]
    print("\n")
    for i in range(nb_villes):
        cycle.append(j)
        prec = j
        j = (j + 1) % nb_villes
        cout = cout + distances[prec][j]

    cycle.append(ville_initiale)
    cout = calculer_cout(cycle, distances)
    return cycle, cout


def ppv(debut, distances):
    debut = debut + 1
    visite = [debut - 1]
    N = distances.shape[0]
    last = debut
    cout = 0
    not_visite = list(range(1, N + 1))
    not_visite.remove(debut)
    while (len(visite) != N):
        min_ville = None
        min_distance = None

        for i in not_visite:
            num_ville = i
            if (num_ville != last):
                if (min_ville) == None:
                    min_ville = num_ville
                    min_distance = distances[num_ville - 1, last - 1]
                    (a, b) = (num_ville - 1, last - 1)

                elif (distances[num_ville - 1, last - 1] < min_distance):
                    min_ville = num_ville
                    min_distance = distances[num_ville - 1, last - 1]
                    (a,b) =(num_ville - 1, last -1)
        last = min_ville
        visite.append(min_ville - 1)
        not_visite.remove(min_ville)
        #print((a,b), min_distance)
        cout += min_distance
    cout += distances[last - 1, debut -1]
    #print((last, debut),distances[last, debut])
    visite.append(debut - 1)
    return visite, cout


def mini_ppv(chaine, distances):
    not_visite = chaine.copy()
    not_visite.pop()
    not_visite.pop(0)
    new_chaine = []
    new_chaine.append(chaine[0])
    cout = 0
    last = chaine[0]
    a= 0
    while(len(not_visite)>0):
        #print(a)
        a+=1
        min_ville = None
        min_distance = None
        for i in not_visite:
            num_ville = i
            #print("distances[",num_ville,",", last,"]", distances[num_ville, last])
            if (min_ville) == None:
                min_ville = num_ville
                min_distance = distances[num_ville, last]
                #(a, b) = (num_ville - 1, last - 1)

            elif (distances[num_ville, last] < min_distance):
                min_ville = num_ville
                min_distance = distances[num_ville, last]
                #(a, b) = (num_ville - 1, last - 1)

        last = min_ville
        new_chaine.append(min_ville)
        #print(min_ville)
        not_visite.remove(min_ville)
        # print((a,b), min_distance)
        #cout += min_distance
    new_chaine.append(chaine[-1])
    return new_chaine






def RGR(solution_courante, distances, mu):
    s_rgr = solution_courante.copy()
    cout = calculer_cout(s_rgr, distances)
    print(distances.shape[0])
    i = randint(1,distances.shape[0]-1-mu)
    tmp = s_rgr[i:i+mu]
    tmp = mini_ppv(tmp, distances)
    s_rgr[i:i + mu] = tmp
    return s_rgr, calculer_cout(s_rgr, distances)




def recherche_tabou(distances, ville_initiale):
    PAS_AUGMENTATION = 0.75
    PAS_DIMINUTION = 1.25
    nb_villes = distances.shape[0]
    nb_iteration = 0
    MAX_ITERATION = 10000
    TAILLE_LISTE_TABOU_MAX = 100
    print(nb_villes)
    continu = True
    taille_voisinage = 20.0
    TAILLE_VOISINAGE_MIN = 20
    TAILLE_VOISINAGE_MAX = 40
    taille_liste_tabou = 0
    liste_tabou = []
    solution_courante, cout = ppv(ville_initiale, distances)
    cout = calculer_cout(solution_courante, distances)
    solution_max = solution_courante  # la meilleure sol
    cout_min = cout
    taille_list_tabou = 0
    cout_initial = cout
    print("solution plus proche voisin", solution_courante, cout)
    print("cout plus proche voisin ", calculer_cout(solution_courante, distances))



    """voisinage,couts,i_min,permut_min = generer_voisinage(solution_courante,cout,taille_voisinage,distances,liste_tabou)
    for i in range(taille_voisinage):
        print(couts[i], voisinage[i])


    print("\n imin = ",i_min,"cout = ",couts[i_min],"permut min ",permut_min)
    liste_tabou.append((permut_min[1],permut_min[0]))

    print("la liste tabou ",len(liste_tabou),"\n",liste_tabou)

    print("amelioration = ",(cout_initial*100)/cout_min,"%")"""

    while (continu):
        if (nb_iteration % 10000 == 0):
            print(nb_iteration)
            # print("taille v ", taille_voisinage)
        voisinage, couts, i_min, permut_min = generer_voisinage(solution_courante, cout, int(taille_voisinage),
                                                                distances,
                                                                liste_tabou)

        solution_courante = voisinage[i_min]
        # print("", couts[i_min], solution_courante)
        if (taille_list_tabou < TAILLE_LISTE_TABOU_MAX):
            liste_tabou.append((permut_min[1], permut_min[0]))
            taille_list_tabou = taille_list_tabou + 1
            # print("on ajoute ",(permut_min[1], permut_min[0]))
        else:
            # print((permut_min[1], permut_min[0])," liste tabou",liste_tabou)
            liste_tabou.append((permut_min[1], permut_min[0]))
            liste_tabou.pop(0)
            # print((permut_min[1], permut_min[0])," liste tabou", liste_tabou)

        # maj de la taille du voisinnage
        if (couts[i_min] < cout):

            taille_voisinage = taille_voisinage + PAS_AUGMENTATION

            if (taille_voisinage > TAILLE_VOISINAGE_MAX):
                taille_voisinage = TAILLE_VOISINAGE_MAX

        else:
            taille_voisinage = taille_voisinage - PAS_DIMINUTION

            if (taille_voisinage < TAILLE_VOISINAGE_MIN):
                taille_voisinage = TAILLE_VOISINAGE_MIN

        # print(taille_voisinage)
        cout = couts[i_min]

        if (cout < cout_min):
            solution_max = solution_courante
            cout_min = cout

        # print(cout, solution_courante)
        nb_iteration = nb_iteration + 1
        if (nb_iteration > MAX_ITERATION):
            continu = False

    amelioration = (cout_initial * 100) / cout_min

    return solution_max, cout_min, amelioration



def diversification(sol_courante, distances):
    noeud_1 = 0
    noeud_2 = 0
    nb = randint(1, len(sol_courante) - 2)
    nb = nb % 30
    new_sol = sol_courante.copy()

    for i in range(nb):

        while ((noeud_1 == noeud_2) or (noeud_1 == noeud_2 + 1) or (noeud_2 == noeud_1 + 1)):
            noeud_1 = randint(1, len(sol_courante) - 2)
            noeud_2 = randint(1, len(sol_courante) - 2)
            new_sol[noeud_2] = sol_courante[noeud_1]
            new_sol[noeud_1] = sol_courante[noeud_2]
    cout = calculer_cout(new_sol, distances)
    print("div", nb, cout)
    return new_sol, cout


def fichier_save_tabou_hyb(file,nom_fichier,cout,temps ,depart, mu,PAS_AUGMENTATION ,PAS_DIMINUTION , MAX_ITERATION, TAILLE_LISTE_TABOU_MAX , taille_voisinage ,TAILLE_VOISINAGE_MIN , TAILLE_VOISINAGE_MAX):
    df = pd.read_csv(file)
    data2 = {
        "cout" : cout,
        "temps": temps,
        "depart": depart,
        "mu" : mu,
        "PAS_AUGMENTATION" : PAS_AUGMENTATION,
        "PAS_DIMINUTION" : PAS_DIMINUTION,
        "MAX_ITERATION" : MAX_ITERATION,
        "TAILLE_LISTE_TABOU_MAX" : TAILLE_LISTE_TABOU_MAX,
        "taille_voisinage" : taille_voisinage,
        "TAILLE_VOISINAGE_MIN" : TAILLE_VOISINAGE_MIN,
        "TAILLE_VOISINAGE_MAX" : TAILLE_VOISINAGE_MAX
    }
    df = df.append(data2, ignore_index=True)
    df.to_csv(nom_fichier, index=False)


    return None


def recherche_tabou_2opt(distances, ville_initiale,depart="opt" ,mu = 150,PAS_AUGMENTATION = 0.75,PAS_DIMINUTION = 1.0, MAX_ITERATION =18000, TAILLE_LISTE_TABOU_MAX = 80, taille_voisinage = 20 ,TAILLE_VOISINAGE_MIN = 15, TAILLE_VOISINAGE_MAX = 25):

    div = 0
    nb_villes = distances.shape[0]

    nb_iteration = 0
    print(nb_villes)
    continu = True
    liste_tabou = []

    print("parametrable")
    #18000


    NB_ESSAIS = 25

    if(depart=="ppv1"):
        print("depart = ", depart)
        solution_courante, cout = ppv1(ville_initiale, distances)
        print(" interface ", distances.shape, "solution plus proche voisin", cout)

    else:
        solution_courante, cout = ppv(ville_initiale, distances)
        print(" interface ", distances.shape, "solution plus proche voisin", cout)
        if((depart=="opt")or(depart=="mc")):

            cout, solution_courante, temps = moindre_cout(distances)
            print("solution moindre cout ", temps, cout, calculer_cout(solution_courante, distances))

            if (depart == "opt"):
                cout, solution_courante, temps = two_opt2(solution_courante, distances)
                print("solution 2OPT ", temps, cout, calculer_cout(solution_courante, distances))





    solution_max = solution_courante  # la meilleure sol

    cout_min = cout
    taille_list_tabou = 0
    cout_initial = cout

    start = timer()

    while (continu):
        """if (nb_iteration % 2000 == 0):
            print(nb_iteration, taille_voisinage, cout)
            # print("taille v ", taille_voisinage)"""

        solution_courante, new_cout, permut_min = generer_voisinage_opt(solution_courante, cout, int(taille_voisinage),
                                                                     distances,
                                                                     liste_tabou, NB_ESSAIS)


        # print("", couts[i_min], solution_courante)
        if (taille_list_tabou < TAILLE_LISTE_TABOU_MAX):
            liste_tabou.append((permut_min[1], permut_min[0]))
            taille_list_tabou = taille_list_tabou + 1
            # print("on ajoute ",(permut_min[1], permut_min[0]))
        else:
            # print((permut_min[1], permut_min[0])," liste tabou",liste_tabou)
            liste_tabou.append((permut_min[1], permut_min[0]))
            liste_tabou.pop(0)
            # print((permut_min[1], permut_min[0])," liste tabou", liste_tabou)

        # maj de la taille du voisinnage
        if (new_cout < cout):
            taille_voisinage = taille_voisinage + PAS_AUGMENTATION

            if (taille_voisinage > TAILLE_VOISINAGE_MAX):
                taille_voisinage = TAILLE_VOISINAGE_MAX

        else:
            taille_voisinage = taille_voisinage - PAS_DIMINUTION

            if (taille_voisinage < TAILLE_VOISINAGE_MIN):
                taille_voisinage = TAILLE_VOISINAGE_MIN

        # print(taille_voisinage)
        cout = new_cout

        if (cout < cout_min):
            solution_max = solution_courante

            cout_min1, solution_max, t = two_opt2(solution_max, distances)

            cout_min = cout_min1

        else:
            div = div + 1
        # print(cout, solution_courante)
        if(div>4000):
            div = 0
            cout1 = cout
            #solution_courante, cout = diversification(solution_max, distances)
            solution_courante, cout = RGR(solution_max, distances, mu)
            cout2 = cout
            cout, solution_courante, t = two_opt2(solution_courante, distances)
            #print("apres diiiv", cout1, cout2, cout)
            if (cout < cout_min):
                solution_max = solution_courante
                cout_min = cout



        nb_iteration = nb_iteration + 1
        if (nb_iteration > MAX_ITERATION):
            continu = False
    end = timer()
    amelioration = (cout_initial * 100) / cout_min

    # -*- coding: utf -*-
    # ouverture en écriture

    #fichier_save_tabou_hyb ("save.csv",file_name, str(cout_min), str(end - start), depart, str(mu), str(PAS_AUGMENTATION), str(PAS_DIMINUTION), str(MAX_ITERATION),str(TAILLE_LISTE_TABOU_MAX), str(taille_voisinage), str(TAILLE_VOISINAGE_MIN), str(TAILLE_VOISINAGE_MAX))

    f = open("savetabou.txt", "a+")
    # écriture

    f.write("sol initiale = PPV")
    f.write(" | instance = ")
    f.write(file_name)
    f.write(" | amelioration ")
    f.write(str(amelioration))
    f.write(" | cout=")
    f.write(str(cout_min))
    f.write(" | temps=")
    f.write(str(end - start))
    f.write(" | PAS_AUGMENTATION=")
    f.write(str(PAS_AUGMENTATION))
    f.write(" | PAS_DIMINUTION=")
    f.write(str(PAS_DIMINUTION))
    f.write(" | MAX_ITERATION=")
    f.write(str(MAX_ITERATION))
    f.write(" | TAILLE_LISTE_TABOU_MAX=")
    f.write(str(TAILLE_LISTE_TABOU_MAX))
    f.write(" | taille_voisinage=")
    f.write(str(taille_voisinage))
    f.write(" | TAILLE_VOISINAGE_MIN=")
    f.write(str(TAILLE_VOISINAGE_MIN))
    f.write(" | TAILLE_VOISINAGE_MAX=")
    f.write(str(TAILLE_VOISINAGE_MAX))
    f.write(" |NB_ESSAIS=")
    f.write(str(NB_ESSAIS))
    f.write("\n")
    f.write("******************************************************************************************************************")
    f.write("\n")

    # fermeture
    f.close()

    return solution_max, cout_min, amelioration, (end-start)

def tabou_simple(distances, ville_initiale, solution_courante, cout, MAX_ITERATION= 1500, PAS_AUGMENTATION = 0.75, PAS_DIMINUTION = 1.0, TAILLE_LISTE_TABOU_MAX = 80, taille_voisinage = 20, TAILLE_VOISINAGE_MIN = 15, TAILLE_VOISINAGE_MAX = 25):
    div = 0
    nb_villes = distances.shape[0]


    #MAX_ITERATION = 1500
    NB_ESSAIS = 55

    nb_iteration = 0
    print(nb_villes)
    continu = True
    liste_tabou = []

    solution_max = solution_courante  # la meilleure sol

    cout_min = cout
    taille_list_tabou = 0
    cout_initial = cout

    start = timer()

    while (continu):
        if (nb_iteration % 2000 == 0):
            print(nb_iteration, taille_voisinage, cout)
            # print("taille v ", taille_voisinage)

        solution_courante, new_cout, permut_min = generer_voisinage_opt(solution_courante, cout, int(taille_voisinage),
                                                                        distances,
                                                                        liste_tabou, NB_ESSAIS)

        # print("", couts[i_min], solution_courante)
        if (taille_list_tabou < TAILLE_LISTE_TABOU_MAX):
            liste_tabou.append((permut_min[1], permut_min[0]))
            taille_list_tabou = taille_list_tabou + 1
            # print("on ajoute ",(permut_min[1], permut_min[0]))
        else:
            # print((permut_min[1], permut_min[0])," liste tabou",liste_tabou)
            liste_tabou.append((permut_min[1], permut_min[0]))
            liste_tabou.pop(0)
            # print((permut_min[1], permut_min[0])," liste tabou", liste_tabou)

        # maj de la taille du voisinnage
        if (new_cout < cout):
            taille_voisinage = taille_voisinage + PAS_AUGMENTATION

            if (taille_voisinage > TAILLE_VOISINAGE_MAX):
                taille_voisinage = TAILLE_VOISINAGE_MAX

        else:
            taille_voisinage = taille_voisinage - PAS_DIMINUTION

            if (taille_voisinage < TAILLE_VOISINAGE_MIN):
                taille_voisinage = TAILLE_VOISINAGE_MIN

        # print(taille_voisinage)
        cout = new_cout

        if (cout < cout_min):
            solution_max = solution_courante
            #cout_min1, solution_max, t = two_opt2(solution_max, distances)
            #print("HEEEEY", cout_min, cout)
            cout_min = cout

        else:
            div = div + 1
        # print(cout, solution_courante)


        nb_iteration = nb_iteration + 1
        if (nb_iteration > MAX_ITERATION):
            continu = False
    end = timer()
    amelioration = (cout_initial * 100) / cout_min


    """# ouverture en écriture
    f = open("savetabou.txt", "a+")
    # écriture

    f.write(" | amelioration ")
    f.write(str(amelioration))
    f.write(" | cout=")
    f.write(str(cout_min))
    f.write(" | PAS_AUGMENTATION=")
    f.write(str(PAS_AUGMENTATION))
    f.write(" | PAS_DIMINUTION=")
    f.write(str(PAS_DIMINUTION))
    f.write(" | MAX_ITERATION=")
    f.write(str(MAX_ITERATION))
    f.write(" | TAILLE_LISTE_TABOU_MAX=")
    f.write(str(TAILLE_LISTE_TABOU_MAX))
    f.write(" | taille_voisinage=")
    f.write(str(taille_voisinage))
    f.write(" | TAILLE_VOISINAGE_MIN=")
    f.write(str(TAILLE_VOISINAGE_MIN))
    f.write(" | TAILLE_VOISINAGE_MAX=")
    f.write(str(TAILLE_VOISINAGE_MAX))
    f.write(" |NB_ESSAIS=")
    f.write(str(NB_ESSAIS))
    f.write("\n")
    f.write(
        "******************************************************************************************************************")
    f.write("\n")

    # fermeture
    f.close()
    """
    return solution_max, cout_min, amelioration, (end - start)





def ITS(distances, ville_initiale, mu = 150, NB_IT_ITS = 12,MAX_ITERATION=800 ,PAS_AUGMENTATION = 0.75, PAS_DIMINUTION = 1.0, TAILLE_LISTE_TABOU_MAX = 80, taille_voisinage = 20, TAILLE_VOISINAGE_MIN = 15, TAILLE_VOISINAGE_MAX = 25):
    print("IIIITTTSSSSS")
    s_initale, cout_initial = ppv1(ville_initiale, distances)
    print("solution plus proche voisin 1", cout_initial, s_initale)
    # cout, solution_courante, temps = moindre_cout(distances)
    # print("solution moindre cout ",temps, cout, solution_courante, cout)

    # cout, solution_courante, temps = two_opt2(solution_courante, distances)
    # print("solution 2OPT ",temps, cout, solution_courante, cout)

    #s_point first optimized solution
    #s sol courant
    s_point, cout_point, amelioration, temps = tabou_simple(distances, ville_initiale, s_initale, cout_initial, MAX_ITERATION=1500,PAS_AUGMENTATION = PAS_AUGMENTATION, PAS_DIMINUTION = PAS_DIMINUTION, TAILLE_LISTE_TABOU_MAX = TAILLE_LISTE_TABOU_MAX, taille_voisinage = taille_voisinage, TAILLE_VOISINAGE_MIN = TAILLE_VOISINAGE_MIN, TAILLE_VOISINAGE_MAX = TAILLE_VOISINAGE_MAX)
    s_opt = s_point
    cout_opt = cout_point

    s = s_point
    cout = cout_point


    nb_it = 0
    debut = timer()
    while((nb_it<NB_IT_ITS)):
        print("nbit", nb_it)
        nb_it += 1
        s = s_opt
        cout = cout_opt
        s_tilt, cout_tilt = RGR(s, distances, mu)
        #print("RGR",cout_tilt, calculer_cout(s_tilt, distances))
        print("cout avant 2 opt ", cout_tilt)
        cout_tilt, s_tilt, t = two_opt2(s_tilt, distances)
        print("cout apres 2 opt ", cout_tilt)
        #print("++++++++++++++++++++",cout_tilt, calculer_cout(s_tilt, distances))
        if(cout_tilt <cout_opt):
            print("ouiii tilt", cout_opt)
            cout_opt = cout_tilt
            s_opt = s_tilt


        s_point, cout_point, amelioration, temps = tabou_simple(distances, ville_initiale, s_tilt, cout_tilt, MAX_ITERATION=MAX_ITERATION,PAS_AUGMENTATION = PAS_AUGMENTATION, PAS_DIMINUTION = PAS_DIMINUTION, TAILLE_LISTE_TABOU_MAX = TAILLE_LISTE_TABOU_MAX, taille_voisinage = taille_voisinage, TAILLE_VOISINAGE_MIN = TAILLE_VOISINAGE_MIN, TAILLE_VOISINAGE_MAX = TAILLE_VOISINAGE_MAX)

        #print("--------------------", calculer_cout(s_point, distances), cout_point)
        if(cout_point<cout_opt):
            print("ouiii", cout_point)
            cout_opt = cout_point
            s_opt = s_point
            print("cout avant 2 opt ", cout_opt)
            cout_opt, s_opt, t = two_opt2(s_opt, distances)

            print("cout apres 2 opt ", cout_opt)


    fin = timer()
    #print("ccccccccccccccccccccccccccccccc avanttt ", cout_opt, calculer_cout(s_opt, distances))
    #cout_opt,  s_opt, t = two_opt2(s_opt, distances)
    print("cout opt apres ", cout_opt, calculer_cout(s_opt, distances))

    f = open("savetabouITS.txt", "a+")
    # écriture

    f.write("            sol initiale = PPV1")
    f.write(" | instance = ")
    f.write(file_name)
    f.write(" | cout_opt=")
    f.write(str(cout_opt))
    f.write(" | temps=")
    f.write(str(fin - debut))

    f.write(
        "******************************************************************************************************************\n\n\n")
    f.write("\n")

    # fermeture
    f.close()


    return s_opt, cout_opt, (fin-debut)


def recherche_tabou1(distances, ville_initiale):
    div = 0
    nb_villes = distances.shape[0]
    PAS_AUGMENTATION = 0.75
    PAS_DIMINUTION = 1.0
    MAX_ITERATION =10000
    TAILLE_LISTE_TABOU_MAX = 80
    taille_voisinage = 15.0
    TAILLE_VOISINAGE_MIN = 15
    TAILLE_VOISINAGE_MAX = 30
    NB_ESSAIS = 1000


    nb_iteration = 0
    print(nb_villes)
    continu = True
    liste_tabou = []
    solution_courante, cout = ppv1(ville_initiale, distances)
    print("solution plus proche voisin",cout, solution_courante, cout)
    #cout, solution_courante, temps = moindre_cout(distances)
    #print("solution moindre cout ",temps, cout, solution_courante, cout)

    cout, solution_courante, temps = two_opt2(solution_courante, distances)
    print("solution 2OPT ",temps, cout, solution_courante, cout)

    solution_max = solution_courante  # la meilleure sol

    cout_min = cout
    taille_list_tabou = 0
    cout_initial = cout

    start = timer()

    while (continu):
        if (nb_iteration % 100 == 0):
            print(nb_iteration, taille_voisinage, cout)
            # print("taille v ", taille_voisinage)

        solution_courante, new_cout, permut_min = generer_voisinage1(solution_courante, cout, int(taille_voisinage),
                                                                     distances,
                                                                     liste_tabou, NB_ESSAIS)


        # print("", couts[i_min], solution_courante)
        if (taille_list_tabou < TAILLE_LISTE_TABOU_MAX):
            liste_tabou.append((permut_min[1], permut_min[0]))
            taille_list_tabou = taille_list_tabou + 1
            # print("on ajoute ",(permut_min[1], permut_min[0]))
        else:
            # print((permut_min[1], permut_min[0])," liste tabou",liste_tabou)
            liste_tabou.append((permut_min[1], permut_min[0]))
            liste_tabou.pop(0)
            # print((permut_min[1], permut_min[0])," liste tabou", liste_tabou)

        # maj de la taille du voisinnage
        if (new_cout < cout):
            taille_voisinage = taille_voisinage + PAS_AUGMENTATION

            if (taille_voisinage > TAILLE_VOISINAGE_MAX):
                taille_voisinage = TAILLE_VOISINAGE_MAX

        else:
            taille_voisinage = taille_voisinage - PAS_DIMINUTION

            if (taille_voisinage < TAILLE_VOISINAGE_MIN):
                taille_voisinage = TAILLE_VOISINAGE_MIN

        # print(taille_voisinage)
        cout = new_cout

        if (cout < cout_min):
            solution_max = solution_courante

            cout_min1, solution_max, t = two_opt2(solution_max, distances)
            #print("HEEEEY",  cout_min, cout, cout_min1)
            cout_min = cout_min1

        else:
            div = div + 1
        # print(cout, solution_courante)
        if(div>1000):
            div = 0
            cout1 = cout
            solution_courante, cout = diversification(solution_max, distances)
            cout2 = cout
            cout, solution_courante, t = two_opt2(solution_courante, distances)
            print("apres diiiv", cout1, cout2, cout)





        nb_iteration = nb_iteration + 1
        if (nb_iteration > MAX_ITERATION):
            continu = False
    end = timer()
    amelioration = (cout_initial * 100) / cout_min

    # -*- coding: utf -*-
    # ouverture en écriture
    f = open("savetabou.txt", "a+")
    # écriture

    f.write("sol initiale = PPV")
    f.write(" | instance = ")
    f.write(file_name)
    f.write(" | amelioration ")
    f.write(str(amelioration))
    f.write(" | cout=")
    f.write(str(cout_min))
    f.write(" | temps=")
    f.write(str(end - start))
    f.write(" | PAS_AUGMENTATION=")
    f.write(str(PAS_AUGMENTATION))
    f.write(" | PAS_DIMINUTION=")
    f.write(str(PAS_DIMINUTION))
    f.write(" | MAX_ITERATION=")
    f.write(str(MAX_ITERATION))
    f.write(" | TAILLE_LISTE_TABOU_MAX=")
    f.write(str(TAILLE_LISTE_TABOU_MAX))
    f.write(" | taille_voisinage=")
    f.write(str(taille_voisinage))
    f.write(" | TAILLE_VOISINAGE_MIN=")
    f.write(str(TAILLE_VOISINAGE_MIN))
    f.write(" | TAILLE_VOISINAGE_MAX=")
    f.write(str(TAILLE_VOISINAGE_MAX))
    f.write(" |NB_ESSAIS=")
    f.write(str(NB_ESSAIS))
    f.write("\n")
    f.write("******************************************************************************************************************")
    f.write("\n")

    # fermeture
    f.close()

    return solution_max, cout_min, amelioration, (end-start)



"""points, N = load_points(file_name)
distances = load_distances(points, N)
np.savetxt("distances.txt", distances)
# print(distances)"""


"""distances2 = None
distances = np.loadtxt("distances.txt")

start = timer()
solution_max, cout_min, amelioration = recherche_tabou(distances, 0)
end = timer()
print(end - start)

print("temps d'ecution", (end - start), "seconds")

print("solution opt ")
print(cout_min,calculer_cout(solution_max, distances), solution_max)
print("amelioration = ", amelioration, "%\n\n\n")
"""

"""for i in range(0):
    a, b, c = ITS(distances, 0, 150)
    print("temps d'exécution ", c, "cout ", b)

for i in range(4):
    solution_max, cout_min, amelioration, temps = recherche_tabou_2opt(distances, 0)
    print("temps dexecution recherche_tabou_2opt ", temps, "cout opt",cout_min)

"""
"""sol_courante, cout = ppv1(0, distances)
print(sol_courante, cout, calculer_cout(sol_courante, distances))
RGR(sol_courante, distances, 8)"""



"""print("TABOU 1")




for a in range(4):
    solution_max, cout_min, amelioration, temps = recherche_tabou_2opt(distances, 0)
    print("temps d'execution", temps, "secondes")
    print("solution opt ")
    print(cout_min,calculer_cout(solution_max, distances), solution_max)
    print("amelioration = ", amelioration, "%")
"""

"""
sol_courante, cout = ppv(0, distances)
print(sol_courante, cout, calculer_cout(sol_courante, distances))
#solution_courante, new_cout, permut_min = generer_voisinage_opt(solution_courante, cout, int(1),distances,[], 1)
node1 = 0
node2 = 0

while node1 == node2:
    node1 = randint(1, distances.shape[0] - 2)
    node2 = randint(1, distances.shape[0] - 2)


if node1 > node2:
    swap = node1
    node1 = node2
    node2 = swap


nb_villes = distances.shape[0]-1

new_cout1 = cout + distances[sol_courante[(node1 - 1) % (nb_villes+1)]][sol_courante[node2]] + \
                            distances[sol_courante[(node2 + 1) % (nb_villes+1)]][sol_courante[node1]] - \
                            distances[sol_courante[(node1 - 1) % (nb_villes+1)]][sol_courante[node1]] - \
                            distances[sol_courante[(node2 + 1) % (nb_villes+1)]][sol_courante[node2]]

tmp = sol_courante[node1:(node2+1)%(distances.shape[0]-1)]



print("+ ", sol_courante[(node1 - 1) % nb_villes], ", ",sol_courante[node2])
print("+ ",sol_courante[(node2 + 1) % nb_villes],", ",sol_courante[node1])
print("- ", sol_courante[(node1 - 1) % nb_villes],", ",sol_courante[node1])
print("- ", sol_courante[(node2 + 1) % nb_villes],", ",sol_courante[node2])

#sol_courante = sol_courante[:node1] + tmp[::-1] + sol_courante[(node2+1)%(nb_villes):]
sol_courante[node1 : node2 +1] = sol_courante[node2:node1 - 1:-1]
print("opt", sol_courante, new_cout1, calculer_cout(sol_courante, distances))
"""



"""
print(calculer_cout([0, 7, 1, 13, 11, 2, 3, 4, 5, 6, 12, 8, 9, 10, 0],distances))
liste = [(1,2),(3,4)]
for i in range(10):
    liste.append((i,i+1))
print(liste.count((1,2)))

# print("calculer ", calculer_cout([0, 4, 3, 2, 1, 0],distances))





test, cout = ppv1(0,distances)
print(cout, test)
print("\n\n")
liste = []
voisinage, couts, i_min, permut_min = generer_voisinage(test, cout, 0, distances,liste)



#print("le min ",i_min, couts[i_min], voisinage[i_min])
min_c = couts[i_min]
min_s = voisinage[i_min]
cout = min_c
test = min_s
taille_list_tabou = 0
for i in range(100000):
    voisinage, couts, i_min, permut_min = generer_voisinage(test, cout, 40, distances, liste)
    test = voisinage[i_min]
    cout = couts[i_min]
    # print("", couts[i_min], solution_courante)
    if (taille_list_tabou < 5):
        liste.append((permut_min[1], permut_min[0]))
        taille_list_tabou = taille_list_tabou + 1
        # print("on ajoute ",(permut_min[1], permut_min[0]))
    else:
        # print((permut_min[1], permut_min[0])," liste tabou",liste_tabou)
        liste.append((permut_min[1], permut_min[0]))
        liste.pop(0)
        # print((permut_min[1], permut_min[0])," liste tabou", liste_tabou)
    if (cout<min_c):
        min_c = cout
        min_s = test

print(min_c,liste)"""


