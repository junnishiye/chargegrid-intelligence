import time
import datetime

class Usuario:  #cria um classe para poder gerar um formulário de usuário
    nome = ""   #não usei uma função construtora, porque eu queria que fosse contruido pelo input, e não ao instanciar
    nascimento = ""
    endereco = ""
    telefone = ""
    cpf = ""
    email = ""

    def Formulario(self):   #o self é usado para guardar as informações da instância, e não pegar da classe em geral
        self.nome = input("Digite o seu nome: ")
        self.nascimento = input("Digite a sua data de nascimento: ")
        self.endereco = input("Digite o seu endereço: ")
        self.telefone = input("Digite o seu telefone: ")
        self.cpf = input("Digite o seu cpf: ")
        self.email = input("Digite o seu e-mail: ")

    def MostrarUsuario(self):   #basicamente mostra todas as variáveis criadas com a função acima
        print(f"""
nome: {self.nome}
nascimento: {self.nascimento}
endereço: {self.endereco}
telefone: {self.telefone}
cpf: {self.cpf}
email: {self.email}
""")


tempoRecarga = 0
valorRecarga = 0
valorkWh = 0.805 * 30   # para esse carregador: 30kWh por R$0.805 cada

def CalcularRecarga(tempo, valor):    # verifica se uma das variáveis é 0 para poder atribuir um valor nela de acordo com a outra
    if tempo == 0:
        return valorRecarga / valorkWh
    elif valor == 0:
        return tempoRecarga * valorkWh

def VerificacaoVariavel(texto):    # usei uma função para impedir que valores errados sejam colocados nas variáveis
    try:    # try tenta fazer algo
        valor = float(input(f"\nDigite o {texto} da recarga: "))
    except ValueError:    # ativa quando o try falha e aparece um erro, nesse caso é erro de valor
        return VerificacaoVariavel(texto)    # função recursiva precisa retornar ela mesma, senão quando sair vai ser NoneType
    else:    # else funciona como no if, caso dê certo ele roda
        if valor <= 0:    # impede que valores negativos ou iguais a zero sejam aceitos
            return VerificacaoVariavel(texto)
        else:
            return valor

# --- tipo de usuário com tarifa diferenciada ---
while True:    # mantém o usuário no loop até escolher uma opção válida
    tipoUsuario = input("""
    Tipo de usuário:
    1 - Comum
    2 - Assinante (5% de desconto)  
    """)    #diminui o desconto porque 20% é muita coisa
    if tipoUsuario in ["1", "2"]:    # verifica se a escolha está dentro das opções permitidas
        break
    print("Opção inválida.")

if tipoUsuario == "2":
    print("Para se tornar assinante, é necessário preencher um simples formulário ")
    escolha = input("Deseja continuar? (s/n) ").lower()

    while True:
        if escolha in ["s", "sim"]:
            usuarioTeste = Usuario()    #aqui foi criado uma nova instancia da classe usuário
            usuarioTeste.Formulario()   #e aqui usa a função criada na classe

            print("\n---------------------------------------")
            print("Confirme as informações")
            usuarioTeste.MostrarUsuario()   #mostra as informações usando a função da classe
            confirmacao = input("As informações estão corretas? (s/n) ").lower()

            if confirmacao in ["s", "sim"]:
                valorkWh = valorkWh * 0.95   # aplica desconto de 5% na tarifa para assinantes
                break

            else:
                print("Por favor, repita o preenchimento do formulário\n")

        elif escolha in ["n", "não", "nao"]:
            break

        else:
            print("Valor inválido")

# --- escolha de cobrança ---
while True:    # para evitar erros, o while mantém o programa no loop até que uma das opções seja escolhida
    escolhaCobranca = input("""
    Escolha uma opção (digite o número apenas)
    1 - Recarregar por tempo
    2 - Recarregar por valor
    """)

    match escolhaCobranca:    # o match serve como um if melhorado para a escolha da cobrança de recarga
        case "1":
            tempoRecarga = VerificacaoVariavel("tempo em horas")    # recebe o tempo da recarga e valida o valor
            valorRecarga = CalcularRecarga(tempoRecarga, valorRecarga)    # calcula o valor da recarga com base no tempo
            break    # sai do loop para continuar o código

        case "2":
            valorRecarga = VerificacaoVariavel("valor")    # recebe o valor da recarga e valida o valor
            tempoRecarga = CalcularRecarga(tempoRecarga, valorRecarga)    # calcula o tempo da recarga com base no valor
            break

        case _:
            print("\nValor inválido, tente novamente")

# --- função de recarga com barra de progresso ---
def Recarga(tempo):                         # função para calcular o valor da recarga e mostrar uma barra de carregamento
    barraBase = "----------"                # valor inicial da barra de carregamento

    print("\nRecarregando...")

    i = 0
    divTempo = tempo / 10                   # aqui o tempo foi dividido em 10 partes iguais, para poder aumentar a barra de 10% em 10%
    contadorDiv = 0                         # variável usada para controlar quantas partes da barra já foram preenchidas

    while i < tempo:                        # loop para fazer o carregamento demorar de acordo com o tempo colocado inicialmente
        if i > divTempo * contadorDiv:      # a cada parte do tempo concluída, uma parte da barra é preenchida
            contadorDiv += 1
            barra = barraBase.replace("-", "*", contadorDiv)    # troca "-" por "*" uma certa quantidade de vezes, definida pelo contadorDiv
            print(f"\r[{barra}]", end="")                       # o \r volta para o começo da linha e o end evita pular linha

        time.sleep(0.1)                     # importado da biblioteca time, o sleep faz o código esperar um pouco antes de continuar
        i += 0.1                            # o aumento é menor que o normal para poder contar valores flutuantes

    print("\nRecarregado ^_^")
    print("Agradecemos por escolher os nossos serviços!")

# --- confirmação e relatório ---
while True:    # mantém o usuário no loop até responder corretamente se deseja prosseguir ou não
    escolhaRecarga = input(
        f"""
Valor da recarga: R${valorRecarga:.2f}
Tempo de espera: {tempoRecarga:.2f} horas

Deseja prosseguir com a recarga? (s/n)
        """
    ).lower()    # transforma a resposta em minúscula para aceitar respostas como "S", "Sim", "NÃO", etc.

    if escolhaRecarga in ["s", "sim"]:
        horarioInicio = datetime.datetime.now()   # registra o horário de início da recarga

        Recarga(tempoRecarga)                     # chama a função que simula a recarga

        horarioFim = datetime.datetime.now()      # registra o horário de fim da recarga

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
        """)    # relatório final mostrando os dados principais da sessão de recarga
        break

    elif escolhaRecarga in ["n", "nao", "não"]:
        print("Obrigado por escolher nossos serviços, tenha um ótimo dia")
        quit()    # encerra o programa caso o usuário não queira continuar

    else:
        print("Resposta inválida.")    # caso o usuário digite algo diferente de sim ou não
