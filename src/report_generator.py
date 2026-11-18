
"""
Génère automatiquement le rapport Excel mensuel avec Actual vs Budget.
"""
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference
from datetime import datetime

class ReportGenerator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate(self, month: str, output_path: str):
        wb = Workbook()

        # ===== FEUILLE 1 : SYNTHÈSE =====
        ws = wb.active
        ws.title = "Summary"

        # Titre
        ws['A1'] = f"Monthly Financial Report — {month}"
        ws['A1'].font = Font(size=16, bold=True, color="1F4E78")
        ws.merge_cells('A1:F1')
        ws['A1'].alignment = Alignment(horizontal='center')

        ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ws['A2'].font = Font(italic=True, size=10, color="666666")

        # KPIs
        monthly = self.df[self.df['month'] == month]
        total_budget = monthly['budget'].sum()
        total_actual = monthly['actual'].sum()
        total_variance = total_actual - total_budget
        variance_pct = (total_variance / total_budget * 100) if total_budget else 0

        ws['A4'] = "KPI"
        ws['B4'] = "Value"
        for cell in ['A4', 'B4']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill("solid", fgColor="1F4E78")

        kpis = [
            ("Total Budget", f"${total_budget:,.2f}"),
            ("Total Actual", f"${total_actual:,.2f}"),
            ("Variance", f"${total_variance:,.2f}"),
            ("Variance %", f"{variance_pct:.2f}%"),
            ("Status", "⚠️ OVER BUDGET" if total_variance > 0 else "✅ UNDER BUDGET"),
        ]
        for i, (k, v) in enumerate(kpis, start=5):
            ws[f'A{i}'] = k
            ws[f'B{i}'] = v
            ws[f'A{i}'].font = Font(bold=True)

        # ===== FEUILLE 2 : DÉTAIL PAR DÉPARTEMENT =====
        ws2 = wb.create_sheet("By Department")

        headers = ['Department', 'Budget', 'Actual', 'Variance', 'Variance %', 'Status']
        for col, h in enumerate(headers, 1):
            cell = ws2.cell(row=1, column=col, value=h)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E78")
            cell.alignment = Alignment(horizontal='center')

        for row, (_, data) in enumerate(monthly.iterrows(), start=2):
            ws2.cell(row=row, column=1, value=data['department'])
            ws2.cell(row=row, column=2, value=f"${data['budget']:,.2f}")
            ws2.cell(row=row, column=3, value=f"${data['actual']:,.2f}")
            ws2.cell(row=row, column=4, value=f"${data['variance']:,.2f}")
            ws2.cell(row=row, column=5, value=f"{data['variance_pct']:.2f}%")

            # Coloration conditionnelle
            if abs(data['variance_pct']) > 40:
                status = "🚨 ANOMALY"
                fill = PatternFill("solid", fgColor="FF6B6B")
            elif abs(data['variance_pct']) > 15:
                status = "⚠️  Warning"
                fill = PatternFill("solid", fgColor="FFE66D")
            else:
                status = "✅ OK"
                fill = PatternFill("solid", fgColor="95E1A3")

            ws2.cell(row=row, column=6, value=status)
            for col in range(1, 7):
                ws2.cell(row=row, column=col).fill = fill

        # Graphique
        chart = BarChart()
        chart.title = f"Budget vs Actual — {month}"
        chart.y_axis.title = "Amount ($)"
        chart.x_axis.title = "Department"

        data = Reference(ws2, min_col=2, max_col=3, min_row=1, max_row=len(monthly)+1)
        cats = Reference(ws2, min_col=1, min_row=2, max_row=len(monthly)+1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        ws2.add_chart(chart, "H2")

        # ===== FEUILLE 3 : ANOMALIES =====
        ws3 = wb.create_sheet("Anomalies")
        anomalies = monthly[monthly.get('anomaly_label', pd.Series()) == 'Anomaly'] if 'anomaly_label' in monthly else pd.DataFrame()

        if len(anomalies) > 0:
            ws3['A1'] = "🚨 Detected Anomalies"
            ws3['A1'].font = Font(size=14, bold=True, color="C00000")
            for col, h in enumerate(['Department', 'Budget', 'Actual', 'Variance %'], 1):
                ws3.cell(row=3, column=col, value=h).font = Font(bold=True)
            for row, (_, data) in enumerate(anomalies.iterrows(), start=4):
                ws3.cell(row=row, column=1, value=data['department'])
                ws3.cell(row=row, column=2, value=data['budget'])
                ws3.cell(row=row, column=3, value=data['actual'])
                ws3.cell(row=row, column=4, value=data['variance_pct'])
        else:
            ws3['A1'] = "✅ No anomalies detected this month"

        wb.save(output_path)
        print(f"✅ Report saved: {output_path}")


if __name__ == "__main__":
    df = pd.read_csv("data/processed/financial_data_scored.csv")

    # Trouver le dernier mois disponible
    last_month = df['month'].max()

    generator = ReportGenerator(df)
    generator.generate(
        month=last_month,
        output_path=f"reports/generated/report_{last_month.replace('-', '_')}.xlsx"
    )