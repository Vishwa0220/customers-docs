#!/usr/bin/env python3
"""
Script to update HTML files with the fixed SVG content from the images folder.
The HTML files have inline SVGs that need to be replaced with the fixed versions.
"""

import os
import re
import glob

def get_svg_id_mapping(html_path):
    """Get mapping of SVG position to external file name based on document name."""
    basename = os.path.basename(html_path).replace('.html', '')
    images_dir = '/home/ubuntu/go/src/customers-docs/docs/images'

    # Find all SVG files for this document
    svg_files = sorted(glob.glob(os.path.join(images_dir, f'{basename}_diagram_*.svg')))
    return svg_files

def read_svg_file(filepath):
    """Read SVG file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def update_html_with_svgs(html_path):
    """Update HTML file by replacing inline SVGs with fixed versions."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Get the SVG files for this document
    svg_files = get_svg_id_mapping(html_path)

    if not svg_files:
        print(f"  No SVG files found for {os.path.basename(html_path)}")
        return False

    # Find all inline SVGs in the HTML
    # Pattern to match SVG elements inside diagram divs
    svg_pattern = r'(<div class="diagram">\s*)(<svg[^>]*>.*?</svg>)(\s*</div>)'

    matches = list(re.finditer(svg_pattern, html_content, flags=re.DOTALL))

    if len(matches) != len(svg_files):
        print(f"  Warning: {os.path.basename(html_path)} has {len(matches)} inline SVGs but {len(svg_files)} SVG files")

    # Replace SVGs from last to first to preserve positions
    modified = False
    for i in range(min(len(matches), len(svg_files)) - 1, -1, -1):
        match = matches[i]
        svg_file = svg_files[i]

        new_svg_content = read_svg_file(svg_file)

        # Reconstruct the diagram div with new SVG
        new_block = match.group(1) + new_svg_content + match.group(3)

        html_content = html_content[:match.start()] + new_block + html_content[match.end():]
        modified = True

    if modified:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  Updated {os.path.basename(html_path)} with {min(len(matches), len(svg_files))} SVGs")
        return True

    return False

def main():
    """Main function to update all HTML files."""
    html_dir = '/home/ubuntu/go/src/customers-docs/docs/html'

    # Get all HTML files (excluding index.html)
    html_files = [f for f in glob.glob(os.path.join(html_dir, '*.html'))
                  if not f.endswith('index.html')]

    print(f"Found {len(html_files)} HTML files to update")
    print("-" * 50)

    updated_count = 0
    for html_path in sorted(html_files):
        if update_html_with_svgs(html_path):
            updated_count += 1

    print("-" * 50)
    print(f"Updated {updated_count} out of {len(html_files)} HTML files")

if __name__ == '__main__':
    main()
