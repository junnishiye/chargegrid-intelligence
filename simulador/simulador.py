import time
import datetime

tempoRecarga = 0
valorRecarga = 0
valorkWh = 0.805 * 30   # para esse carregador: 30kWh por R$0.805 cada

def CalcularRecarga(tempo, valor):
    # verifica qual variável é 0 para calcular a outra
    if tempo == 0:
        return valorRecarga / valorkWh
    elif valor == 0:
        return tempoRecarga * valorkWh

def VerificacaoVariavel(texto):
    # impede que valores inválidos sejam aceitos
    try:
        valor = float(input(f"\nDigite o {texto} da recarga: "))
    except ValueError:
        return VerificacaoVariavel(texto)
    else:
        if valor <= 0:
            return VerificacaoVariavel(texto)
        else:
            return valor

# --- tipo de usuário com tarifa diferenciada ---
while True:
    tipoUsuario = input("""
    Tipo de usuário:
    1 - Comum
    2 - Assinante (20% de desconto)
    """)
    if tipoUsuario in ["1", "2"]:
        break
    print("Opção inválida.")

if tipoUsuario == "2":
    valorkWh = valorkWh * 0.8   # aplica desconto de 20% na tarifa

# --- escolha de cobrança ---
while True:
    escolhaCobranca = input("""
    Escolha uma opção (digite o número apenas)
    1 - Recarregar por tempo
    2 - Recarregar por valor
    """)

    match escolhaCobranca:
        case "1":
            tempoRecarga = VerificacaoVariavel("tempo em horas")
            valorRecarga = CalcularRecarga(tempoRecarga, valorRecarga)
            break
        case "2":
            valorRecarga = VerificacaoVariavel("valor")
            tempoRecarga = CalcularRecarga(tempoRecarga, valorRecarga)
            break
        case _:
            print("\nValor inválido, tente novamente")

# --- função de recarga com barra de progresso ---
def Recarga(tempo):
    barraBase = "----------"

    print("\nRecarregando...")

    i = 0
    divTempo = tempo / 10
    contadorDiv = 0

    while i < tempo:
        if i > divTempo * contadorDiv:
            contadorDiv += 1
            barra = barraBase.replace("-", "*", contadorDiv)
            print(f"\r[{barra}]", end="")

        time.sleep(0.1)
        i += 0.1

    print("\nRecarregado ^_^")
    print("Agradecemos por escolher os nossos serviços!")

# --- confirmação e relatório ---
while True:
    escolhaRecarga = input(
        f"""
Valor da recarga: R${valorRecarga:.2f}
Tempo de espera: {tempoRecarga:.2f} horas

Deseja prosseguir com a recarga? (s/n)
        """
    ).lower()

    if escolhaRecarga in ["s", "sim"]:
        horarioInicio = datetime.datetime.now()   # registra início
        Recarga(tempoRecarga)
        horarioFim = datetime.datetime.now()      # registra fim

        print(f"""
╔══════════════════════════════════╗
       RELATÓRIO DA SESSÃO
╠══════════════════════════════════╣
  Tipo de usuário : {"Assinante" if tipoUsuario == "2" else "Comum"}
  Início          : {horarioInicio.strftime("%H:%M:%S")}
  Fim             : {horarioFim.strftime("%H:%M:%S")}
  Tempo de recarga: {tempoRecarga:.2f} horas
  Energia consumida: {tempoRecarga * 30:.2f} kWh
  Custo total     : R${valorRecarga:.2f}
╚══════════════════════════════════╝
        """)
        break

    elif escolhaRecarga in ["n", "nao", "não"]:
        print("Obrigado por escolher nossos serviços, tenha um ótimo dia")
        quit()

    else:
        print("Resposta inválida.")
