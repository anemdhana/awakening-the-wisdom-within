from pathlib import Path
import argparse


def build_page(template_path: Path, body_path: Path, output_path: Path, title: str, css_path: str) -> None:
    template = template_path.read_text(encoding='utf-8')
    body_html = body_path.read_text(encoding='utf-8')

    filled = template.replace('{{PAGE_TITLE}}', title)
    filled = filled.replace('{{CSS_PATH}}', css_path)
    filled = filled.replace('{{BODY_CONTENT}}', body_html)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(filled, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Build a static page from a shared HTML shell and a body-only fragment.')
    parser.add_argument('--template', required=True, type=Path, help='Path to page-shell.html')
    parser.add_argument('--body', required=True, type=Path, help='Path to content-only HTML body fragment')
    parser.add_argument('--output', required=True, type=Path, help='Output HTML file path')
    parser.add_argument('--title', required=True, help='Page title for the generated document')
    parser.add_argument('--css', default='../../css/site.css', help='Relative CSS path inside generated page')
    args = parser.parse_args()

    build_page(args.template, args.body, args.output, args.title, args.css)


if __name__ == '__main__':
    main()
