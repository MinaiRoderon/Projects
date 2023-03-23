# -*- coding: utf-8 -*-
"""
Created on "Now it's show time"

@author: Amadéo
"""

from colorama import Back
import time

TIME = [0,0]

Lignes = "ABCDEFGHIJKLMNO"
Colonnes = [str(i) for i in range(1,16)]

CASES = {L+C:'   ' for L in Lignes for C in Colonnes}

CASES_PROCHES = {L+C:'   ' for L in Lignes for C in Colonnes}
for case in CASES_PROCHES :
    CASES_PROCHES[case] = set([case])
    i = Lignes.index(case[0])
    j = Colonnes.index(case[1:])
    if j-1 >= 0 :
        CASES_PROCHES[case].add(Lignes[i]+Colonnes[j-1])
        if i-1 >= 0 :
            CASES_PROCHES[case].add(Lignes[i-1]+Colonnes[j-1])
        if i+1 <= 14 :
            CASES_PROCHES[case].add(Lignes[i+1]+Colonnes[j-1])
    if j+1 <= 14 :
        CASES_PROCHES[case].add(Lignes[i]+Colonnes[j+1])
        if i-1 >= 0 :
            CASES_PROCHES[case].add(Lignes[i-1]+Colonnes[j+1])
        if i+1 <= 14 :
            CASES_PROCHES[case].add(Lignes[i+1]+Colonnes[j+1])
    if i-1 >= 0 :
        CASES_PROCHES[case].add(Lignes[i-1]+Colonnes[j])
    if i+1 <= 14 :
        CASES_PROCHES[case].add(Lignes[i+1]+Colonnes[j])

def affichage2(grille = CASES) : #petit
    print('\n   ', end = '')
    for C in Colonnes :
        if int(C) < 11 :
            print('  '+C+' ', end = '')
        else :
            print(' '+C+' ', end = '')
    print('\n   '+'-'*61)
    for L in Lignes :
        print(' '+L+' '+'|', end = '')
        for C in Colonnes :
            print(grille[L+C], end = '')
            print(Back.RESET + '|', end = '')
        print('\n   '+'-'*61)

def affichage(grille = CASES) : #grand
    print('\n   ', end = '')
    for C in Colonnes :
        if int(C) < 10 :
            print('   '+C+'   ', end = '')
        else :
            print('   '+C+'  ', end = '')
    print('\n   '+'-'*106)
    for L in Lignes :
        for k in range(2) :
            print(' '+L+' '+'|', end = '')
            for C in Colonnes :
                print(grille[L+C], end = '')
                print(grille[L+C], end = '')
                print(Back.RESET + '|', end = '')
            if k == 1 :
                print('\n   '+'-'*106)
            else :
                print()

#BARRES= Toutes les suites possibles de 5 pions rangées dans BARRES.keys() et values()=None
BARRES = dict() #Utile
X = 0
BARRES_DESC = dict()
for L in Lignes :
    for i in range(len(Colonnes)-4) :
        b = L+Colonnes[i]
        for j in range(1,5) :
            b += '-'+L+Colonnes[i+j]
        BARRES[b] = X
        X += 1
        BARRES_DESC[b] = (L,i)
for C in Colonnes :
    for i in range(len(Lignes)-4) :
        b = Lignes[i]+C
        for j in range(1,5) :
            b += '-'+Lignes[i+j]+C
        BARRES[b] = X
        X += 1
        BARRES_DESC[b] = (C,i)
for i in range(len(Lignes)-4) :
    for j in range(len(Colonnes)-4) :
        b = Lignes[i]+Colonnes[j]
        for k in range(1,5) :
            b += '-'+Lignes[i+k]+Colonnes[j+k]
        BARRES[b] = X
        X += 1
        BARRES_DESC[b] = (str(j-i)+'D',j)
for i in range(4,len(Lignes)) :
    for j in range(len(Colonnes)-4) :
        b = Lignes[i]+Colonnes[j]
        for k in range(1,5) :
            b += '-'+Lignes[i-k]+Colonnes[j+k]
        BARRES[b] = X
        X += 1
        BARRES_DESC[b] = (str(-i-j)+'A',j)
INT_TO_BARRES = {v:k for k,v in BARRES.items()}
BARRES_DESC = {BARRES[k]:v for k,v in BARRES_DESC.items()}

#BARRES_PAR_CASE = contient en values() toutes les barres possibles contenant la case en keys()
BARRES_PAR_CASE = dict() #Utile
for case in CASES :
    BARRES_PAR_CASE[case] = []
    for barre in BARRES :
        if case in barre.split('-') :
            BARRES_PAR_CASE[case].append(BARRES[barre])

#Utile
CASES_JOUABLES_PAR_BARRES = dict() #Donne les cases jouables selon chaque barre
for barre in BARRES :
    CASES_JOUABLES_PAR_BARRES[BARRES[barre]] = set(barre.split('-'))

CASES_DEJA_JOUEES = set() #Utile

#Utile ; Nos barres sont en indice 0
FITNESS_BARRE = [[set() for k in range(5)],[set() for k in range(5)],set(INT_TO_BARRES.copy())]
CASES_COUP_3 = set() #Utile pour pour le coup 3 en tant que noir (zone interdite prise en compte)
CASES_COUP_3.update({'D4','D5','D6','D7', 'D8', 'D9', 'D10', 'D11', 'D12'})
CASES_COUP_3.update({'E4', 'F4', 'G4', 'H4', 'I4', 'J4', 'K4', 'L4'})
CASES_COUP_3.update({'E12', 'F12', 'G12', 'H12', 'I12', 'J12', 'K12', 'L12'})
CASES_COUP_3.update({'L5','L6','L7', 'L8', 'L9', 'L10', 'L11'})

#Poids testés :
#[100,20,6,3,1]
#[200,25,8,4,1]
#[200,12,12,6,1]
#[200,16,16,8,1]
def fitness(fit_barre) : #1.5 micros sec
    res = 0
    poids = [200,16,16,8,1]
    for k in range(5) :
        res += (len(fit_barre[0][k])-len(fit_barre[1][k]))*poids[k]
    return res

def terminal_test(situation) : #250 ns
    return (len(situation[0][0][0]) >= 1) or (len(situation[0][1][0]) >= 1) or (len(situation[1]) >= 120)

def resultat(situation, case_jouee, joueur) : #En dessous de 30 micros sec
    adversaire = (joueur+1)%2
    fit_barre_res = [[situation[0][0][i].copy() for i in range(5)], [situation[0][1][i].copy() for i in range(5)], situation[0][2].copy()]
    cases_deja_jouee_res = situation[1].copy()
    for barre in BARRES_PAR_CASE[case_jouee] :
        if barre in fit_barre_res[2] :
            fit_barre_res[joueur][4].add(barre)
            fit_barre_res[2].discard(barre)
            continue
        for k in range(1,5) :
            fit_barre_res[adversaire][k].discard(barre)
            if barre in fit_barre_res[joueur][k] :
                fit_barre_res[joueur][k].discard(barre)
                fit_barre_res[joueur][k-1].add(barre)
                break
    cases_deja_jouee_res.add(case_jouee)
    return fit_barre_res, cases_deja_jouee_res


#2500000 pour 5 sec (python)
#20000000 pour battre difficulté hard internet (20 sec)
FEUILLES_MAX = 3000000

def ALPHA_BETA_SEARCH(situation) :
    #temp = actions00(situation)
    #if len(temp) == 1 :
        #return '/', temp.pop()
    return MAX_VALUE(situation, -8000, 8000, 1)

def MAX_VALUE(situation, alpha, beta, n) :
    if terminal_test(situation) :
        if len(situation[1]) >= 120 :
            return 0
        if len(situation[0][0][0]) >= 1 :
            return 10000, ""
        else :
            return -10000, ""
    v = -1000000
    actionM = ""
    Actions = actions00(situation)
    n1 = len(Actions)
    n = n*n1
    if n > FEUILLES_MAX :
        if n1 > 6 and n > 2*FEUILLES_MAX :
            return fitness(situation[0]), ""
        for action in Actions :
            aux = fitness(resultat(situation, action, 0)[0])
            if aux > v :
                v = aux
                actionM = action
            if v >= beta :
                return v, actionM
        return v, actionM
    for action in Actions :
        aux = MIN_VALUE(resultat(situation, action, 0), alpha, beta, n)
        if aux > v :
            v = aux
            actionM = action
        if v >= beta :
            return v, actionM
        alpha = max(alpha, v)
    return v, actionM

def MIN_VALUE(situation, alpha, beta, n) :
    if terminal_test(situation) :
        if len(situation[1]) >= 120 :
            return 0
        if len(situation[0][0][0]) >= 1 :
            return 10000
        else :
            return -10000
    v = 1000000
    Actions = actions11(situation)
    n1 = len(Actions)
    n = n*n1
    if n > FEUILLES_MAX :
        if n1 > 6 and n > 2*FEUILLES_MAX :
            return fitness(situation[0])
        for action in Actions :
            aux = fitness(resultat(situation, action, 1)[0])
            v = min(v, aux)
            if v <= alpha :
                return v
        return v
    for action in Actions :
        v = min(v, MAX_VALUE(resultat(situation, action, 1), alpha, beta, n)[0])
        if v <= alpha :
            return v
        beta = min(beta, v)
    return v

def actions00(situation) :
    fit_barre, cases_deja_jouee = situation
    res = set()
    
    if (len(cases_deja_jouee) == 2) : #Coups 3
        for barre in fit_barre[0][4] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
        for barre in fit_barre[1][4] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
        res.difference_update(cases_deja_jouee)
        res.intersection_update(CASES_COUP_3)
        return res

    # 4 into 5
    if len(fit_barre[0][1]) != 0 :
        for barre in fit_barre[0][1] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
            break
        res.difference_update(cases_deja_jouee)
        return res
    if len(fit_barre[1][1]) != 0 :
        for barre in fit_barre[1][1] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
            break
        res.difference_update(cases_deja_jouee)
        return res

    
    # 3s into 4 double
    A = set()
    for barre1 in fit_barre[0][2] :
        A.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for barre2 in fit_barre[0][2] :
            temp = (CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])).difference(cases_deja_jouee)
            if len(temp) == 1 :
                return temp
    
    # 3&2 into 4&3double sep
    C, E = set(), set()
    AL = list(fit_barre[0][3])
    n = len(AL)
    for i in range(n) :
        barre1 = AL[i]
        C.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for j in range(i+1,n) :
            barre2 = AL[j]
            if BARRES_DESC[barre1][0] == BARRES_DESC[barre2][0] :
                if abs(BARRES_DESC[barre1][1] - BARRES_DESC[barre2][1]) == 1 :
                    temp = (CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])).difference(cases_deja_jouee)
                    E.update(temp)
                    for barre3 in fit_barre[0][2] :
                        if BARRES_DESC[barre1][0] != BARRES_DESC[barre3][0] :
                            temp2 = temp.intersection(CASES_JOUABLES_PAR_BARRES[barre3])
                            if len(temp2) == 1 :
                                return temp2
    
    # 3s into 4 double    
    B = set()
    T = set()
    for barre1 in fit_barre[1][2] :
        B.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for barre2 in fit_barre[1][2] :
            if len((CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])).difference(cases_deja_jouee)) == 1 :
                T.update(CASES_JOUABLES_PAR_BARRES[barre1].union(CASES_JOUABLES_PAR_BARRES[barre2]))
                
    # 3&2 into 4&3 sep
    D = set()
    AL2 = list(fit_barre[1][3])
    n2 = len(AL2)
    for i in range(n2) :
        barre1 = AL2[i]
        D.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for j in range(i+1,n2) :
            barre2 = AL2[j]
            if BARRES_DESC[barre1][0] == BARRES_DESC[barre2][0] :
                if abs(BARRES_DESC[barre1][1] - BARRES_DESC[barre2][1]) == 1 :
                    temp = CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])
                    E.update(temp)
                    for barre3 in fit_barre[1][2] :
                        if BARRES_DESC[barre1][0] != BARRES_DESC[barre3][0] :
                            temp2 = (temp.intersection(CASES_JOUABLES_PAR_BARRES[barre3])).difference(cases_deja_jouee)
                            if len(temp2) == 1 :
                                T.update(CASES_PROCHES[temp2.pop()].intersection(CASES_JOUABLES_PAR_BARRES[barre3].union(CASES_JOUABLES_PAR_BARRES[barre1]).union(CASES_JOUABLES_PAR_BARRES[barre2])))
    
    if T != set() :
        return (T.union(A)).difference(cases_deja_jouee)
    
    A.difference_update(cases_deja_jouee)
    B.difference_update(cases_deja_jouee)
    E.difference_update(cases_deja_jouee)

    res = (E.union(A).union(B).union(C.intersection(D))).difference(cases_deja_jouee)
    
    F, G = set(), set()
    if len(res) < 10 :
        for barre in fit_barre[0][4] :
            F.update(CASES_JOUABLES_PAR_BARRES[barre])
        F.difference_update(cases_deja_jouee)
        for barre in fit_barre[1][4] :
            G.update(CASES_JOUABLES_PAR_BARRES[barre])
        G.difference_update(cases_deja_jouee)
        res.update((C.union(D)).intersection(F.union(G)))
        
        if len(res) < 5 :
            res.update(F.intersection(G))
        
        H = cases_deja_jouee.copy()
        while len(res) < 10 and H != set() :
            res.update(CASES_PROCHES[H.pop()].difference(cases_deja_jouee))

    return res


def actions11(situation) :
    fit_barre, cases_deja_jouee = situation
    res = set()
    
    if (len(cases_deja_jouee) == 2) : #Coups 3
        for barre in fit_barre[0][4] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
        for barre in fit_barre[1][4] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
        res.difference_update(cases_deja_jouee)
        res.intersection_update(CASES_COUP_3)
        return res

    # 4 into 5
    if len(fit_barre[1][1]) != 0 :
        for barre in fit_barre[1][1] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
            break
        res.difference_update(cases_deja_jouee)
        return res
    if len(fit_barre[0][1]) != 0 :
        for barre in fit_barre[0][1] :
            res.update(CASES_JOUABLES_PAR_BARRES[barre])
            break
        res.difference_update(cases_deja_jouee)
        return res

    
    # 3s into 4 double
    A = set()
    for barre1 in fit_barre[1][2] :
        A.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for barre2 in fit_barre[1][2] :
            temp = (CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])).difference(cases_deja_jouee)
            if len(temp) == 1 :
                return temp
    
    # 3&2 into 4&3 sep
    C, E = set(), set()
    AL = list(fit_barre[1][3])
    n = len(AL)
    for i in range(n) :
        barre1 = AL[i]
        C.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for j in range(i+1,n) :
            barre2 = AL[j]
            if BARRES_DESC[barre1][0] == BARRES_DESC[barre2][0] :
                if abs(BARRES_DESC[barre1][1] - BARRES_DESC[barre2][1]) == 1 :
                    temp = (CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])).difference(cases_deja_jouee)
                    E.update(temp)
                    for barre3 in fit_barre[1][2] :
                        if BARRES_DESC[barre1][0] != BARRES_DESC[barre3][0] :
                            temp2 = temp.intersection(CASES_JOUABLES_PAR_BARRES[barre3])
                            if len(temp2) == 1 :
                                return temp2
    
    # 3s into 4 double    
    B = set()
    T = set()
    for barre1 in fit_barre[0][2] :
        B.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for barre2 in fit_barre[0][2] :
            if len((CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])).difference(cases_deja_jouee)) == 1 :
                T.update(CASES_JOUABLES_PAR_BARRES[barre1].union(CASES_JOUABLES_PAR_BARRES[barre2]))

    # 3&2 into 4&3 sep
    D = set()
    AL2 = list(fit_barre[0][3])
    n2 = len(AL2)
    for i in range(n2) :
        barre1 = AL2[i]
        D.update(CASES_JOUABLES_PAR_BARRES[barre1])
        for j in range(i+1,n2) :
            barre2 = AL2[j]
            if BARRES_DESC[barre1][0] == BARRES_DESC[barre2][0] :
                if abs(BARRES_DESC[barre1][1] - BARRES_DESC[barre2][1]) == 1 :
                    temp = CASES_JOUABLES_PAR_BARRES[barre1].intersection(CASES_JOUABLES_PAR_BARRES[barre2])
                    E.update(temp)
                    for barre3 in fit_barre[0][2] :
                        if BARRES_DESC[barre1][0] != BARRES_DESC[barre3][0] :
                            temp2 = (temp.intersection(CASES_JOUABLES_PAR_BARRES[barre3])).difference(cases_deja_jouee)
                            if len(temp2) == 1 :
                                T.update(CASES_PROCHES[temp2.pop()].intersection(CASES_JOUABLES_PAR_BARRES[barre3].union(CASES_JOUABLES_PAR_BARRES[barre1]).union(CASES_JOUABLES_PAR_BARRES[barre2])))
    
    if T != set() :
        return (T.union(A)).difference(cases_deja_jouee)
    
    A.difference_update(cases_deja_jouee)
    B.difference_update(cases_deja_jouee)
    E.difference_update(cases_deja_jouee)

    res = (E.union(A).union(B).union(C.intersection(D))).difference(cases_deja_jouee)
    
    F, G = set(), set()
    if len(res) < 10 :
        for barre in fit_barre[0][4] :
            F.update(CASES_JOUABLES_PAR_BARRES[barre])
        F.difference_update(cases_deja_jouee)
        for barre in fit_barre[1][4] :
            G.update(CASES_JOUABLES_PAR_BARRES[barre])
        G.difference_update(cases_deja_jouee)
        res.update((C.union(D)).intersection(F.union(G)))
        
        if len(res) < 5 :
            res.update(F.intersection(G))
    
        H = cases_deja_jouee.copy()
        while len(res) < 10 and H != set() :
            res.update(CASES_PROCHES[H.pop()].difference(cases_deja_jouee))

    return res

# run jeu() to play, replace affichage2 function by affichage function in order to display a larger game board
def jeu() :
    C = set(CASES)
    CASES2 = CASES.copy()
    nb_coups = 0
    premier = int(input("\nQuel joueur commence en H8 (0: IA, 1: other_player): "))
    situation = FITNESS_BARRE, CASES_DEJA_JOUEES
    situation = resultat(situation, 'H8', premier)
    nb_coups = 1
    CASES2['H8'] = Back.RED + '   '
    joueur = (premier+1)%2
    while not terminal_test(situation) :
        case = ''
        affichage2(CASES2)
        if joueur == 1 :
            while not case in C.difference(situation[1]) :
                case = input("\nCase jouée par l'adversaire : ")
            situation = resultat(situation, case, joueur)
        if joueur == 0 :
            TIME[0] = time.time()
            fit, case = ALPHA_BETA_SEARCH(situation)
            situation = resultat(situation, case, joueur)
            TIME[1] = time.time()
            print()
            print(f"Case jouée : {case}, fitness prévue = {fit}, actuelle = {fitness(situation[0])}, response time = {round(TIME[1]-TIME[0],2)} sec.")
        nb_coups += 1
        if nb_coups%2 == 1 :
            CASES2[case] = Back.RED + '   '
        else :
            CASES2[case] = Back.WHITE + '   '
        joueur = (joueur+1)%2
    print(f"Plateau final : ({len(situation[1])} cases jouées)")
    affichage2(CASES2)
    if len(situation[1]) == 120 :
        print("\nMatch nul, chaque joueur a joué ses 60 jetons")
    elif len(situation[0][0][0]) > 0 :
        print("\nIA GAGNE : 'Now it's show time', Amadéo")
    else :
        print("\nL'Adversaire a gagné")

def jeu_without_fitness_displayed() : #without printing the game evaluation bar
    C = set(CASES)
    CASES2 = CASES.copy()
    nb_coups = 0
    premier = int(input("\nQuel joueur commence en H8 (0: IA, 1: other_player): "))
    situation = FITNESS_BARRE, CASES_DEJA_JOUEES
    situation = resultat(situation, 'H8', premier)
    nb_coups = 1
    CASES2['H8'] = Back.RED + '   '
    joueur = (premier+1)%2
    while not terminal_test(situation) :
        case = ''
        affichage2(CASES2)
        if joueur == 1 :
            while not case in C.difference(situation[1]) :
                case = input("Case jouée par l'adversaire : ")
            situation = resultat(situation, case, joueur)
        if joueur == 0 :
            TIME[0] = time.time()
            fit, case = ALPHA_BETA_SEARCH(situation)
            situation = resultat(situation, case, joueur)
            TIME[1] = time.time()
            print()
            print(f"Case jouée : {case}, response time = {round(TIME[1]-TIME[0],1)} sec.")
        nb_coups += 1
        if nb_coups%2 == 1 :
            CASES2[case] = Back.RED + '   '
        else :
            CASES2[case] = Back.WHITE + '   '
        joueur = (joueur+1)%2
    print(f"Plateau final : ({len(situation[1])} cases jouées)")
    affichage2(CASES2)
    if len(situation[1]) == 120 :
        print("Match nul, chaque joueur a joué ses 60 jetons")
    elif len(situation[0][0][0]) > 0 :
        print("\nIA GAGNE : 'Now it's show time', Amadéo")
    else :
        print("\nL'Adversaire a gagné la partie")

def jeu_without_response_time() : #without printing response time
    C = set(CASES)
    CASES2 = CASES.copy()
    nb_coups = 0
    premier = int(input("\nQuel joueur commence en H8 (0: IA, 1: other_player): "))
    situation = FITNESS_BARRE, CASES_DEJA_JOUEES
    situation = resultat(situation, 'H8', premier)
    nb_coups = 1
    CASES2['H8'] = Back.RED + '   '
    joueur = (premier+1)%2
    while not terminal_test(situation) :
        case = ''
        affichage2(CASES2)
        if joueur == 1 :
            while not case in C.difference(situation[1]) :
                case = input("Case jouée par l'adversaire : ")
            situation = resultat(situation, case, joueur)
        if joueur == 0 :
            TIME[0] = time.time()
            fit, case = ALPHA_BETA_SEARCH(situation)
            situation = resultat(situation, case, joueur)
            TIME[1] = time.time()
            print()
            print(f"Case jouée : {case}, fitness prévue = {fit}, actuelle = {fitness(situation[0])}")
        nb_coups += 1
        if nb_coups%2 == 1 :
            CASES2[case] = Back.RED + '   '
        else :
            CASES2[case] = Back.WHITE + '   '
        joueur = (joueur+1)%2
    print(f"Plateau final : ({len(situation[1])} cases jouées)")
    affichage2(CASES2)
    if len(situation[1]) == 120 :
        print("\nMatch nul, chaque joueur a joué ses 60 jetons")
    elif len(situation[0][0][0]) > 0 :
        print("\nIA GAGNE : 'Now it's show time', Amadéo")
    else :
        print("\nL'Adversaire a gagné")





