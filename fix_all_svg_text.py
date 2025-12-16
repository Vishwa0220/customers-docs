#!/usr/bin/env python3
"""
Comprehensive SVG text fix script.
Fixes text visibility issues in SVG diagrams by:
1. Adding explicit white fill to text in colored nodes
2. Ensuring text elements have proper fill colors based on background
"""

import os
import re
import glob

def fix_svg_text_in_colored_nodes(svg_content, filename):
    """
    Fix text colors in SVGs to ensure visibility on colored backgrounds.
    """
    changes_made = []

    # Pattern 1: Fix text inside nodes with colored styles (primaryStyle, secondaryStyle, etc.)
    # These styles in mermaid have color:#fff but it may not be applied to text elements

    # Find all node groups and fix text fill inside colored ones
    def fix_node_group(match):
        node_content = match.group(0)
        original = node_content

        # Check if this node has a colored style class
        colored_styles = ['primaryStyle', 'secondaryStyle', 'arbiterStyle', 'userStyle',
                         'soarStyle', 'failoverStyle', 'titleStyle']

        has_colored_style = any(style in node_content for style in colored_styles)

        # Also check for inline fill colors that indicate colored background
        # These are typically blue, green, gray, orange backgrounds
        colored_fills = ['fill:#4169e1', 'fill:#10b981', 'fill:#6b7280', 'fill:#f59e0b',
                        'fill:#ef4444', 'fill:#4169E1', 'fill:#10B981', 'fill:#6B7280',
                        'fill:#F59E0B', 'fill:#EF4444']
        has_colored_fill = any(fill in node_content for fill in colored_fills)

        if has_colored_style or has_colored_fill:
            # Change text fill from #333 to #fff (white)
            node_content = re.sub(
                r'(<text[^>]*style="[^"]*)(fill:\s*#333)([^"]*")',
                r'\1fill: #fff\3',
                node_content
            )
            node_content = re.sub(
                r'(<text[^>]*style="[^"]*)(fill:#333)([^"]*")',
                r'\1fill:#fff\3',
                node_content
            )
            # Also fix tspan fill
            node_content = re.sub(
                r'(<tspan[^>]*style="[^"]*)(fill:\s*#333)([^"]*")',
                r'\1fill: #fff\3',
                node_content
            )
            node_content = re.sub(
                r'(<tspan[^>]*style="[^"]*)(fill:#333)([^"]*")',
                r'\1fill:#fff\3',
                node_content
            )

        return node_content

    # Process node groups
    svg_content = re.sub(
        r'<g class="node[^"]*"[^>]*>.*?</g>',
        fix_node_group,
        svg_content,
        flags=re.DOTALL
    )

    # Pattern 2: Fix CSS style rules in the SVG
    # Add !important to text fill rules for colored sections
    def fix_css_style(match):
        css = match.group(0)

        # Make sure section text colors are applied with higher specificity
        # For mermaid mindmaps, sections have colors defined
        css = re.sub(
            r'(\.section-\d+\s+text\s*\{[^}]*fill:)([^;!}]+)([^}]*\})',
            r'\1\2 !important\3',
            css
        )
        css = re.sub(
            r'(\.section--\d+\s+text\s*\{[^}]*fill:)([^;!}]+)([^}]*\})',
            r'\1\2 !important\3',
            css
        )

        return css

    svg_content = re.sub(r'<style[^>]*>.*?</style>', fix_css_style, svg_content, flags=re.DOTALL)

    # Pattern 3: For flowcharts, fix text in nodes with colored class definitions
    # These nodes have class assignments like "class DC_PRI,DR_PRI primaryStyle"
    # and text elements need white fill

    # Find nodes that are assigned to colored classes by checking classDef
    class_defs = re.findall(r'classDef\s+(\w+Style)\s+[^;]*color:#fff', svg_content)

    # Pattern 4: Direct fix for text elements with fill:#333 that are inside
    # elements with colored backgrounds

    # Find rect elements with colored fills and their associated text
    def fix_labeled_elements(svg_content):
        # Pattern for rect with colored fill followed by text
        # In mermaid, the structure is often <rect .../><text>...</text>

        # Fix text after colored rects in same group
        colored_rect_pattern = r'(<rect[^>]*fill="(#4169e1|#10b981|#6b7280|#f59e0b|#ef4444)"[^>]*/>\s*)(<text[^>]*)'

        def add_white_fill_to_text(match):
            rect_part = match.group(1)
            text_tag = match.group(3)

            # Add fill="white" if not present, or change existing fill
            if 'fill=' in text_tag:
                text_tag = re.sub(r'fill="[^"]*"', 'fill="white"', text_tag)
            else:
                text_tag = text_tag.replace('<text ', '<text fill="white" ')

            return rect_part + text_tag

        svg_content = re.sub(colored_rect_pattern, add_white_fill_to_text, svg_content, flags=re.IGNORECASE)

        return svg_content

    svg_content = fix_labeled_elements(svg_content)

    return svg_content

def fix_svg_file(filepath):
    """Fix a single SVG file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    original = content
    content = fix_svg_text_in_colored_nodes(content, filename)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix all SVG files in the images directory."""
    images_dir = '/home/ubuntu/go/src/customers-docs/docs/images'

    # Get all SVG files
    svg_files = glob.glob(os.path.join(images_dir, '*.svg'))

    print(f"Found {len(svg_files)} SVG files")
    print("-" * 50)

    fixed_count = 0
    for svg_file in sorted(svg_files):
        if fix_svg_file(svg_file):
            print(f"  Fixed: {os.path.basename(svg_file)}")
            fixed_count += 1
        else:
            print(f"  No changes: {os.path.basename(svg_file)}")

    print("-" * 50)
    print(f"Fixed {fixed_count} out of {len(svg_files)} files")

if __name__ == '__main__':
    main()
