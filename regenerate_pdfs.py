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
        # Custom CSS to ensure good PDF output with clear diagrams
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
                margin: 20px 0;
                padding: 15px;
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            /* SVG diagram styling for clarity */
            svg {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
            }
            /* Ensure SVG text is crisp and readable */
            svg text {
                font-family: 'trebuchet ms', verdana, arial, sans-serif;
                font-size: 14px;
            }
            svg tspan {
                font-family: 'trebuchet ms', verdana, arial, sans-serif;
            }
            /* Make diagram lines clear */
            svg .flowchart-link,
            svg .edgePath path {
                stroke-width: 2px !important;
            }
            /* Ensure node boxes are visible */
            svg .node rect,
            svg .node circle,
            svg .node ellipse,
            svg .node polygon {
                stroke-width: 1.5px !important;
            }
            /* Cluster/subgraph borders */
            svg .cluster rect {
                stroke-width: 1.5px !important;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            th {
                background-color: #f8f9fa;
            }
            pre {
                background-color: #f5f5f5;
                padding: 10px;
                font-size: 9pt;
                overflow-wrap: break-word;
                white-space: pre-wrap;
                border-radius: 4px;
            }
            code {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 0.9em;
            }
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
            }
            /* Avoid orphaned headers */
            h1 + *, h2 + *, h3 + * {
                page-break-before: avoid;
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
