import matplotlib.pyplot as plt

"""
definiçao das funções do problema
"""

#funcao que define a velocidade da massa 1
def fa(x1):
    return x1

#funcao que define posicao da massa 1
def fb(k1, k2, m1, z,d, y, c, fa):
    return (k2/m1)*(z-d) - (k1/m1)*y - (c/m1)*fa

#funcao que define a velocidade da massa 2
def fc(x2):
    return x2

#funcao que define posicao da massa 2
def fd(k2, m2, z, d):
    return -(k2/m2)*(z-d)


# heun ou rk2 usado para fazer a inicialização do problema
def heun(z, x1, y,d, x2, h, fa, fb, fc,fd, k1, k2, m1, m2, c):

    # calcula os valores de k1 para cada uma das funções
    k1fa = fa(x1)
    k1fb = fb(k1, k2, m1, z, d, y, c, fa(x1))
    k1fc = fc(x2)
    k1fd = fd(k2, m2, z, d)

    # calcula os valores de k2 para cada uma das funções
    k2fa = fa(x1 + k1fa * h)
    k2fb = fb(k2, k1, m1, z + k1fb * h , d , y + k1fb * h , c, fa(x1))
    k2fc = fc(x2 + h  * k1fc)
    k2fd = fd(k2, m2, z + h * k1fd, d )

    # calcula os novos valores para o vetor [x1, z, x2, y]
    x1 = x1 + (k1fa + k2fa) * h/2
    z = (z + (k1fb + k2fb ) * h/2) + d
    x2 = x2 + (k1fc + k2fc) * h/2
    y = y + (k1fd + k2fd) * h/2

    return x1, z, x2, y

# ab para previsao
def ab2(x1atual, x1anterior, h):
    return x1atual + (3 * x1atual - x1anterior) * h/2

# am para correcao
def am2(x1atual, x1anterior, h):
    return x1atual + (x1atual + ab2(x1atual, x1anterior, h)) * h / 2

# utiliza os metodos ab e am definidos para calcular os novos valores para o vetor [x1, z, x2, y]
def preditorCorretor(x1atual, x1anterior, zatual, zanterior, x2atual, x2anterior, yatual, yanterior, h):
    x1novo = am2(x1atual, x1anterior, h)
    znovo = am2(zatual, zanterior, h)
    x2novo = am2(x2atual, x2anterior, h)
    ynovo = am2(yatual, yanterior, h)

    return x1novo, znovo, x2novo, ynovo

if __name__ =='__main__':

    # inicialização com valores iniciais
    x1 = 1      #velocidade de m1
    y = 1       #posicao de m1
    x2 = -1     #velocidade de m2
    z = 2       #posicao de m2
    d = 1.5     #posicao de m2 na qual a mola esta em repouso
    h = 1
    k1 = 0.2    #constante elastica da mola 1
    k2 = 0.5    #constante elastica da mola 2
    m1 = 2      #massa m1
    m2 = 2      #massa m2
    c = 0.2     #constante de proporcionalidade do atrito

    #vetores para guardar os valores obtdos para serem usandos mais tarde no grafico
    velocidadeM1 = []
    posicaoM1 = []

    velocidadeM2 = []
    posicaoM2 = []

    #inicializa os vetores com os valores inicias
    velocidadeM1.append(x1)
    velocidadeM2.append(x2)
    posicaoM1.append(y)
    posicaoM2.append(z)

    #calcula os novos valores para o vetor [x1 z x2 y] a serem utilizados para inicializar a previsao-correcao
    x1atual, zatual, x2atual, yatual = heun(z, x1, y, d, x2, h, fa, fb, fc, fd, k1, k2, m1, m2, c)

    #armazena os novos valores encontrados
    velocidadeM1.append(x1atual)
    velocidadeM2.append(x2atual)
    posicaoM1.append(yatual)
    posicaoM2.append(zatual)

    for i in range(300):
        # calcula os novos valores para o vetor [x1 z x2 y]
        x1novo, znovo, x2novo, ynovo = preditorCorretor(x1atual, x1, zatual, z, x2atual, x2, yatual, y, h)

        # armazena os novos valores encontrados
        velocidadeM1.append(x1novo)
        velocidadeM2.append(x2novo)
        posicaoM1.append(ynovo)
        posicaoM2.append(znovo)

        #anda com os valores para serem utilizados na proxima iteracao
        x1 = x1atual
        x1atual = x1novo
        z = zatual
        zatual = znovo
        x2 = x2atual
        x2atual = x2novo
        y = yatual
        yatual = ynovo

#plot o grafico com os valores obtidos

plt.plot(posicaoM1, 'b')
plt.plot(velocidadeM1, 'g')
plt.plot(posicaoM2, 'r')
plt.plot(velocidadeM2, 'y')
print  "posicao m1: {}".format(posicaoM1)
print  "velocidade m1: {}".format(velocidadeM1)
print  "posicao m2: {}".format(posicaoM2)
print  "velocidade m2: {}".format(velocidadeM2)
plt.show()

