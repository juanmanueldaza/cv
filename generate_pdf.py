import os
import sys
import subprocess
from pathlib import Path

def generate_pdf():
    try:
        import markdown
    except ImportError:
        print("Please install markdown package: pip install markdown")
        return

    cv_dir = Path("/home/ultravietnamita/Projects/cv")
    md_path = cv_dir / "cv.md"
    html_temp_path = Path("/tmp/cv_temp.html")
    pdf_path = cv_dir / "Juan_Manuel_Daza_AI_Full_Stack_Engineer_CV.pdf"
    downloads_path = Path("/home/ultravietnamita/Downloads/Juan_Manuel_Daza_AI_Full_Stack_Engineer_CV.pdf")
    
    if not md_path.exists():
        print(f"Markdown file not found at {md_path}")
        return

    md_content = md_path.read_text(encoding='utf-8')
    
    # Render markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code"]
    )
    
    # Styled HTML with professional print/PDF CSS
    styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Juan Manuel Daza - CV</title>
    <style>
        @page {{
            size: A4;
            margin: 15mm;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 8pt;
                font-family: Arial, sans-serif;
                color: #777;
            }}
        }}
        body {{
            font-family: Arial, sans-serif;
            font-size: 9.5pt;
            line-height: 1.45;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        h1 {{
            font-size: 20pt;
            font-weight: bold;
            color: #111;
            margin: 0 0 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        p {{
            margin: 0 0 10px 0;
        }}
        strong {{
            color: #111;
        }}
        h1 + p {{
            font-size: 11pt;
            color: #0056b3;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        /* Contact block */
        h1 + p + p {{
            font-size: 9pt;
            color: #555;
            margin-bottom: 15px;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        h2 {{
            font-size: 12pt;
            color: #111;
            border-bottom: 1px solid #aaa;
            padding-bottom: 3px;
            margin: 18px 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        h3 {{
            font-size: 10.5pt;
            color: #111;
            margin: 12px 0 4px 0;
        }}
        h3 strong {{
            font-weight: bold;
        }}
        h3 + p {{
            font-style: italic;
            color: #555;
            margin-bottom: 6px;
            font-size: 9pt;
        }}
        ul {{
            margin: 0 0 10px 0;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 4px;
            text-align: justify;
        }}
        hr {{
            display: none; /* Hide horizontal rules since we use borders on headers */
        }}
        a {{
            color: #0056b3;
            text-decoration: none;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

    html_temp_path.write_text(styled_html, encoding='utf-8')
    print(f"HTML temp file created at {html_temp_path}")
    
    # Run weasyprint via subprocess
    print(f"Running weasyprint via pipx on {html_temp_path}...")
    try:
        result = subprocess.run(
            ["/usr/bin/pipx", "run", "--spec", "weasyprint", "weasyprint", str(html_temp_path), str(pdf_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Generated PDF at {pdf_path}")
        
        # Copy to downloads
        import shutil
        shutil.copy(pdf_path, downloads_path)
        print(f"Copied PDF to Downloads at {downloads_path}")
        
        # Clean up
        if html_temp_path.exists():
            html_temp_path.unlink()
            
    except subprocess.CalledProcessError as e:
        print(f"Error running Weasyprint: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_pdf()
