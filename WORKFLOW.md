# CV Variants & Job Search Pipeline — Implementation Plan

> **For Hermes:** Execute directly with Hermes tools. Tasks are bite-sized and self-contained.

**Goal:** Formalize a two-variant CV strategy (Spain/EU vs. Buenos Aires) with a single-command PDF generation pipeline, and document the recruiter response workflow.

**Architecture:** Two Markdown sources (`cv.md` for Spain/EU, `cv_ba.md` for Buenos Aires), one script (`gen_cv.py`) that converts either to PDF via markdown → HTML → pipx weasyprint. No tailoring per offer — CVs are fixed. The variant choice depends on whether the role is in Spain/EU or Argentina/local.

**Tech Stack:** Python 3, markdown library, weasyprint (via pipx), bash

---

## CV Variants

| Variant | File | Use When |
|---------|------|----------|
| Spain/EU | `cv.md` | Role in Spain or EU. Includes "Relocating to Spain (Oct 2026)" and EU citizenship. |
| Buenos Aires | `cv_ba.md` | Role in Argentina or LATAM (remote or hybrid). No Spain references. |

**Rule:** CV content is fixed per variant. Do not tailor per offer. Only choose the correct variant.

---

## Phase 1: Single-Command PDF Generator (Tasks 1–4)

### Task 1: Create `gen_cv.py`

**Objective:** One script that takes a variant name (`es` or `ba`) and outputs a PDF.

**Files:**
- Create: `~/Projects/cv/gen_cv.py`

**Step 1: Write the script**

```python
#!/usr/bin/env python3
"""Generate a PDF CV from the Spain/EU or Buenos Aires variant.

Usage:
    python gen_cv.py es     # Spain/EU variant (cv.md)
    python gen_cv.py ba     # Buenos Aires variant (cv_ba.md)
"""
import subprocess
import sys
from pathlib import Path

CV_DIR = Path.home() / "Projects" / "cv"

VARIANTS = {
    "es": {"md": CV_DIR / "cv.md", "pdf": CV_DIR / "Juan_Manuel_Daza_AI_Engineer_CV_ES.pdf"},
    "ba": {"md": CV_DIR / "cv_ba.md", "pdf": CV_DIR / "Juan_Manuel_Daza_AI_Engineer_CV_BA.pdf"},
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Juan Manuel Daza - CV</title>
<style>
@page {{ size: A4; margin: 15mm; @bottom-right {{ content: "Page " counter(page) " of " counter(pages); font-size: 8pt; font-family: Arial, sans-serif; color: #777; }} }}
body {{ font-family: Arial, sans-serif; font-size: 9.5pt; line-height: 1.45; color: #333; margin: 0; padding: 0; }}
h1 {{ font-size: 20pt; font-weight: bold; color: #111; margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 0.5px; }}
p {{ margin: 0 0 10px 0; }} strong {{ color: #111; }}
h1 + p {{ font-size: 11pt; color: #0056b3; font-weight: bold; margin-bottom: 8px; }}
h1 + p + p {{ font-size: 9pt; color: #555; margin-bottom: 15px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
h2 {{ font-size: 12pt; color: #111; border-bottom: 1px solid #aaa; padding-bottom: 3px; margin: 18px 0 10px 0; text-transform: uppercase; letter-spacing: 0.5px; }}
h3 {{ font-size: 10.5pt; color: #111; margin: 12px 0 4px 0; }}
h3 strong {{ font-weight: bold; }}
h3 + p {{ font-style: italic; color: #555; margin-bottom: 6px; font-size: 9pt; }}
ul {{ margin: 0 0 10px 0; padding-left: 20px; }} li {{ margin-bottom: 4px; text-align: justify; }}
hr {{ display: none; }} a {{ color: #0056b3; text-decoration: none; }}
</style></head><body>{body}</body></html>"""


def generate(variant: str) -> Path:
    if variant not in VARIANTS:
        print(f"Unknown variant: {variant}. Use 'es' or 'ba'.")
        sys.exit(1)

    cfg = VARIANTS[variant]
    md_path = cfg["md"]
    pdf_path = cfg["pdf"]

    if not md_path.exists():
        print(f"Markdown not found: {md_path}")
        sys.exit(1)

    import markdown
    md_content = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])
    html = HTML_TEMPLATE.format(body=html_body)

    html_tmp = Path("/tmp/cv_gen.html")
    html_tmp.write_text(html, encoding="utf-8")

    result = subprocess.run(
        ["/usr/bin/pipx", "run", "--spec", "weasyprint", "weasyprint",
         str(html_tmp), str(pdf_path)],
        capture_output=True, text=True
    )

    html_tmp.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"Weasyprint failed: {result.stderr}")
        sys.exit(1)

    size_kb = pdf_path.stat().st_size / 1024
    print(f"Generated: {pdf_path} ({size_kb:.0f} KB)")
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_cv.py [es|ba]")
        sys.exit(1)
    generate(sys.argv[1])
```

**Step 2: Test both variants**

```bash
cd ~/Projects/cv
python gen_cv.py es
python gen_cv.py ba
ls -la Juan_Manuel_Daza_AI_Engineer_CV_ES.pdf Juan_Manuel_Daza_AI_Engineer_CV_BA.pdf
```

**Step 3: Commit**

```bash
cd ~/Projects/cv
git add gen_cv.py
git commit -m "feat: add single-command CV PDF generator (es/ba variants)"
```

---

### Task 2: Remove old generate_pdf.py (replaced by gen_cv.py)

**Objective:** Clean up the now-redundant script.

**Files:**
- Remove: `~/Projects/cv/generate_pdf.py`

```bash
cd ~/Projects/cv
git rm generate_pdf.py
git commit -m "chore: remove generate_pdf.py (replaced by gen_cv.py)"
```

---

### Task 3: Add shebang and make gen_cv.py executable

**Objective:** Make the script directly runnable.

```bash
cd ~/Projects/cv
chmod +x gen_cv.py
git add gen_cv.py
git commit -m "chore: make gen_cv.py executable"
```

---

### Task 4: Verify both PDFs are correct

**Objective:** Spot-check that each PDF variant has the right header line.

```bash
cd ~/Projects/cv
# Spain variant should mention relocation
python gen_cv.py es
python3 -c "
import subprocess
result = subprocess.run(['pdftotext', 'Juan_Manuel_Daza_AI_Engineer_CV_ES.pdf', '-', '-l', '1'], capture_output=True, text=True)
print('ES variant first page:')
print(result.stdout[:500])
"

# BA variant should NOT mention relocation
python gen_cv.py ba
python3 -c "
import subprocess
result = subprocess.run(['pdftotext', 'Juan_Manuel_Daza_AI_Engineer_CV_BA.pdf', '-', '-l', '1'], capture_output=True, text=True)
print('BA variant first page:')
print(result.stdout[:500])
"
```

**Expected:** ES contains "Relocating to Spain". BA does not.

---

## Phase 2: Recruiter Response Workflow Documentation (Tasks 5–6)

### Task 5: Document the workflow in the CV repo README

**Objective:** Add a `WORKFLOW.md` that documents the full recruiter response pipeline. This makes the process explicit and referenceable.

**Files:**
- Create: `~/Projects/cv/WORKFLOW.md`

```markdown
# Job Search Workflow

## CV Variants

Two fixed CVs. Do not tailor per offer — choose the correct variant.

| Variant | File | PDF (generated) | Use When |
|---------|------|-----------------|----------|
| Spain/EU | `cv.md` | `Juan_Manuel_Daza_AI_Engineer_CV_ES.pdf` | Role in Spain or EU |
| Buenos Aires | `cv_ba.md` | `Juan_Manuel_Daza_AI_Engineer_CV_BA.pdf` | Role in Argentina/LATAM |

Generate PDF: `python gen_cv.py es` or `python gen_cv.py ba`

## Recruiter Response Pipeline

### Step 1: Triage

When a recruiter messages on LinkedIn:
- Is it personalized or generic?
- Third-party staffing agency or in-house?
- Comp range stated or hidden?
- Role and tech stack clear?

**Red flags:**
- Generic "gente con tu perfil" without specifics
- No comp range after two asks
- "Apply via JD link" from third-party = volume sourcing
- Extensive written tech breakdown before any interview = gatekeeping

### Step 2: Qualify

If the message is generic, send qualifying questions:

```
Hola [name], gracias por escribirme. Me interesa saber más.
¿Me podrías compartir algo de contexto? Empresa, modalidad
(relación de dependencia o contractor), rango de compensación
y en qué etapa está el producto.
```

### Step 3: Assess Fit

When details arrive:
- Comp >= $4,000 USD floor?
- Tech stack alignment?
- Location/hybrid fit?

### Step 4: Choose CV Variant

- Role in Spain/EU → `cv.md` → `gen_cv.py es`
- Role in Argentina/LATAM → `cv_ba.md` → `gen_cv.py ba`

### Step 5: Respond

**Rate not stated yet:**
```
Hola [name], gracias por la data. El rol me interesa, pero
mi rango está en USD 4.000 mensuales. Si ese número es viable,
coordinamos una call. Si no, no hay problema.
```

**Rate stated and acceptable:**
```
Hola [name], me interesa. El rol tiene buena alineación
con mi perfil. Adjunto mi CV. Quedo atento a los próximos pasos.
```

**Rate below floor ($4k):**
```
Hola [name], gracias por la data. El rol es interesante,
pero mi rango está en USD 4.000 mensuales. Si hay flexibilidad
en el presupuesto, coordinamos. Si no, gracias igual.
```

### Step 6: Follow-Up

Do not chase. If the recruiter comes back with paperwork before an interview, push back:

```
Prefiero tener una conversación con el equipo técnico antes
de completar formularios extensos. ¿Es posible coordinar una call?
```

## Comp Rules

- **Floor:** $4,000 USD/month
- **Middle ground:** $3,500 if cap is firm below $4k
- **Never anchor first.** Always ask their range first.
- **Only state your number when asked directly.**
```

**Step 2: Commit**

```bash
cd ~/Projects/cv
git add WORKFLOW.md
git commit -m "docs: add recruiter response workflow documentation"
```

---

### Task 6: Update recruiter-triage skill to reference the two-CV setup

**Objective:** Ensure the recruiter-triage skill knows about the CV variants and gen_cv.py.

**Files:**
- Modify: `~/.hermes/skills/productivity/recruiter-triage/SKILL.md`

**Step 1: Add CV variants section**

Patch into the skill, after the "Response Style" section:

```markdown
## CV Variants

Two fixed CVs in `~/Projects/cv/`. Do not tailor per offer — choose the correct variant.

| Variant | File | PDF | Use When |
|---------|------|-----|----------|
| Spain/EU | `cv.md` | `Juan_Manuel_Daza_AI_Engineer_CV_ES.pdf` | Role in Spain or EU |
| Buenos Aires | `cv_ba.md` | `Juan_Manuel_Daza_AI_Engineer_CV_BA.pdf` | Role in Argentina/LATAM |

Generate PDF: `cd ~/Projects/cv && python gen_cv.py es` or `python gen_cv.py ba`
```

**Step 2: Commit both repos**

```bash
cd ~/Projects/cv
git add WORKFLOW.md
git commit -m "docs: add CV variants section to recruiter workflow"

# Skill is in hermes config, update via skill_manage
```

---

## Verification Checklist

Before considering this complete:

- [ ] `python gen_cv.py es` produces a valid PDF with Spain references
- [ ] `python gen_cv.py ba` produces a valid PDF without Spain references
- [ ] `generate_pdf.py` is removed (replaced)
- [ ] `WORKFLOW.md` exists and covers the full pipeline
- [ ] Hermes memory has the two-CV strategy recorded
- [ ] When a new recruiter message arrives, Hermes picks the correct CV variant automatically
