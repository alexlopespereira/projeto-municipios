# Maior PIB per capita acompanha IDEB mais alto?

## Decisões da análise

- Responder primeiro para o Brasil. Depois, repetir a análise dentro de cada UF.
- Usar todos os municípios com IDEB disponível em cada etapa, anos iniciais e anos finais do ensino fundamental da rede pública. Usar os municípios com as duas notas como verificação ao comparar as etapas.
- Dar o mesmo peso a cada município. Calcular o PIB por habitante em reais multiplicando o PIB em mil reais por mil e dividindo pela população residente.
- Medir a associação com a correlação de Spearman. Apresentar dois gráficos nacionais de dispersão, um por etapa, e uma tabela por UF.
- Mostrar todas as correlações calculáveis e a cobertura em cada etapa, expressa em municípios com nota sobre o total da UF. Indicar que a correlação do DF é indefinida porque há uma única unidade na base.

## Cobertura nacional

| Etapa | Com IDEB | Sem IDEB | Spearman |
| --- | ---: | ---: | ---: |
| Anos iniciais | 5.430 | 140 | +0,378 |
| Anos finais | 5.382 | 188 | +0,366 |

Das 5.570 unidades da base, 289 ficaram sem nota em pelo menos uma etapa. Entre as 5.281 com as duas notas, Spearman foi +0,380 nos anos iniciais e +0,367 nos anos finais.

## Fontes e reprodução

O PIB e a população residente são de 2022 e vêm do IBGE/SIDRA, tabelas 5938 e 4714. O IDEB municipal da rede pública é de 2023 e vem do Inep. As fontes foram relacionadas pelo código de sete dígitos do IBGE. Consulte a [documentação da base](dados/LEIA-ME.md).

Na raiz do projeto, execute `python .\analise.py --pib-ideb` para gerar os dois gráficos nacionais em [graficos/pib-per-capita-ideb.png](graficos/pib-per-capita-ideb.png).
