# # pdf_utils.py


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO

def generate_attendance_report_pdf(attendance_data, report_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # Title of the report
    title = f"{report_type.capitalize()} Absence Report"
    elements.append(Paragraph(title, styles['Title']))

    # Table header
    table_data = [
        ["Student Name", "Class", "Date", "Guardian Number", "Presence","father_name"]
    ]

    # Iterate through attendance data and append rows for each absence
    for item in attendance_data:
        table_data.append([
            item['student__name'],            # Student's name
            item['school_class__name'],       # Class name
            item['date'].strftime('%Y-%m-%d'), # Date of absence
            item['student__father_nammber'],  # Guardian's contact number
            'Absent',                          # Mark as absent student__father
            item['student__father'],
        ])

    # Create the table with the gathered data
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),         # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),    # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                # Center alignment for all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),      # Header font style
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),               # Bottom padding for header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),       # Background color for the rest of the table
        ('GRID', (0, 0), (-1, -1), 1, colors.black),          # Add grid lines to the table
    ]))

    elements.append(table)
    
    # Build the PDF document with the elements
    doc.build(elements)

    buffer.seek(0)
    return buffer






# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from io import BytesIO

# def generate_attendance_report_pdf(attendance_data, report_type):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)

#     styles = getSampleStyleSheet()
#     elements = []

#     title = f"{report_type.capitalize()} Absence report"
#     elements.append(Paragraph(title, styles['Title']))

#     table_data = [
#         ["Student Name", "Class", "Date","Guardian number" ,"Presence"]
#     ]

#     for item in attendance_data:
#         table_data.append([
#             item['student__name'],
#             item['school_class__name'],
#             item['date'].strftime('%Y-%m-%d'),
#             item['student__father_nammber'],
#             'Absent'

#             # 'Present' if item['is_present'] else 'Absent'
#         ])

#     table = Table(table_data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(table)
#     doc.build(elements)

#     buffer.seek(0)
#     return buffer
