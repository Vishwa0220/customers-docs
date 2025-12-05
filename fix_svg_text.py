#!/usr/bin/env python3
"""
Script to fix SVG files with foreignObject elements that don't render in PDFs.
Converts foreignObject elements containing text to native SVG text elements.
"""

import os
import re
import glob
from html import unescape

def extract_text_from_foreignobject(fo_content):
    """Extract text content from foreignObject HTML content."""
    # Look for text in nodeLabel or edgeLabel spans
    text_match = re.search(r'<span class="(?:nodeLabel|edgeLabel)"[^>]*>(?:<p>)?([^<]*?)(?:</p>)?</span>', fo_content)
    if text_match:
        text = text_match.group(1)
        # Unescape HTML entities
        text = unescape(text)
        return text.strip()

    # Try to find text in p tags
    p_match = re.search(r'<p>([^<]*)</p>', fo_content)
    if p_match:
        return unescape(p_match.group(1).strip())

    return ""

def convert_foreignobject_to_text(svg_content):
    """Convert foreignObject elements to native SVG text elements."""

    # Pattern to find label groups with foreignObject containing nodeLabel
    # This handles the node labels
    node_pattern = r'(<g class="label"[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>)\s*<rect[^/]*/>\s*<foreignObject width="([^"]+)" height="([^"]+)">\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*(</g>)'

    def replace_node_label(match):
        g_open = match.group(1)
        tx = float(match.group(2))
        ty = float(match.group(3))
        width = float(match.group(4))
        height = float(match.group(5))
        div_content = match.group(6)
        g_close = match.group(7)

        text = extract_text_from_foreignobject(div_content)
        if not text:
            return match.group(0)

        # Calculate text position (center of the foreignObject area)
        text_x = width / 2
        text_y = height / 2 + 5  # Slight adjustment for vertical centering

        # Create SVG text element
        text_element = f'<text x="{text_x}" y="{text_y}" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 14px; fill: #333;">{text}</text>'

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(node_pattern, replace_node_label, svg_content, flags=re.DOTALL)

    # Pattern for cluster labels (subgraph titles)
    cluster_pattern = r'(<g class="cluster-label"[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>)\s*<foreignObject width="([^"]+)" height="([^"]+)">\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*(</g>)'

    def replace_cluster_label(match):
        g_open = match.group(1)
        tx = float(match.group(2))
        ty = float(match.group(3))
        width = float(match.group(4))
        height = float(match.group(5))
        div_content = match.group(6)
        g_close = match.group(7)

        text = extract_text_from_foreignobject(div_content)
        if not text:
            return match.group(0)

        text_x = width / 2
        text_y = height / 2 + 5

        text_element = f'<text x="{text_x}" y="{text_y}" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 14px; fill: #333;">{text}</text>'

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(cluster_pattern, replace_cluster_label, svg_content, flags=re.DOTALL)

    # Also handle edge labels if they have content
    edge_pattern = r'(<g class="edgeLabel"[^>]*>)\s*<g class="label"[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>\s*<foreignObject[^>]*>\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*</g>\s*(</g>)'

    def replace_edge_label(match):
        g_open = match.group(1)
        tx = match.group(2)
        ty = match.group(3)
        div_content = match.group(4)
        g_close = match.group(5)

        text = extract_text_from_foreignobject(div_content)
        if not text:
            return match.group(0)

        text_element = f'<g class="label" transform="translate({tx}, {ty})"><text x="0" y="0" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 12px; fill: #333;">{text}</text></g>'

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(edge_pattern, replace_edge_label, svg_content, flags=re.DOTALL)

    return svg_content

def process_svg_file(filepath):
    """Process a single SVG file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if this file has foreignObject elements
    if '<foreignObject' not in content:
        print(f"  Skipping {os.path.basename(filepath)} - no foreignObject elements")
        return False

    new_content = convert_foreignobject_to_text(content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Fixed {os.path.basename(filepath)}")
        return True
    else:
        print(f"  No changes needed for {os.path.basename(filepath)}")
        return False

def main():
    """Main function to process all SVG files."""
    svg_dir = '/home/ubuntu/go/src/customers-docs/docs/images'
    svg_files = glob.glob(os.path.join(svg_dir, '*.svg'))

    print(f"Found {len(svg_files)} SVG files to process")
    print("-" * 50)

    fixed_count = 0
    for filepath in sorted(svg_files):
        if process_svg_file(filepath):
            fixed_count += 1

    print("-" * 50)
    print(f"Fixed {fixed_count} out of {len(svg_files)} files")

if __name__ == '__main__':
    main()
