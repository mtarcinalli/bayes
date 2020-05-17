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
        tupl = tupla[:-1]
        pred = clf2.predizer(tupl, debug=False) 
        if pred == tupla[-1]:
            ok += 1

    print('Conj Teste:',len(dadosTestes))
    print('Acertos   :',ok)
    print('Acurácia  :',ok/len(dadosTestes)*100,'%')
    