Documentação Lógica: Simulador de Sessão de Recarga
1. Visão Geral do Sistema
O programa foi desenvolvido em Python com o objetivo de simular uma estação de recarga para veículos elétricos. Ele permite que o usuário escolha seu perfil (Comum ou Assinante), o formato de cobrança (por tempo ou por valor) e exibe um relatório detalhado ao final do processo.

2. Estruturação e Modularização
Para manter o código organizado e facilitar a manutenção, o sistema foi dividido em funções específicas:

CalcularRecarga(tempo, valor): Responsável pela regra de três básica. Se o usuário informa o tempo, ela calcula o valor total. Se informa o valor, calcula o tempo equivalente.

VerificacaoVariavel(texto): Garante a integridade do sistema. Utiliza uma estrutura try/except aliada à recursividade para impedir que o programa quebre caso o usuário digite letras no lugar de números ou insira valores negativos/zerados.

Recarga(tempo): Função visual que simula o tempo passando através de uma barra de carregamento dinâmica impressa no terminal, utilizando a biblioteca time (time.sleep).

3. Fluxo Principal de Execução
   
Definição de Tarifa: O sistema inicia perguntando o tipo de usuário através de um loop while True, que só é quebrado quando uma opção válida ("1" ou "2") é inserida. Se o usuário for Assinante, o valor do kWh recebe uma multiplicação por 0.8, aplicando 20% de desconto.

Escolha do Método de Recarga: Utilizando a estrutura match/case (equivalente ao switch), o usuário decide se quer definir a recarga baseada no tempo que ficará na vaga ou no valor em dinheiro que deseja gastar.

Confirmação: O sistema exibe uma prévia do custo e do tempo. Caso o usuário não confirme, o sistema é encerrado.

Sessão de Recarga: Ao confirmar, o sistema utiliza a biblioteca datetime para registrar o horário exato de início. A função da barra de progresso é chamada e, ao finalizar, o horário de término é registrado.

Geração do Relatório: O programa imprime um cupom formatado contendo: o perfil do usuário, os horários de início e fim, o tempo total da sessão, a energia simulada consumida (calculada com base na potência do carregador de 30kWh) e o custo total da operação.
