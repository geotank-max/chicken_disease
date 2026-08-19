# app/services/pdf_service.py
import os
from io import BytesIO
from flask import render_template, current_app
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT


def _register_khmer_font():
    """Register Noto Sans Khmer font with xhtml2pdf."""
    from reportlab.lib.fonts import addMapping
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_path = os.path.join(
        current_app.root_path, "static", "fonts", "NotoSansKhmer.ttf"
    )
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont("NotoSansKhmer", font_path))
            addMapping("NotoSansKhmer", 0, 0, "NotoSansKhmer")  # normal
            addMapping("NotoSansKhmer", 1, 0, "NotoSansKhmer")  # bold (same file)
            return True
        except Exception:
            return False
    return False


def _link_callback(uri, rel):
    """Resolve static file paths for xhtml2pdf."""
    static_dir = os.path.join(current_app.root_path, "static")
    if uri.startswith("/static/"):
        return os.path.join(static_dir, uri.replace("/static/", ""))
    if uri.startswith("static/"):
        return os.path.join(static_dir, uri.replace("static/", ""))
    return uri


class PdfService:
    @staticmethod
    def render_case_pdf(case) -> BytesIO | None:
        _register_khmer_font()
        html = render_template("expert_system/cases/print.html", case=case, pdf_mode=True)
        buffer = BytesIO()
        result = pisa.CreatePDF(
            html,
            dest=buffer,
            encoding="utf-8",
            link_callback=_link_callback,
        )
        if result.err:
            return None
        buffer.seek(0)
        return buffer
