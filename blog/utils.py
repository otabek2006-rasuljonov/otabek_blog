from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


def generate_pdf_resume(about, experiences, projects, language='en'):
    """Generate PDF resume/CV"""
    buffer = BytesIO()
    
    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a202c'),
        spaceAfter=6,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=6,
        borderPadding=5,
        borderColor=colors.HexColor('#cbd5e0'),
        borderWidth=0.5,
        borderRadius=2,
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
    )
    
    elements = []
    
    # Header with name and contact info
    elements.append(Paragraph(about.title, title_style))
    elements.append(Spacer(1, 0.1*inch))
    
    contact_info = f"{about.email}"
    if about.phone:
        contact_info += f" | {about.phone}"
    if about.location:
        contact_info += f" | {about.location}"
    
    elements.append(Paragraph(contact_info, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Bio/Summary
    elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    bio_text = about.bio.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
    elements.append(Paragraph(bio_text[:500], body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Experience
    if experiences:
        elements.append(Paragraph("EXPERIENCE", heading_style))
        
        for exp in experiences[:5]:  # Show top 5 experiences
            exp_header = f"<b>{exp.position}</b> - {exp.company}"
            elements.append(Paragraph(exp_header, body_style))
            
            date_range = f"{exp.start_date.strftime('%b %Y')} - "
            if exp.end_date:
                date_range += exp.end_date.strftime('%b %Y')
            else:
                date_range += "Present"
            
            elements.append(Paragraph(date_range, ParagraphStyle('Small', parent=styles['Normal'], fontSize=9)))
            
            if exp.description:
                desc_text = exp.description.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
                elements.append(Paragraph(desc_text[:200], body_style))
            
            elements.append(Spacer(1, 0.08*inch))
        
        elements.append(Spacer(1, 0.1*inch))
    
    # Skills
    if about.skills:
        elements.append(Paragraph("SKILLS", heading_style))
        skills_text = about.skills.replace('\n', ' | ')
        elements.append(Paragraph(skills_text, body_style))
        elements.append(Spacer(1, 0.15*inch))
    
    # Featured Projects
    if projects:
        elements.append(Paragraph("FEATURED PROJECTS", heading_style))
        
        for project in projects[:3]:
            proj_header = f"<b>{project.title}</b>"
            elements.append(Paragraph(proj_header, body_style))
            
            if project.description:
                desc_text = project.description.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
                elements.append(Paragraph(desc_text[:150], body_style))
            
            if project.technologies:
                tech = f"<i>Tech: {project.technologies}</i>"
                elements.append(Paragraph(tech, ParagraphStyle('Small', parent=styles['Normal'], fontSize=9)))
            
            elements.append(Spacer(1, 0.08*inch))
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
    elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=2)))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer.read()
