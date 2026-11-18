"""
Contrôles de qualité, cohérence et traçabilité des données.
"""
import pandas as pd
from datetime import datetime

class DataQualityChecker:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.report = []

    def run_all(self):
        print("🔍 Running Data Quality Checks...\n")
        self.check_missing_values()
        self.check_duplicates()
        self.check_negative_values()
        self.check_variance_consistency()
        self.check_department_consistency()
        self.check_data_completeness()
        return self.report

    def check_missing_values(self):
        nulls = self.df.isnull().sum()
        total = nulls.sum()
        status = "✅ PASS" if total == 0 else f"⚠️  {total} nulls found"
        self.report.append(f"[MISSING VALUES] {status}")
        print(f"1. Missing values: {status}")

    def check_duplicates(self):
        dups = self.df.duplicated(subset=['month', 'department']).sum()
        status = "✅ PASS" if dups == 0 else f"⚠️  {dups} duplicates"
        self.report.append(f"[DUPLICATES] {status}")
        print(f"2. Duplicates: {status}")

    def check_negative_values(self):
        neg = ((self.df['budget'] < 0) | (self.df['actual'] < 0)).sum()
        status = "✅ PASS" if neg == 0 else f"❌ {neg} negative values"
        self.report.append(f"[NEGATIVE VALUES] {status}")
        print(f"3. Negative values: {status}")

    def check_variance_consistency(self):
        expected = self.df['actual'] - self.df['budget']
        diff = (self.df['variance'] - expected).abs()
        inconsistent = (diff > 0.01).sum()
        status = "✅ PASS" if inconsistent == 0 else f"❌ {inconsistent} inconsistent"
        self.report.append(f"[VARIANCE CONSISTENCY] {status}")
        print(f"4. Variance consistency: {status}")

    def check_department_consistency(self):
        invalid = self.df[~self.df['department'].isin(['Furniture', 'Office Supplies', 'Technology'])]
        if len(invalid) > 0:
            status = f"⚠️  {len(invalid)} rows with non-standard department names"
        else:
            status = "✅ PASS"
        self.report.append(f"[DEPARTMENT CONSISTENCY] {status}")
        print(f"5. Department naming: {status}")

    def check_data_completeness(self):
        expected_months = self.df['month'].nunique()
        expected_depts = self.df['department'].str.title().nunique()
        total_expected = expected_months * 3  # 3 departments
        completeness = len(self.df.drop_duplicates(subset=['month', 'department'])) / total_expected * 100
        status = "✅ PASS" if completeness >= 95 else f"⚠️  Only {completeness:.1f}% complete"
        self.report.append(f"[COMPLETENESS] {status}")
        print(f"6. Data completeness: {status} ({completeness:.1f}%)")


if __name__ == "__main__":
    df = pd.read_csv("data/processed/financial_data.csv")
    checker = DataQualityChecker(df)
    report = checker.run_all()

    # Sauvegarder le rapport
    with open("reports/quality_report.txt", "w") as f:
        f.write(f"Data Quality Report — {datetime.now()}\n")
        f.write("=" * 50 + "\n")
        f.write("\n".join(report))
    print(f"\n📄 Report saved to reports/quality_report.txt")