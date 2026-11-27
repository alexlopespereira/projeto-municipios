import argparse
import csv
import os
from math import ceil, floor, log10
from operator import itemgetter
from pathlib import Path
from statistics import correlation

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "dados" / "municipios.csv"
REGIONS = {
    "Norte": "AC AP AM PA RO RR TO",
    "Nordeste": "AL BA CE MA PB PE PI RN SE",
    "Centro-Oeste": "DF GO MT MS",
    "Sudeste": "ES MG RJ SP",
    "Sul": "PR RS SC",
}
REGION_BY_UF = {uf: region for region, ufs in REGIONS.items() for uf in ufs.split()}
STAGES = {
    "Anos iniciais": "ideb_anos_iniciais",
    "Anos finais": "ideb_anos_finais",
}


def load_municipalities():
    with DATA.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        row["pib_per_capita"] = float(row["pib_mil_reais"]) * 1000 / int(row["populacao"])
        row["regiao"] = REGION_BY_UF[row["uf"]]
        for column in STAGES.values():
            value = row[column].strip()
            row[column] = float(value) if value else None
    return rows


def average_ranks(values):
    ordered = sorted(enumerate(values), key=itemgetter(1))
    ranks = [0.0] * len(ordered)
    start = 0
    while start < len(ordered):
        end = start + 1
        while end < len(ordered) and ordered[end][1] == ordered[start][1]:
            end += 1
        average = (start + 1 + end) / 2
        for index, _ in ordered[start:end]:
            ranks[index] = average
        start = end
    return ranks


def spearman(rows, column):
    return correlation(
        average_ranks([row["pib_per_capita"] for row in rows]),
        average_ranks([row[column] for row in rows]),
    )


def format_number(value):
    return f"{value:,}".replace(",", ".")


def format_correlation(value):
    return f"{value:+.3f}".replace(".", ",")


def font(size, bold=False):
    filename = "arialbd.ttf" if bold else "arial.ttf"
    directory = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    for candidate in (str(directory / filename), "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def load_top_population():
    with DATA.open(encoding="utf-8-sig", newline="") as source:
        municipalities = [
            (row["municipio"], row["uf"], int(row["populacao"]))
            for row in csv.DictReader(source)
        ]
    return sorted(municipalities, key=itemgetter(2), reverse=True)[:10]


def render_population_chart(municipalities):
    width, height = 1280, 920
    navy = "#102746"
    blue = "#246bab"
    muted = "#496178"
    background = "#eef4f9"
    border = "#d7e3ee"
    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)
    title = f"Os {len(municipalities)} municípios mais populosos em 2022"
    draw.text((width // 2, 48), title, font=font(44, True), fill=navy, anchor="mt")
    draw.text(
        (width // 2, 112),
        "População residente em habitantes, em ordem decrescente",
        font=font(23),
        fill=muted,
        anchor="mt",
    )
    draw.rounded_rectangle((64, 170, 1216, 868), radius=20, fill="white", outline=border)

    label_font = font(22, True)
    note_font = font(18)
    plot_left, plot_right = 380, 1018
    plot_width = plot_right - plot_left
    axis_max = max(2, ceil(municipalities[0][2] / 2_000_000) * 2) * 1_000_000
    row_top, row_height = 190, 52
    for index, (name, uf, population) in enumerate(municipalities):
        top = row_top + index * row_height
        middle = top + row_height // 2
        draw.text((100, middle), f"{name} / {uf}", font=label_font, fill=navy, anchor="lm")
        draw.rounded_rectangle((plot_left, middle - 9, plot_right, middle + 9), radius=4, fill=background)
        bar_right = plot_left + round(plot_width * population / axis_max)
        draw.rounded_rectangle((plot_left, middle - 9, bar_right, middle + 9), radius=4, fill=blue)
        draw.text((1180, middle), format_number(population), font=label_font, fill=navy, anchor="rm")
        draw.line((100, top + row_height, 1180, top + row_height), fill=border)

    axis_y = row_top + len(municipalities) * row_height + 16
    for fraction, anchor in ((0, "lt"), (0.5, "mt"), (1, "rt")):
        millions = int(axis_max * fraction / 1_000_000)
        unit = "milhão" if millions == 1 else "milhões"
        label = f"{millions} {unit}" if millions else "0"
        draw.text((plot_left + plot_width * fraction, axis_y), label, font=note_font, fill=muted, anchor=anchor)

    draw.line((100, 780, 1180, 780), fill=border)
    draw.text((100, 800), "Fonte dos dados — IBGE · Censo Demográfico 2022 · SIDRA, tabela 4714.", font=note_font, fill=muted)
    draw.text((100, 830), "Brasília integra a base de nível municipal do IBGE e tem situação administrativa própria.", font=note_font, fill=muted)
    return image


def render_chart(municipalities, results, common_count, common_scores, highlight):
    image = Image.new("RGB", (1600, 860), "#f2f5f8")
    draw = ImageDraw.Draw(image, "RGBA")
    ink = "#142c3b"
    muted = "#425969"
    blue = (16, 101, 143, 102)
    background_point = (16, 101, 143, 36) if highlight else blue
    orange = (170, 65, 14, 210)
    label = font(19)
    footnote = font(18)

    draw.text((64, 42), "Maior PIB per capita acompanha IDEB mais alto?", font=font(44, True), fill=ink)
    draw.text((66, 108), "Brasil · PIB per capita de 2022 e IDEB de 2023 da rede pública", font=font(23), fill=muted)
    draw.ellipse((67, 157, 77, 167), fill=blue)
    draw.text((88, 151), "Cada ponto representa um município com IDEB disponível.", font=label, fill=muted)
    if highlight:
        draw.ellipse((700, 157, 711, 168), fill=orange)
        draw.text((721, 151), f"Destaque: {highlight} · métricas nacionais", font=label, fill=muted)

    values = [row["pib_per_capita"] for row in municipalities]
    smallest, largest = min(values), max(values)
    if smallest <= 0:
        raise ValueError("A escala logarítmica exige PIB per capita positivo.")
    ticks = [
        multiple * 10**decade
        for decade in range(floor(log10(smallest)), ceil(log10(largest)) + 1)
        for multiple in (1, 2, 5)
    ]
    lower_tick = max(tick for tick in ticks if tick <= smallest)
    upper_tick = next(tick for tick in ticks if tick >= largest and tick > lower_tick)
    log_min = log10(lower_tick)
    log_span = log10(upper_tick) - log_min
    for panel, (stage, column, rows, coefficient) in enumerate(results):
        left = 64 + panel * 752
        draw.rounded_rectangle((left, 195, left + 720, 706), radius=16, fill="white", outline="#d8e1e9")
        draw.text((left + 26, 217), stage, font=font(28, True), fill=ink)
        included = format_number(len(rows))
        excluded = format_number(len(municipalities) - len(rows))
        caption = f"Spearman {format_correlation(coefficient)}  ·  {included} com IDEB  ·  {excluded} sem IDEB"
        draw.text((left + 26, 260), caption, font=label, fill=muted)

        x0, y0, x1, y1 = left + 70, 335, left + 664, 625

        def x_position(value):
            return x0 + (log10(value) - log_min) / log_span * (x1 - x0)

        draw.text((x0, 303), "IDEB 2023", font=label, fill=muted)
        for value in range(0, 11, 2):
            y = y1 - value / 10 * (y1 - y0)
            draw.line((x0, y, x1, y), fill="#dbe4eb")
            draw.text((x0 - 12, y), str(value), font=footnote, fill=muted, anchor="rm")
        for value in ticks:
            if not lower_tick <= value <= upper_tick:
                continue
            x = x_position(value)
            draw.line((x, y0, x, y1), fill="#dbe4eb")
            tick = format_number(value)
            draw.text((x, y1 + 13), tick, font=footnote, fill=muted, anchor="mt")
        draw.line((x0, y0, x0, y1, x1, y1), fill="#8299a9", width=2)

        if highlight:
            rows = sorted(rows, key=lambda row: highlight in (row["uf"], row["regiao"]))
        for row in rows:
            selected = highlight in (row["uf"], row["regiao"])
            x = x_position(row["pib_per_capita"])
            y = y1 - row[column] / 10 * (y1 - y0)
            radius = 3 if selected else 2
            color = orange if selected else background_point
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
        draw.text(((x0 + x1) / 2, 674), "PIB per capita 2022 (R$) · escala logarítmica", font=label, fill=ink, anchor="mt")

    common_initial, common_final = common_scores
    missing_either = format_number(len(municipalities) - common_count)
    common_summary = (
        f"{format_number(common_count)} municípios com IDEB nas duas etapas · "
        f"{missing_either} sem IDEB em pelo menos uma etapa."
    )
    common_correlations = (
        f"Spearman {format_correlation(common_initial)} nos anos iniciais e "
        f"{format_correlation(common_final)} nos anos finais na amostra comum."
    )
    draw.text((66, 724), common_summary, font=footnote, fill=ink)
    draw.text((66, 747), common_correlations, font=footnote, fill=ink)
    draw.line((66, 773, 1534, 773), fill="#c5d3de")
    draw.text((66, 790), "Fontes: IBGE/SIDRA, Censo 2022 (tab. 4714) e PIB dos Municípios 2022 (tab. 5938).", font=footnote, fill=muted)
    draw.text((66, 817), "Inep, resultados municipais do IDEB 2023, rede pública do ensino fundamental.", font=footnote, fill=muted)
    return image


def generate_pib_ideb_chart(highlight):
    municipalities = load_municipalities()
    results = []
    for stage, column in STAGES.items():
        rows = [row for row in municipalities if row[column] is not None]
        coefficient = spearman(rows, column)
        results.append((stage, column, rows, coefficient))
        missing = len(municipalities) - len(rows)
        print(f"{stage}: {len(rows)} municípios, {missing} sem IDEB, Spearman {format_correlation(coefficient)}")

    common = [row for row in municipalities if all(row[column] is not None for column in STAGES.values())]
    common_scores = [spearman(common, column) for column in STAGES.values()]
    print(f"Amostra comum: {len(common)} municípios, {len(municipalities) - len(common)} sem pelo menos uma nota")
    for stage, score in zip(STAGES, common_scores):
        print(f"{stage} na amostra comum: Spearman {format_correlation(score)}")

    suffix = f"-{highlight.lower()}" if highlight else ""
    destination = ROOT / "graficos" / f"pib-per-capita-ideb{suffix}.png"
    destination.parent.mkdir(exist_ok=True)
    render_chart(municipalities, results, len(common), common_scores, highlight).save(destination)
    print(f"Gráfico salvo em {destination.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Gera o gráfico dos municípios mais populosos em 2022.")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--pib-ideb", action="store_true", help="gera o gráfico nacional de PIB per capita e IDEB")
    selection.add_argument("--uf", type=str.upper, choices=sorted(REGION_BY_UF), help="destaca uma UF no gráfico de PIB e IDEB")
    selection.add_argument("--regiao", choices=REGIONS, help="destaca uma região no gráfico de PIB e IDEB")
    args = parser.parse_args()
    highlight = args.uf or args.regiao
    if args.pib_ideb or highlight:
        generate_pib_ideb_chart(highlight)
        return

    municipalities = load_top_population()
    if not municipalities:
        parser.error(f"{DATA.relative_to(ROOT)} não contém linhas de dados")

    destination = ROOT / "graficos" / "populacao-top10.png"
    destination.parent.mkdir(exist_ok=True)
    render_population_chart(municipalities).save(destination)
    print(f"Gráfico salvo em {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
