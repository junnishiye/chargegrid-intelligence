import time

import datetime

tempoRecarga = 0
valorRecarga = 0
valorkWh = 0.805 * 30   #para esse carregador eu coloquei 30kWh por R$0.805 cada

def CalcularRecarga(tempo, valor):    #verifica se uma das vari�veis � 0 para poder atribuir um valor nela de acordo com as outras
    if tempo == 0:
        return valorRecarga / valorkWh
    elif valor == 0:
        return tempoRecarga * valorkWh

def VerificacaoVariavel(texto):    #usei uma funcao para impedir que valores errados sejam colocados nas vari�veis
    try:    #try tenta fazer algo
        valor = float(input(f"\nDigite o {texto} da recarga: "))
    except ValueError:    #ativa quando o try falha e aparece um erro, pode ser especificado ou n�o, nesse caso � erro de valor
        return VerificacaoVariavel(texto)    #esse eu vou colocar s� pra me relembrar no futuro, fun��o recursiva precisa retornar ela mesma, sen�o quando sair vai ser NoneType
    else:    #else funciona assim como no if, caso d� certo ele roda
        if valor <= 0:
            return VerificacaoVariavel(texto)
        else:
            return valor

# --- tipo de usu�rio com tarifa diferenciada ---
while True:
    tipoUsuario = input("""
    Tipo de usu�rio:
    1 - Comum
    2 - Assinante (20% de desconto)
    """)
    if tipoUsuario in ["1", "2"]:
        break
    print("Op��o inv�lida.")

if tipoUsuario == "2":
    valorkWh = valorkWh * 0.8   # aplica desconto de 20% na tarifa

# --- escolha de cobran�a ---
while True:    #para evitar erros, o while mant�m ela no loop at� que uma das duas op��es sejam escolhidas
    escolhaCobranca = input(
    """
    Escolha uma op��o de recarregamento (digite o n�mero apenas)
    1 - Recarregar por tempo
    2 - Recarregar por valor
    """)

    match escolhaCobranca:    #o match serve como um if melhorado para a escolha da cobran�a de recarga
        case "1":
            tempoRecarga = VerificacaoVariavel("tempo em horas")

            valorRecarga = CalcularRecarga(tempoRecarga, valorRecarga)
            break    #para continuar o c�digo

        case "2":
            valorRecarga = VerificacaoVariavel("valor")

            tempoRecarga = CalcularRecarga(tempoRecarga, valorRecarga)
            break

        case _:
            print("\nValor inv�lido, tente novamente")

def Recarga(tempo):                         #fun��o para calcular o valor da recarga e mostar uma bela barra de carregamento
    barraBase = "----------"                #valor inicial da barra de carregamento

    print("\nRecarregando...")

    i = 0
    divTempo = tempo / 10                   #aqui o tempo foi dividido em 10 partes iguais, para poder aumentar a barra de 10% em 10%
    contadorDiv = 0                         #aqui foi feito uma vari�vel para poder aumentar o valor da divis�o
    while i < tempo:                        #um loop para fazer o carregamento demorar de acordo com o tempo colocado inicialmente
        if i > divTempo * (contadorDiv):    #a ideia � fazer com que o tempo seja dividido em 10 partes iguais e ent�o a cada vez que a condi�ao ativa, uma parte a mais � adicionada ao valor necess�rio para entrar no loop
            contadorDiv += 1
            barra = barraBase.replace("-", "*", contadorDiv)           #essa fun��o troca um car�cter de uma string por outro uma certa quantidade de vezes, ditado pelo contadorDiv
            print(f"\r[{barra}]", end="")                                       #o end faz com que o print adicione algo a mais no final, sem trocar de linha, e o \r faz voltar de volta ao come�o da linha, substituindo a linha toda vez que rodar

        time.sleep(0.1)                     #importado da biblioteca time, o sleep faz com que tenha um delay at� a rodar o c�digo de novo
        i += 0.1                            #o aumento � menor que o normal, para poder contar valores flutuantes

    print("\nRecarregado ^_^")
    print("Agrade�emos por escolher os nossos servi�os!")

while True:
    escolhaRecarga = input(
        f"""
Valor da recarga: R${valorRecarga:.2f}
Tempo de espera: {tempoRecarga:.2f} horas

Deseja prosseguir com a recarga? (s/n)
        """
    ).lower()

    if escolhaRecarga in ["s", "sim"]:
        horarioInicio = datetime.datetime.now()  # registra in�cio
        Recarga(tempoRecarga)
        horarioFim = datetime.datetime.now()  # registra fim

        print(f"""
    ????????????????????????????????????
           RELAT�RIO DA SESS�O
    ????????????????????????????????????
      Tipo de usu�rio : {"Assinante" if tipoUsuario == "2" else "Comum"}
      In�cio          : {horarioInicio.strftime("%H:%M:%S")}
      Fim             : {horarioFim.strftime("%H:%M:%S")}
      Tempo de recarga: {tempoRecarga:.2f} horas
      Energia consumida: {tempoRecarga * 30:.2f} kWh
      Custo total     : R${valorRecarga:.2f}
    ????????????????????????????????????
            """)
        break

    elif escolhaRecarga in ["n", "nao", "n�o"]:
        print("Obrigado por escolher nossos servi�os, tenha um �timo dia")
        quit()

    else:
        print("Resposta inv�lida.")
