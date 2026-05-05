# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import time
import threading

# ─── constantes ───────────────────────────────────────────────────────────────
TARIFA_BASE = 0.805 * 30   # R$ por hora (30 kWh * R$0.805)
DESCONTO_ASSINANTE = 0.20

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

# ─── lógica de cálculo ────────────────────────────────────────────────────────
def calcular_tarifa(tipo_usuario):
    tarifa = TARIFA_BASE
    if tipo_usuario == "2":
        tarifa *= (1 - DESCONTO_ASSINANTE)
    return tarifa

def calcular_por_tempo(tempo, tarifa):
    return tempo * tarifa

def calcular_por_valor(valor, tarifa):
    return valor / tarifa

# ─── janela principal ─────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Recarga")
        self.configure(bg=COR_FUNDO)
        self.resizable(False, True)
        self._centralizar(520, 780)
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
        for val, txt in [("1", "Comum"), ("2", "Assinante  (20% de desconto)")]:
            tk.Radiobutton(painel, text=txt, variable=self.var_tipo, value=val,
                           font=FONTE_LABEL, bg=COR_PAINEL, fg=COR_TEXTO,
                           selectcolor=COR_FUNDO, activebackground=COR_PAINEL,
                           activeforeground=COR_VERDE).pack(anchor="w", padx=20, pady=2)

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

        self.progress = ttk.Progressbar(self, length=456, mode="determinate")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                        troughcolor=COR_PAINEL,
                        background=COR_VERDE,
                        bordercolor=COR_BORDA)
        self.progress.configure(style="green.Horizontal.TProgressbar")
        self.progress.pack(padx=32, pady=(4, 0))

        # ── relatório ──
        self.frame_relatorio = tk.Frame(self, bg=COR_FUNDO)
        self.frame_relatorio.pack(padx=32, pady=16, fill="x")

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

    # ── validação e início ─────────────────────────────────────────────────────
    def _iniciar(self):
        texto = self.entry.get().strip().replace(",", ".")
        try:
            valor_entrada = float(texto)
            if valor_entrada <= 0:
                raise ValueError
        except ValueError:
            self.label_erro.config(text="⚠ Digite um número válido maior que zero.")
            return

        self.label_erro.config(text="")
        tarifa = calcular_tarifa(self.var_tipo.get())

        if self.var_modo.get() == "1":
            tempo  = valor_entrada
            valor  = calcular_por_tempo(tempo, tarifa)
        else:
            valor  = valor_entrada
            tempo  = calcular_por_valor(valor, tarifa)

        self.btn.config(state="disabled")
        threading.Thread(target=self._simular_recarga,
                         args=(tempo, valor), daemon=True).start()

    # ── simulação com barra ────────────────────────────────────────────────────
    def _simular_recarga(self, tempo, valor):
        horario_inicio = datetime.datetime.now()
        passos = 100
        intervalo = (tempo * 3600) / passos   # tempo real em segundos por passo
        intervalo = min(intervalo, 0.05)       # limita a 5s total na simulação

        for i in range(passos + 1):
            pct = i
            self.after(0, self._atualizar_barra, pct, i, passos)
            time.sleep(intervalo)

        horario_fim = datetime.datetime.now()
        self.after(0, self._mostrar_relatorio,
                   tempo, valor, horario_inicio, horario_fim)

    def _atualizar_barra(self, pct, i, total):
        self.progress["value"] = pct
        self.label_status.config(text=f"Recarregando... {pct}%")

    # ── relatório final ────────────────────────────────────────────────────────
    def _mostrar_relatorio(self, tempo, valor, inicio, fim):
        self.label_status.config(text="Recarregado ✓")
        self.progress["value"] = 100

        tipo_txt = "Assinante (–20%)" if self.var_tipo.get() == "2" else "Comum"
        energia  = tempo * 30

        # limpa relatório anterior
        for w in self.frame_relatorio.winfo_children():
            w.destroy()

        linhas = [
            ("─" * 46, COR_BORDA),
            ("  RELATÓRIO DA SESSÃO", COR_VERDE),
            ("─" * 46, COR_BORDA),
            (f"  Tipo de usuário  : {tipo_txt}", COR_TEXTO),
            (f"  Início           : {inicio.strftime('%H:%M:%S')}", COR_TEXTO),
            (f"  Fim              : {fim.strftime('%H:%M:%S')}", COR_TEXTO),
            (f"  Tempo de recarga : {tempo:.2f} h", COR_TEXTO),
            (f"  Energia consumida: {energia:.2f} kWh", COR_TEXTO),
            (f"  Custo total      : R$ {valor:.2f}", COR_VERDE),
            ("─" * 46, COR_BORDA),
        ]

        for txt, cor in linhas:
            tk.Label(self.frame_relatorio, text=txt,
                     font=FONTE_RELATORIO, bg=COR_FUNDO, fg=cor,
                     anchor="w").pack(fill="x")

        self.btn.config(state="normal", text="NOVA RECARGA",
                        command=self._nova_recarga)

    def _nova_recarga(self):
        self.entry.delete(0, tk.END)
        self.progress["value"] = 0
        self.label_status.config(text="")
        for w in self.frame_relatorio.winfo_children():
            w.destroy()
        self.btn.config(text="INICIAR RECARGA", command=self._iniciar)

# ─── entrada ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
