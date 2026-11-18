"""
Transforme le dataset Superstore en données de reporting financier mensuel.
Chaque ligne = 1 département × 1 mois, avec Budget (objectif) et Actual (réalisé).
"""
import pandas as pd
import numpy as np

np.random.seed(42)

def prepare_data(input_path: str, output_path: str) -> pd.DataFrame:
    # 1. Charger le dataset réel
    df = pd.read_csv(input_path, encoding='latin-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
    df['YearMonth'] = df['Order Date'].dt.to_period('M')

    # 2. Agréger par mois × catégorie (nos "départements" = Category)
    agg = df.groupby(['YearMonth', 'Category']).agg(
        actual_sales=('Sales', 'sum'),
        actual_profit=('Profit', 'sum'),
        n_orders=('Order ID', 'nunique')
    ).reset_index()
    agg['YearMonth'] = agg['YearMonth'].astype(str)

    # 3. Créer un BUDGET réaliste (objectif = moyenne historique ± variation)
    # Le budget est défini en début d'année = moyenne des 3 derniers mois + 5% de croissance
    rows = []
    for category in agg['Category'].unique():
        cat_df = agg[agg['Category'] == category].sort_values('YearMonth').copy()
        cat_df['rolling_avg'] = cat_df['actual_sales'].rolling(3, min_periods=1).mean()

        for _, row in cat_df.iterrows():
            # Budget = moyenne mobile + 5% croissance + bruit contrôlé
            budget = row['rolling_avg'] * 1.05
            budget += np.random.uniform(-0.05, 0.05) * budget  # ±5%

            rows.append({
                'month': row['YearMonth'],
                'department': category,
                'budget': round(budget, 2),
                'actual': round(row['actual_sales'], 2),
            })

    result = pd.DataFrame(rows)
    result['variance'] = result['actual'] - result['budget']
    result['variance_pct'] = (result['variance'] / result['budget'] * 100).round(2)

    # 4. INJECTER des problèmes de qualité réalistes
    print("🧪 Injection de problèmes de qualité...")

    # 4a. Valeurs manquantes (2%)
    mask = np.random.random(len(result)) < 0.02
    result.loc[mask, 'actual'] = np.nan
    print(f"   → {mask.sum()} valeurs manquantes ajoutées")

    # 4b. Doublons (1%)
    dups = result.sample(frac=0.01, random_state=42)
    result = pd.concat([result, dups], ignore_index=True)
    print(f"   → {len(dups)} doublons ajoutés")

    # 4c. Incohérences de casse (5%)
    idx = result.sample(frac=0.05, random_state=1).index
    result.loc[idx[:len(idx)//2], 'department'] = result.loc[idx[:len(idx)//2], 'department'].str.lower()
    result.loc[idx[len(idx)//2:], 'department'] = result.loc[idx[len(idx)//2:], 'department'].str.upper()
    print(f"   → {len(idx)} incohérences de casse ajoutées")

    # 4d. Anomalies financières (5%) — Écarts > 40%
    anomaly_idx = result.sample(frac=0.05, random_state=2).index
    result.loc[anomaly_idx, 'actual'] = result.loc[anomaly_idx, 'budget'] * np.random.uniform(0.3, 2.0, len(anomaly_idx))
    print(f"   → {len(anomaly_idx)} anomalies financières injectées")

    # 5. Recalculer variance pour les lignes modifiées
    result['variance'] = result['actual'] - result['budget']
    result['variance_pct'] = (result['variance'] / result['budget'] * 100).round(2)

    # 6. Sauvegarder
    result.to_csv(output_path, index=False)
    print(f"\n✅ Dataset prêt: {output_path}")
    print(f"   📊 {len(result)} lignes × {result.shape[1]} colonnes")
    return result


if __name__ == "__main__":
    prepare_data(
        input_path="data/raw/Sample - Superstore.csv",
        output_path="data/processed/financial_data.csv"
    )