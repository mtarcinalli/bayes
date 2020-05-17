def g(self, x, media, desvio):
    p1 = 1 / ( (2*3.141592653589793)**0.5 * desvio  )
    p2=2.718281828459045**(-((x-media)**2)/(2*desvio**2))
    return p1 * p2
