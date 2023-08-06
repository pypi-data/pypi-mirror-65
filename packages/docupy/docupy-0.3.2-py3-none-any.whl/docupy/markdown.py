"""This module contains for functions for parsing markdown."""

import re
from collections import OrderedDict

BLOCKS = ["h", "code", "div", "figure", "video", "li"]

PATTERNS = OrderedDict((
 (r"<", "&#60;"),
 (r">", "&#62;"),
 (r"\n### (.+)", "\n<h3>\\1</h3>"),
 (r"\n## (.+)", "\n<h2>\\1</h2>"),
 (r"\n# (.+)", "\n<h1>\\1</h1>"),
 (r"\~\~(.+?)\~\~", "<del>\\1</del>"),
 (r"\*\*(.+?)\*\*", "<strong>\\1</strong>"),
 (r"\*(.+?)\*", "<em>\\1</em>"),
 (r"\n- *(.+)", "\n<li>\\1</li>u"),
 (r"\n\d+\. *(.+)", "\n<li>\\1</li>o"),
 (r"\n\!\[(.+?)\]\[(.+?)\]\((.+?)\)", "\n<figure><img src=\"\\3\" "
  "title=\"\\1\"><figcaption>\\2</figcaption></figure>"),
 (r"\n\!\[(.+?)\]\((.+?)\)", "\n<figure><img src=\"\\2\" title=\"\\1\"></figure>"),
 (r"\n\!\((.+?)\)", "\n<video src=\"\\1\" controls></video>"),
 (r"\n\!\{(.+?)\}", "\n<div class=\"youtube\">""<iframe src=\"//www.youtube.com"
  "/embed/\\1/\" frameborder=\"0\" allowfullscreen></iframe></div>"),
 (r"\[(.+?)\]\(((.(?!\"))+?)\)", "<a href=\"\\2\">\\1</a>"),
 (r"\[(.+?)\]\((.+?) \"(.+)\"\)", "<a href=\"\\2\" title=\"\\3\">\\1</a>"),
 (r"\{(.+?)\}\(((.(?!\"))+?)\)", "<a href=\"\\2\" target=\"_blank\">\\1</a>"),
 (r"\{(.+?)\}\((.+?) \"(.+)\"\)", "<a href=\"\\2\" target=\"_blank\" "
  "title=\"\\3\">\\1</a>"),
 (r"\{(.+?)\}\((.+?)\)", "<a href=\"\\2\" target=\"_blank\">\\1</a>"),
 (r"```(.+?)\n([\S\s]+?)\n```", "<pre><code data-language=\"\\1\">\\2</code></pre>"),
 (r"```\n([\S\s]+?)\n```", "<pre><code>\\1</code></pre>"),
 (r"`([\S\s]+?)`", "<code>\\1</code>")
))

def markdown_to_html(markdown, paths=None):
    """Takes a string in markdown, and converts it to HTML.

    :param str markdown: The maekdown to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    markdown, characters = escape_characters(markdown)
    html = "\n" + markdown
    for key, value in PATTERNS.items():
        html = re.sub(key, value, html)
    if paths:
        for k, v in paths.items():
            html = html.replace('src="{}"'.format(k), 'src="{}"'.format(v))
    for character in characters:
        html = html.replace("\x1A", character, 1)
    lines = html.splitlines()
    lines = add_p_tags(lines)
    lines = add_list_tags(lines)
    return "\n".join(lines)


def escape_characters(markdown):
    """Takes some markdown and replaces escaped characters with the substition
    character. This is returned along with a list of escaped characters.

    You cannot escape line breaks - the backslash will be removed but not the
    line break.

    :param str markdown: The string to break up.
    :rtype: ``str``, ``list``"""

    characters = []
    while "\\" in markdown:
        loc = markdown.find("\\")
        if loc != len(markdown) - 1:
            character = markdown[loc + 1]
            if character != "\n":
                characters.append(character)
                markdown = markdown[:loc] + "\x1A" + markdown[loc + 2:]
            else:
                markdown = markdown[:loc] + markdown[loc + 1:]
        else:
            break
    return markdown, characters


def add_p_tags(lines):
    """Takes a list of HTML lines and puts p tags around all the lines that
    need it.

    It will also remove empty lines.

    :param list lines: the lines to convert.
    :rtype: ``list``"""

    output_lines = []
    in_code = False
    for line in lines:
        if line.strip():
            if line.strip().startswith("<pre"): in_code = True
            for b in BLOCKS:
                if line.startswith("<" + b) or line.startswith("</" + b)\
                 or in_code: break
            else:
                line = "<p>{}</p>".format(line)
            if line.strip().endswith("</pre>"): in_code = False
            output_lines.append(line)
        elif in_code: output_lines.append(line)
    return output_lines


def add_list_tags(lines):
    """Takes a list of HTML lines and puts list tags around all the lines that
    need it.

    :param list lines: the lines to convert.
    :rtype: ``list``"""

    output_lines = []
    list_type = "u"
    while lines:
        if lines[0][:3] == "<li" and output_lines[-1][:3] != "<li":
            list_type = lines[0][-1]
            output_lines.append("<{}l>".format(list_type))
        if lines[0][:3] == "<li":
            output_lines.append(lines.pop(0)[:-1])
        else:
            output_lines.append(lines.pop(0))
        if output_lines[-1][:3] == "<li":
            if not len(lines) or lines[0][:3] != "<li":
                output_lines.append("</{}l>".format(list_type))
    return output_lines
