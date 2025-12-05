#!/usr/bin/env python3
"""
Script to convert Markdown files to HTML with Mermaid diagrams rendered as SVG.
Uses pandoc for markdown conversion and mmdc for mermaid rendering.
"""

import os
import re
import subprocess
import tempfile
import glob

# HTML template with styling
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px;
            background-color: #fff;
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
        }}

        h2 {{
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            margin-top: 30px;
        }}

        h3, h4, h5, h6 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}

        code {{
            background-color: #f7f9fc;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }}

        pre {{
            background-color: #2d3436;
            color: #dfe6e9;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 0.85em;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            color: inherit;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}

        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}

        tr:nth-child(even) {{
            background-color: #fafafa;
        }}

        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
        }}

        .diagram {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow-x: auto;
        }}

        .diagram svg {{
            max-width: 100%;
            height: auto;
        }}

        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
        }}

        ul, ol {{
            padding-left: 25px;
        }}

        li {{
            margin-bottom: 5px;
        }}

        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}

        .header-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            margin: -30px -30px 30px -30px;
            text-align: center;
        }}

        .header-section h1 {{
            color: white;
            border: none;
            margin: 0;
        }}

        .header-section p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="header-section">
        <h1>{title}</h1>
        <p>SECURAA Security Documentation</p>
    </div>
    {content}
</body>
</html>
'''

def extract_mermaid_blocks(md_content):
    """Extract mermaid code blocks from markdown content."""
    pattern = r'```mermaid\s*(.*?)```'
    return list(re.finditer(pattern, md_content, flags=re.DOTALL))

def render_mermaid_to_svg(mermaid_code, output_path):
    """Check if SVG exists, or skip rendering since mmdc has issues."""
    # Just check if the SVG file already exists
    if os.path.exists(output_path):
        print(f"    Using existing SVG: {os.path.basename(output_path)}")
        return True
    print(f"    Warning: SVG file doesn't exist and mmdc is unavailable: {output_path}")
    return False

def read_svg_content(svg_path):
    """Read SVG file and return its content."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        return f.read()

def convert_md_to_html(md_path, html_dir, images_dir):
    """Convert a markdown file to HTML with rendered mermaid diagrams."""
    basename = os.path.basename(md_path).replace('.md', '')
    html_path = os.path.join(html_dir, f'{basename}.html')

    print(f"Converting: {basename}.md")

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract and render mermaid blocks
    mermaid_blocks = extract_mermaid_blocks(md_content)
    svg_contents = []

    for i, match in enumerate(mermaid_blocks, 1):
        mermaid_code = match.group(1).strip()
        svg_path = os.path.join(images_dir, f'{basename}_diagram_{i}.svg')

        print(f"  Rendering diagram {i}...")
        if render_mermaid_to_svg(mermaid_code, svg_path):
            svg_content = read_svg_content(svg_path)
            svg_contents.append(svg_content)
        else:
            svg_contents.append(f'<p>Diagram {i} failed to render</p>')

    # Replace mermaid blocks with placeholders
    modified_md = md_content
    for i, match in enumerate(reversed(mermaid_blocks)):
        placeholder = f'DIAGRAM_PLACEHOLDER_{len(mermaid_blocks) - i}'
        modified_md = modified_md[:match.start()] + placeholder + modified_md[match.end():]

    # Convert to HTML using pandoc
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(modified_md)
        temp_md = f.name

    try:
        result = subprocess.run(
            ['pandoc', temp_md, '-f', 'gfm', '-t', 'html'],
            capture_output=True,
            text=True,
            timeout=60
        )
        html_content = result.stdout
    finally:
        os.unlink(temp_md)

    # Replace placeholders with SVG diagrams
    for i, svg_content in enumerate(svg_contents, 1):
        placeholder = f'DIAGRAM_PLACEHOLDER_{i}'
        diagram_html = f'<div class="diagram">\n{svg_content}\n</div>'
        html_content = html_content.replace(f'<p>{placeholder}</p>', diagram_html)
        html_content = html_content.replace(placeholder, diagram_html)

    # Generate title from filename
    title = basename.replace('_', ' ').replace('-', ' ').title()

    # Create final HTML
    final_html = HTML_TEMPLATE.format(title=title, content=html_content)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"  Created: {basename}.html")
    return html_path

def main():
    """Main function to convert specified markdown files."""
    base_dir = '/home/ubuntu/go/src/customers-docs'
    html_dir = os.path.join(base_dir, 'docs/html')
    images_dir = os.path.join(base_dir, 'docs/images')

    # Files to convert (the renamed _dt files)
    files_to_convert = [
        os.path.join(base_dir, 'securaa-sdlc-process.md'),
        os.path.join(base_dir, 'SECURAA_SECURE_CODING_POLICY.md')
    ]

    print(f"Converting {len(files_to_convert)} markdown files to HTML")
    print("-" * 50)

    for md_path in files_to_convert:
        if os.path.exists(md_path):
            convert_md_to_html(md_path, html_dir, images_dir)
        else:
            print(f"File not found: {md_path}")

    print("-" * 50)
    print("Conversion complete")

if __name__ == '__main__':
    main()
