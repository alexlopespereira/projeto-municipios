# Projeto Municípios

Projeto do curso Introdução a Agentes de IA — Nivelamento. Usa dados públicos dos 5.570 municípios brasileiros para responder a uma pergunta:

**Municípios com maior PIB por habitante têm IDEB mais alto na rede pública?**

## O que encontramos

Há uma associação positiva e moderada: a correlação de Spearman entre PIB por habitante e IDEB foi de +0,378 nos anos iniciais (5.430 municípios com nota) e de +0,366 nos anos finais (5.382 municípios com nota) do ensino fundamental. A associação, por si só, não demonstra causalidade, e PIB por habitante mede produção econômica por pessoa, não renda familiar.

Decisões da análise, cobertura e verificação entre etapas estão em [pib-ideb.md](pib-ideb.md).

## De onde vêm os dados

| Indicador | Ano | Fonte |
| --- | --- | --- |
| População residente | 2022 | Censo 2022, IBGE/SIDRA, tabela 4714 |
| PIB municipal, em mil reais | 2022 | IBGE/SIDRA, tabela 5938 |
| IDEB da rede pública, anos iniciais e finais do ensino fundamental | 2023 | Inep |

As fontes foram relacionadas pelo código de sete dígitos do IBGE. O PIB por habitante, em reais, é `pib_mil_reais * 1000 / populacao`. Campos vazios de IDEB significam ausência de valor, não nota zero. Colunas, unidades, links e limites estão em [dados/LEIA-ME.md](dados/LEIA-ME.md).

## Como reproduzir

Na raiz do projeto, no PowerShell:

```powershell
python -m pip install Pillow
python .\analise.py --pib-ideb
```

O segundo comando gera os gráficos nacionais em [graficos/pib-per-capita-ideb.png](graficos/pib-per-capita-ideb.png).
