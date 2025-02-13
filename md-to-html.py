import os
import html 
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

def setup_markdown_with_css():
    md = (
        MarkdownIt('commonmark', {'breaks': True, 'html': True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable('table')
    )

    css = """
    <style>
        /* Styles généraux GitHub-like */
        .markdown-body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            padding: 45px;
            max-width: 900px;
            margin: 0 auto;
            color: #24292e;
            background: #ffffff;
        }

        /* Images responsives */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }

        /* Blocs de code façon GitHub */
        pre {
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            font-size: 14px;
            line-height: 1.45;
            border: 1px solid #d0d7de;
        }
    </style>
    """

    def render_with_css(markdown_content):
        html_content = md.render(markdown_content)
        html_content = html.unescape(html_content)

        wrapped_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            {css}
            <link rel="stylesheet" href="/assets/css/prism.css">
        </head>
        <body>
            <div class="markdown-body">
                {html_content}
            </div>
            <script src="/assets/js/prism.js"></script>
            <script src="/assets/js/prism-python.js"></script>
            <script src="/assets/js/prism-javascript.js"></script>
            <script src="/assets/js/prism-bash.js"></script>
            <script src="/assets/js/prism-go.js"></script>
            <script>
                if (typeof Prism !== 'undefined') {{
                    Prism.highlightAll();
                }}
            </script>
        </body>
        </html>
        """
        return wrapped_content

    return render_with_css


if __name__ == "__main__":
    markdown_renderer = setup_markdown_with_css()
    remove_md = False
    for dirpath, _, filenames in os.walk("./"):
        for filename in filenames:
            if filename.endswith('.md'):
                try:
                    md_path = os.path.join(dirpath, filename)
                    html_path = os.path.splitext(md_path)[0] + '.html'

                    with open(md_path, 'r', encoding="utf-8") as f:
                        data = f.read()

                    html_output = markdown_renderer(data)

                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html_output)
                    
                    if remove_md:
                        os.remove(md_path)

                except Exception as e:
                    print(f"Erreur avec {md_path}: {e}")
