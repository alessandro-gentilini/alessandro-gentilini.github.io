from sympy import symbols, Eq, solve, pprint, simplify

# Definire le variabili
rho_C, rho_L, a, b = symbols('rho_C rho_L a b')

# Definire il sistema di equazioni
equilibrio_prima = Eq(b,a*(rho_L-rho_C)/(rho_C))
pprint(equilibrio_prima)

alpha, beta, gamma, r = symbols('alpha beta gamma r')

invarianza_altezza = Eq(alpha+beta,a+b)
pprint(invarianza_altezza)

equilibrio_dopo = Eq(alpha*r**2*rho_L,rho_C*(alpha*r**2+beta*r**2-gamma**3/4))
pprint(equilibrio_dopo)



# Risolvere il sistema
solution = solve((equilibrio_prima, invarianza_altezza, equilibrio_dopo), (alpha, beta, b))

# Stampare la soluzione
Delta = solution[beta]-solution[b]
Delta = simplify(Delta)
pprint(Delta)