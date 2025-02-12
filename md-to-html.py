from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
import os
from pathlib import Path
import html

def setup_markdown_with_css():
    # Initialize markdown-it instance
    md = (
        MarkdownIt('commonmark' ,{'breaks':True,'html':True})
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .enable('table')
    )
    
    # CSS styles with Prism themes
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

        /* Base styles unchanged... */
        [Previous CSS styles remain the same...]

        /* Syntax highlighting styles */
        code[class*="language-"],
        pre[class*="language-"] {
            color: #c5c8c6;
            text-shadow: 0 1px rgba(0, 0, 0, 0.3);
            font-family: Consolas, Monaco, 'Andale Mono', monospace;
            direction: ltr;
            text-align: left;
            white-space: pre;
            word-spacing: normal;
            word-break: normal;
            line-height: 1.5;
            background: #1d1f21;
            border-radius: 8px;
        }

        pre[class*="language-"] {
            padding: 1em;
            margin: .5em 0;
            overflow: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* Tokens colors */
        .token.comment,
        .token.prolog,
        .token.doctype,
        .token.cdata {
            color: #7C7C7C;
        }

        .token.punctuation {
            color: #c5c8c6;
        }

        .namespace {
            opacity: .7;
        }

        .token.property,
        .token.keyword,
        .token.tag {
            color: #96CBFE;
        }

        .token.class-name {
            color: #FFFFB6;
        }

        .token.boolean,
        .token.constant {
            color: #99CC99;
        }

        .token.symbol,
        .token.deleted {
            color: #f92672;
        }

        .token.number {
            color: #FF73FD;
        }

        .token.selector,
        .token.attr-name,
        .token.string,
        .token.char,
        .token.builtin,
        .token.inserted {
            color: #A8FF60;
        }

        .token.variable {
            color: #C6C5FE;
        }

        .token.operator {
            color: #EDEDED;
        }

        .token.entity {
            color: #FFFFB6;
            cursor: help;
        }

        .token.url {
            color: #96CBFE;
        }

        .token.regex,
        .token.important {
            color: #E9C062;
        }

        .token.function {
            color: #DAD085;
        }
    </style>
    """

    # Add Prism.js for syntax highlighting
    prism_js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-go.min.js"></script>
    """

    def render_with_css(markdown_content):
        # Convert markdown to HTML
        html_content = md.render(markdown_content)
        
        # Add language class to code blocks
        html_content = html_content.replace('<code>', '<code class="language-python">')
        html_content = html_content.replace('<code class="language-python">python', '<code class="language-python">')
        html_content = html_content.replace('<code class="language-python">javascript', '<code class="language-javascript">')
        html_content = html_content.replace('<code class="language-python">bash', '<code class="language-bash">')
        html_content = html_content.replace('<code class="language-python">go', '<code class="language-go">')
        
        # Wrap the content in a div with our CSS class
        wrapped_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {css}
            <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css" rel="stylesheet" />
        </head>
        <body>
            <div class="markdown-body">
                {html_content}
            </div>
            {prism_js}
            <script>
                // Re-trigger Prism highlighting
                if (typeof Prism !== 'undefined') {
                    "{Prism.highlightAll();}"
                }
            </script>
        </body>
        </html>
        """
        return wrapped_content

    return render_with_css


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
                    
                    os.remove(md_path)

                except Exception as e:
                    print("Failed for", md_path, ",", e)
