# -*- coding: utf-8 -*-
"""
Created on "Now it's show time"

@author: Amadéo
"""

from colorama import Fore, Back

GRILLE = [[9*j+i for i in range(9)] for j in range(9)]
Colonnes = [set([GRILLE[i][j] for i in range(9)]) for j in range(9)]
Lignes = [set([GRILLE[j][i] for i in range(9)]) for j in range(9)]
Carres = [set([GRILLE[j+3*x][i+3*y] for i in range(3) for j in range(3)]) for x in range(3) for y in range(3)]
CASES = {case for c in Colonnes for case in c}
CASES_DESC = {case : (case%9, case//9, 3*((case//9)//3)+(case%9)//3) for case in CASES}
VALEURS_POSSIBLES = set(range(1,10))

def affichage(sudoku, base = None) :
    if 0 in sudoku :
        base = sudoku
    print(Fore.MAGENTA + '\n'+'-'*37)
    for i in range(9) :
        print(Fore.MAGENTA + '|', end = '')
        print(Fore.RESET, end = '')
        for j in range(9) :
            chiffre = sudoku[9*i+j]
            if chiffre != 0 :
                if base and base[9*i+j] == chiffre :
                    print(Back.BLACK + ' ' + str(chiffre) + ' ', end = '')
                    print(Fore.RESET + Back.RESET, end = '')
                else :
                    print(Back.WHITE + Fore.BLACK + ' ' + str(chiffre) + ' ', end = '')
                    print(Fore.RESET + Back.RESET, end = '')
            else :
                print(' '*3, end = '')
            if j%3 == 2 :
                print(Fore.MAGENTA + '|', end = '')
                print(Fore.RESET, end = '')
            else :
                print('|', end = '')
        if i%3 == 2 :
            print(Fore.MAGENTA + '\n'+'-'*37)
            print(Fore.RESET, end = '')
        else :
            print(Fore.MAGENTA + '\n' +'|', end = '')
            print(Fore.RESET, end = '')
            for k in range(3) :
                print('-'*11, end = '')
                print(Fore.MAGENTA + '|', end = '')
                print(Fore.RESET, end = '')
            print()

def remplissage() :
    sudoku = [0 for k in range(81)]
    affichage(sudoku)
    VAL = set(map(str,VALEURS_POSSIBLES.union({0})))
    k = 0
    while k < 81 :
        cases = (input("Case suivante : ")).replace(' ','').split(',')
        test = True
        for case in cases :
            test = test and (case in VAL)
        while not test :
            print("La case doit être comprise entre 0 et 9")
            cases = (input("Ressaisir la/les case(s) suivante(s) : ")).split(',')
            test = True
            for case in cases :
                test = test and (case in VAL)
        sudoku = sudoku[:k]+list(map(int, cases))+sudoku[k+len(cases):]
        affichage(sudoku)
        k += len(cases)
        print(sudoku)
    return sudoku

def contraintes(sudoku, case, chiffre) :
    res = 1
    for case2 in Colonnes[CASES_DESC[case][0]] :
        res *= (chiffre != sudoku[case2])
    for case2 in Lignes[CASES_DESC[case][1]] :
        res *= (chiffre != sudoku[case2])
    for case2 in Carres[CASES_DESC[case][2]] :
        res *= (chiffre != sudoku[case2])
    return (res == 1)

def sudoku(sudoku) :
    print("\nGrille d'origine :")
    affichage(sudoku)
    print()
    res = [sudoku]
    while 0 in res[0] :
        for supp in res[:] :
            Valeurs_supp = dict()
            for k in range(81) :
                if supp[k] == 0 :
                    valeurs = set()
                    for val in VALEURS_POSSIBLES :
                        if contraintes(supp, k, val) :
                            valeurs.add(val)
                    Valeurs_supp[k] = valeurs
            case = min(Valeurs_supp, key = lambda k : len(Valeurs_supp[k]))
            for val in Valeurs_supp[case] :
                if contraintes(supp, case, val) :
                    res.append(supp[:case]+[val]+supp[case+1:])
            delete = res.pop(0)
    if len(res) == 0 :
        print("Ce sudoku n'admet aucune solution")
    else :
        for soluce in res :
            affichage(soluce, sudoku)
        print(f"Nombre de solutions : {len(res)}")



        
