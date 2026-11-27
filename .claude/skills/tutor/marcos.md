# Marcos do projeto

Critérios que o tutor usa para avaliar cada marco. Para cada um: o que deve existir, o que o script confere, o que você confere lendo, as dicas em três degraus e os blocos do vídeo a rever.

| Marco | Módulo do curso |
|---|---|
| 1 | 3 |
| 2 | 4 |
| 3 | 5 |
| 4 | 7 |
| 5 | 8 |
| 6 | 10 |

Os módulos 1, 2, 6, 9 e 11 não têm marco.

O projeto responde a uma pergunta: municípios com maior PIB per capita têm IDEB mais alto? Os dados estão em `dados/municipios.csv`, com uma linha por município.

---

## Marco 1: primeiro gráfico em uma página

**Módulo 3.** Uma página HTML que mostra um gráfico feito a partir do arquivo de dados.

**O script confere:** existe um arquivo `.html`; a página tem um gráfico; a página usa os dados dos municípios.

**Você confere lendo a página:**

- O gráfico mostra dados do arquivo, e não números inventados ou de exemplo.
- Dá para entender o que o gráfico mostra: há título, ou os eixos estão identificados.

Não avalie beleza nem escolha do tipo de gráfico. Neste ponto do curso, basta existir e ser legível.

**Dicas**

1. O primeiro marco é ver um resultado: uma página que abre no navegador com um gráfico dos dados.
2. Olhe o que há na pasta `dados`. O agente precisa saber que é desse arquivo que o gráfico deve sair.
3. Um bom pedido diz de qual arquivo vêm os dados, o que você quer ver (qual medida, de quais municípios ou estados) e em que formato quer o resultado (uma página que abre no navegador).

**Rever:** blocos 3.5 e 3.6.

---

## Marco 2: gráfico em Python

**Módulo 4.** O Python está funcionando, há um script, e o script gerou o gráfico como imagem.

**O script confere:** existe um arquivo `.py`; existe uma imagem de gráfico (`.png`, `.svg` ou `.jpg`). A versão do Python aparece como informação. Se o script de checagem rodou, o Python está funcionando.

**Você confere lendo o script do aluno:**

- O script lê `dados/municipios.csv`, e não tem os dados digitados dentro dele.

Não revise o estilo do código. O aluno não programa; quem escreveu foi o agente.

**Dicas**

1. Agora o mesmo gráfico é feito por um programa em Python, que você pode rodar de novo quando os dados mudarem.
2. Verifique duas coisas separadas: o Python está instalado? E o agente já escreveu e rodou o script? Uma pode estar feita sem a outra.
3. Um bom pedido diz que o gráfico deve ser gerado por um script em Python, a partir do arquivo de dados, e salvo como imagem em uma pasta do projeto.

**Rever:** blocos 4.4 e 4.8.

---

## Marco 3: instruções do projeto

**Módulo 5.** Um arquivo `CLAUDE.md` (ou `AGENTS.md`, no Codex) que o agente lê no início de toda sessão.

**O script confere:** o arquivo existe na raiz do projeto; tem conteúdo suficiente; cita o arquivo de dados.

**Você confere lendo o arquivo. Ele deve dizer:**

- para que serve o projeto, em uma ou duas frases;
- quais são os dados: de onde vêm e o que significam as colunas principais;
- pelo menos uma convenção de trabalho, por exemplo onde salvar os gráficos ou em que língua escrever.

Aponte como ajuste a fazer se o arquivo for só o texto genérico gerado automaticamente, sem nada específico deste projeto, ou se descrever algo que não bate com a pasta.

**Dicas**

1. O agente esquece tudo entre uma sessão e outra. Este arquivo é o que ele lê toda vez para saber onde está.
2. Imagine uma pessoa nova chegando ao projeto. O que ela precisaria saber para não perguntar o óbvio? Compare com o que o arquivo diz hoje.
3. Um bom pedido manda o agente olhar a pasta e os dados antes de escrever, e diz quais três coisas o arquivo precisa conter: o objetivo, a descrição dos dados e as convenções.

**Rever:** blocos 5.5 e 5.6.

---

## Marco 4: a pergunta sem ambiguidade

**Módulo 7.** Um arquivo `pergunta.md` que registra a pergunta de análise de modo que duas pessoas a entendam do mesmo jeito.

**O script confere:** o arquivo existe; menciona PIB per capita; menciona o código do IBGE como chave.

**Você confere lendo o arquivo. Ele deve deixar claro:**

- que a riqueza é medida por PIB per capita, e não por PIB total;
- qual IDEB é usado: anos iniciais, anos finais ou os dois;
- que fontes diferentes são juntadas pelo código do município, e não pelo nome;
- o que conta como resposta: que gráfico ou que número responde à pergunta.

Mencionar "per capita" não basta. O texto precisa dizer que essa é a medida escolhida. Se alguma das quatro definições faltar, aponte como ajuste.

**Dicas**

1. "Municípios mais ricos" pode significar duas coisas, e elas dão respostas diferentes. A pergunta escrita precisa escolher uma.
2. Releia a pergunta procurando palavras que admitem mais de uma leitura: rico, melhor, maior. Para cada uma, pergunte-se "medido como?".
3. Um bom caminho é pedir ao agente que o entreviste sobre a pergunta antes de escrever, e só depois registrar as decisões no arquivo: a medida de riqueza, qual IDEB, como as fontes são juntadas e o que conta como resposta.

**Rever:** blocos 7.1, 7.5 e 7.6.

---

## Marco 5: números conferidos

**Módulo 8.** Um arquivo `verificacao.md` que registra a conferência de pelo menos dois números contra a fonte oficial.

**O script confere:** o arquivo existe; contém pelo menos dois números; cita uma fonte oficial (IBGE ou INEP).

**Você confere lendo o arquivo. Para cada número conferido, deve haver:**

- o que é o número e de qual município;
- o valor que está no projeto;
- o valor na fonte oficial, com o endereço de onde foi tirado;
- se bateu e, se não bateu, uma explicação.

Aponte como ajuste se houver só um número, se a fonte for vaga ("site do IBGE", sem endereço), ou se o registro disser que conferiu sem mostrar os dois valores.

Não confira você mesmo os valores na internet. Avalie se o registro está completo.

**Dicas**

1. O agente entrega o certo e o errado com a mesma confiança. Conferir é olhar um número do seu resultado na fonte original.
2. Escolha um município que você conhece. Qual é a população dele no seu projeto? E no site do IBGE?
3. Um bom registro tem, para cada número, quatro coisas: o que é, o valor no projeto, o valor na fonte com o endereço, e a conclusão.

**Rever:** blocos 8.2 e 8.5.

---

## Marco 6: projeto publicado

**Módulo 10.** O projeto é um repositório Git com histórico, publicado no GitHub, com um `README.md`.

**O script confere:** a pasta é um repositório Git; há pelo menos dois commits; há um endereço remoto no GitHub; existe `README.md`. Como informação, mostra se há alterações não salvas em commit e se há commits ainda não enviados.

**Você confere lendo o `README.md`. Ele deve dizer:**

- o que é o projeto e qual pergunta ele responde;
- o que foi encontrado, em uma ou duas frases;
- de onde vêm os dados.

Se houver alterações não salvas ou commits não enviados, avise: o que está no GitHub pode estar diferente do que está na pasta.

O script não consegue confirmar que o projeto aparece no site do GitHub. Peça ao aluno que abra o endereço no navegador e confira.

**Dicas**

1. Até aqui o projeto existe só no seu computador. Publicar é guardar o histórico e ter um endereço para mostrar.
2. São três etapas, e cada uma pode estar feita ou não: a pasta virou um repositório? Há fotos do projeto guardadas (commits)? Elas foram enviadas ao GitHub?
3. Um bom pedido diz ao agente em qual das três etapas você está, pede que ele explique cada comando antes de rodar, e pede que ele mostre o resultado no final.

**Rever:** blocos 10.4, 10.5 e 10.8.
