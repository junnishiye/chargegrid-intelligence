# Tabela Verdade — Circuito de Autorização de Sessão de Recarga 
**Disciplina:** Computer Science  
**Integrantes:** 
| Nome                    |     RM |
| ----------------        | -----: |
| Davi Sinhori            | 569487 |
| Gabriel da Silva        | 568910 |
| Henrique de Souza       | 570529 |
| André Balan             | 571691 |
| João Vitor Jun          | 572079 |

---

## Variáveis de Entrada

| Variável | Descrição |
|----------|-----------|
| **A** | Usuário autenticado (RFID/cartão válido) |
| **B** | Vaga disponível no eletroposto |
| **C** | Energia suficiente na rede |

## Variável de Saída

| Variável | Descrição |
|----------|-----------|
| **S** | Sessão de recarga autorizada |

---

## Expressão Booleana

```
S = (A · B) + (B · C)
```

Forma simplificada (fatorando B):

```
S = B · (A + C)
```

---

## Tabela Verdade Completa

| A | B | C | A · B | B · C | S = (A·B) + (B·C) | Resultado     |
|---|---|---|-------|-------|-------------------|---------------|
| 0 | 0 | 0 |   0   |   0   |         0         | ❌ Negada     |
| 0 | 0 | 1 |   0   |   0   |         0         | ❌ Negada     |
| 0 | 1 | 0 |   0   |   0   |         0         | ❌ Negada     |
| 0 | 1 | 1 |   0   |   1   |         1         | ✅ Autorizada |
| 1 | 0 | 0 |   0   |   0   |         0         | ❌ Negada     |
| 1 | 0 | 1 |   0   |   0   |         0         | ❌ Negada     |
| 1 | 1 | 0 |   1   |   0   |         1         | ✅ Autorizada |
| 1 | 1 | 1 |   1   |   1   |         1         | ✅ Autorizada |

---

## Análise das Combinações

### Quando a sessão é AUTORIZADA (S = 1):

- **A=0, B=1, C=1** → A vaga está disponível E a energia é suficiente. Mesmo sem autenticação prévia do usuário, o sistema autoriza — isso representa um modo de acesso por energia, útil em situações de emergência ou pré-pago.
- **A=1, B=1, C=0** → O usuário está autenticado E a vaga está disponível. O sistema autoriza mesmo com energia baixa — representa uma sessão de carga mínima ou de baixa potência.
- **A=1, B=1, C=1** → Condição ideal: usuário autenticado, vaga disponível e energia suficiente. Sessão completa autorizada com máxima prioridade.

### Quando a sessão é NEGADA (S = 0):

- **B = 0 em qualquer combinação** → A variável B (vaga disponível) é o fator mais crítico: sem vaga disponível, **nenhuma combinação de A e C** autoriza a sessão. Isso reflete a lógica real do ChargeGrid: não adianta ter usuário autenticado e energia disponível se não há ponto de carga livre.
- **A=1, B=0** → Usuário autenticado mas sem vaga: sessão negada.
- **A=0, B=1, C=0** → Vaga disponível mas sem usuário autenticado nem energia: negada.

### Conclusão da Análise

A variável **B (vaga disponível)** é a condição necessária do sistema — ela aparece em ambos os termos da expressão booleana (`A·B` e `B·C`). Sem B=1, a saída S é sempre 0, independente das outras entradas.

Isso demonstra, em linguagem de circuitos lógicos, o princípio central do ChargeGrid Intelligence: **a disponibilidade de infraestrutura física é o pré-requisito para qualquer operação de recarga inteligente**.
