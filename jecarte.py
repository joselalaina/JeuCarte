import random
import time
import sys

class JeuDeCartes:
    def __init__(self):
        self.paquet = []
        for couleur in ["carreau", "coeur", "pique", "trèfle"]:
            for valeur in list(range(2,11)):
                carte = Carte(couleur, valeur)
                self.paquet.append(carte)
            for (nom, valeur) in {"as": 14, "valet": 11, "dame": 12, "roi": 13}.items():
                carte = Carte(couleur, valeur, nom)
                self.paquet.append(carte)
        self.melange()
        self.position = 0
        self.paquetPourDistribue = self.paquet.copy()
        
    def melange(self):
        random.shuffle(self.paquet)
        return self.paquet
        
    def choisitCarte(self, paquet=None):
        carte = ""
        if (len(self.paquetPourDistribue) > 0):
            carte = self.paquetPourDistribue.pop(random.randrange(len(self.paquetPourDistribue)))
        return carte
        
    def __iter__(self):
        return iter(self.paquet)
        
    def __next__(self):
        carte = self.paquet[self.position]
        self.position += 1
        return carte
        
    
class Carte:
    def __init__(self, couleur, valeur, nom=None):
        if not nom: nom = valeur
        self.couleur, self.valeur, self.nom = couleur, int(valeur), nom
    def __str__(self):
        mapping = {"carreau": "", "coeur": "", "pique": "", "trèfle": ""}
        return f"{mapping[self.couleur]} {self.nom}"
    def __repr__(self):
        return f"{self.couleur}.{self.nom}"
        
    
class Jeu:
    def __init__(self, nbJoueurs=2, interactif=True):
        self.interactif = interactif
        if self.interactif:
            print(f"\033[1mSaisir q ou quit pour quitter le jeu\033[0m")
        self.jeu = JeuDeCartes()
        self.mains = {}
        for i in range(nbJoueurs):
            self.mains["joueur" + str(i + 1)] = []
        self.distribue()
        
    def distribue(self):
        nbCartesParJoueur = 52 // len(self.mains)
        for joueur in self.mains:
            for i in range(nbCartesParJoueur):
                self.mains[joueur].append(self.jeu.choisitCarte())
                
    def gereInteraction(self):
        if self.interactif:
            key = input().rstrip()
            if key == "q" or key == "quit":
                print(f"Fin du jeu")
                exit()
            elif len(key) > 0 and key[0] == "a":
                joueur = key[2:] if len(key) > 1 else "all"
                if joueur in self.mains.keys():
                    print(f"{joueur} a les  cartes suivantes : ", end="")
                    for carte in self.mains[joueur]:
                        print(carte, end=",")
                    print("")
                elif joueur == "all":
                    for (joueur, main) in self.mains.items():
                        print(f"{joueur} a les cartes suivates : ", end="")
                        for carte in main:
                            print(carte, end=",")
                        print("")
        else:
            time.sleep(0.5)
            
    def joue(self):
        raise NotImplementedError
        

class Bataille(Jeu):
    def joue(self):
        while len(self.mains) > 1:
            self.tour()
            print("RESTE: ")
            for (joueur, main) in self.mains.copy().items():
                if (len(main) == 0):
                    del self.mains[joueur]
                    print(f"\n\033[1m{joueur} est éliminé !\033[0m")
                else:
                    print(f"{joueur}:{len(main)}", end="")
            self.gereInteraction()
        vainqueur = list(self.mains.key())[0]
        print(f"\n\033[1m{vainqueur} a gagné !\033[0m")
    
    def tour(self):
        tour = {}
        for (joueur, main) in self.mains.items():
            carte = main.pop(0)
            tour[joueur] = {"carte": carte, "score": carte.valeur}
        scoreMax, vainqueur = None, None
        i = 32
        for (joueur, details) in tour.items():
            if self.interactif:
                print(f"\033[{i}m{joueur} : \033[1m{details['carte']}\033[0m")
            if not scoreMax:
                scoreMax, vainqueur = details["score"], joueur
            else:
                if details["score"] > scoreMax:
                    scoreMax, vainqueur = details["score"], joueur
                elif details["score"] == scoreMax:
                    vainqueur = None
                else:
                    continue
            i += 1
        if vainqueur:
            if self.interactif:
                print(f"{vainqueur} gagne")
            self.donneCartesVainqueur(vainqueur, tour)
        else:
            print(f"\033[1mBataille !\033[0m")
            cartesRetournees = []
            while not vainqueur:
                for main in self.mains.values():
                    carte = main.pop(0)
                    cartesRetournees.append(carte)
                vainqueur, tour = self.tour()
            self.donneCartesVainqueur(vainqueur, tour)
            if self.interactif:
                print(f"Les cartes retournées sont :", end="")
            for carte in cartesRetournees:
                if self.interactif:
                    print(f"\033[1m{carte}\033[0m", end="")
                self.mains[vainqueur].append(carte)
            print("")
        return vainqueur, tour
        
    
    def donneCartesVainqueur(self, vainqueur, tour):
        for (joueur, details) in tour.items():
            self.mains[vainqueur].append(details["carte"])
            
            
class Pouilleux(Jeu):
    def joue(self):
        for (joueur, main) in self.mains.items():
            i = 0
            for carte in main:
                if carte.couleur == "trèfle" and carte.nom == "valet":
                    main.pop(i)
                    
        self.paires = []
        for carte in self.jeu:
            for (couleur1, couleur2) in {"coeur": "carreau", "pique": "trèfle"}.items():
                if carte.couleur == couleur1:
                    for carte2 in self.jeu:
                        if carte2.couleur == couleur2 and carte.valeur == carte.valeur:
                            self.paires.append([carte, carte2])
        
        for main in self.mains.values():
            self.supprimePaires(main)
            
        while len(self.mains) > 1:
            self.tour()
        
    def tour(self):
        ordreJoueur = list(self.mains.keys())
        i, j = 1, 32
        for joueur in ordreJoueurs:
            if i < len(ordreJoueurs):
                pioche = ordreJoueurs[i]
            else:
                pioche = ordreJoueurs[0]
            i += 1
            nbCartesJoueur, nbCartesPioche = len(self.mains[joueur]), len(self.mains[pioche])
            if nbCartesPioche == 0:
                continue
            print(f"\033[{j}m{joueur} ({nbCartesJoueur}) pioche chez {pioche} ({nbCartesPioche})")
            carte = self.mains[pioche].pop(random.randrange(len(self.mains[pioche])))
            print(f"{joueur} a pioché {carte}\033[0m", end="")
            self.mains[joueur].append(carte)
            self.supprimePaires(self.mains[joueur])
            if not j == 33:
                j += 1
            else:
                j += 2
            if len(self.mains[pioche]) == 0:
                del self.mains[pioche]
                print(f"\n\033[1m{pioche} a terminé le jeu :-)\033[0m")
                if len(self.mains) == 1:
                    print(f"\033[1m{joueur} a perdu !!!\033[Om")
                break
            
            slef.gereInteraction()
            
    def supprimePaires(self, main):
        for carte in main:
            for paire in self.paires:
                if carte.couleur in ["coeur", "pique"] and carte in paire:
                    carte2 = paire [1]
                    if carte2 in main:
                        del main[main.index(carte)]
                        del main[main.index(carte2)]
                        
                        
                        
if __name__ == "__main__":
    jeu, nbJoueurs, interactif = "bataille", 5, True
    i = 0
    while sys.argv:
        i += 1
        if i == 1:
            sys.argv.pop(0)
            continue
        elif i == 2:
            jeu = sys.argv.pop(0).lower()
        elif i == 3:
            nbJoueurs = int(sys.argv.pop(0))
        elif i == 4:
            arg = sys.argv.pop(0)
            if arg == "0" or arg == "" or arg == "False":
                interactif = False
                
if jeu == "bataille":
    jeu = Bataille(nbJoueurs, interactif)
    jeu.joue()
elif jeu in ["pouilleux", "valetpuant", "zwartepiet"]:
    jeu = Pouilleux(nbJoueurs, interactif)
    jeu.joue()                        
                                                                                                            
                                                                                                                  
                                                                                                                                                           
