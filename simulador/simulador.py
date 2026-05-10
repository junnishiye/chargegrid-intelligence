import time
import datetime
import re

class Usuario:  #cria um classe para poder gerar um formulário de usuário
    nome = ""   #não usei uma função construtora, porque eu queria que fosse contruido pelo input, e não ao instanciar
    nascimento = ""
    endereco = ""
    telefone = ""
    cpf = ""
    email = ""

    def Formulario(self):   #o self é usado para guardar as informações da instância, e não pegar da classe em geral
        self.nome = VerificacaoNome()
        self.nascimento = VerificacaoNascimento()
        self.endereco = VerificacaoTexto("endereço")
        self.telefone = VerificacaoTelefone()
        self.cpf = VerificacaoCPF()
        self.email = VerificacaoEmail()

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
assinanteConfirmado = False    # controla se o usuário realmente concluiu o cadastro de assinante

def LimparDigitos(texto):    # remove tudo que não for número, usado em CPF e telefone
    return re.sub(r"\D", "", texto)

def VerificacaoNome():    # valida se o nome não está vazio e se tem letras
    while True:
        nome = input("Digite o seu nome: ").strip()

        if len(nome) >= 3 and any(letra.isalpha() for letra in nome):
            return nome

        print("Nome inválido. Digite um nome com pelo menos 3 caracteres e letras.")

def VerificacaoTexto(texto):    # valida textos simples, como endereço, impedindo campo vazio
    while True:
        valor = input(f"Digite o seu {texto}: ").strip()

        if valor != "":
            return valor

        print(f"{texto.capitalize()} inválido. Esse campo não pode ficar vazio.")

def VerificacaoNascimento():    # valida a data de nascimento no formato dia/mês/ano
    while True:
        nascimento = input("Digite a sua data de nascimento (dd/mm/aaaa): ").strip()

        try:    # tenta transformar o texto digitado em uma data real
            dataNascimento = datetime.datetime.strptime(nascimento, "%d/%m/%Y").date()
            dataAtual = datetime.date.today()

            if dataNascimento > dataAtual:
                print("Data inválida. A data de nascimento não pode estar no futuro.")
            else:
                return dataNascimento.strftime("%d/%m/%Y")

        except ValueError:    # ativa quando a data não existe ou está em formato errado
            print("Data inválida. Use o formato dd/mm/aaaa. Exemplo: 25/08/2006")

def ValidarCPF(cpf):    # valida CPF usando os dígitos verificadores
    cpf = LimparDigitos(cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:    # impede CPF com tamanho errado ou todos os números iguais
        return False

    soma = 0
    for i in range(9):    # calcula o primeiro dígito verificador
        soma += int(cpf[i]) * (10 - i)

    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    soma = 0
    for i in range(10):    # calcula o segundo dígito verificador
        soma += int(cpf[i]) * (11 - i)

    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return cpf[-2:] == f"{digito1}{digito2}"

def FormatarCPF(cpf):    # deixa o CPF no formato 000.000.000-00
    cpf = LimparDigitos(cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def VerificacaoCPF():    # pede o CPF até ele ser válido
    while True:
        cpf = input("Digite o seu cpf: ").strip()

        if ValidarCPF(cpf):
            return FormatarCPF(cpf)

        print("CPF inválido. Digite um CPF com 11 números válidos.")

def VerificacaoTelefone():    # valida telefone com DDD, aceitando 10 ou 11 números
    while True:
        telefone = input("Digite o seu telefone com DDD: ").strip()
        telefone = LimparDigitos(telefone)

        if len(telefone) == 11:
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

        elif len(telefone) == 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"

        else:
            print("Telefone inválido. Digite com DDD, usando 10 ou 11 números.")

def VerificacaoEmail():    # valida e-mail de forma simples, verificando @ e domínio
    while True:
        email = input("Digite o seu e-mail: ").strip().lower()

        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            return email

        print("E-mail inválido. Exemplo válido: nome@email.com")

def CalcularRecarga(tempo, valor):    # verifica se uma das variáveis é 0 para poder atribuir um valor nela de acordo com a outra
    if tempo == 0:
        return valor / valorkWh
    elif valor == 0:
        return tempo * valorkWh
    else:
        return 0

def VerificacaoVariavel(texto):    # usei uma função para impedir que valores errados sejam colocados nas variáveis
    while True:
        try:    # try tenta fazer algo
            valor = float(input(f"\nDigite o {texto} da recarga: ").replace(",", "."))
        except ValueError:    # ativa quando o try falha e aparece um erro, nesse caso é erro de valor
            print("Valor inválido. Digite apenas números.")
        else:    # else funciona como no if, caso dê certo ele roda
            if valor <= 0:    # impede que valores negativos ou iguais a zero sejam aceitos
                print("Valor inválido. Digite um número maior que zero.")
            else:
                return valor

# --- tipo de usuário com tarifa diferenciada ---
while True:    # mantém o usuário no loop até escolher uma opção válida
    tipoUsuario = input("""
    Tipo de usuário:
    1 - Comum
    2 - Assinante (5% de desconto)  
    """).strip()    #diminui o desconto porque 20% é muita coisa

    if tipoUsuario in ["1", "2"]:    # verifica se a escolha está dentro das opções permitidas
        break

    print("Opção inválida.")

if tipoUsuario == "2":
    print("Para se tornar assinante, é necessário preencher um simples formulário ")

    while True:
        escolha = input("Deseja continuar? (s/n) ").lower().strip()

        if escolha in ["s", "sim"]:
            usuarioTeste = Usuario()    #aqui foi criado uma nova instancia da classe usuário
            usuarioTeste.Formulario()   #e aqui usa a função criada na classe

            print("\n---------------------------------------")
            print("Confirme as informações")
            usuarioTeste.MostrarUsuario()   #mostra as informações usando a função da classe

            while True:
                confirmacao = input("As informações estão corretas? (s/n) ").lower().strip()

                if confirmacao in ["s", "sim"]:
                    valorkWh = valorkWh * 0.95   # aplica desconto de 5% na tarifa para assinantes
                    assinanteConfirmado = True    # confirma que o usuário realmente virou assinante
                    break

                elif confirmacao in ["n", "não", "nao"]:
                    print("Por favor, repita o preenchimento do formulário\n")
                    break

                else:
                    print("Resposta inválida. Digite s para sim ou n para não.")

            if assinanteConfirmado:
                break

        elif escolha in ["n", "não", "nao"]:
            tipoUsuario = "1"    # se o usuário desistir do cadastro, ele volta a ser usuário comum
            print("Cadastro recusado. Você continuará como usuário comum.")
            break

        else:
            print("Valor inválido")

# --- escolha de cobrança ---
while True:    # para evitar erros, o while mantém o programa no loop até que uma das opções seja escolhida
    escolhaCobranca = input("""
    Escolha uma opção (digite o número apenas)
    1 - Recarregar por tempo
    2 - Recarregar por valor
    """).strip()

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

    for contadorDiv in range(1, 11):        # a barra vai preencher 10 partes, de 10% em 10%
        time.sleep(0.1)                     # importado da biblioteca time, o sleep faz o código esperar um pouco antes de continuar
        barra = barraBase.replace("-", "*", contadorDiv)    # troca "-" por "*" uma certa quantidade de vezes, definida pelo contadorDiv
        print(f"\r[{barra}]", end="")                       # o \r volta para o começo da linha e o end evita pular linha

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
    ).lower().strip()    # transforma a resposta em minúscula para aceitar respostas como "S", "Sim", "NÃO", etc.

    if escolhaRecarga in ["s", "sim"]:
        horarioInicio = datetime.datetime.now()   # registra o horário de início da recarga

        Recarga(tempoRecarga)                     # chama a função que simula a recarga

        horarioFim = datetime.datetime.now()      # registra o horário de fim da recarga

        print(f"""
╔══════════════════════════════════╗
       RELATÓRIO DA SESSÃO
╠══════════════════════════════════╣
  Tipo de usuário : {"Assinante" if assinanteConfirmado else "Comum"}
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
        break    # encerra o programa caso o usuário não queira continuar

    else:
        print("Resposta inválida.")    # caso o usuário digite algo diferente de sim ou não
