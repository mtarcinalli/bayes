tenis2 = Classificador()
tenis2.carregar('data/tenis2.csv')
tenis2.treinar()
tenis2.predizer(['sol', 83, 73, 'verdadeiro'], debug=True)

sim 0.2984141388375451
não 0.6661952433370804

'não'
