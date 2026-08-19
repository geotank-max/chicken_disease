# app/services/pdf_service.py
import os
from io import BytesIO
from flask import render_template, current_app
from xhtml2pdf import pisa


def _fetch_resource(uri, rel):
    """Resolve static file paths for xhtml2pdf."""
    if uri.startswith("http"):
        return uri
    static_dir = os.path.join(current_app.root_path, "static")
    path = os.path.join(static_dir, uri.replace("/static/", ""))
    return path


class PdfService:
    @staticmethod
    def render_case_pdf(case) -> BytesIO | None:
        html = render_template("expert_system/cases/print.html", case=case, pdf_mode=True)
        buffer = BytesIO()
        result = pisa.CreatePDF(
            html,
            dest=buffer,
            encoding="utf-8",
            link_callback=_fetch_resource,
        )
        if result.err:
            return None
        buffer.seek(0)
        return buffer
