# Eletropostos Eficientes

Projeto desenvolvido para a Sprint 1 do EV Challenge 2026.

O objetivo do projeto é mostrar como a utilização de Assembly e arquitetura RISC-V pode ajudar a reduzir o consumo computacional em eletropostos, tornando o sistema mais eficiente e sustentável.

---

## Integrantes

- André Felix – RM 571691
- Davi Pacheco – RM 569487
- Gabriel Silveira – RM 568910
- Henrique Aragão – RM 570529
- João Vitor Jun – RM 572079

---

## Problema

Atualmente muitos eletropostos utilizam softwares desenvolvidos em linguagens de alto nível e executados em hardwares genéricos. Isso pode gerar:

- Maior uso da CPU
- Mais consumo energético
- Processamento menos eficiente
- Desperdício de recursos computacionais

Operações simples como leitura de sensores, autenticação e controle de carga acabam utilizando mais processamento do que o necessário.

---

## Proposta da Solução

A proposta do projeto foi desenvolver um sistema de controle de carga utilizando Assembly RISC-V.

O foco da solução é reduzir a quantidade de instruções executadas pelo processador, diminuindo ciclos de CPU e consumo energético.

O sistema simula:

- Leitura de tensão
- Controle de carga
- Processamento otimizado
- Tomada de decisão em baixo nível

---

## Arquitetura Utilizada

Foi utilizada a arquitetura RISC-V por possuir:

- Conjunto reduzido de instruções
- Melhor eficiência energética
- Simplicidade de execução
- Melhor desempenho em sistemas embarcados

Também foram aplicados conceitos de:

- RISC vs CISC
- Pipeline
- Clock cycles
- Eficiência computacional

---

## Sustentabilidade

A relação do projeto com sustentabilidade está na otimização do processamento.

Com menos instruções sendo executadas:

- O processador consome menos energia
- O hardware trabalha de forma mais eficiente
- Há menor desperdício computacional
- Sistemas embarcados podem ser utilizados com menor consumo

Isso contribui diretamente para eletropostos mais eficientes e sustentáveis.

---

## Comparação Conceitual

| Sistema | Ciclos de CPU | Consumo Energético |
|---|---|---|
| Código em C | 200 | 100% |
| Código em Assembly | 120 | 60% |

Os valores apresentados são conceituais e foram utilizados apenas para demonstrar a diferença de eficiência entre soluções de alto nível e baixo nível.

---

## Código Utilizado

Trecho do código desenvolvido em RISC-V Assembly:

```assembly
loop:
        lw t3, 0(t0)
        lw t4, LIMITE

        blt t3, t4, LIGAR
        j DESLIGAR

LIGAR:
        li t5, 1
        la t6, CHARGE
        sw t5, 0(t6)

DESLIGAR:
        li t5, 0
        la t6, CHARGE
        sw t5, 0(t6)
```

O código realiza a leitura de tensão e decide automaticamente se a carga deve ser ligada ou desligada.

---

## Tecnologias Utilizadas

- Assembly RISC-V
- Simuladores de arquitetura
- Sistemas embarcados
- GitHub
- PowerPoint

---

## Simulador Utilizado

[Simulador de Risc-V usado](https://riscv-simulator-five.vercel.app/)

---

## Vídeo Pitch

O projeto possui um vídeo pitch apresentando:

- O problema identificado
- A proposta da solução
- Explicação dos slides
- Funcionamento do código
- Relação entre arquitetura e sustentabilidade

Link do vídeo:

https://www.youtube.com/watch?v=DgBtgoWw5fs

---

## Estrutura do Repositório

```bash
projeto-eletropostos-eficientes
│
├── README.md
├── Código Sprint 1 - Eletropostos.txt
├── Eletropostos Eficientes Slides.pptx
```

---

## Impactos Esperados

- Redução do consumo computacional
- Maior eficiência energética
- Melhor aproveitamento do hardware
- Menor desperdício de energia
- Sistemas embarcados mais eficientes

---

## Conclusão

O projeto demonstra como a programação em baixo nível pode contribuir para soluções mais eficientes em eletropostos.

A utilização de Assembly e arquitetura RISC-V permite reduzir processamento desnecessário e melhorar a eficiência energética do sistema, contribuindo para uma solução mais sustentável.