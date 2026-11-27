"""Read-only milestone checks for the course project.

Prints a JSON report to stdout. Uses only the standard library and never
writes to the project or to the network.

Usage:
    python verificar.py [project_dir] [--marco N]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", ".claude", ".agents", ".codex", ".venv", "venv", "env",
    "node_modules", "__pycache__", ".ipynb_checkpoints",
}
IMAGE_SUFFIXES = {".png", ".svg", ".jpg", ".jpeg"}
MIN_IMAGE_BYTES = 1024
MIN_INSTRUCTION_CHARS = 300
MAX_EVIDENCE_FILES = 5

RE_CHART = re.compile(r"<svg|<canvas|chart|plotly|vega|echarts|d3\.", re.I)
RE_DATA = re.compile(r"municipios\.csv|popula[cç][aã]o|\bpib\b|\bideb\b", re.I)
RE_DATA_FILE = re.compile(r"municipios\.csv|dados[/\\]", re.I)
RE_PER_CAPITA = re.compile(r"per\s*capita|por\s+habitante", re.I)
RE_JOIN_KEY = re.compile(
    r"codigo_ibge|c[oó]digo\s+(do\s+)?ibge|c[oó]digo\s+do\s+munic[ií]pio", re.I
)
RE_OFFICIAL = re.compile(r"ibge\.gov\.br|inep\.gov\.br|[\w.-]+\.gov\.br", re.I)
RE_URL = re.compile(r"https?://\S+")
RE_NUMBER = re.compile(r"\d[\d.,]*")


def default_root() -> Path:
    """The project is four levels above this file: <root>/.claude/skills/tutor/scripts."""
    here = Path(__file__).resolve()
    if len(here.parents) > 4 and here.parents[3].name in {".claude", ".agents"}:
        return here.parents[4]
    return Path.cwd()


def project_files(root: Path) -> list[Path]:
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        found.extend(Path(current) / name for name in files)
    return found


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(root: Path, paths: list[Path]) -> str:
    shown = [p.relative_to(root).as_posix() for p in paths[:MAX_EVIDENCE_FILES]]
    extra = len(paths) - len(shown)
    return ", ".join(shown) + (f" e mais {extra}" if extra > 0 else "")


def root_file(root: Path, *names: str) -> Path | None:
    """Case-insensitive lookup of a file directly in the project root."""
    wanted = {n.lower() for n in names}
    try:
        for entry in root.iterdir():
            if entry.is_file() and entry.name.lower() in wanted:
                return entry
    except OSError:
        pass
    return None


def check(cid: str, descricao: str, ok: bool, evidencia: str, informativo: bool = False) -> dict:
    return {
        "id": cid,
        "descricao": descricao,
        "ok": bool(ok),
        "evidencia": evidencia,
        "informativo": informativo,
    }


def git(root: Path, *args: str) -> tuple[bool, str]:
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20,
        )
    except FileNotFoundError:
        return False, "git não encontrado neste computador"
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"falha ao rodar git: {exc}"
    return done.returncode == 0, (done.stdout or done.stderr).strip()


def marco_1(root: Path, files: list[Path]) -> dict:
    pages = [f for f in files if f.suffix.lower() in {".html", ".htm"}]
    with_chart = [p for p in pages if RE_CHART.search(read_text(p))]
    with_data = [p for p in pages if RE_DATA.search(read_text(p))]
    return {
        "numero": 1, "modulo": 3, "titulo": "Primeiro gráfico em uma página",
        "checagens": [
            check("pagina_html", "Existe uma página HTML", pages,
                  rel(root, pages) if pages else "nenhum arquivo .html na pasta"),
            check("grafico_na_pagina", "A página tem um gráfico", with_chart,
                  rel(root, with_chart) if with_chart else "nenhuma página com gráfico"),
            check("dados_na_pagina", "A página usa os dados dos municípios", with_data,
                  rel(root, with_data) if with_data else "nenhuma página cita os dados"),
        ],
        "arquivos_para_ler": [p.relative_to(root).as_posix() for p in (with_chart or pages)[:1]],
    }


def marco_2(root: Path, files: list[Path]) -> dict:
    scripts = [f for f in files if f.suffix.lower() == ".py"]
    images = [
        f for f in files
        if f.suffix.lower() in IMAGE_SUFFIXES and f.stat().st_size >= MIN_IMAGE_BYTES
    ]
    return {
        "numero": 2, "modulo": 4, "titulo": "Gráfico em Python",
        "checagens": [
            check("python", "O Python está funcionando", True,
                  "versão " + sys.version.split()[0], informativo=True),
            check("script_python", "Existe um script em Python", scripts,
                  rel(root, scripts) if scripts else "nenhum arquivo .py na pasta"),
            check("imagem_do_grafico", "Existe uma imagem de gráfico", images,
                  rel(root, images) if images else "nenhuma imagem de gráfico na pasta"),
        ],
        "arquivos_para_ler": [p.relative_to(root).as_posix() for p in scripts[:1]],
    }


def marco_3(root: Path, files: list[Path]) -> dict:
    doc = root_file(root, "CLAUDE.md", "AGENTS.md")
    text = read_text(doc) if doc else ""
    size = len(re.sub(r"\s+", "", text))
    return {
        "numero": 3, "modulo": 5, "titulo": "Instruções do projeto",
        "checagens": [
            check("arquivo_de_instrucoes", "Existe CLAUDE.md ou AGENTS.md na raiz", doc,
                  doc.name if doc else "nenhum dos dois arquivos na raiz do projeto"),
            check("instrucoes_com_conteudo", "O arquivo tem conteúdo suficiente",
                  size >= MIN_INSTRUCTION_CHARS,
                  f"{size} caracteres (mínimo {MIN_INSTRUCTION_CHARS})"),
            check("instrucoes_citam_os_dados", "O arquivo cita o arquivo de dados",
                  bool(RE_DATA_FILE.search(text)),
                  "cita os dados" if RE_DATA_FILE.search(text) else "não cita dados/municipios.csv"),
        ],
        "arquivos_para_ler": [doc.name] if doc else [],
    }


def marco_4(root: Path, files: list[Path]) -> dict:
    doc = root_file(root, "pergunta.md")
    text = read_text(doc) if doc else ""
    return {
        "numero": 4, "modulo": 7, "titulo": "A pergunta sem ambiguidade",
        "checagens": [
            check("arquivo_pergunta", "Existe pergunta.md na raiz", doc,
                  doc.name if doc else "pergunta.md não encontrado na raiz do projeto"),
            check("define_per_capita", "A pergunta menciona PIB per capita",
                  bool(RE_PER_CAPITA.search(text)),
                  "menciona per capita" if RE_PER_CAPITA.search(text) else "não menciona per capita"),
            check("define_chave", "A pergunta menciona o código do IBGE como chave",
                  bool(RE_JOIN_KEY.search(text)),
                  "menciona o código" if RE_JOIN_KEY.search(text) else "não menciona o código do município"),
        ],
        "arquivos_para_ler": [doc.name] if doc else [],
    }


def marco_5(root: Path, files: list[Path]) -> dict:
    doc = root_file(root, "verificacao.md", "verificação.md")
    text = read_text(doc) if doc else ""
    numbers = RE_NUMBER.findall(RE_URL.sub(" ", text))
    official = RE_OFFICIAL.search(text)
    return {
        "numero": 5, "modulo": 8, "titulo": "Números conferidos",
        "checagens": [
            check("arquivo_verificacao", "Existe verificacao.md na raiz", doc,
                  doc.name if doc else "verificacao.md não encontrado na raiz do projeto"),
            check("dois_numeros", "O arquivo contém pelo menos dois números",
                  len(numbers) >= 2, f"{len(numbers)} números no texto"),
            check("cita_fonte_oficial", "O arquivo cita uma fonte oficial", bool(official),
                  official.group(0) if official else "nenhum endereço do IBGE ou do INEP"),
        ],
        "arquivos_para_ler": [doc.name] if doc else [],
    }


def marco_6(root: Path, files: list[Path]) -> dict:
    is_repo = (root / ".git").exists()
    readme = root_file(root, "README.md")
    commits, remote = 0, ""
    commits_note = remote_note = "a pasta ainda não é um repositório Git"
    extras: list[dict] = []
    if is_repo:
        ok, out = git(root, "rev-list", "--count", "HEAD")
        commits = int(out) if ok and out.isdigit() else 0
        commits_note = f"{commits} commits" if ok else "nenhum commit ainda"
        ok, out = git(root, "remote", "get-url", "origin")
        remote = out if ok else ""
        remote_note = remote if remote else "nenhum endereço remoto configurado"
        ok, out = git(root, "status", "--porcelain")
        pending = len(out.splitlines()) if ok else 0
        extras.append(check(
            "alteracoes_nao_salvas", "Não há alterações fora de commit", pending == 0,
            "tudo salvo em commit" if pending == 0 else f"{pending} arquivos alterados fora de commit",
            informativo=True))
        ok, out = git(root, "rev-list", "--count", "@{u}..HEAD")
        if ok and out.isdigit():
            extras.append(check(
                "commits_enviados", "Todos os commits foram enviados", out == "0",
                "tudo enviado" if out == "0" else f"{out} commits ainda não enviados",
                informativo=True))
        else:
            extras.append(check(
                "commits_enviados", "Todos os commits foram enviados", False,
                "o ramo local ainda não está ligado a um ramo no GitHub", informativo=True))
    return {
        "numero": 6, "modulo": 10, "titulo": "Projeto publicado",
        "checagens": [
            check("repositorio_git", "A pasta é um repositório Git", is_repo,
                  "pasta .git presente" if is_repo else "sem pasta .git"),
            check("dois_commits", "Há pelo menos dois commits", commits >= 2, commits_note),
            check("remoto_github", "Há um endereço remoto no GitHub",
                  "github.com" in remote.lower(), remote_note),
            check("readme", "Existe README.md na raiz", readme,
                  readme.name if readme else "README.md não encontrado na raiz do projeto"),
            *extras,
        ],
        "arquivos_para_ler": [readme.name] if readme else [],
    }


def situacao(checagens: list[dict]) -> str:
    required = [c["ok"] for c in checagens if not c["informativo"]]
    if all(required):
        return "feito"
    return "em_andamento" if any(required) else "nao_iniciado"


def build_report(root: Path, only: int | None = None) -> dict:
    files = project_files(root)
    marcos = []
    for builder in (marco_1, marco_2, marco_3, marco_4, marco_5, marco_6):
        marco = builder(root, files)
        marco["situacao"] = situacao(marco["checagens"])
        marcos.append(marco)
    data_file = root / "dados" / "municipios.csv"
    report = {
        "pasta": str(root),
        "python": sys.version.split()[0],
        "dados_presentes": data_file.is_file(),
        "resumo": {
            "feitos": sum(m["situacao"] == "feito" for m in marcos),
            "total": len(marcos),
        },
        "marcos": [m for m in marcos if only in (None, m["numero"])],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pasta", nargs="?", help="pasta do projeto (padrão: a que contém esta skill)")
    parser.add_argument("--marco", type=int, choices=range(1, 7), help="mostra só um marco")
    args = parser.parse_args()

    root = Path(args.pasta).resolve() if args.pasta else default_root()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not root.is_dir():
        print(json.dumps({"erro": f"pasta não encontrada: {root}"}, ensure_ascii=False))
        return 1
    print(json.dumps(build_report(root, args.marco), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
