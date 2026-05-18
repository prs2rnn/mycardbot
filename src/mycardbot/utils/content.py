from pathlib import Path


def load_html_content(section: str) -> str:
    file_path = Path(__file__).parent.parent / f'templates/{section}.html'

    if not file_path.exists():
        return ''

    return file_path.read_text(encoding='utf-8')
