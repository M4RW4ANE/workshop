class node:
    def __init__(self, word, word_count=0, parent=None, link=None):
        # Initialisation d'un nœud dans l'arbre
        self.word = word  # Mot représenté par le nœud
        self.word_count = word_count  # Compte d'occurrence du mot
        self.parent = parent  # Référence au parent du nœud
        self.link = link  # Lien vers un autre nœud ayant le même mot
        self.children = {}  # Dictionnaire des enfants du nœud

    def visittree(self):
        # Méthode pour parcourir l'arbre et afficher ses nœuds
        output = [f"{self.word} ({self.word_count})"]  # Ajout du mot et du compte au résultat
        if len(self.children) > 0:  # Si le nœud a des enfants
            for i in self.children.keys():
                output.extend(self.children[i].visittree())  # Appel récursif pour visiter les enfants
        return output


class fptree:
    def __init__(self, data, minsup=400):
        # Initialisation de l'arbre FP
        self.data = data  # Données transactionnelles
        self.minsup = minsup  # Seuil minimal de support

        # Racine de l'arbre FP (nœud vide)
        self.root = node(word="Null", word_count=1)

        # Structures pour le traitement
        self.wordlinesort = []  # Transactions triées par fréquence des mots
        self.nodetable = []  # Table des nœuds pour gérer les liens
        self.wordsortdic = []  # Liste des mots triés par fréquence
        self.worddic = {}  # Dictionnaire des mots avec leurs comptes
        self.wordorderdic = {}  # Dictionnaire des positions des mots dans le tri

        # Construction de l'arbre FP
        self.construct(data)

    def construct(self, data):
        # Première étape : comptage des supports des mots
        for tran in data:  # Parcours des transactions
            for words in tran:  # Parcours des mots dans une transaction
                if words in self.worddic.keys():
                    self.worddic[words] += 1
                else:
                    self.worddic[words] = 1

        # Suppression des mots avec un support < minsup
        wordlist = list(self.worddic.keys())
        for word in wordlist:
            if self.worddic[word] < self.minsup:
                del self.worddic[word]

        # Tri des mots restants par fréquence décroissante
        self.wordsortdic = sorted(self.worddic.items(), key=lambda x: (-x[1], x[0]))

        # Création de la table des nœuds (pour gérer les liens entre nœuds du même mot)
        t = 0
        for i in self.wordsortdic:
            word = i[0]
            wordc = i[1]
            self.wordorderdic[word] = t  # Enregistrement de la position du mot dans le tri
            t += 1
            wordinfo = {'wordn': word, 'wordcc': wordc, 'linknode': None}
            self.nodetable.append(wordinfo)

        # Deuxième étape : construction de l'arbre ligne par ligne
        for line in data:
            supword = []  # Liste des mots ayant un support suffisant
            for word in line:
                if word in self.worddic.keys():
                    supword.append(word)

            if len(supword) > 0:
                # Trie des mots dans la ligne selon l'ordre des fréquences
                sortsupword = sorted(supword, key=lambda k: self.wordorderdic[k])
                self.wordlinesort.append(sortsupword)
                R = self.root  # Commence à la racine
                for i in sortsupword:
                    if i in R.children.keys():
                        R.children[i].word_count += 1  # Incrémente si le nœud existe
                        R = R.children[i]
                    else:
                        # Crée un nouveau nœud et l'ajoute comme enfant
                        R.children[i] = node(word=i, word_count=1, parent=R, link=None)
                        R = R.children[i]
                        # Mise à jour des liens dans la table des nœuds
                        for wordinfo in self.nodetable:
                            if wordinfo["wordn"] == R.word:
                                if wordinfo["linknode"] is None:
                                    wordinfo["linknode"] = R
                                else:
                                    iter_node = wordinfo["linknode"]
                                    while iter_node.link is not None:
                                        iter_node = iter_node.link
                                    iter_node.link = R

    def condtreetran(self, N):
        # Création des transactions pour un arbre conditionnel
        if N.parent is None:
            return None

        condtreeline = []
        while N is not None:
            line = []
            PN = N.parent
            while PN.parent is not None:
                line.append(PN.word)  # Ajout des mots depuis le nœud jusqu'à la racine
                PN = PN.parent
            line = line[::-1]  # Inverse l'ordre pour conserver la hiérarchie
            for _ in range(N.word_count):
                condtreeline.append(line)
            N = N.link  # Passe au prochain nœud dans la liste des liens
        return condtreeline

    def findfqt(self, parentnode=None):
        # Recherche des ensembles fréquents
        if len(list(self.root.children.keys())) == 0:
            return None
        result = []
        sup = self.minsup
        revtable = self.nodetable[::-1]  # Parcours en sens inverse de la table des nœuds
        for n in revtable:
            fqset = [set(), 0]
            if parentnode is None:
                fqset[0] = {n['wordn']}
            else:
                fqset[0] = {n['wordn']}.union(parentnode[0])
            fqset[1] = n['wordcc']
            result.append(fqset)
            condtran = self.condtreetran(n['linknode'])
            contree = fptree(condtran, sup)
            conwords = contree.findfqt(fqset)
            if conwords is not None:
                for words in conwords:
                    result.append(words)
        return result

    def checkheight(self):
        # Vérifie si l'arbre a une hauteur > 1
        return len(list(self.root.children.keys())) > 0


# Exemple de test
min_sup = 4

test_data = [['I1', 'I2', 'I5'],
             ['I2', 'I4'],
             ['I2', 'I3'],
             ['I1', 'I2', 'I4'],
             ['I1', 'I3'],
             ['I2', 'I3'],
             ['I1', 'I3'],
             ['I1', 'I2', 'I3', 'I5'],
             ['I1', 'I2', 'I3']]

vocabdic = {"I1": "Item1", "I2": "Item2", "I3": "Item3", "I4": "Item4", "I5": "Item5"}

fp_tree = fptree(test_data, min_sup)

print("\n========== Ensembles fréquents ==========")
frequentwordset = fp_tree.findfqt()
frequentwordset = sorted(frequentwordset, key=lambda k: -k[1])

for word in frequentwordset:
    count = str(word[1]) + "\t"
    words = ' '.join(vocabdic[val] for val in word[0])
    print(count + words)

print("\n========== Arbres conditionnels ==========")
for i in fp_tree.nodetable[::-1]:
    lines = fp_tree.condtreetran(i['linknode'])
    condtree = fptree(lines, min_sup)
    if condtree.checkheight():
        print(f"Arbre conditionnel pour {vocabdic[i['wordn']]}")
        print('\n'.join(condtree.root.visittree()))
