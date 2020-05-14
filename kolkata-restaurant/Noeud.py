class Noeud:
	def __init__(self, etat, g, pere=None):
		self.etat = etat
		self.g = g
		self.pere = pere

	def __str__(self):
		#return np.array_str(self.etat) + "valeur=" + str(self.g)
		return str(self.etat) + "valeur=" + str(self.g)

	def __eq__(self, other):
		return str(self) == str(other)

	def __lt__(self, other):
		return str(self) < str(other)

	def expand(self,p,acutalPos):
		#extension des noeud
		nouveaux_fils = [Noeud(s,self.g+p.cost(self.etat,s),self) for s in p.successeurs(self.etat,acutalPos)]
		return nouveaux_fils

	def expandNext(self,p,k):
		#etend un noeud unique le k-ieme fils du noeud n ou liste vide si plus de noeud a etendre
		nouveaux_fils = self.expand(p)
		if len(nouveaux_fils)<k: 
			return []
		else: 
			return self.expand(p)[k-1]

	def trace(self,p):
		#affiche tous les ancetres du noeud
		n = self
		c=0    
		while n!=None :
			print (n)
			n = n.pere
			c+=1
			print ("Nombre d'etapes de la solution:", c-1)
		return
