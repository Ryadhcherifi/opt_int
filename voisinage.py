from random import randint
from twoopt import cost, cost_change
def calculer_cout(solution, distances):
    nb_villes = len(solution)
    # print("nb_villes = ", nb_villes)
    cout = 0

    for i in range(nb_villes - 1):
        #print(solution[i],solution[i+1],distances[solution[i]][solution[i+1]])
        cout = cout + distances[solution[i]][solution[i + 1]]

    # print("\n\n")
    return cout




def generer_voisinage1(sol_courante, cout, taille_voisinage, distances, liste_tabou, NB_ESSAIS):
    couts = []
    voisinage = []
    nb_villes = distances.shape[0]
    i_min = 0  # indice de la meilleure solution
    i = 0

    while (i < taille_voisinage):
        noeud_1 = 0
        noeud_2 = 0
        nope = True
        nb_essais = 0
        while (nope):
            while((noeud_1 == noeud_2) or (noeud_1 == noeud_2 + 1) or (noeud_2 == noeud_1 + 1)):
                noeud_1 = randint(1, len(sol_courante) - 2)
                noeud_2 = randint(1, len(sol_courante) - 2)

            if noeud_1 > noeud_2:
                a = noeud_1
                noeud_1 = noeud_2
                noeud_2 = a

            new_cout1 = cout - distances[sol_courante[(noeud_1 - 1) % nb_villes]][sol_courante[noeud_1]] - \
                        distances[sol_courante[(noeud_1 + 1) % nb_villes]][sol_courante[noeud_1]] - \
                        distances[sol_courante[(noeud_2 - 1) % nb_villes]][sol_courante[noeud_2]] - \
                        distances[sol_courante[(noeud_2 + 1) % nb_villes]][sol_courante[noeud_2]]
            new_cout1 = new_cout1 + distances[sol_courante[(noeud_1 - 1) % nb_villes]][sol_courante[noeud_2]] + \
                        distances[sol_courante[(noeud_1 + 1) % nb_villes]][sol_courante[noeud_2]] + \
                        distances[sol_courante[(noeud_2 - 1) % nb_villes]][sol_courante[noeud_1]] + \
                        distances[sol_courante[(noeud_2 + 1) % nb_villes]][sol_courante[noeud_1]]
            nb_essais = nb_essais + 1
            if((new_cout1<cout) or (nb_essais>=NB_ESSAIS)):
                #if(new_cout1 < cout): print("YAAAAAAAAAAAAY")
                nope = False




        new_sol = sol_courante.copy()
        new_sol[noeud_2] = sol_courante[noeud_1]
        new_sol[noeud_1] = sol_courante[noeud_2]
        new_cout = new_cout1
        permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
        if ((new_cout < cout) or (liste_tabou.count((noeud_1, noeud_2)) == 0)):

            if (i == 0):
                cout_min = new_cout
                permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
                sol_min = new_sol

            else:
                if (new_cout < cout_min):
                    cout_min = new_cout
                    permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
                    sol_min = new_sol
            i = i + 1

    return sol_min, cout_min, permut_min

def generer_voisinage_opt(sol_courante, cout, taille_voisinage, distances, liste_tabou, NB_ESSAIS):
    couts = []
    voisinage = []
    nb_villes = len(sol_courante) - 1
    i_min = 0  # indice de la meilleure solution
    i = 0

    while (i < taille_voisinage):
        noeud_1 = 0
        noeud_2 = 0
        nope = True
        nb_essais = 0

        while ((nope)):
            while ((noeud_1 == noeud_2) or (noeud_1 == (noeud_2 + 1) % nb_villes) or (noeud_2 == (noeud_1 + 1) % nb_villes)):
                noeud_1 = randint(1, len(sol_courante) - 2)
                noeud_2 = randint(1, len(sol_courante) - 2)

            if noeud_1 > noeud_2:
                a = noeud_1
                noeud_1 = noeud_2
                noeud_2 = a
            #print(noeud_1,noeud_2,"AVAAAAAAAAAAAAAAAAAAAAAAANT",len(sol_courante))
            node1 = noeud_1
            node2 = noeud_2

            new_cout1 = cout + distances[sol_courante[(node1 - 1) % (nb_villes )]][sol_courante[node2]] + \
                        distances[sol_courante[(node2 + 1) % (nb_villes )]][sol_courante[node1]] - \
                        distances[sol_courante[(node1 - 1) % (nb_villes )]][sol_courante[node1]] - \
                        distances[sol_courante[(node2 + 1) % (nb_villes )]][sol_courante[node2]]




            nb_essais = nb_essais + 1
            if((new_cout1<cout) or (nb_essais>=NB_ESSAIS)):
                #if(new_cout1 < cout): print("YAAAAAAAAAAAAY")
                nope = False




        new_sol = sol_courante.copy()
        new_sol[node1: node2 + 1] = new_sol[node2:node1 - 1:-1]

        #if(new_cout1!=calculer_cout(new_sol, distances)): print("LES CALCULS SONT PAS BONS KEVIN", new_cout1, calculer_cout(new_sol, distances))
        new_cout = new_cout1
        permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
        if ((new_cout < cout) or (liste_tabou.count((noeud_1, noeud_2)) == 0)):

            if (i == 0):
                cout_min = new_cout
                permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
                sol_min = new_sol

            else:
                if (new_cout < cout_min):
                    cout_min = new_cout
                    permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
                    sol_min = new_sol
            i = i + 1

    return sol_min, cout_min, permut_min


def generer_voisinage(sol_courante, cout, taille_voisinage, distances, liste_tabou):
    couts = []
    voisinage = []
    nb_villes = distances.shape[0]

    i_min = 0  # indice de la meilleure solution
    i = 0
    # print("------------------------solcourante", sol_courante, cout,"liste tabou", liste_tabou)
    # print(noeud_1, noeud_2)
    # calcul du cout de la nouvelle solution
    # print(" - : ",sol_courante[(noeud_1 - 1) % nb_villes], noeud_1,"   ", sol_courante[(noeud_1 + 1) % nb_villes],noeud_1 ,"   ", sol_courante[(noeud_2 - 1) % nb_villes], noeud_2 ,"   ", sol_courante[(noeud_2 + 1) % nb_villes],noeud_2)
    # if(new_cout<0): print("ce nest pas narmoooooooooooooooooooooooooooooool")
    # print(" + : ", sol_courante[(noeud_1 - 1) % nb_villes],noeud_2 ,"   ", sol_courante[(noeud_1 + 1) % nb_villes],noeud_2 , "   ",sol_courante[(noeud_2 - 1) % nb_villes], noeud_1 ,"   ", sol_courante[(noeud_2 + 1) % nb_villes],noeud_1)
    # print("new cout = ",new_cout)
    """
    print("couuuuuuuuuuuuuuuuuuuuuuunt ",(noeud_1, noeud_2),liste_tabou,liste_tabou.count((noeud_1, noeud_2)))
    """

    while (i < taille_voisinage):
        noeud_1 = 0
        noeud_2 = 0
        while ((noeud_1 == noeud_2) or (noeud_1 == noeud_2 + 1) or (noeud_2 == noeud_1 + 1)):
            noeud_1 = randint(1, len(sol_courante) - 2)
            noeud_2 = randint(1, len(sol_courante) - 2)

        if noeud_1 > noeud_2:
            a = noeud_1
            noeud_1 = noeud_2
            noeud_2 = a

        new_cout1 = cout - distances[sol_courante[(noeud_1 - 1) % nb_villes]][sol_courante[noeud_1]] - \
                    distances[sol_courante[(noeud_1 + 1) % nb_villes]][sol_courante[noeud_1]] - \
                    distances[sol_courante[(noeud_2 - 1) % nb_villes]][sol_courante[noeud_2]] - \
                    distances[sol_courante[(noeud_2 + 1) % nb_villes]][sol_courante[noeud_2]]
        new_cout1 = new_cout1 + distances[sol_courante[(noeud_1 - 1) % nb_villes]][sol_courante[noeud_2]] + \
                    distances[sol_courante[(noeud_1 + 1) % nb_villes]][sol_courante[noeud_2]] + \
                    distances[sol_courante[(noeud_2 - 1) % nb_villes]][sol_courante[noeud_1]] + \
                    distances[sol_courante[(noeud_2 + 1) % nb_villes]][sol_courante[noeud_1]]

        # print(noeud_1, noeud_2)
        # calcul du cout de la nouvelle solution
        # print(" - : ",sol_courante[(noeud_1 - 1) % nb_villes],sol_courante[noeud_1] ," ",sol_courante[(noeud_1 + 1) % nb_villes],sol_courante[noeud_1]," ",sol_courante[(noeud_2 - 1) % nb_villes],sol_courante[noeud_2]," " ,sol_courante[(noeud_2 + 1) % nb_villes],sol_courante[noeud_2])
        # if(new_cout<0): print("ce nest pas narmoooooooooooooooooooooooooooooool")
        # print(" + : ", sol_courante[(noeud_1 - 1) % nb_villes],sol_courante[noeud_2]," ", sol_courante[(noeud_1 + 1) % nb_villes], sol_courante[noeud_2]," ", sol_courante[(noeud_2 - 1) % nb_villes], sol_courante[noeud_1]," ", sol_courante[(noeud_2 + 1) % nb_villes],sol_courante[noeud_1])

        new_sol = sol_courante.copy()
        new_sol[noeud_2] = sol_courante[noeud_1]
        new_sol[noeud_1] = sol_courante[noeud_2]
        # new_cout = calculer_cout(new_sol, distances)
        # print(new_cout1, new_cout )
        # print(new_cout, new_cout1)
        new_cout = new_cout1
        # print("new cout = ", new_cout1, new_cout)
        # if(new_cout!=new_cout1): print("I KNEW IIIIIT")
        # critère d'aspiration : on accepte une solution tabou qui améliore la solution courante
        # if ((new_cout < cout) or ((noeud_1, noeud_2) not in liste_tabou)):
        permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]
        if ((new_cout < cout) or (liste_tabou.count((noeud_1, noeud_2)) == 0)):
            if (i == 0):
                cout_min = new_cout
                i_min = 0
                permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]

            else:
                if (new_cout < cout_min):
                    cout_min = new_cout
                    i_min = i
                    permut_min = [sol_courante[noeud_1], sol_courante[noeud_2]]

            # print("(",noeud_1,noeud_2,") ",new_cout," : ", new_sol)
            couts.append(new_cout)
            voisinage.append(new_sol)
            i = i + 1

        """
                else:
            if((noeud_1, noeud_2)  in liste_tabou):
                print("HEEEEEEEEEEEEEEEEEEEEEEEEEYYYYY")
        """

        # voisinage opt2
        """tmp = sol_courante[noeud_1:noeud_2]
        new_sol = sol_courante[:noeud_1] + tmp[::-1] + sol_courante[noeud_2:]
        print("reeeeeeeeees",permut_min, cout_min, voisinage[i_min])
        """

    return voisinage, couts, i_min, permut_min

