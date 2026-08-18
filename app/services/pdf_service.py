from io import BytesIO
from flask import render_template
from xhtml2pdf import pisa


class PdfService:
    @staticmethod
    def render_case_pdf(case) -> BytesIO | None:
        html = render_template("expert_system/cases/print.html", case=case, pdf_mode=True)
        buffer = BytesIO()
        result = pisa.CreatePDF(html, dest=buffer, encoding="utf-8")
        if result.err:
            return None
        buffer.seek(0)
        return buffer
