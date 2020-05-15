import csv
import random

class Classificador:
    dados = []
    modelo = {}
    
    def carregar(self, arquivo, delimiter=';', quoteChar='"', ignoraLinha1=True, ignoraColuna1=False):
        self.dados = []
        with open(arquivo) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)
            if ignoraLinha1:
                next(csv_reader)                  
            for i, row in enumerate(csv_reader):
                if type(row[-1]) != str:
                    row[-1] = str(int(row[-1]))
                if ignoraColuna1:
                    self.dados.append(tuple(row[1:]))
                else:
                    self.dados.append(tuple(row))
    
    def carregarTexto(self, arquivo):
        dataset = []
        # lista com todas as palavras encontradas
        palavras = []
        # carregando dataset
        # pré-processamento:
        # - remoção pontuação
        # - conversão para minusculas
        # - remoção de palavras com menos de 3 caracteres
        with open(arquivo) as file:
            for line in file:
                frase = ''
                for ch in line[:-2].lower():
                    if ch.isalpha():
                        frase += ch
                    else:
                        frase += ' '
                # conversão da frase em lista de palavras
                frase = [ x for x in frase.strip().split(' ') if x != '' and len(x) > 3 ]
                classificacao = int(line[-2])
                dataset.append((frase,classificacao))
                palavras += frase
        # removendo repetição de palavras
        palavras = list(set(palavras))
        # convertendo frases para matriz com atributos nominais
        # ps<i> : indica que a palavra de indice <i> foi encontrada
        # pn<i> : indica que a palavra de indice <i> não foi encontrada
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
    
    def treinar(self):
        total = len(self.dados)
        classes = list(set([x[-1] for x in self.dados]))
        combdata = {}
        pdata = {}
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
            if type(c) == tuple:
                if type(combdata[c]) != list:
                    self.modelo[c] = combdata[c] / combdata[c[1]]
                else:
                    media =  sum(combdata[c])/len(combdata[c])
                    desvio = (sum([(x-media)**2 for x in combdata[c]])/(len(combdata[c])-1))**0.5
                    self.modelo[c] = {
                        'media' : media,
                        'desvio' : desvio
                    }
            else:
                if type(combdata[c]) != list:
                    self.modelo[c] = combdata[c] / total
                else:
                    media =  sum(combdata[c])/len(combdata[c])
                    desvio = (sum([(x-media)**2 for x in combdata[c]])/(len(combdata[c])-1))**0.5
                    self.modelo[c] = {
                        'media' : media,
                        'desvio' : desvio
                    }
        self.modelo['classes'] = classes
    
    def g(self, x, media, desvio):
        p1 = 1 / ( (2*3.141592653589793)**0.5 * desvio  )
        p2 = 2.718281828459045 ** (-((x - media) ** 2) / (2 * desvio ** 2))
        return p1 * p2
    
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
                        numerador = numerador * self.g(v,self.modelo[key1]['media'],self.modelo[key1]['desvio'])
                    denominador = denominador * self.g(v,self.modelo[key2]['media'],self.modelo[key2]['desvio'])
            numerador = numerador * self.modelo[classe]
            probClasse[classe] = numerador / denominador
            if debug:
                print(classe,probClasse[classe])
            if probClasse[classe] > valClasse:
                valClasse = probClasse[classe]
                maxClasse = classe
        return(maxClasse)        
    
    # método necessário para gerar gráfico
    def predict(self, tuplas):
        res = []
        for t in tuplas:
            res.append(int(self.predizer(t)))
        return(np.array(res))

    def graficoFronteira(self):
        X = np.array([ [float(x[0]),float(x[1])] for x in self.dados ])
        y = np.array([ int(float(x[2])) for x in self.dados ])
        plot_decision_regions(X, y, clf=self, legend=2)
        
def validacaoCruzada(clf, porcentagem=0.7):
    dados = clf.dados
    random.shuffle(dados)
    dadosTreinamento = dados[:int(len(dados)*porcentagem)]
    dadosTestes = dados[int(len(dados)*porcentagem):]
    clf2 = Classificador()
    clf2.dados = dadosTreinamento
    clf2.treinar()
    ok = 0
    for tupla in dadosTestes:
        #tupl = [ float(x) for x in tupla[:-1]]
        tupl = tupla[:-1]
        pred = clf2.predizer(tupl, debug=False) 
        if pred == tupla[-1]:
            ok += 1
    print('Conj Teste:',len(dadosTestes))
    print('Acertos   :',ok)
    print('Acurácia  :',ok/len(dadosTestes)*100,'%')