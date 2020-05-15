#!/usr/bin/python3
import csv
import classificador as cl
#from validacao import validacaoCruzada
import sys


arquivo = sys.argv[1]
delimiter = sys.argv[2]

#print(vl.validacaoCruzada)
clf = cl.Classificador()
clf.carregar(arquivo, delimiter=delimiter)
cl.validacaoCruzada(clf)