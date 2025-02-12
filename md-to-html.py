from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
import os


def setup_markdown_with_css():
    # Initialize markdown-it instance
    md = (
    MarkdownIt('commonmark' ,{'breaks':True,'html':True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable('table')
    )
    
    # CSS styles
    css = """
    <style>
        .markdown-body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            padding: 45px;
            max-width: 900px;
            margin: 0 auto;
            color: #24292e;
        }

        .markdown-body h1 {
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            margin-bottom: 16px;
        }

        .markdown-body h2 {
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            margin-bottom: 16px;
        }

        .markdown-body code {
            background-color: rgba(27, 31, 35, 0.05);
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
            padding: 0.2em 0.4em;
        }

        .markdown-body pre {
            background-color: #f6f8fa;
            border-radius: 3px;
            font-size: 85%;
            line-height: 1.45;
            overflow: auto;
            padding: 16px;
        }

        .markdown-body blockquote {
            border-left: 0.25em solid #dfe2e5;
            color: #6a737d;
            margin: 0;
            padding: 0 1em;
        }

        .markdown-body table {
            border-collapse: collapse;
            display: block;
            overflow: auto;
            width: 100%;
        }

        .markdown-body table th,
        .markdown-body table td {
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }

        .markdown-body table tr {
            background-color: #fff;
            border-top: 1px solid #c6cbd1;
        }

        .markdown-body table tr:nth-child(2n) {
            background-color: #f6f8fa;
        }

        .markdown-body img {
            max-width: 100%;
            box-sizing: border-box;
        }

        .markdown-body ul,
        .markdown-body ol {
            padding-left: 2em;
        }

        .markdown-body li {
            margin-top: 0.25em;
        }
    </style>
    """

    def render_with_css(markdown_content):
        # Convert markdown to HTML
        html_content = md.render(markdown_content)
        
        # Wrap the content in a div with our CSS class
        wrapped_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {css}
        </head>
        <body>
            <div class="markdown-body">
                {html_content}
            </div>
        </body>
        </html>
        """
        return wrapped_content

    return render_with_css

# Example usage
if __name__ == "__main__":
    # Create a renderer with CSS
    markdown_renderer = setup_markdown_with_css()
    
    for dirpath, _, filenames in os.walk("./"):
        for filename in filenames:
            if filename.endswith('.md'):
                try:
                    md_path = os.path.join(dirpath, filename)
                    html_path = os.path.splitext(md_path)[0] + '.html'

                    with open(md_path, 'r') as f:
                        data = f.read()
                    
                    text = (data)
                    # Convert markdown to HTML with CSS
                    html_output = markdown_renderer(text)
                    
                    # Save to file
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html_output)

                except Exception as e:
                    print("Failed for", md_path, ",", e)