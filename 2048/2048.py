# -*- coding: utf-8 -*-
"""
Created on "Now it's show time"

@author: Amadéo
"""

from colorama import Back
import random

def couleur(val) :
    COULEUR = [Back.WHITE, Back.CYAN, Back.BLUE, Back.GREEN, Back.MAGENTA, Back.YELLOW]
    if val == 0 :
        return ''
    for k in range(1,3*len(COULEUR)) :
        if val == 2**k :
            return COULEUR[(k-1)%len(COULEUR)]
    return COULEUR[-1]

def affichage(grille) :
    hauteur = 9
    largeur = 21
    print('\n   '+'-'*89)
    for i in range(4) :
        for k in range(hauteur) :
            print('   |', end = '')
            for j in range(4) :
                valeur = grille[i][j]
                if k == hauteur//2 :
                    taille = largeur-len(str(valeur))
                    print(couleur(valeur) + ' '*(taille//2) + (str(valeur) if valeur else ' ') + ' '*(taille//2 + taille%2), end = '')
                else :
                    print(couleur(valeur) + ' '*largeur, end = '')
                print(Back.RESET + '|' + '\n'*(j==3), end = '')
        print('   '+'-'*89)


'''
Swap actions : 
    2 : down
    4 : left
    8 : up
    6 : right
'''
def mouvement(grille_ini, action) :
    grille = [[0 for j in range(4)] for i in range(4)]
    if action == 4 :
        grille = [grille_ini[i].copy() for i in range(4)]
    if action == 6 :
        for i in range(4) :
            grille[i] = grille_ini[i][::-1]
    if action == 8 :
        for i in range(4) :
            for j in range(4) :
                grille[i][j] = grille_ini[j][3-i]
    if action == 2 :
        for i in range(4) :
            for j in range(4) :
                grille[i][j] = grille_ini[3-j][i]
    
    for i in range(4) :
        grille[i] = [val for val in grille[i] if val > 0]
        grille[i] = grille[i] + [0 for k in range(4 - len(grille[i]))]
    for i in range(4) :
        a,b,c,d = grille[i]
        if a == b :
            if c == d :
                grille[i] = [2*a, 2*c, 0, 0]
            else :
                grille[i] = [2*a, c, d, 0]
        else :
            if b == c :
                grille[i] = [a, 2*b, d, 0]
            else :
                if c == d :
                    grille[i] = [a, b, 2*c, 0]
    
    res = [[0 for j in range(4)] for i in range(4)]
    if action == 4 :
        res = grille
    if action == 6 :
        for i in range(4) :
            res[i] = grille[i][::-1]
    if action == 8 :
        for i in range(4) :
            for j in range(4) :
                res[i][j] = grille[3-j][i]
    if action == 2 :
        for i in range(4) :
            for j in range(4) :
                res[i][j] = grille[j][3-i]

    return res

def rajout(grille) :
    libre = [(i,j) for i in range(4) for j in range(4) if grille[i][j] == 0]
    if len(libre) == 0 :
        return None
    case = random.choice(libre)
    valeur = random.choice([2,4])
    grille[case[0]][case[1]] = valeur
    return grille

def actions(grille) :
    actions_list = list()
    for k in [2,4,6,8] :
        if grille != mouvement(grille,k) :
            actions_list.append(k)
    return actions_list

def gagner(grille) :
    for i in range(4) :
        for j in range(4) :
            if grille[i][j] == 2048 :
                return True
    return False

def jeu() :
    grille = [[0 for j in range(4)] for i in range(4)]
    grille = rajout(grille)
    affichage(grille)
    actions_list = actions(grille)
    while len(actions_list) != 0 :
        try:
            action = int(input("Sélectionner votre action (2,4,6,8) : "))
        except ValueError:
            action = None
        while action not in actions_list :
            try:
                action = int(input(f"Action {action} non autorisée, veuillez choisir dans {actions_list} : "))
            except ValueError:
                pass
        grille = rajout(mouvement(grille, action))
        affichage(grille)
        if gagner(grille) :
            print("Vous avez gagné !")
            break
        actions_list = actions(grille)
    if not gagner(grille):
        print("Vous avez perdu...")




