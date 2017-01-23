class Life:

	def __init__(self, lemons="lemons"):
		self.__lemons = lemons;

	def __give_lemons(self):
		return self.__lemons

class Me:
	def __init__(self, awesomeness="Truly awesome"):
		self.__awesomeness = awesomeness

	def __make_lemonade(self, lemons):
		for i in range(lemons):
			print(lemons[slice(i, i+1)]) # slice 'em (just for fun)
		return lemons[:-1] + "ade"

if __name__ == "__main__":
	life = Life() #lemons
	cyn = Me() # Truly awesome
	print(life.__give_lemons())
	lemonade = cyn.__make_lemonade(life.__give_lemons())
	print(lemonade)