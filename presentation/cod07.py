def predizer(self, tupla, debug=False):
    probClasse = {}
    valClasse = 0
    maxClasse = ''
    for classe in self.modelo['classes']:
        numerador = 1
        denominador = 1
        for i, v in enumerate(tupla):







# atributo nominal
if type(v) == str:
    key = (v, classe)
    if key in self.modelo:
        numerador = numerador * self.modelo[key]
    else:
        numerador = numerador * 0.001
    if v in self.modelo:
        denominador = denominador * self.modelo[v]
    else:
        denominador = denominador * 0.001




    # atributo continuo
    else:
        v = float(v)
        key1 = ('i'+str(i),classe)
        key2 = 'i'+str(i)
        if key1 in self.modelo:
            numerador=numerador*self.g(v,
                            self.modelo[key1]['media'],
                            self.modelo[key1]['desvio'])
        denominador=denominador*self.g(v,
                            self.modelo[key2]['media'],
                            self.modelo[key2]['desvio'])
numerador = numerador * self.modelo[classe]
probClasse[classe] = numerador / denominador

    if debug:
        print(classe,probClasse[classe])
    if probClasse[classe] > valClasse:
        valClasse = probClasse[classe]
        maxClasse = classe
return(maxClasse)        
