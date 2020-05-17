def predict(self, tuplas):
    res = []
    for t in tuplas:
        res.append(int(self.predizer(t)))
    return(np.array(res))

def graficoFronteira(self):
    X=np.array([[float(x[0]),float(x[1])] 
                    for x in self.dados])
    y=np.array([int(float(x[2])) for x in self.dados])
    plot_decision_regions(X, y, clf=self, legend=2)
