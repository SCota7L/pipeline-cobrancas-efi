"""Extrai séries do SGS (Banco Central) e salva em data/raw/ como CSV."""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

SERIES = {
    "selic_diaria": 11,
    "cdi_diario": 12,
    "meta_selic": 432,
    "ipca_mensal": 433,
}

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
PASTA_SAIDA = Path(__file__).resolve().parent.parent / "data" / "raw"


def extrair_serie(codigo: int, inicio: date, fim: date) -> pd.DataFrame:
    params = {
        "formato": "json",
        "dataInicial": inicio.strftime("%d/%m/%Y"),
        "dataFinal": fim.strftime("%d/%m/%Y"),
    }
    resposta = requests.get(URL.format(codigo=codigo), params=params, timeout=30)
    resposta.raise_for_status()

    df = pd.DataFrame(resposta.json())
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"])
    return df


def main() -> None:
    fim = date.today()
    inicio = fim - timedelta(days=365)
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    for nome, codigo in SERIES.items():
        df = extrair_serie(codigo, inicio, fim)
        df.to_csv(PASTA_SAIDA / f"{nome}.csv", index=False)
        print(f"{nome}: {len(df)} registros")


if __name__ == "__main__":
    main()
