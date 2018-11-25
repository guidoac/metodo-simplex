import numpy as np

arq = open('in.txt', 'r').read()
arq_s = open('out.txt', 'w')

def criar_matriz(str_matriz):
    matriz = str_matriz.splitlines()
    matriz_ret = []
    for linha in matriz:
        linha = linha.split()
        matriz_ret.append(linha)
    return matriz_ret

def forma_padrao(mat_inicial):
    func_obj = np.array(mat_inicial[0])
    restri_inicial = np.array(mat_inicial[1:])

    matriz_ini_larg = func_obj.shape[0]
    num_restri = restri_inicial.shape[0]

    restri_f = np.delete(restri_inicial, matriz_ini_larg-1, axis=1)

    func_obj_folga = np.zeros(num_restri, dtype=int)
    restri_folga = np.eye(num_restri,dtype=int)

    func_obj_final = np.insert(func_obj, matriz_ini_larg-1, values=func_obj_folga)
    restri_final = np.insert(restri_f,matriz_ini_larg-1, values=restri_folga, axis=1)

    mat_forma_padrao = np.append([func_obj_final], restri_final, axis=0)

    return mat_forma_padrao.astype(float)

def coluna_pivo(matriz):
    func_obj = matriz[0]
    menor_elem = func_obj[0]
    i_col_pivo = 0
    for i, elem in enumerate(func_obj):
        if elem < menor_elem:
            menor_elem = elem
            i_col_pivo = i

    col_pivo = matriz[:,i_col_pivo]
    return col_pivo

def elem_pivo(coluna_pivo, const):
    lista_aux = []

    for i, coef in enumerate(coluna_pivo):
        if coef >= 0:
            aux = const[i]/coef
            lista_aux.append((aux,i))
    menor_aux = min(lista_aux)
    elem_pivo = coluna_pivo[menor_aux[1]]
    print('coluna pivo: {0}, constantes: {1}'.format(coluna_pivo, const))
    arq_s.write('\ncoluna pivo: {0}, constantes: {1}'.format(coluna_pivo, const))
    print('coef depois da divisao: {0}\n'.format(lista_aux))
    arq_s.write('\ncoef depois da divisao: {0}\n'.format(lista_aux))

    print('numero pivo: {}'.format(elem_pivo))
    arq_s.write('\nnumero pivo: {}'.format(elem_pivo))
    return elem_pivo, menor_aux[1]

def escalonar(matriz, num_pivo, linha_pivo, coluna_pivo):
    nova_linha_p = matriz[linha_pivo]/num_pivo
    matriz[linha_pivo] = nova_linha_p

    print('nova linha pivo: {}'.format(matriz[linha_pivo]))
    arq_s.write('\nnova linha pivo: {}'.format(matriz[linha_pivo]))

    matriz_escalonada = []

    print('----------------------- ESCALONANDO -------------------------\n')
    arq_s.write('\n----------------------- ESCALONANDO -------------------------\n')
    for i,linha in enumerate(matriz):
        if i != linha_pivo:
            nova_linha= linha - (coluna_pivo[i] * nova_linha_p)
            matriz_escalonada.append(nova_linha)
        else:
            matriz_escalonada.append(nova_linha_p)

    matriz_escalonada = np.array(matriz_escalonada)
    print(matriz_escalonada)
    arq_s.write('\n{}'.format(matriz_escalonada))
    return matriz_escalonada

def solucao_otima(func_obj):
    menor_valor = min(func_obj)
    if menor_valor < 0:
        return False
    else:
        return True

print(arq)
arq_s.write(arq)
print('-------------------------------------------------------------')
arq_s.write('\n-------------------------------------------------------------')
matriz_final = criar_matriz(arq)

mat_padrao = forma_padrao(matriz_final)
print(mat_padrao)
arq_s.write('\n{}'.format(mat_padrao))

mat_aux = mat_padrao

while solucao_otima(mat_aux[0]) != True:
    print('função objetivo: {}\n'.format(mat_aux[0]))
    arq_s.write('\nfunção objetivo: {}\n'.format(mat_aux[0]))

    col_pivo = coluna_pivo(mat_aux)
    constantes = mat_aux[:,len(mat_aux[0])- 1]

    num_pivo, i_num_pivo = elem_pivo(col_pivo, constantes)

    mat_aux = escalonar(mat_aux, num_pivo, i_num_pivo, col_pivo)
    func_obj = mat_aux[0]

max_z = mat_aux[0][len(mat_aux[0])-1]

print('\nRESULTADO FINAL -- MAX Z = {}'.format(max_z))
arq_s.write('\nRESULTADO FINAL -- MAX Z = {}'.format(max_z))
arq_s.close()
