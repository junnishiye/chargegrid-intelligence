import time

tempoRecarga = 0
valorRecarga = 0
valorkWh = 0.805 * 30   #para esse carregador eu coloquei 30kWh por R$0.805 cada

def CalcularRecarga(tempo, valor):    #verifica se uma das variáveis é 0 para poder atribuir um valor nela de acordo com as outras
    if tempo == 0:
        return valorRecarga / valorkWh
    elif valor == 0:
        return tempoRecarga * valorkWh

def VerificacaoVariavel(texto):    #usei uma funcao para impedir que valores errados sejam colocados nas variáveis
    try:    #try tenta fazer algo
        valor = float(input(f"\nDigite o {texto} da recarga: "))
    except ValueError:    #ativa quando o try falha e aparece um erro, pode ser especificado ou não, nesse caso é erro de valor
        return VerificacaoVariavel("texto")    #esse eu vou colocar só pra me relembrar no futuro, função recursiva precisa retornar ela mesma, senão quando sair vai ser NoneType
    else:    #else funciona assim como no if, caso dê certo ele roda
        if valor <= 0:
            return VerificacaoVariavel("texto")
        else:
            return valor


while True:    #para evitar erros, o while mantém ela no loop até que uma das duas opções sejam escolhidas
    escolhaCobranca = input(
        """
        Escolha uma opção (digite o número apenas)
        1 - Recarregar por tempo
        2 - Recarregar por valor
        """)

    match escolhaCobranca:    #o match serve como um if melhorado para a escolha da cobrança de recarga
        case "1":
            tempoRecarga = VerificacaoVariavel("tempo")

            valorRecarga = CalcularRecarga(tempoRecarga, valorRecarga)
            break    #para continuar o código

        case "2":
            valorRecarga = VerificacaoVariavel("valor")

            tempoRecarga = CalcularRecarga(tempoRecarga, valorRecarga)
            break

        case _:
            print("\nValor inválido, tente novamente")

def Recarga(tempo):                         #função para calcular o valor da recarga e mostar uma bela barra de carregamento
    barraBase = "----------"                #valor inicial da barra de carregamento

    print("\nRecarregando...")

    i = 0
    divTempo = tempo / 10                   #aqui o tempo foi dividido em 10 partes iguais, para poder aumentar a barra de 10% em 10%
    contadorDiv = 0                         #aqui foi feito uma variável para poder aumentar o valor da divisão
    while i < tempo:                        #um loop para fazer o carregamento demorar de acordo com o tempo colocado inicialmente
        if i > divTempo * (contadorDiv):    #a ideia é fazer com que o tempo seja dividido em 10 partes iguais e então a cada vez que a condiçao ativa, uma parte a mais é adicionada ao valor necessário para entrar no loop
            contadorDiv += 1
            barra = barraBase.replace("-", "*", contadorDiv)           #essa função troca um carácter de uma string por outro uma certa quantidade de vezes, ditado pelo contadorDiv
            print(f"\r[{barra}]", end="")                                       #o end faz com que o print adicione algo a mais no final, sem trocar de linha, e o \r faz voltar de volta ao começo da linha, substituindo a linha toda vez que rodar

        time.sleep(0.1)                     #importado da biblioteca time, o sleep faz com que tenha um delay até a rodar o código de novo
        i += 0.1                            #o aumento é menor que o normal, para poder contar valores flutuantes

    print("\nRecarregado ^_^")
    print("Agradeçemos por escolher os nossos serviços!")

escolhaRecarga = input(    #apenas um verificador para ter certeza de que é isso que a pessoa quer
f"""
Valor da recarga: R${valorRecarga:.2f}
Tempo de espera: {tempoRecarga:.2f} horas

Deseja prosseguir com a recarga? (s/n)
""")

if escolhaRecarga == "s":
    Recarga(tempoRecarga)
else:
    print("Obrigado por escolher nossos serviços, tenha um ótimo dia")
    quit()
