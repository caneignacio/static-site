from splitters import markdown_to_html_node, markdown_to_blocks

print(markdown_to_html_node(
    """
# This is the heading

### This is heading 2
"""
))