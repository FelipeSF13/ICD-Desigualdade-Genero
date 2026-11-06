
"""
Executa o treinamento do modelo preditivo
para o projeto Desigualdade de Gênero.
"""

from modelo import treinar_e_salvar


def main():
    print("=" * 50)
    print("MODELAGEM PREDITIVA - PNAD CONTÍNUA")
    print("Desigualdade de gênero em São Paulo")
    print("=" * 50)

    print("\nIniciando treinamento...\n")

    metricas = treinar_e_salvar()

    print("\nTreinamento concluído com sucesso!")
    print(f"Registros utilizados: {metricas['n_total']}")
    print(f"MAE: R$ {metricas['mae_reais']:.2f}")
    print(f"R²: {metricas['r2']:.4f}")

    print("\nArquivos gerados na pasta modelos:")
    print("- modelo_rendimento.joblib")
    print("- metricas_modelo.json")


if __name__ == "__main__":
    main()
