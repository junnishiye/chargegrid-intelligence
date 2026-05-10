# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import time
import threading
import re

# ─── constantes ───────────────────────────────────────────────────────────────
TARIFA_BASE = 0.805 * 30   # para esse carregador: 30kWh por R$0.805 cada
DESCONTO_ASSINANTE = 0.05  # diminui o desconto porque 20% é muita coisa

COR_FUNDO      = "#0d1117"
COR_PAINEL     = "#161b22"
COR_BORDA      = "#30363d"
COR_VERDE      = "#00ff88"
COR_VERDE_ESC  = "#00cc6a"
COR_TEXTO      = "#e6edf3"
COR_TEXTO_DIM  = "#8b949e"
COR_ERRO       = "#ff6b6b"
FONTE_TITULO   = ("Courier New", 22, "bold")
FONTE_LABEL    = ("Courier New", 11)
FONTE_VALOR    = ("Courier New", 13, "bold")
FONTE_RELATORIO= ("Courier New", 10)

class Usuario:  #cria um classe para poder gerar um formulário de usuário
    nome = ""   #mantive a ideia da classe de usuário, só que agora os valores vêm da interface
    nascimento = ""
    endereco = ""
    telefone = ""
    cpf = ""
    email = ""

    def MostrarUsuario(self):   #basicamente mostra todas as variáveis criadas com a função acima
        return f"""
nome: {self.nome}
nascimento: {self.nascimento}
endereço: {self.endereco}
telefone: {self.telefone}
cpf: {self.cpf}
email: {self.email}
"""

# ─── funções de validação ─────────────────────────────────────────────────────
def LimparDigitos(texto):    # remove tudo que não for número, usado em CPF e telefone
    return re.sub(r"\D", "", texto)

def VerificarNome(nome):    # valida se o nome não está vazio e se tem letras
    nome = nome.strip()

    if len(nome) >= 3 and any(letra.isalpha() for letra in nome):
        return True, nome

    return False, "Nome inválido. Digite um nome com pelo menos 3 caracteres e letras."

def VerificarTexto(valor, texto):    # valida textos simples, como endereço, impedindo campo vazio
    valor = valor.strip()

    if valor != "":
        return True, valor

    return False, f"{texto.capitalize()} inválido. Esse campo não pode ficar vazio."

def VerificarNascimento(nascimento):    # valida a data de nascimento no formato dia/mês/ano
    nascimento = nascimento.strip()

    try:    # tenta transformar o texto digitado em uma data real
        dataNascimento = datetime.datetime.strptime(nascimento, "%d/%m/%Y").date()
        dataAtual = datetime.date.today()

        if dataNascimento > dataAtual:
            return False, "Data inválida. A data de nascimento não pode estar no futuro."

        return True, dataNascimento.strftime("%d/%m/%Y")

    except ValueError:    # ativa quando a data não existe ou está em formato errado
        return False, "Data inválida. Use o formato dd/mm/aaaa. Exemplo: 25/08/2006"

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

def VerificarCPF(cpf):    # verifica se o CPF é válido e retorna ele formatado
    if ValidarCPF(cpf):
        return True, FormatarCPF(cpf)

    return False, "CPF inválido. Digite um CPF com 11 números válidos."

def VerificarTelefone(telefone):    # valida telefone com DDD, aceitando 10 ou 11 números
    telefone = LimparDigitos(telefone)

    if len(telefone) == 11:
        return True, f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

    elif len(telefone) == 10:
        return True, f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"

    else:
        return False, "Telefone inválido. Digite com DDD, usando 10 ou 11 números."

def VerificarEmail(email):    # valida e-mail de forma simples, verificando @ e domínio
    email = email.strip().lower()

    if re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
        return True, email

    return False, "E-mail inválido. Exemplo válido: nome@email.com"

def VerificarNumero(texto):    # usei uma função para impedir que valores errados sejam colocados na recarga
    try:    # try tenta fazer algo
        valor = float(texto.strip().replace(",", "."))
    except ValueError:    # ativa quando o try falha e aparece um erro, nesse caso é erro de valor
        return False, "Digite apenas números."

    if valor <= 0:    # impede que valores negativos ou iguais a zero sejam aceitos
        return False, "Digite um número maior que zero."

    return True, valor

# ─── lógica de cálculo ────────────────────────────────────────────────────────
def CalcularTarifa(assinanteConfirmado):    # calcula a tarifa final de acordo com o tipo de usuário
    valorkWh = TARIFA_BASE

    if assinanteConfirmado:
        valorkWh = valorkWh * (1 - DESCONTO_ASSINANTE)   # aplica desconto de 5% na tarifa para assinantes

    return valorkWh

def CalcularRecarga(tempo, valor, valorkWh):    # verifica se uma das variáveis é 0 para poder atribuir um valor nela de acordo com a outra
    if tempo == 0:
        return valor / valorkWh
    elif valor == 0:
        return tempo * valorkWh
    else:
        return 0

# ─── janela principal ─────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de Recarga")
        self.configure(bg=COR_FUNDO)
        self.resizable(True, True)     # permite aumentar e diminuir a janela principal
        self.minsize(520, 620)          # define um tamanho mínimo para a interface não quebrar

        self.assinanteConfirmado = False    # controla se o usuário realmente concluiu o cadastro de assinante
        self.usuarioTeste = None            # guarda os dados do assinante quando o cadastro for confirmado

        self._centralizar(560, 720)
        self._construir_ui()

    def _centralizar(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _construir_ui(self):
        # título
        tk.Label(self, text="⚡ RECARGA EV", font=FONTE_TITULO,
                 bg=COR_FUNDO, fg=COR_VERDE).pack(pady=(28, 4))
        tk.Label(self, text="Simulador de Sessão de Recarga",
                 font=("Courier New", 10), bg=COR_FUNDO,
                 fg=COR_TEXTO_DIM).pack(pady=(0, 20))

        painel = tk.Frame(self, bg=COR_PAINEL,
                          highlightbackground=COR_BORDA,
                          highlightthickness=1)
        painel.pack(padx=32, fill="x")

        # ── tipo de usuário ──
        self._secao(painel, "TIPO DE USUÁRIO")
        self.var_tipo = tk.StringVar(value="1")
        for val, txt in [("1", "Comum"), ("2", "Assinante  (5% de desconto)")]:
            tk.Radiobutton(painel, text=txt, variable=self.var_tipo, value=val,
                           font=FONTE_LABEL, bg=COR_PAINEL, fg=COR_TEXTO,
                           selectcolor=COR_FUNDO, activebackground=COR_PAINEL,
                           activeforeground=COR_VERDE).pack(anchor="w", padx=20, pady=2)

        tk.Label(painel, text="Se escolher assinante, será necessário preencher o formulário antes da recarga.",
                 font=("Courier New", 8), bg=COR_PAINEL,
                 fg=COR_TEXTO_DIM, wraplength=480, justify="left").pack(anchor="w", padx=20, pady=(3, 0))

        self._divisor(painel)

        # ── modo de cobrança ──
        self._secao(painel, "MODO DE COBRANÇA")
        self.var_modo = tk.StringVar(value="1")
        for val, txt in [("1", "Por tempo (horas)"), ("2", "Por valor (R$)")]:
            tk.Radiobutton(painel, text=txt, variable=self.var_modo, value=val,
                           font=FONTE_LABEL, bg=COR_PAINEL, fg=COR_TEXTO,
                           selectcolor=COR_FUNDO, activebackground=COR_PAINEL,
                           activeforeground=COR_VERDE,
                           command=self._atualizar_label_entrada).pack(anchor="w", padx=20, pady=2)

        self._divisor(painel)

        # ── entrada ──
        self._secao(painel, "DADOS DA RECARGA")
        frame_entrada = tk.Frame(painel, bg=COR_PAINEL)
        frame_entrada.pack(padx=20, pady=(4, 16), fill="x")

        self.label_entrada = tk.Label(frame_entrada, text="Tempo (horas):",
                                      font=FONTE_LABEL, bg=COR_PAINEL, fg=COR_TEXTO_DIM)
        self.label_entrada.pack(anchor="w")

        self.entry = tk.Entry(frame_entrada, font=FONTE_VALOR,
                              bg=COR_FUNDO, fg=COR_VERDE,
                              insertbackground=COR_VERDE,
                              relief="flat", bd=0,
                              highlightbackground=COR_BORDA,
                              highlightthickness=1)
        self.entry.pack(fill="x", ipady=8, pady=(4, 0))

        self.label_erro = tk.Label(frame_entrada, text="",
                                   font=("Courier New", 9),
                                   bg=COR_PAINEL, fg=COR_ERRO)
        self.label_erro.pack(anchor="w")

        # ── botão ──
        self.btn = tk.Button(self, text="INICIAR RECARGA",
                             font=("Courier New", 12, "bold"),
                             bg=COR_VERDE, fg=COR_FUNDO,
                             activebackground=COR_VERDE_ESC,
                             activeforeground=COR_FUNDO,
                             relief="flat", cursor="hand2",
                             command=self._iniciar)
        self.btn.pack(padx=32, pady=20, fill="x", ipady=10)

        # ── barra de progresso ──
        self.label_status = tk.Label(self, text="",
                                     font=("Courier New", 10),
                                     bg=COR_FUNDO, fg=COR_TEXTO_DIM)
        self.label_status.pack()

        self.progress = ttk.Progressbar(self, mode="determinate")    # sem tamanho fixo para acompanhar a largura da janela
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                        troughcolor=COR_PAINEL,
                        background=COR_VERDE,
                        bordercolor=COR_BORDA)
        self.progress.configure(style="green.Horizontal.TProgressbar")
        self.progress.pack(padx=32, pady=(4, 0), fill="x")    # a barra aumenta ou diminui junto com a janela

        # ── relatório ──
        self.frame_relatorio = tk.Frame(self, bg=COR_FUNDO)
        self.frame_relatorio.pack(padx=32, pady=16, fill="both", expand=True)    # o relatório acompanha o redimensionamento da janela

    # ── helpers de layout ──────────────────────────────────────────────────────
    def _secao(self, pai, titulo):
        tk.Label(pai, text=titulo, font=("Courier New", 9, "bold"),
                 bg=COR_PAINEL, fg=COR_VERDE).pack(anchor="w", padx=20, pady=(14, 2))

    def _divisor(self, pai):
        tk.Frame(pai, bg=COR_BORDA, height=1).pack(fill="x", padx=12, pady=4)

    def _atualizar_label_entrada(self):
        if self.var_modo.get() == "1":
            self.label_entrada.config(text="Tempo (horas):")
        else:
            self.label_entrada.config(text="Valor (R$):")
        self.entry.delete(0, tk.END)
        self.label_erro.config(text="")

    def _criar_campo(self, pai, texto):
        tk.Label(pai, text=texto, font=FONTE_LABEL,
                 bg=COR_PAINEL, fg=COR_TEXTO_DIM).pack(anchor="w", padx=20, pady=(8, 0))

        entrada = tk.Entry(pai, font=FONTE_LABEL,
                           bg=COR_FUNDO, fg=COR_VERDE,
                           insertbackground=COR_VERDE,
                           relief="flat", bd=0,
                           highlightbackground=COR_BORDA,
                           highlightthickness=1)
        entrada.pack(fill="x", padx=20, ipady=6, pady=(3, 0))

        return entrada

    # ── formulário de assinante ────────────────────────────────────────────────
    def _abrir_formulario_assinante(self):
        resultado = {"confirmado": False, "usuario": None}

        janela = tk.Toplevel(self)
        janela.title("Cadastro de Assinante")
        janela.configure(bg=COR_FUNDO)
        janela.resizable(True, True)     # permite redimensionar também a janela de cadastro
        janela.minsize(420, 560)          # tamanho mínimo para o formulário continuar legível
        janela.transient(self)
        janela.grab_set()

        largura = 460
        altura = 610
        x = self.winfo_x() + (self.winfo_width() - largura) // 2
        y = self.winfo_y() + 40
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

        tk.Label(janela, text="CADASTRO DE ASSINANTE",
                 font=("Courier New", 16, "bold"),
                 bg=COR_FUNDO, fg=COR_VERDE).pack(pady=(18, 4))

        tk.Label(janela, text="Preencha os dados para receber o desconto de 5%.",
                 font=("Courier New", 9),
                 bg=COR_FUNDO, fg=COR_TEXTO_DIM).pack(pady=(0, 12))

        painel = tk.Frame(janela, bg=COR_PAINEL,
                          highlightbackground=COR_BORDA,
                          highlightthickness=1)
        painel.pack(padx=24, fill="x")

        campo_nome = self._criar_campo(painel, "Nome:")
        campo_nascimento = self._criar_campo(painel, "Data de nascimento (dd/mm/aaaa):")
        campo_endereco = self._criar_campo(painel, "Endereço:")
        campo_telefone = self._criar_campo(painel, "Telefone com DDD:")
        campo_cpf = self._criar_campo(painel, "CPF:")
        campo_email = self._criar_campo(painel, "E-mail:")

        label_erro_formulario = tk.Label(painel, text="",
                                         font=("Courier New", 9),
                                         bg=COR_PAINEL, fg=COR_ERRO,
                                         wraplength=390, justify="left")
        label_erro_formulario.pack(anchor="w", padx=20, pady=(10, 12))

        def confirmar_formulario():
            usuarioTeste = Usuario()    #aqui foi criado uma nova instancia da classe usuário

            valido, resposta = VerificarNome(campo_nome.get())
            if not valido:
                label_erro_formulario.config(text=resposta)
                campo_nome.focus_set()
                return
            usuarioTeste.nome = resposta

            valido, resposta = VerificarNascimento(campo_nascimento.get())
            if not valido:
                label_erro_formulario.config(text=resposta)
                campo_nascimento.focus_set()
                return
            usuarioTeste.nascimento = resposta

            valido, resposta = VerificarTexto(campo_endereco.get(), "endereço")
            if not valido:
                label_erro_formulario.config(text=resposta)
                campo_endereco.focus_set()
                return
            usuarioTeste.endereco = resposta

            valido, resposta = VerificarTelefone(campo_telefone.get())
            if not valido:
                label_erro_formulario.config(text=resposta)
                campo_telefone.focus_set()
                return
            usuarioTeste.telefone = resposta

            valido, resposta = VerificarCPF(campo_cpf.get())
            if not valido:
                label_erro_formulario.config(text=resposta)
                campo_cpf.focus_set()
                return
            usuarioTeste.cpf = resposta

            valido, resposta = VerificarEmail(campo_email.get())
            if not valido:
                label_erro_formulario.config(text=resposta)
                campo_email.focus_set()
                return
            usuarioTeste.email = resposta

            # mostra as informações usando a função da classe
            confirmar = messagebox.askyesno(
                "Confirme as informações",
                f"As informações estão corretas?\n{usuarioTeste.MostrarUsuario()}",
                parent=janela
            )

            if confirmar:
                resultado["confirmado"] = True
                resultado["usuario"] = usuarioTeste
                janela.destroy()
            else:
                label_erro_formulario.config(text="Confira os campos e corrija as informações necessárias.")

        def recusar_formulario():
            resultado["confirmado"] = False
            resultado["usuario"] = None
            janela.destroy()

        frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
        frame_botoes.pack(padx=24, pady=16, fill="x")

        tk.Button(frame_botoes, text="RECUSAR / CONTINUAR COMO COMUM",
                  font=("Courier New", 9, "bold"),
                  bg=COR_BORDA, fg=COR_TEXTO,
                  activebackground=COR_PAINEL,
                  activeforeground=COR_TEXTO,
                  relief="flat", cursor="hand2",
                  command=recusar_formulario).pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 6))

        tk.Button(frame_botoes, text="CONFIRMAR ASSINANTE",
                  font=("Courier New", 9, "bold"),
                  bg=COR_VERDE, fg=COR_FUNDO,
                  activebackground=COR_VERDE_ESC,
                  activeforeground=COR_FUNDO,
                  relief="flat", cursor="hand2",
                  command=confirmar_formulario).pack(side="left", expand=True, fill="x", ipady=8, padx=(6, 0))

        campo_nome.focus_set()
        janela.wait_window()

        return resultado["confirmado"], resultado["usuario"]

    # ── validação e início ─────────────────────────────────────────────────────
    def _iniciar(self):
        valido, resposta = VerificarNumero(self.entry.get())

        if not valido:
            self.label_erro.config(text=f"⚠ {resposta}")
            return

        valor_entrada = resposta
        self.label_erro.config(text="")

        # se o usuário escolher assinante, o formulário precisa ser confirmado antes de aplicar o desconto
        if self.var_tipo.get() == "2":
            confirmado, usuario = self._abrir_formulario_assinante()

            if confirmado:
                self.assinanteConfirmado = True    # confirma que o usuário realmente virou assinante
                self.usuarioTeste = usuario
            else:
                self.assinanteConfirmado = False
                self.usuarioTeste = None
                self.var_tipo.set("1")    # se o usuário desistir do cadastro, ele volta a ser usuário comum
                messagebox.showinfo("Cadastro recusado", "Cadastro recusado. Você continuará como usuário comum.")

        else:
            self.assinanteConfirmado = False
            self.usuarioTeste = None

        valorkWh = CalcularTarifa(self.assinanteConfirmado)

        if self.var_modo.get() == "1":
            tempoRecarga = valor_entrada
            valorRecarga = CalcularRecarga(tempoRecarga, 0, valorkWh)    # calcula o valor da recarga com base no tempo
        else:
            valorRecarga = valor_entrada
            tempoRecarga = CalcularRecarga(0, valorRecarga, valorkWh)    # calcula o tempo da recarga com base no valor

        escolhaRecarga = messagebox.askyesno(
            "Confirmar recarga",
            f"Valor da recarga: R${valorRecarga:.2f}\n"
            f"Tempo de espera: {tempoRecarga:.2f} horas\n\n"
            "Deseja prosseguir com a recarga?"
        )

        if not escolhaRecarga:
            messagebox.showinfo("Recarga cancelada", "Obrigado por escolher nossos serviços, tenha um ótimo dia.")
            return

        self.btn.config(state="disabled")
        threading.Thread(target=self._simular_recarga,
                         args=(tempoRecarga, valorRecarga), daemon=True).start()

    # ── simulação com barra ────────────────────────────────────────────────────
    def _simular_recarga(self, tempoRecarga, valorRecarga):
        horarioInicio = datetime.datetime.now()   # registra o horário de início da recarga

        passos = 100
        intervalo = (tempoRecarga * 3600) / passos   # tempo real em segundos por passo
        intervalo = min(intervalo, 0.05)              # limita a simulação para não demorar horas de verdade

        for i in range(passos + 1):
            self.after(0, self._atualizar_barra, i)
            time.sleep(intervalo)                     # importado da biblioteca time, o sleep faz o código esperar um pouco antes de continuar

        horarioFim = datetime.datetime.now()      # registra o horário de fim da recarga

        self.after(0, self._mostrar_relatorio,
                   tempoRecarga, valorRecarga, horarioInicio, horarioFim)

    def _atualizar_barra(self, porcentagem):
        self.progress["value"] = porcentagem
        self.label_status.config(text=f"Recarregando... {porcentagem}%")

    # ── relatório final ────────────────────────────────────────────────────────
    def _mostrar_relatorio(self, tempoRecarga, valorRecarga, horarioInicio, horarioFim):
        self.label_status.config(text="Recarregado ✓")
        self.progress["value"] = 100

        energiaConsumida = tempoRecarga * 30
        tipoUsuario = "Assinante (5% de desconto)" if self.assinanteConfirmado else "Comum"

        # limpa relatório anterior
        for widget in self.frame_relatorio.winfo_children():
            widget.destroy()

        linhas = [
            ("─" * 50, COR_BORDA),
            ("  RELATÓRIO DA SESSÃO", COR_VERDE),
            ("─" * 50, COR_BORDA),
            (f"  Tipo de usuário   : {tipoUsuario}", COR_TEXTO),
            (f"  Início            : {horarioInicio.strftime('%H:%M:%S')}", COR_TEXTO),
            (f"  Fim               : {horarioFim.strftime('%H:%M:%S')}", COR_TEXTO),
            (f"  Tempo de recarga  : {tempoRecarga:.2f} horas", COR_TEXTO),
            (f"  Energia consumida : {energiaConsumida:.2f} kWh", COR_TEXTO),
            (f"  Custo total       : R$ {valorRecarga:.2f}", COR_VERDE),
            ("─" * 50, COR_BORDA),
        ]

        if self.assinanteConfirmado and self.usuarioTeste is not None:
            linhas.insert(4, (f"  Assinante         : {self.usuarioTeste.nome}", COR_TEXTO))

        for texto, cor in linhas:
            tk.Label(self.frame_relatorio, text=texto,
                     font=FONTE_RELATORIO, bg=COR_FUNDO, fg=cor,
                     anchor="w").pack(fill="x")

        self.btn.config(state="normal", text="NOVA RECARGA",
                        command=self._nova_recarga)

    def _nova_recarga(self):
        self.entry.delete(0, tk.END)
        self.progress["value"] = 0
        self.label_status.config(text="")
        self.label_erro.config(text="")
        self.assinanteConfirmado = False
        self.usuarioTeste = None
        self.var_tipo.set("1")

        for widget in self.frame_relatorio.winfo_children():
            widget.destroy()

        self.btn.config(text="INICIAR RECARGA", command=self._iniciar)

# ─── entrada ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
