def carregar(self, arquivo, delimiter, quoteChar, 
                ignoraLinha1, ignoraColuna1):
    self.dados = []
    with open(arquivo) as csv_file:
        csv_reader = csv.reader(csv_file, 
                        delimiter=delimiter, 
                        quoting=csv.QUOTE_NONNUMERIC)
        if ignoraLinha1:
            next(csv_reader)                  
        for i, row in enumerate(csv_reader):
            if type(row[-1]) != str:
                row[-1] = str(int(row[-1]))
            if ignoraColuna1:
                self.dados.append(tuple(row[1:]))
            else:
                self.dados.append(tuple(row))
