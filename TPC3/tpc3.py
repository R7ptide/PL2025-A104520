import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def markdown_to_html(file):
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    # headers
    text = re.sub(r'^###\s+(.+)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s+(.+)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # italico
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # imagens
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', text)

    # links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    # listas
    lines = text.split('\n')
    html_lines = []
    in_ol = False
    for line in lines:
        match = re.match(r'^(\d+)\.\s+(.+)', line)
        if match:
            if not in_ol:
                html_lines.append('<ol>')
                in_ol = True
            html_lines.append(f'<li>{match.group(2)}</li>')
        else:
            if in_ol:
                html_lines.append('</ol>')
                in_ol = False
            html_lines.append(line)
    if in_ol:
        html_lines.append('</ol>')
    
    result = '\n'.join(html_lines)

    with open("resultado.html", "w", encoding="utf-8") as f:
        f.write(result)




markdown_to_html("teste.md")