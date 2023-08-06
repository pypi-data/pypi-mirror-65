from rest_framework.renderers import BaseRenderer

from puppeteer_pdf import render_pdf_from_template
from puppeteer_pdf.views import PDFResponse


class PDFReportRendererPuppeteer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if data is None:
            return bytes()

        context = {}

        pdf = render_pdf_from_template(
            input_template='table_renderer_template.html',
            header_template='pdf_renderer_header.html',
            footer_template='pdf_renderer_footer.html',
            context=context,
            cmd_options={
                'format': 'A3',
                'scale': '0.9',
                'landscape': True,
                'displayHeaderFooter': True,
                'marginTop': '90px',
                'marginLeft': '50px',
                'marginRight': '50px',
                'marginBottom': '50px',
            }
        )
        return PDFResponse(pdf)
