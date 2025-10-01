# utils.py
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_comparison_table(store, competitors):
    table = pd.DataFrame({
        "지표": ["배달비율", "재방문율", "신규고객비율"],
        "해당 매장": [store["배달비율"], store["재방문율"], store["신규고객비율"]],
        "경쟁 평균": [
            competitors["배달비율"].mean(),
            competitors["재방문율"].mean(),
            competitors["신규고객비율"].mean()
        ]
    })

    percentile = {
        "배달비율": store["배달비율"] / (competitors["배달비율"].max() + 1e-5) * 100,
        "재방문율": store["재방문율"] / (competitors["재방문율"].max() + 1e-5) * 100,
    }

    return table, percentile

def export_pdf(store, table, strategies, caption):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph("📌 마케팅 전략 리포트", styles['Heading1'])]

    for i, s in enumerate(strategies, 1):
        content.append(Paragraph(f"{i}. {s}", styles['Normal']))
    content.append(Paragraph("💬 마케팅 문구: " + caption, styles['Normal']))

    doc.build(content)
    return buffer.getvalue()
