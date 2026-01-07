#!/usr/bin/env python3
"""
SPECTRA Notebook Header Generator

Generates SPECTRA-grade markdown headers for Fabric notebooks.
Multiple styles available - clean, minimal, high signal.
"""

import argparse
from typing import List, Optional


def style_minimal(title: str, subtitle: str, outputs: List[str]) -> str:
    """Minimal style - clean, simple, SPECTRA-grade."""
    return f"""# {title}

{subtitle}

**Outputs:** {' | '.join(f'`{o}`' for o in outputs)}"""


def style_centered(title: str, subtitle: str, outputs: List[str]) -> str:
    """Centered style with horizontal rule."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""<div align="center">

# {title}

{subtitle}

**Outputs:** {outputs_str}

</div>"""


def style_table(title: str, subtitle: str, outputs: List[str]) -> str:
    """Table-based layout - structured, clean."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""# {title}

| **Purpose** | {subtitle} |
|-------------|------------|
| **Outputs** | {outputs_str} |"""


def style_emoji_badge(title: str, subtitle: str, outputs: List[str]) -> str:
    """Emoji + badge style - visual but clean."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""# 📊 {title}

{subtitle}

**Outputs:** {outputs_str}"""


def style_unicode_minimal(title: str, subtitle: str, outputs: List[str]) -> str:
    """Unicode minimal - subtle dividers, no boxes."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""# {title}

{subtitle}

**Outputs:** {outputs_str}

---"""


def style_ascii_art(title: str, subtitle: str, outputs: List[str]) -> str:
    """ASCII art style using simple characters."""
    # Simple ASCII banner
    width = max(len(title), len(subtitle), 60)
    border = "=" * width
    
    # Split subtitle if too long
    subtitle_lines = []
    words = subtitle.split()
    current_line = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + 1 <= width - 4:
            current_line.append(word)
            current_len += len(word) + 1
        else:
            if current_line:
                subtitle_lines.append(' '.join(current_line))
            current_line = [word]
            current_len = len(word)
    if current_line:
        subtitle_lines.append(' '.join(current_line))
    
    # Build ASCII art
    lines = [
        border,
        f"  {title}",
        "",
    ]
    for line in subtitle_lines:
        lines.append(f"  {line}")
    lines.extend([
        "",
        f"  Outputs: {' | '.join(f'`{o}`' for o in outputs)}",
        border
    ])
    
    return '\n'.join(lines)


def style_geometric(title: str, subtitle: str, outputs: List[str]) -> str:
    """Geometric style - uses SPECTRA's sacred geometry theme."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""# ◇ {title} ◇

{subtitle}

**Outputs:** {outputs_str}

◇◇◇"""


def style_badge(title: str, subtitle: str, outputs: List[str]) -> str:
    """Badge-style with visual elements."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""# {title}

> {subtitle}

**Outputs:** {outputs_str}"""


def style_unicode_box(title: str, subtitle: str, outputs: List[str]) -> str:
    """Unicode box-drawing style - clean, framed, professional."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    width = 70
    
    # Box drawing characters
    top_left = '╔'
    top_right = '╗'
    bottom_left = '╚'
    bottom_right = '╝'
    horizontal = '═'
    vertical = '║'
    
    lines = [
        top_left + horizontal * (width - 2) + top_right,
        vertical + ' ' * (width - 2) + vertical,
        vertical + f' {title}'.ljust(width - 3) + vertical,
        vertical + ' ' * (width - 2) + vertical,
    ]
    
    # Wrap subtitle
    words = subtitle.split()
    current_line = ' '
    for word in words:
        if len(current_line) + len(word) + 1 <= width - 4:
            current_line += word + ' '
        else:
            lines.append(vertical + current_line.ljust(width - 3) + vertical)
            current_line = ' ' + word + ' '
    if current_line.strip():
        lines.append(vertical + current_line.ljust(width - 3) + vertical)
    
    lines.extend([
        vertical + ' ' * (width - 2) + vertical,
        vertical + f' Outputs: {outputs_str}'.ljust(width - 3) + vertical,
        vertical + ' ' * (width - 2) + vertical,
        bottom_left + horizontal * (width - 2) + bottom_right,
    ])
    
    return '\n'.join(lines)


def style_spectra_geometric(title: str, subtitle: str, outputs: List[str]) -> str:
    """SPECTRA sacred geometry style - seven-pointed star pattern."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""<div align="center">

# ◇◇◇ {title} ◇◇◇

{subtitle}

**Outputs:** {outputs_str}

</div>

<div align="center">

◇ ◇ ◇

</div>"""


def style_ascii_art_enhanced(title: str, subtitle: str, outputs: List[str]) -> str:
    """Enhanced ASCII art with borders and styling."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    width = 76
    border_top = "┌" + "─" * (width - 2) + "┐"
    border_bottom = "└" + "─" * (width - 2) + "┘"
    border_side = "│"
    
    lines = [border_top]
    lines.append(border_side + " " * (width - 2) + border_side)
    
    # Title (centered)
    title_padded = f"  {title}  "
    title_line = border_side + title_padded.center(width - 2) + border_side
    lines.append(title_line)
    lines.append(border_side + " " * (width - 2) + border_side)
    
    # Divider
    lines.append(border_side + " " + "─" * (width - 4) + " " + border_side)
    lines.append(border_side + " " * (width - 2) + border_side)
    
    # Subtitle (wrapped)
    words = subtitle.split()
    current_line = " "
    for word in words:
        if len(current_line) + len(word) + 1 <= width - 4:
            current_line += word + " "
        else:
            lines.append(border_side + current_line.ljust(width - 3) + border_side)
            current_line = " " + word + " "
    if current_line.strip():
        lines.append(border_side + current_line.ljust(width - 3) + border_side)
    
    lines.append(border_side + " " * (width - 2) + border_side)
    lines.append(border_side + " " + "─" * (width - 4) + " " + border_side)
    lines.append(border_side + " " * (width - 2) + border_side)
    
    # Outputs (wrapped if needed)
    outputs_prefix = " Outputs: "
    if len(outputs_str) <= width - len(outputs_prefix) - 4:
        outputs_line = outputs_prefix + outputs_str + " "
        lines.append(border_side + outputs_line.ljust(width - 3) + border_side)
    else:
        # Split outputs across multiple lines if too long
        outputs_line = outputs_prefix + outputs_str + " "
        lines.append(border_side + outputs_line[:width - 3].ljust(width - 3) + border_side)
        if len(outputs_line) > width - 3:
            remaining = outputs_line[width - 3:].strip()
            if remaining:
                lines.append(border_side + (" " + remaining).ljust(width - 3) + border_side)
    
    lines.append(border_side + " " * (width - 2) + border_side)
    lines.append(border_bottom)
    
    return "\n".join(lines)


def style_minimal_elegant(title: str, subtitle: str, outputs: List[str]) -> str:
    """Minimal but elegant - clean lines, subtle separators."""
    outputs_str = ' | '.join(f'`{o}`' for o in outputs)
    return f"""# {title}

{subtitle}

──────────────────────────────────────────────────────────────────────────

**Outputs:** {outputs_str}"""


STYLES = {
    "minimal": style_minimal,
    "centered": style_centered,
    "table": style_table,
    "emoji": style_emoji_badge,
    "unicode": style_unicode_minimal,
    "ascii": style_ascii_art,
    "geometric": style_geometric,
    "badge": style_badge,
    "unicode_box": style_unicode_box,
    "spectra_geometric": style_spectra_geometric,
    "ascii_enhanced": style_ascii_art_enhanced,
    "minimal_elegant": style_minimal_elegant,
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate SPECTRA-grade notebook headers"
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Source Stage — Zephyr Enterprise",
        help="Header title"
    )
    parser.add_argument(
        "--subtitle",
        type=str,
        default="Establishes connectivity, validates authentication, and catalogs all available API endpoints for downstream pipeline stages.",
        help="Subtitle/description"
    )
    parser.add_argument(
        "--outputs",
        type=str,
        nargs="+",
        default=["source.portfolio", "source.config", "source.credentials", "source.endpoints"],
        help="Output table names"
    )
    parser.add_argument(
        "--style",
        type=str,
        choices=list(STYLES.keys()),
        default="minimal",
        help="Header style"
    )
    parser.add_argument(
        "--preview-all",
        action="store_true",
        help="Preview all styles"
    )
    
    args = parser.parse_args()
    
    if args.preview_all:
        print("=" * 80)
        print("🎨 SPECTRA NOTEBOOK HEADER STYLES - PREVIEW")
        print("=" * 80)
        print()
        
        for style_name, style_func in STYLES.items():
            print(f"\n{'=' * 80}")
            print(f"Style: {style_name.upper()}")
            print('=' * 80)
            print()
            header = style_func(args.title, args.subtitle, args.outputs)
            print(header)
            print()
    else:
        style_func = STYLES[args.style]
        header = style_func(args.title, args.subtitle, args.outputs)
        print(header)


if __name__ == "__main__":
    main()

