#!/usr/bin/env python3
"""Generate a PDF CV from Markdown with daza.ar dark-ocean aesthetic.

Usage:
    python gen_cv.py es | ba | ho
"""
import subprocess
import sys
import re
from pathlib import Path

CV_DIR = Path.home() / "Projects" / "cv"

VARIANTS = {
    "es": {"md": CV_DIR / "cv.md", "pdf": CV_DIR / "Juan_Manuel_Daza_AI_Engineer_CV_ES.pdf"},
    "ba": {"md": CV_DIR / "cv_ba.md", "pdf": CV_DIR / "Juan_Manuel_Daza_AI_Engineer_CV_BA.pdf"},
    "ho": {"md": CV_DIR / "cv_ho_engineering_role.md", "pdf": CV_DIR / "Juan_Manuel_Daza_AI_Engineer_CV_HO.pdf"},
}

# daza.ar palettes
PALETTES = {
    "dark": {
        "bg": "#0d1b2a",        # deep sea
        "panel": "#1b263b",     # midnight blue (summary box)
        "ink": "#e0d8c0",       # moonlit sand (body text)
        "head": "#f5f0e1",      # parchment (name / h3)
        "accent": "#ffd700",    # pirate gold (h2, links, markers)
        "accent_soft": "#415a77",  # teal (datelines, borders, page no)
    },
    "light": {
        "bg": "#f5f0e1",        # parchment
        "panel": "#ece5d0",     # darker parchment (summary box)
        "ink": "#1b263b",       # midnight blue (body text)
        "head": "#0d1b2a",      # deep sea (name / h3)
        "accent": "#9a7d0a",    # dark gold (h2, links, markers)
        "accent_soft": "#415a77",  # teal (datelines, borders, page no)
    },
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Juan Manuel Daza — CV</title>
<style>
@page {{
  size: A4;
  margin: 14mm 15mm 16mm 15mm;
  background: {bg};
  @bottom-right {{
    content: counter(page) " / " counter(pages);
    font-family: 'Press Start 2P', monospace;
    font-size: 5.5pt;
    color: {accent_soft};
  }}
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 9.8pt;
  line-height: 1.4;
  color: {ink};
  background: {bg};
}}

a {{ color: {accent}; text-decoration: none; }}
strong {{ color: {head}; font-weight: 600; }}

/* ---- Header ---- */
.cv-header {{
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid {accent};
  margin-bottom: 6px;
}}
.cv-header img.avatar {{
  width: 96px;
  height: 96px;
  border: 3px solid {accent};
  border-radius: 8px;
  image-rendering: pixelated;
  flex-shrink: 0;
}}
.cv-header .hero-text {{ flex: 1; }}
.cv-header h1 {{
  font-family: 'Press Start 2P', monospace;
  font-size: 14pt;
  color: {head};
  letter-spacing: 1px;
  margin-bottom: 8px;
  line-height: 1.4;
}}
.cv-header .tagline {{
  font-size: 12.5pt;
  font-weight: 600;
  color: {accent};
  font-style: italic;
  margin-bottom: 5px;
}}
.cv-header .location {{
  font-size: 9pt;
  color: {ink};
  margin-bottom: 5px;
}}
.cv-header .location .pin {{ color: {accent}; font-weight: 600; }}
.cv-header .contact {{
  font-size: 9pt;
  color: {ink};
}}
.cv-header .contact .sep {{ color: {accent_soft}; padding: 0 5px; }}

/* ---- Sections ---- */
h2 {{
  font-family: 'Press Start 2P', monospace;
  font-size: 7.5pt;
  color: {accent};
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin: 18px 0 9px 0;
  padding-bottom: 5px;
  border-bottom: 1px solid {accent_soft};
  page-break-after: avoid;
}}

h3 {{
  font-size: 11pt;
  font-weight: 600;
  color: {head};
  margin: 12px 0 2px 0;
  page-break-after: avoid;
}}
h3 .sep {{ color: {accent_soft}; font-weight: 400; }}
.dateline {{
  font-style: italic;
  color: {accent_soft};
  font-size: 9pt;
  margin-bottom: 5px;
  page-break-after: avoid;
}}
.dateline strong {{ color: {accent_soft}; font-weight: 400; }}

ul {{
  margin: 0 0 10px 0;
  padding-left: 16px;
  list-style: square;
}}
ul li {{
  margin-bottom: 3.5px;
  text-align: justify;
  page-break-inside: avoid;
}}
ul li::marker {{ color: {accent}; }}

/* ---- Summary box ---- */
.summary {{
  background: {panel};
  border-left: 3px solid {accent};
  padding: 10px 14px;
  margin: 0 0 4px 0;
  font-size: 9.6pt;
  line-height: 1.5;
}}
.summary > p {{ margin-bottom: 8px; }}
.summary ul {{ margin: 0; padding-left: 15px; }}
.summary li {{ margin-bottom: 4px; }}

/* ---- Skills ---- */
.skill-cat {{
  font-family: 'Press Start 2P', monospace;
  font-size: 6.5pt;
  color: {accent};
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 10px 0 5px 0;
  page-break-after: avoid;
}}
.skills-grid {{
  margin: 0 0 2px 0;
  line-height: 2;
}}
.skill-tag {{
  display: inline-block;
  border: 1px solid {accent_soft};
  color: {ink};
  font-size: 8.2pt;
  padding: 1.5px 8px;
  border-radius: 3px;
  margin: 0 4px 4px 0;
  line-height: 1.4;
  page-break-inside: avoid;
}}

/* ---- Projects ---- */
.projects-list li {{ margin-bottom: 9px; page-break-inside: avoid; }}
.project-head {{ font-size: 10.5pt; }}
.project-head .project-name {{ color: {accent}; font-weight: 600; }}
.project-head .project-role {{ font-style: italic; color: {accent_soft}; font-size: 9pt; }}
.project-head {{ margin-bottom: 1px; }}\n.project-desc {{ font-size: 9.2pt; line-height: 1.45; }}

/* ---- Education / Languages ---- */
.edu-list li, .lang-list li {{ page-break-inside: avoid; }}

/* ---- Recommendations ---- */
blockquote {{
  border-left: 2px solid {accent};
  padding: 2px 0 2px 12px;
  margin: 0 0 10px 0;
  font-style: italic;
  font-size: 9.5pt;
  page-break-inside: avoid;
}}
blockquote .attrib {{
  font-style: normal;
  font-size: 8.5pt;
  color: {accent_soft};
  margin-top: 3px;
}}
blockquote .attrib strong {{ color: {ink}; font-weight: 600; }}

hr {{ display: none; }}
p, .summary {{ orphans: 3; widows: 3; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def md_links(text: str) -> str:
    """Convert markdown links to HTML anchors."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_header(header_lines) -> str:
    name = "Juan Manuel Daza"
    tagline = ""
    location = ""
    contact = ""
    for line in header_lines:
        line = line.rstrip()
        if line.startswith("# "):
            name = line[2:].strip()
        elif line.startswith("**") and line.endswith("**") and "|" in line:
            tagline = line.strip("* ")
        elif line.startswith("\U0001F4CD") or line.lower().startswith("buenos aires") or "argentina" in line.lower() and "mailto" not in line and "[" not in line:
            location = line.replace("\U0001F4CD", "").strip()
        elif "mailto:" in line or "daza.ar" in line:
            contact = line.strip()

    # contact: split markdown links, join with gold separators
    parts = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', contact)
    if parts:
        anchors = [f'<a href="{url}">{escape(txt)}</a>' for txt, url in parts]
        contact_html = '<span class="sep">|</span>'.join(anchors)
    else:
        contact_html = md_links(escape(contact))

    loc_html = ""
    if location:
        loc = escape(location)
        loc = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', loc)
        loc = md_links(loc)
        loc_html = f'<p class="location"><span class="pin">&#9670;</span> {loc}</p>'

    avatar_path = CV_DIR / "assets" / "profile.png"
    avatar_html = ""
    if avatar_path.exists():
        avatar_html = f'<img class="avatar" src="{avatar_path.as_uri()}" width="96" height="96" alt="Juan Manuel Daza">'

    return f"""<div class="cv-header">
{avatar_html}
<div class="hero-text">
<h1>{escape(name).upper()}</h1>
<p class="tagline">{escape(tagline)}</p>
{loc_html}
<p class="contact">{contact_html}</p>
</div>
</div>"""



def normalize_md(md_text: str) -> str:
    """Ensure list items are separated from preceding paragraphs by blank lines.

    The CV markdown has bullets directly under date lines with no blank line,
    which makes the markdown parser treat them as lazy paragraph continuations.
    """
    lines = md_text.splitlines()
    out = []
    for i, line in enumerate(lines):
        is_bullet = re.match(r'^\s*[*-]\s+', line)
        prev = lines[i - 1] if i > 0 else ""
        prev_is_bullet = re.match(r'^\s*[*-]\s+', prev)
        if is_bullet and prev.strip() and not prev_is_bullet:
            out.append("")
        out.append(line)
    return "\n".join(out)

def preprocess_md(md_text: str) -> str:
    """Rewrite sections into semantic HTML blocks before markdown conversion."""
    lines = md_text.splitlines()
    out = []
    in_skills = False
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.strip() == "## Skills":
            in_skills = True
            out.append(line)
            i += 1
            continue

        if in_skills:
            if line.startswith("## "):
                in_skills = False
                # fall through to normal handling below
            else:
                m = re.match(r'\s*\*\s+\*\*(.+?)\*\*\s*:\s*(.+)', line)
                if m:
                    cat, items = m.group(1), m.group(2)
                    tags = [t.strip() for t in split_skills(items)]
                    tag_html = "".join(
                        f'<span class="skill-tag">{escape(t)}</span>' for t in tags
                    )
                    out.append(f'<p class="skill-cat">{escape(cat)}</p>')
                    out.append(f'<p class="skills-grid">{tag_html}</p>')
                i += 1
                continue

        out.append(line)
        i += 1
    return "\n".join(out)


def split_skills(items: str):
    """Split skill list on commas, but not inside parentheses."""
    parts, depth, cur = [], 0, []
    for ch in items:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def postprocess_html(html: str) -> str:
    # Summary box: h2 + following <p> (+ optional <ul>)
    html = re.sub(
        r'(<h2>Professional Summary</h2>)\s*(<p>.*?</p>\s*(?:<ul>.*?</ul>)?)\s*(?=<h2>)',
        r'\1<div class="summary">\2</div>',
        html, flags=re.DOTALL,
    )

    # Date lines under h3: <p><strong>...</strong></p> -> dateline
    html = re.sub(
        r'(<h3>.*?</h3>)\s*<p><strong>([^<]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^<]*)</strong></p>',
        r'\1<p class="dateline">\2</p>',
        html, flags=re.DOTALL,
    )

    # Projects: <li><strong>name</strong> | <em>role</em><br>\n desc</li>
    def proj_repl(m):
        name, role, desc = m.group(1), m.group(2), m.group(3).strip()
        return (f'<li><p class="project-head">'
                f'<span class="project-name">{name}</span>'
                f'<span class="project-role"> &#8212; {role}</span></p>'
                f'<p class="project-desc">{desc}</p></li>')
    html = re.sub(
        r'<li>\s*<p><strong>([^<]+)</strong> \| <em>([^<]+)</em>\s*(.*?)</p>\s*</li>',
        proj_repl, html, flags=re.DOTALL,
    )

    # Recommendations: <li><em>"quote"</em> — <strong>name</strong></li>
    def rec_repl(m):
        quote, attrib = m.group(1), m.group(2)
        return (f'<blockquote><p>&#8220;{quote}&#8221;</p>'
                f'<p class="attrib">&#8212; {attrib}</p></blockquote>')
    html = re.sub(
        r'<li><em>&#8220;([^<]+)&#8221;</em> &#8212; <strong>([^<]+)</strong></li>',
        rec_repl, html)
    html = re.sub(
        r'<li><em>"([^"]+)"</em> — <strong>([^<]+)</strong></li>',
        lambda m: (f'<blockquote><p>&#8220;{m.group(1)}&#8221;</p>'
                   f'<p class="attrib">&#8212; {m.group(2)}</p></blockquote>'),
        html)
    html = re.sub(r'<ul>\s*(<blockquote>.*?</blockquote>\s*)+</ul>',
                  lambda m: m.group(0).replace('<ul>', '').replace('</ul>', ''),
                  html, flags=re.DOTALL)

    # Experience section h3 separators: "Role | Company" -> styled
    html = re.sub(
        r'(<h3>)([^<]*) \| ([^<]*)(</h3>)',
        r'\1\2<span class="sep"> &#8212; </span>\3\4',
        html)

    return html


def generate(variant: str, theme: str = "dark") -> Path:
    if variant not in VARIANTS:
        print(f"Unknown variant: {variant}. Use: es, ba, ho.")
        sys.exit(1)

    cfg = VARIANTS[variant]
    if theme not in PALETTES:
        print(f"Unknown theme: {theme}. Use: dark, light.")
        sys.exit(1)
    md_path = cfg["md"]
    pdf_path = cfg["pdf"]
    if theme == "light":
        pdf_path = pdf_path.with_name(pdf_path.stem + "_LIGHT.pdf")
    if not md_path.exists():
        print(f"Markdown not found: {md_path}")
        sys.exit(1)

    import markdown as md_lib
    md_raw = md_path.read_text(encoding="utf-8")

    header_lines, body_lines, in_header = [], [], True
    for line in md_raw.splitlines():
        if in_header and line.startswith("## "):
            in_header = False
        (header_lines if in_header else body_lines).append(line)

    header_html = build_header(header_lines)
    body_md = normalize_md("\n".join(body_lines))
    body_md = preprocess_md(body_md)
    html_body = md_lib.markdown(body_md, extensions=["tables", "fenced_code"])
    html_body = postprocess_html(html_body)

    pal = PALETTES[theme]
    full_html = HTML_TEMPLATE.format(body=header_html + html_body, **pal)

    html_tmp = Path("/tmp/cv_styled.html")
    html_tmp.write_text(full_html, encoding="utf-8")

    result = subprocess.run(
        ["weasyprint", str(html_tmp), str(pdf_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Weasyprint failed:\n{result.stderr}")
        sys.exit(1)
    html_tmp.unlink(missing_ok=True)

    size_kb = pdf_path.stat().st_size / 1024
    print(f"Generated: {pdf_path} ({size_kb:.0f} KB)")
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_cv.py [es|ba|ho] [dark|light]")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "dark")
