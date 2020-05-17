def carregarTexto(self, arquivo):
    dataset = []
    palavras = []
    with open(arquivo) as file:
        for line in file:
            frase = ''
            for ch in line[:-2].lower():
                if ch.isalpha():
                    frase += ch
                else:
                    frase += ' '
            frase = [ x for x in frase.strip().split(' ') 
                        if x != '' and len(x) > 3 ]
            classificacao = int(line[-2])
            dataset.append((frase,classificacao))
            palavras += frase
    palavras = list(set(palavras))
    dataset2 = []
    for x in dataset:
        aux = []
        for i,p in enumerate(palavras):
            if p in x[0]:
                aux.append('ps'+str(i))
            else:
                aux.append('pn'+str(i))
        aux.append(str(x[1]))
        dataset2.append(aux)
    self.dados = dataset2
