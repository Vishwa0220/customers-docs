#!/usr/bin/env python3
"""
Script to fix SVG files with foreignObject elements that don't render in PDFs.
Converts foreignObject elements containing text to native SVG text elements.
Handles multi-line text, cluster labels, node labels, and edge labels.
"""

import os
import re
import glob
from html import unescape


def extract_text_lines_from_html(html_content):
    """
    Extract text content from HTML, handling multi-line content with <br /> tags.
    Returns a list of text lines.
    """
    # Remove the outer div and span wrappers
    content = html_content

    # Unescape HTML entities
    content = unescape(content)

    # Replace <br /> and <br> with a special marker
    content = re.sub(r'<br\s*/?>', '\n', content)

    # Remove all HTML tags but preserve text
    content = re.sub(r'<[^>]+>', '', content)

    # Split by newlines and clean up
    lines = [line.strip() for line in content.split('\n')]
    lines = [line for line in lines if line]  # Remove empty lines

    return lines


def extract_text_color_from_style(style_content):
    """Extract text color from style attribute."""
    # Look for fill or color in inline styles
    color_match = re.search(r'(?:fill|color):\s*([^;!]+)', style_content)
    if color_match:
        color = color_match.group(1).strip()
        # Handle rgb format
        if color.startswith('rgb'):
            return color
        # Handle hex and named colors
        if color and color != 'inherit':
            return color
    return '#333'


def create_multiline_svg_text(lines, width, height, font_size=14, fill='#333', font_weight='normal'):
    """
    Create SVG text element(s) for multi-line text.
    Uses tspan elements for proper line spacing.
    """
    if not lines:
        return ''

    line_height = font_size * 1.4
    total_height = len(lines) * line_height

    # Calculate starting y position to center all lines
    start_y = (height - total_height) / 2 + font_size
    center_x = width / 2

    if len(lines) == 1:
        # Single line - simple text element
        return f'<text x="{center_x}" y="{height/2 + font_size/3}" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: {font_size}px; fill: {fill}; font-weight: {font_weight};">{lines[0]}</text>'

    # Multi-line - use tspan elements
    tspans = []
    for i, line in enumerate(lines):
        y_pos = start_y + i * line_height
        tspans.append(f'<tspan x="{center_x}" y="{y_pos}">{line}</tspan>')

    tspan_content = ''.join(tspans)
    return f'<text text-anchor="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: {font_size}px; fill: {fill}; font-weight: {font_weight};">{tspan_content}</text>'


def convert_foreignobject_to_text(svg_content):
    """Convert foreignObject elements to native SVG text elements."""

    # Pattern 1: Node labels within g.label (with rect before foreignObject)
    # These are the main node boxes
    node_pattern = r'(<g class="label"[^>]*(?:style="([^"]*)")?[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>)\s*<rect[^/]*/>\s*<foreignObject width="([^"]+)" height="([^"]+)">\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*(</g>)'

    def replace_node_label(match):
        g_open = match.group(1)
        g_style = match.group(2) or ''
        tx = float(match.group(3))
        ty = float(match.group(4))
        width = float(match.group(5))
        height = float(match.group(6))
        div_content = match.group(7)
        g_close = match.group(8)

        lines = extract_text_lines_from_html(div_content)
        if not lines:
            return match.group(0)

        # Determine text color from style
        fill = extract_text_color_from_style(g_style)
        # Check for white text indicator
        if 'fff' in g_style.lower() or 'white' in g_style.lower():
            fill = '#fff'

        # Check for bold
        font_weight = 'bold' if 'bold' in g_style.lower() or '<b>' in div_content.lower() else 'normal'

        text_element = create_multiline_svg_text(lines, width, height, font_size=14, fill=fill, font_weight=font_weight)

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(node_pattern, replace_node_label, svg_content, flags=re.DOTALL)

    # Pattern 2: Cluster labels (subgraph titles)
    cluster_pattern = r'(<g class="cluster-label"[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>)\s*<foreignObject width="([^"]+)" height="([^"]+)">\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*(</g>)'

    def replace_cluster_label(match):
        g_open = match.group(1)
        tx = float(match.group(2))
        ty = float(match.group(3))
        width = float(match.group(4))
        height = float(match.group(5))
        div_content = match.group(6)
        g_close = match.group(7)

        lines = extract_text_lines_from_html(div_content)
        if not lines:
            return match.group(0)

        # Check for custom fill color in the div style
        fill = '#333'
        style_match = re.search(r'style="[^"]*color:\s*([^;!"]+)', div_content)
        if style_match:
            color = style_match.group(1).strip()
            if color and color != 'inherit':
                fill = color

        text_element = create_multiline_svg_text(lines, width, height, font_size=14, fill=fill, font_weight='bold')

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(cluster_pattern, replace_cluster_label, svg_content, flags=re.DOTALL)

    # Pattern 3: Edge labels with foreignObject (multi-line edge annotations)
    edge_pattern = r'(<g class="edgeLabel"[^>]*>)\s*<g class="label"[^>]*data-id="([^"]*)"[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>\s*<foreignObject width="([^"]+)" height="([^"]+)">\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*</g>\s*(</g>)'

    def replace_edge_label(match):
        g_open = match.group(1)
        data_id = match.group(2)
        tx = float(match.group(3))
        ty = float(match.group(4))
        width = float(match.group(5))
        height = float(match.group(6))
        div_content = match.group(7)
        g_close = match.group(8)

        lines = extract_text_lines_from_html(div_content)
        if not lines:
            return match.group(0)

        # Create text with tspans for multi-line
        line_height = 14
        total_height = len(lines) * line_height
        start_y = -total_height / 2 + line_height / 2

        if len(lines) == 1:
            text_inner = lines[0]
            text_element = f'<g class="label" data-id="{data_id}" transform="translate({tx}, {ty})"><text x="0" y="0" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 12px; fill: #333;">{text_inner}</text></g>'
        else:
            tspans = []
            for i, line in enumerate(lines):
                y_pos = start_y + i * line_height
                tspans.append(f'<tspan x="0" y="{y_pos}">{line}</tspan>')
            text_element = f'<g class="label" data-id="{data_id}" transform="translate({tx}, {ty})"><text text-anchor="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 12px; fill: #333;">{"".join(tspans)}</text></g>'

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(edge_pattern, replace_edge_label, svg_content, flags=re.DOTALL)

    # Pattern 4: Simple edge labels without data-id
    simple_edge_pattern = r'(<g class="edgeLabel"[^>]*>)\s*<g class="label"[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>\s*<foreignObject[^>]*>\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*</g>\s*(</g>)'

    def replace_simple_edge_label(match):
        g_open = match.group(1)
        tx = match.group(2)
        ty = match.group(3)
        div_content = match.group(4)
        g_close = match.group(5)

        lines = extract_text_lines_from_html(div_content)
        if not lines:
            return match.group(0)

        text = ' '.join(lines)  # Join multi-line to single for simple edges
        text_element = f'<g class="label" transform="translate({tx}, {ty})"><text x="0" y="0" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 12px; fill: #333;">{text}</text></g>'

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(simple_edge_pattern, replace_simple_edge_label, svg_content, flags=re.DOTALL)

    # Pattern 5: Any remaining foreignObject in g.label without rect
    remaining_label_pattern = r'(<g class="label"[^>]*(?:style="([^"]*)")?[^>]*transform="translate\(([^,]+),\s*([^)]+)\)"[^>]*>)\s*<foreignObject width="([^"]+)" height="([^"]+)">\s*(<div[^>]*>.*?</div>)\s*</foreignObject>\s*(</g>)'

    def replace_remaining_label(match):
        g_open = match.group(1)
        g_style = match.group(2) or ''
        tx = float(match.group(3))
        ty = float(match.group(4))
        width = float(match.group(5))
        height = float(match.group(6))
        div_content = match.group(7)
        g_close = match.group(8)

        lines = extract_text_lines_from_html(div_content)
        if not lines:
            return match.group(0)

        fill = extract_text_color_from_style(g_style)
        if 'fff' in g_style.lower() or 'white' in g_style.lower():
            fill = '#fff'

        font_weight = 'bold' if 'bold' in g_style.lower() or '<b>' in div_content.lower() else 'normal'

        text_element = create_multiline_svg_text(lines, width, height, font_size=14, fill=fill, font_weight=font_weight)

        return f'{g_open}{text_element}{g_close}'

    svg_content = re.sub(remaining_label_pattern, replace_remaining_label, svg_content, flags=re.DOTALL)

    # Pattern 6: Empty edge labels (width="0" height="0") - remove the foreignObject completely
    # These are placeholders with no content
    empty_fo_pattern = r'<foreignObject width="0" height="0">\s*<div[^>]*>\s*<span class="edgeLabel">\s*</span>\s*</div>\s*</foreignObject>'
    svg_content = re.sub(empty_fo_pattern, '', svg_content, flags=re.DOTALL)

    # Pattern 7: Any remaining foreignObject with empty edgeLabel spans
    empty_edge_pattern = r'<foreignObject[^>]*>\s*<div[^>]*class="labelBkg"[^>]*>\s*<span class="edgeLabel">\s*</span>\s*</div>\s*</foreignObject>'
    svg_content = re.sub(empty_edge_pattern, '', svg_content, flags=re.DOTALL)

    # Pattern 8: Edge labels with height="0" width="0" (reversed attribute order) with content
    # These have actual text content like Yes/No but zero dimensions
    reversed_fo_pattern = r'<foreignObject height="0" width="0">\s*<div[^>]*class="labelBkg"[^>]*>\s*<span class="edgeLabel">(<p>[^<]+</p>)</span>\s*</div>\s*</foreignObject>'

    def replace_zero_dim_label(match):
        p_content = match.group(1)
        # Extract text from <p>text</p>
        text_match = re.search(r'<p>([^<]+)</p>', p_content)
        if text_match:
            text = text_match.group(1).strip()
            # Create a simple text element - position will be handled by parent transform
            return f'<text x="0" y="0" text-anchor="middle" dominant-baseline="middle" style="font-family: trebuchet ms, verdana, arial, sans-serif; font-size: 12px; fill: #333;">{text}</text>'
        return ''

    svg_content = re.sub(reversed_fo_pattern, replace_zero_dim_label, svg_content, flags=re.DOTALL)

    # Pattern 9: Any remaining zero-dimension foreignObjects (cleanup)
    zero_dim_pattern = r'<foreignObject[^>]*(?:width="0"|height="0")[^>]*>\s*<div[^>]*>.*?</div>\s*</foreignObject>'
    svg_content = re.sub(zero_dim_pattern, '', svg_content, flags=re.DOTALL)

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
