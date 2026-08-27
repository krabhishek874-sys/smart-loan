from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
def create_pdf(path,text):
 doc=SimpleDocTemplate(path); s=getSampleStyleSheet(); doc.build([Paragraph(text,s['BodyText'])])
