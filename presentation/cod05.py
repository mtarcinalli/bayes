    def treinar(self):
        total = len(self.dados)
        classes = list(set([x[-1] for x in self.dados]))
        combdata = {}
        pdata = {}
        # contagem dos dados
        for row in self.dados:
            classe = (row[-1])
            if classe in combdata:
                combdata[classe] += 1
            else:
                combdata[classe] = 1
                
                
                
            for i, d in enumerate(row[:-1]):
                # variavel continua
                if type(d) != str:
                    ind = 'i'+str(i)
                    if ind in combdata:
                        combdata[ind].append(float(d))
                    else:
                        combdata[ind] = [ float(d) ]
                    key = (ind,classe)    
                    if key in combdata:
                        combdata[key].append(float(d))
                    else:
                        combdata[key] = [float(d)]


                # variavel nominal
                else:
                    if d in combdata:
                        combdata[d] += 1
                    else:
                        combdata[d] = 1
                    key = (d,classe)
                    if key in combdata:
                        combdata[key] += 1
                    else:
                        combdata[key] = 1




# calculando probabilidades
self.modelo = {}
for c in combdata:
    # atributo + classe
    if type(c) == tuple:
        # variável continua
        if type(combdata[c]) != list:
            self.modelo[c] = combdata[c] / combdata[c[1]]
        else:
            media =  sum(combdata[c])/len(combdata[c])
            desvio=(sum([(x-media)**2 for x in combdata[c]]
                    )/(len(combdata[c])-1))**0.5
            self.modelo[c]={'media':media,'desvio':desvio}
    
    
    # somente classe
    else:
        if type(combdata[c]) != list:
            self.modelo[c] = combdata[c] / total
        else:
            media =  sum(combdata[c])/len(combdata[c])
            desvio=(sum([(x-media)**2 for x in combdata[c]]
                    )/(len(combdata[c])-1))**0.5
            self.modelo[c] = {
                'media' : media,
                'desvio' : desvio
            }
self.modelo['classes'] = classes
