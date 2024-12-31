from weasyprint import HTML
from jinja2 import Environment, PackageLoader, select_autoescape
from src.models.schemas import ReportCreateRequest
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('src', 'templates'),
            autoescape=select_autoescape(['html'])
        )
        
    def generate_report(self, data: ReportCreateRequest) -> bytes:
        template = self.env.get_template('report_template.html')
        html_content = template.render(
            report=data,
            current_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return HTML(string=html_content).write_pdf()