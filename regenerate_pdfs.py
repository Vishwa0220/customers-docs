#!/usr/bin/env python3
"""
Script to regenerate PDF files from HTML files using weasyprint.
The HTML files embed SVG diagrams which now have proper text elements.
"""

import os
import sys
import glob

# Add weasyprint from venv
sys.path.insert(0, '/tmp/pdfenv/lib/python3.12/site-packages')

from weasyprint import HTML, CSS

def regenerate_pdf(html_path, pdf_path):
    """Regenerate a single PDF from HTML."""
    print(f"  Generating: {os.path.basename(pdf_path)}")

    try:
        # Custom CSS to ensure good PDF output
        custom_css = CSS(string='''
            @page {
                size: A4;
                margin: 1.5cm;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 11pt;
                line-height: 1.4;
            }
            .diagram {
                page-break-inside: avoid;
            }
            svg {
                max-width: 100%;
                height: auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            pre {
                background-color: #f5f5f5;
                padding: 10px;
                font-size: 9pt;
                overflow-wrap: break-word;
                white-space: pre-wrap;
            }
        ''')

        html = HTML(filename=html_path, base_url=os.path.dirname(html_path))
        html.write_pdf(pdf_path, stylesheets=[custom_css])
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False

def main():
    """Main function to regenerate all PDFs."""
    html_dir = '/home/ubuntu/go/src/customers-docs/docs/html'
    pdf_dir = '/home/ubuntu/go/src/customers-docs/docs/pdf'

    # Get all HTML files (excluding index.html)
    html_files = [f for f in glob.glob(os.path.join(html_dir, '*.html'))
                  if not f.endswith('index.html')]

    print(f"Found {len(html_files)} HTML files to convert to PDF")
    print("-" * 50)

    success_count = 0
    for html_path in sorted(html_files):
        basename = os.path.basename(html_path)
        pdf_name = basename.replace('.html', '.pdf')
        pdf_path = os.path.join(pdf_dir, pdf_name)

        if regenerate_pdf(html_path, pdf_path):
            success_count += 1

    print("-" * 50)
    print(f"Successfully generated {success_count} out of {len(html_files)} PDFs")

if __name__ == '__main__':
    main()
