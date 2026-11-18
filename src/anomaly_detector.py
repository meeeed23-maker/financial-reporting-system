"""
Détection d'anomalies financières avec Isolation Forest (Machine Learning).
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class AnomalyDetector:
    def __init__(self, contamination=0.05, random_state=42):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.scaler = StandardScaler()

    def fit_predict(self, df: pd.DataFrame, features: list) -> pd.DataFrame:
        X = df[features].fillna(0).values
        X_scaled = self.scaler.fit_transform(X)

        df = df.copy()
        df['anomaly'] = self.model.fit_predict(X_scaled)
        df['anomaly_label'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})
        df['anomaly_score'] = self.model.score_samples(X_scaled)

        n_anomalies = (df['anomaly'] == -1).sum()
        print(f"🎯 Detected {n_anomalies} anomalies ({n_anomalies/len(df)*100:.1f}%)")
        return df

    def plot_anomalies(self, df: pd.DataFrame, save_path: str = None):
        fig, ax = plt.subplots(figsize=(14, 6))

        normal = df[df['anomaly'] == 1]
        anomalies = df[df['anomaly'] == -1]

        ax.scatter(normal['budget'], normal['actual'],
                   c='#2ecc71', label='Normal', alpha=0.6, s=50)
        ax.scatter(anomalies['budget'], anomalies['actual'],
                   c='#e74c3c', label='Anomaly', alpha=0.9, s=100, marker='X')

        ax.plot([0, df['budget'].max()], [0, df['budget'].max()],
                'k--', alpha=0.3, label='Ideal (actual = budget)')

        ax.set_xlabel('Budget ($)', fontsize=12)
        ax.set_ylabel('Actual ($)', fontsize=12)
        ax.set_title('Financial Anomaly Detection — Isolation Forest', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"📊 Plot saved: {save_path}")
        plt.show()


if __name__ == "__main__":
    # Charger les données nettoyées (après data_quality)
    df = pd.read_csv("data/processed/financial_data.csv")

    # Nettoyer avant ML
    df = df.dropna(subset=['budget', 'actual'])
    df['department'] = df['department'].str.title()
    df = df.drop_duplicates(subset=['month', 'department'])

    # Détection
    detector = AnomalyDetector(contamination=0.08)
    result = detector.fit_predict(df, features=['budget', 'actual', 'variance_pct'])

    # Sauvegarder avec les flags
    result.to_csv("data/processed/financial_data_scored.csv", index=False)

    # Visualiser
    detector.plot_anomalies(result, save_path="reports/anomaly_plot.png")

    # Top 5 anomalies
    print("\n🚨 Top 5 anomalies detected:")
    top = result[result['anomaly'] == -1].nlargest(5, 'variance_pct')[['month', 'department', 'budget', 'actual', 'variance_pct']]
    print(top.to_string(index=False))