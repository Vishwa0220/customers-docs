#!/usr/bin/env python3
"""
Fix SVG text colors to ensure visibility on colored backgrounds.
The issue is that text elements have fill:#333 but are on colored boxes
that need white text.
"""

import os
import re
import glob

def fix_text_colors_in_svg(svg_content):
    """
    Fix text colors in SVG to ensure visibility.
    Text inside nodes with colored backgrounds should be white.
    """

    # The SVG uses CSS classes like .primaryStyle, .secondaryStyle, etc.
    # that have tspan{fill:#fff!important} but the text elements have
    # inline fill:#333 that may override this.

    # Fix: In text elements inside .node groups that have colored styles,
    # change fill:#333 to fill:#fff

    # Pattern to find text elements with fill:#333 inside node groups
    # These are the ones inside colored boxes

    # First, let's find all node groups with primaryStyle, secondaryStyle, arbiterStyle, userStyle
    # and fix the text fill inside them

    def fix_node_text(match):
        node_content = match.group(0)
        # Check if this is a styled node (colored background)
        if any(style in node_content for style in ['primaryStyle', 'secondaryStyle', 'arbiterStyle', 'userStyle']):
            # Change fill: #333 to fill: #fff in text elements
            node_content = re.sub(
                r'(<text[^>]*style="[^"]*)(fill:\s*#333)([^"]*")',
                r'\1fill: #fff\3',
                node_content
            )
            # Also fix fill:#333 (no space)
            node_content = re.sub(
                r'(<text[^>]*style="[^"]*)(fill:#333)([^"]*")',
                r'\1fill:#fff\3',
                node_content
            )
        return node_content

    # Process node groups
    svg_content = re.sub(
        r'<g class="node[^"]*"[^>]*>.*?</g>',
        fix_node_text,
        svg_content,
        flags=re.DOTALL
    )

    return svg_content

def fix_svg_file(filepath):
    """Fix a single SVG file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = fix_text_colors_in_svg(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix all HA_DR SVG files."""
    images_dir = '/home/ubuntu/go/src/customers-docs/docs/images'

    # Get HA_DR SVG files
    svg_files = glob.glob(os.path.join(images_dir, 'HA_DR_Architecture_Documentation_dt3_diagram_*.svg'))

    print(f"Found {len(svg_files)} HA_DR SVG files")

    fixed_count = 0
    for svg_file in sorted(svg_files):
        if fix_svg_file(svg_file):
            print(f"  Fixed: {os.path.basename(svg_file)}")
            fixed_count += 1
        else:
            print(f"  No changes: {os.path.basename(svg_file)}")

    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
