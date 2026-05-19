# ChargeGrid Intelligence Chatbot
### EV Challenge 2026 — FIAP × GoodWe | Sprint 1

---

## Integrantes

| Nome                    |     RM |
| ----------------        | -----: |
| Davi Sinhori            | 569487 |
| Gabriel da Silva        | 568910 |
| Henrique de Souza       | 570529 |
| André Balan             | 571691 |
| João Vitor Jun          | 572079 |

---

## Problema abordado

O EV Challenge 2026 propõe resolver a ausência de mecanismos integrados nos eletropostos GoodWe para **orquestrar potência, registrar ciclos de carga, faturar sessões e comunicar eventos operacionais** — o cenário ChargeGrid Intelligence.

Operadores comerciais de eletropostos (postos, estacionamentos, frotas) não possuem uma interface inteligente para consultar configurações, interpretar alertas, entender cobranças e resolver problemas técnicos sem depender de suporte humano. O resultado é tempo ocioso, erros de operação e experiência ruim para o usuário final do veículo elétrico.

---

## Proposta do chatbot

Um assistente conversacional baseado em **RAG (Retrieval-Augmented Generation)** que responde perguntas operacionais do operador comercial em linguagem natural, consultando a documentação técnica oficial da GoodWe em tempo real.

**Persona atendida:** operador comercial de eletroposto — responsável pela gestão do ponto de recarga, configuração de tarifas, monitoramento de sessões e resolução de problemas do equipamento.

**Contexto:** ChargeGrid Intelligence — gestão de eletropostos comerciais com faturamento por sessão, controle de potência e comunicação de eventos.

**Perguntas típicas que o chatbot responde:**
- Como configurar o preço por kWh cobrado em cada sessão?
- O que significa o erro E-04 no display do carregador?
- Como exportar o relatório de sessões do mês?
- Qual a potência máxima simultânea suportada por estação?
- Como cadastrar um novo RFID de acesso ao eletroposto?

---

## Tecnologias selecionadas

| Tecnologia | Papel no sistema | Justificativa |
|---|---|---|
| **LangChain** | Orquestração do pipeline RAG | Framework consolidado para conectar loaders, splitters, embeddings e LLMs em uma cadeia coesa |
| **LangGraph** | Controle do fluxo (retrieve → generate) | Permite modelar o pipeline como grafo de estados, facilitando extensões futuras como memória e múltiplos agentes |
| **OpenAI gpt-4o-mini** | Geração da resposta final | Equilíbrio entre custo e qualidade para respostas técnicas concisas; adequado ao volume de consultas operacionais |
| **text-embedding-ada-002** | Vetorização de documentos e perguntas | Modelo de embedding estável e bem documentado, com boa performance em português técnico |
| **InMemoryVectorStore** | Armazenamento dos vetores | Solução simples para prototipagem na Sprint 1; será substituída por um banco persistente na Sprint 2 |
| **PyPDFLoader / WebBaseLoader** | Ingestão de documentos | Carregamento direto dos manuais GoodWe em PDF e conteúdo do site oficial |
| **LangSmith** | Gerenciamento do prompt RAG | Permite versionar e atualizar o system prompt sem alterar o código |
| **Google Colab + Google Drive** | Ambiente de execução | Acessível a todos os integrantes sem configuração local; PDFs armazenados no Drive compartilhado |

---

## Fluxo de funcionamento

```
Operador faz pergunta
        │
        ▼
System prompt (ChargeGrid Intelligence)
        │
        ▼
Embedding da pergunta ──── Base de conhecimento (7 PDFs + site GoodWe)
        │                          │
        ▼                          │
Busca vetorial ◄───────────────────┘
        │
        ▼
Chunks relevantes recuperados
        │
        ▼
Montar prompt RAG (pergunta + contexto + system prompt)
        │
        ▼
LLM gpt-4o-mini
        │
        ▼
Resposta contextualizada entregue ao operador
```

---

## Base de conhecimento

| Arquivo | Conteúdo |
|---|---|
| `GW_HCA-G2_User-Manual-PT.pdf` | Manual do usuário carregador HCA-G2 |
| `GoodWe_EV_ChargeOps_Base_Conhecimento.pdf` | Base de conhecimento EV ChargeOps |
| `goodwe_carregador.pdf` | Especificações do carregador |
| `goodwe_carregador1.pdf` | Guia complementar do carregador |
| `goodwe_instalacao.pdf` | Manual de instalação |
| `goodwe_manualcarregador.pdf` | Manual completo do carregador |
| `goodwe_manualdousuario.pdf` | Manual do usuário |
| Site `br.goodwe.com` | Informações institucionais e produtos |

---

## System prompt (base para Sprint 2)

```
Você é um assistente técnico especializado nos produtos de recarga de veículos
elétricos da GoodWe, com foco no contexto ChargeGrid Intelligence — gestão de
eletropostos comerciais.

Seu usuário é um OPERADOR COMERCIAL responsável por gerenciar um ou mais pontos
de recarga GoodWe. Ele pode ter dúvidas sobre: configuração de tarifas,
interpretação de erros, exportação de relatórios, controle de acesso por RFID,
monitoramento de sessões e manutenção básica dos equipamentos.

Regras:
- Responda APENAS com base nos documentos fornecidos como contexto.
- Se não souber a resposta, diga: "Não sei."
- Use linguagem clara, direta e profissional. Máximo 4 frases por resposta.
- Quando relevante, indique o nome do manual ou seção de onde a informação foi extraída.
- Não invente especificações técnicas, valores de tensão, corrente ou potência.

Contexto disponível: {context}
Pergunta do operador: {question}
```

---

## Modelo de teste

Perguntas esperadas e respostas ideais para validação na Sprint 2:

| # | Pergunta | Resposta ideal esperada |
|---|---|---|
| 1 | Como configuro o preço por kWh cobrado em cada sessão? | O operador acessa o painel de tarifas no SEMS Portal ou no display do equipamento, define o valor por kWh e confirma. Descrito na seção de tarifação do manual do usuário. |
| 2 | O que significa o código de erro E-04 no display? | O erro E-04 indica falha na comunicação com o servidor de gerenciamento. Verifique a conexão de rede do equipamento e reinicie o módulo de comunicação conforme o manual de instalação. |
| 3 | Como exportar o relatório de sessões do mês? | No SEMS Portal, acesse "Relatórios" > "Sessões de recarga", selecione o período e clique em "Exportar CSV" ou "Exportar PDF". |
| 4 | Qual a potência máxima simultânea suportada por estação? | Depende do modelo instalado. O HCA-G2 suporta até 22 kW em modo AC trifásico. Confirme na plaqueta de identificação do equipamento. |
| 5 | Como cadastrar um novo cartão RFID de acesso? | No SEMS Portal, acesse "Gestão de usuários" > "Adicionar RFID", aproxime o cartão do leitor ou insira o código manualmente e confirme. |
| 6 | O carregador parou no meio da sessão. O que fazer? | Verifique se houve queda de energia ou interrupção de rede. Reinicie a sessão pelo aplicativo ou display. Se persistir, consulte o log de erros na seção de diagnóstico do manual. |
| 7 | Como limitar o consumo máximo por sessão em kWh? | No SEMS Portal, ative o limite de energia por sessão nas configurações de recarga e defina o valor máximo em kWh, conforme a seção "Controle de carga" da documentação. |

---

