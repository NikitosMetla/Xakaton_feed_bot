from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

class PdfExtractor:
    def __init__(self, title: str):
        self.title = title
        self.styles = getSampleStyleSheet()
        self._register_fonts()
        self.story = []
        self._setup_document()

    def _register_fonts(self):
        # Register a font that supports Cyrillic characters
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'utils/DejaVuSans.ttf'))

        # Update styles to use this font
        for style in self.styles.byName.values():
            style.fontName = 'DejaVuSans'

        # Create a custom title style with a unique name
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontName='DejaVuSans',
            fontSize=18,
            spaceAfter=12,
        ))

    def _setup_document(self):
        title_style = self.styles['CustomTitle']
        self.story.append(Paragraph(self.title, title_style))

    def add_text(self, text: str, style_name='BodyText'):
        style = self.styles[style_name]
        self.story.append(Paragraph(text, style))

    def add_image(self, image_bytes: BytesIO, width=4 * inch, height=3 * inch):
        img = Image(image_bytes)
        img.drawHeight = height
        img.drawWidth = width
        self.story.append(img)

    def save_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        doc.build(self.story)
        buffer.seek(0)
        return buffer.getvalue()