from collections import Counter
import pandas as pd

tabela = pd.read_csv("./ev_charging_patterns.csv")

#Custo da recarga
custoRecarga = tabela[["Charging Cost (USD)"]]

menor10 = 0
menor25 = 0
menor50 = 0
menor100 = 0
maior100 = 0

for valor in custoRecarga.values:
    if valor < 10:
        menor10 += 1
    elif valor < 25:
        menor25 += 1
    elif valor < 50:
        menor50 += 1
    elif valor < 100:
        menor100 += 1
    else:
        maior100 += 1

dadosCusto = ["<10 Dólares"]*menor10 + ["<25 Dólares"]*menor25 + ["<50 Dólares"]*menor50 + ["<100 Dólares"]*menor100 + [">100 Dólares"]*maior100

fiCusto = pd.Series(Counter(dadosCusto))
fiCusto.sort_index()

fiaCusto = fiCusto.cumsum()

frCusto = 100 * fiCusto / fiCusto.sum()

fraCusto = frCusto.cumsum()

tabelaCusto = pd.DataFrame({
    "Frequência Absoluta": fiCusto,
    "Frequência Absoluta Acumulada": fiaCusto,
    "Frequência Relativa": frCusto,
    "Frequência Relativa Acumulada": fraCusto
})

tabelaCusto.loc["Total"] = [
    fiCusto.sum(),
    "-",
    fraCusto.sum(),
    "-"
]

print (tabelaCusto)
#De acordo com a tabela frequência do custo de recarga:
#As pessoas não ultrapassam 50 dólares.
#Grande parte das pessoas recarregam mais que 10 dólares.


#Duração de carga
duracaoRecarga = tabela[["Charging Duration (hours)"]]

menor1 = 0
menor2 = 0
menor3 = 0
menor4 = 0
menor5 = 0
maior5 = 0

for tempo in duracaoRecarga.values:
    if tempo < 1:
        menor1 += 1
    elif tempo < 2:
        menor2 += 1
    elif tempo < 3:
        menor3 += 1
    elif tempo < 4:
        menor4 += 1
    elif tempo < 5:
        menor5 += 1
    else:
        maior5 += 1

dadosTempo = ["<1 Hora"]*menor1 + ["<2 Horas"]*menor2 + ["<3 Horas"]*menor3 + ["<4 Horas"]*menor4 + ["<5 Horas"]*menor5 + [">5 Horas"]*maior5

fiTempo = pd.Series(Counter(dadosTempo))
fiTempo.sort_index()

fiaTempo = fiTempo.cumsum()

frTempo = 100 * fiTempo / fiTempo.sum()

fraTempo = frTempo.cumsum()

tabelaTempo = pd.DataFrame({
    "Frequência Absoluta": fiTempo,
    "Frequência Absoluta Acumulada": fiaTempo,
    "Frequência Relativa": frTempo,
    "Frequência Relativa Acumulada": fraTempo
})

tabelaTempo.loc["Total"] = [
    fiTempo.sum(),
    "-",
    frTempo.sum(),
    "-"
]

print (tabelaTempo)
#De acordo com a tabela frequência do tempo de recarga:
#O tempo máximo de permanência é de 4 horas.
#Entre 1 a 4 horas a permanência é bem distríbuida, com uma pequena parte recarregando por menos de uma hora.