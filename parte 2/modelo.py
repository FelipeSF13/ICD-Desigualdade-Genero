
"""Treinamento e avaliação do modelo com dados da PNAD Contínua."""

from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "dados" / "dados_tratados.csv"
MODEL_PATH = ROOT / "modelos" / "modelo_rendimento.joblib"
METRICS_PATH = ROOT / "modelos" / "metricas_modelo.json"

FEATURES = ["Genero", "Idade", "Escolaridade", "Setor"]
CATEGORICAL = ["Genero", "Escolaridade", "Setor"]


def preparar_amostra(df):
    """Seleciona os registros válidos para a modelagem."""

    df = df.copy()

    for coluna in ["Rendimento", "Idade", "Peso", "Ocupado"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df = df[
        (df["Ocupado"] == 1)
        & (df["Rendimento"] > 0)
        & (df["Peso"] > 0)
        & df[FEATURES].notna().all(axis=1)
        & (df["Idade"] >= 14)
        & (df["Idade"] <= 110)
    ].copy()

    return df.reset_index(drop=True)


def treinar_e_salvar():
    """Treina o modelo, avalia os resultados e salva os arquivos."""

    df = preparar_amostra(pd.read_csv(DATA_PATH))

    if len(df) < 100:
        raise ValueError("Amostra insuficiente para treinar o modelo.")

    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        df[FEATURES],
        df["Rendimento"],
        df["Peso"],
        test_size=0.25,
        random_state=42,
        stratify=df["Genero"],
    )

    preprocessamento = ColumnTransformer(
        [
            (
                "categorias",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                CATEGORICAL,
            ),
            ("idade", "passthrough", ["Idade"]),
        ]
    )

    modelo = Pipeline(
        [
            ("preprocessamento", preprocessamento),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=80,
                    max_depth=12,
                    min_samples_leaf=25,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    # O treinamento usa o logaritmo do rendimento.
    # As previsões são convertidas novamente para reais.
    y_train_log = np.log1p(y_train)

    modelo.fit(
        X_train,
        y_train_log,
        regressor__sample_weight=w_train.to_numpy(),
    )

    previsoes = np.expm1(modelo.predict(X_test)).clip(min=0)

    media_referencia = np.average(y_train, weights=w_train)

    metricas = {
        "n_total": int(len(df)),
        "n_treino": int(len(X_train)),
        "n_teste": int(len(X_test)),
        "mae_reais": round(
            float(
                mean_absolute_error(
                    y_test,
                    previsoes,
                    sample_weight=w_test,
                )
            ),
            2,
        ),
        "r2": round(
            float(
                r2_score(
                    y_test,
                    previsoes,
                    sample_weight=w_test,
                )
            ),
            4,
        ),
        "mae_baseline_reais": round(
            float(
                mean_absolute_error(
                    y_test,
                    np.full(len(y_test), media_referencia),
                    sample_weight=w_test,
                )
            ),
            2,
        ),
        "metodo": "Random Forest Regressor com log1p do rendimento",
        "variaveis": FEATURES,
        "recorte": "SP, PNAD Contínua, 4º trimestre de 2025",
        "test_size": 0.25,
        "random_state": 42,
        "resultados_por_genero": [],
    }

    resultados_teste = X_test.copy()
    resultados_teste["Real"] = y_test.to_numpy()
    resultados_teste["Previsto"] = previsoes
    resultados_teste["Peso"] = w_test.to_numpy()

    for genero, grupo in resultados_teste.groupby("Genero"):
        metricas["resultados_por_genero"].append(
            {
                "genero": genero,
                "n": int(len(grupo)),
                "mae_reais": round(
                    float(
                        mean_absolute_error(
                            grupo["Real"],
                            grupo["Previsto"],
                            sample_weight=grupo["Peso"],
                        )
                    ),
                    2,
                ),
            }
        )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(modelo, MODEL_PATH, compress=3)

    METRICS_PATH.write_text(
        json.dumps(metricas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Modelo salvo em:", MODEL_PATH)
    print(json.dumps(metricas, ensure_ascii=False, indent=2))

    return metricas


if __name__ == "__main__":
    treinar_e_salvar()
