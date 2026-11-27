# Dados dos municípios

Uma linha por código do IBGE, com a cobertura completa das **5.570 unidades de nível municipal da base de 2022**, incluindo Brasília e Fernando de Noronha. A base não representa a divisão municipal de todos os anos posteriores.

## Colunas

| Coluna | Significado | Referência |
|---|---|---|
| `codigo_ibge` | Identificador textual de sete dígitos, usado para relacionar as fontes | IBGE |
| `municipio` | Nome do município na base de população | IBGE/SIDRA |
| `uf` | Sigla da unidade da federação | IBGE |
| `populacao` | População residente, em pessoas | Censo 2022, SIDRA 4714, variável 93 |
| `pib_mil_reais` | PIB a preços correntes, em **mil reais** | 2022, SIDRA 5938, variável 37 |
| `ideb_anos_iniciais` | IDEB dos anos iniciais do ensino fundamental da **rede pública** | 2023, INEP |
| `ideb_anos_finais` | IDEB dos anos finais do ensino fundamental da **rede pública** | 2023, INEP |

O CSV usa UTF-8, vírgula como separador de colunas e ponto como separador decimal. Os números não têm separador de milhar. As duas colunas de IDEB contêm índices de 0 a 10, não porcentagens.

## Fontes e preparação

- [População de 2022, IBGE/SIDRA](https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/93/p/2022?formato=json).
- [PIB de 2022, IBGE/SIDRA](https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/37/p/2022?formato=json).
- [Planilhas municipais do IDEB, INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados/2005-2025).

As planilhas do INEP são da divulgação de 2025, mas a extração usa explicitamente as colunas **IDEB 2023**, para a rede **Pública**. Não mistura a rede pública com as linhas Municipal, Estadual ou Federal, nem faz média entre redes.

As fontes foram relacionadas pelo código de sete dígitos. Os nomes e as siglas de UF vêm da população do IBGE. As fontes, endereços dos arquivos, hashes SHA-256, planilhas e colunas selecionadas estão em `fontes.json`. A preparação é de 16/11/2026 e não presume que estes sejam os últimos anos disponíveis de cada indicador.

## Ausências e limites

- Há 140 campos vazios nos anos iniciais e 188 nos anos finais. Um campo vazio significa ausência de valor disponível na extração, **não** IDEB zero. O arquivo `ausencias_ideb.csv` preserva o marcador original e distingue ausência de valor de ausência da linha da rede pública.
- PIB e população são de 2022; o IDEB é de 2023. A análise do projeto relaciona esses períodos e precisa identificá-los no gráfico e no texto.
- A população soma 203.080.756 pessoas nesta extração. Revisões e outras tabelas do IBGE podem apresentar diferenças; a conferência deve usar a tabela e a versão documentadas.
- Para calcular PIB por habitante em reais, a fórmula é `pib_mil_reais * 1000 / populacao`. Esse cálculo usa a população desta extração e não deve ser apresentado automaticamente como reprodução de qualquer indicador per capita publicado em outra tabela.
- PIB por habitante mede produção econômica por pessoa, não renda familiar. A relação com IDEB, por si só, não demonstra causalidade.
- Há municípios com o mesmo nome em UFs diferentes. A base preserva esses casos; a identificação completa inclui código e UF.

No módulo 3, o gráfico usa apenas a população. PIB e IDEB permanecem na mesma base para as atividades posteriores.
