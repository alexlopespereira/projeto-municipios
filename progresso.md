# Progresso

Atualizado em 27/11/2026.

## O que já fizemos

- Criamos `index.html`, com o gráfico da população de 2022.
- Criamos `analise.py`, que gera os gráficos em `graficos/` e calcula a correlação de Spearman entre PIB per capita e IDEB.
- Registramos em `pib-ideb.md` as decisões e o resultado nacional da análise.
- Escrevemos `AGENTS.md` com a estrutura do projeto e as convenções de dados.
- Verificamos se os arquivos que iriam para o GitHub continham dados pessoais, senhas ou chaves e não encontramos nenhum. A pasta `segredos/` não foi aberta, porque uma regra proíbe o agente de lê-la.

## Decisões de `pib-ideb.md`

- Responder primeiro para o Brasil e depois repetir a análise em cada UF.
- Usar todos os municípios com IDEB em cada etapa, anos iniciais e finais da rede pública. Usar os que têm as duas notas como verificação.
- Dar o mesmo peso a cada município. PIB por habitante = PIB em mil reais × 1.000 ÷ população.
- Medir a associação com Spearman, com dois gráficos nacionais de dispersão e uma tabela por UF.
- Mostrar a cobertura de cada etapa e indicar que a correlação do DF é indefinida, pois há uma única unidade.
- Resultado nacional: Spearman de +0,378 nos anos iniciais e de +0,366 nos anos finais, ou seja, uma associação positiva moderada.

## Decisões sobre a publicação

- `segredos/` e `.env` não podem ir para o GitHub.
- O `.env` já está no `.gitignore` da raiz. A pasta `segredos/` ainda não está protegida.

## Próximo passo

Criar um `.gitignore` nesta pasta que exclua `segredos/` e `.env` e conferir com `git status` que os dois ficaram de fora. Depois:

- gerar o gráfico com `python .\analise.py --pib-ideb`, porque `graficos/pib-per-capita-ideb.png` ainda não está na pasta;
- montar a tabela por UF prevista em `pib-ideb.md`;
- decidir se a pasta duplicada `dados - Copy/` será apagada e se `dados/fontes.json` e `dados/ausencias_ideb.csv`, apagados da pasta mas presentes no último commit, serão restaurados ou removidos.
