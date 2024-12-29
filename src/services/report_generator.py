from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from src.models.schemas import ReportRequest

class ReportGenerator:
    #TODO mudar para algo com htlm ou assim
    def generate_report(self, data: ReportRequest) -> bytes:
        """
        Generates a PDF report based on the data provided.
        """
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Add header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, f"Inventory Report - Company: {data.company_name}")
        c.setFont("Helvetica", 12)
        c.drawString(100, 780, f"Restaurant: {data.restaurant_name}")
        c.drawString(100, 760, f"Report Issuer: {data.user_name}")
        c.drawString(100, 740, f"Closing Date: {data.inventory_close_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Add products
        y = 700
        for product in data.products:
            c.drawString(100, y, f"Product: {product.product_id} | Quantity: {product.quantity}")
            y -= 20
            if y < 50:  # Add new page if necessary
                c.showPage()
                y = 800

        # Finalize the PDF
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
