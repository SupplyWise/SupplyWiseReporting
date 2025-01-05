from weasyprint import HTML
from jinja2 import Environment, PackageLoader, select_autoescape
from src.models.schemas import ReportCreateRequest
from src.models.entities import ItemCategory
from datetime import datetime
from collections import defaultdict

class ReportGenerator:
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('src', 'templates'),
            autoescape=select_autoescape(['html'])
        )
        
    def generate_report(self, data: ReportCreateRequest) -> bytes:

        # Fix the category order for every report
        category_order = [
            ItemCategory.DRINKABLE,
            ItemCategory.EATABLE,
            ItemCategory.CUSTOM,
            ItemCategory.UNKNOWN
        ]

        # Group items by category
        items_by_category = defaultdict(list)
        for item in data.inventory_data.items:
            items_by_category[item.category].append(item)

        # Sort items by category and remove empty categories
        ordered_items_by_category = {
            category: items_by_category[category]
            for category in category_order
            if category in items_by_category and items_by_category[category]
        }

        # Render the report template with all the data
        template = self.env.get_template('report_template.html')
        html_content = template.render(
            report=data,
            items_by_category=ordered_items_by_category,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return HTML(string=html_content).write_pdf()