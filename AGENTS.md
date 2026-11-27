# Repository Guidelines

 O brand guideline dessa marca prescreve que devemos usar htmls com titulo centralizado e em azul marinho.

 Leia o arquivo progresso.md ao iniciar uma nova sessao.
## Project Structure

Projeto Municípios is a course project that uses Brazilian municipal data to explore whether higher GDP per capita is associated with higher public-school IDEB scores.

- `index.html` is the standalone 2022 population chart.
- `analise.py` generates charts in `graficos/` and computes Spearman correlations for the GDP and IDEB analysis.
- `dados/municipios.csv` contains 2022 population and GDP from IBGE/SIDRA and 2023 IDEB from INEP for the early and final years of public elementary and lower-secondary education. See `LEIA-ME.txt` for units, coverage, and sources.
- `.agents/skills/tutor/` and `.claude/skills/tutor/` contain the course milestone checker for Codex and Claude, respectively.

## Run and Validate

Run commands from the project root in PowerShell. Use `Start-Process .\index.html` to preview the population chart.

- `python -m pip install Pillow` installs the chart generator’s dependency.
- `python .\analise.py` generates `graficos/populacao-top10.png`. Use `--pib-ideb` for the national scatter plot or `--uf SP` or `--regiao Sudeste` for a highlighted version.
- `python .\.agents\skills\tutor\scripts\verificar.py .` reports course milestone status. Add `--marco 3` to check this guide.

There is no dedicated test suite or coverage threshold. After chart changes, inspect the rendered output and check plotted values against the CSV. For analysis changes, compare the reported sample sizes and missing-score counts with the source rows.

## Style and Data Conventions

Use UTF-8, four-space Python indentation, and `snake_case` for Python functions and variables. Keep chart labels in Brazilian Portuguese and include the reference year, units, and source. Preserve the source CSVs. Join on the seven-digit `codigo_ibge` string, calculate GDP per capita as `pib_mil_reais * 1000 / populacao`, and keep blank IDEB scores missing.

## Commits and Pull Requests

Keep commits atomic and use short English subjects. Follow the course history’s `feat(nivelamento): ...` pattern for new features. In pull requests, describe the change and validation steps, link relevant issues, and include screenshots for visible chart changes.
