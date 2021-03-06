"""
pymdownx.tilde
Really simple plugin to add support for
<del>test</del> tags as ~~test~~ and
<sub>test</sub> tags as ~test~


MIT license.

Copyright (c) 2014 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import SimpleTagPattern, DoubleTagPattern

RE_SMART_CONTENT = r'((?:[^~]|~(?=[^\W_]|~|\s)|(?<=\s)~+?(?=\s))+?~*?)'
RE_CONTENT = r'((?:[^~]|(?<!~)~(?=[^\W_]|~))+?)'
RE_SMART_DEL = r'(?:(?<=_)|(?<![\w~]))(~{2})(?![\s~])%s(?<!\s)\2(?:(?=_)|(?![\w~]))' % RE_SMART_CONTENT
RE_DEL = r'(~{2})(?!\s)%s(?<!\s)\2' % RE_CONTENT

RE_SUB_DEL = r'(~{3})(?!\s)([^~]+?)(?<!\s)\2'
RE_SMART_SUB_DEL = r'(~{3})(?!\s)%s(?<!\s)\2' % RE_SMART_CONTENT
RE_SUB_DEL2 = r'(~{3})(?!\s)([^~]+?)(?<!\s)~{2}([^~ ]+?)~'
RE_SMART_SUB_DEL2 = r'(~{3})(?!\s)%s(?<!\s)~{2}(?:(?=_)|(?![\w~]))([^~ ]+?)~' % RE_SMART_CONTENT
RE_SUB = r'(~)([^~ ]+?|~)\2'


class DeleteSubExtension(Extension):
    """Adds delete and/or subscript extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        self.config = {
            'smart_delete': [True, "Treat ~~connected~~words~~ intelligently - Default: True"],
            'delete': [True, "Enable delete - Default: True"],
            'subscript': [True, "Enable subscript - Default: True"]
        }

        super(DeleteSubExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """<del>test</del> tags as ~~test~~ and <sub>test</sub> tags as ~test~"""
        config = self.getConfigs()
        delete = bool(config.get('delete', True))
        subscript = bool(config.get('subscript', True))
        smart = bool(config.get('smart_delete', True))

        if "~" not in md.ESCAPED_CHARS and (delete or subscript):
            md.ESCAPED_CHARS.append('~')
        if " " not in md.ESCAPED_CHARS and subscript:
            md.ESCAPED_CHARS.append(' ')

        delete_rule = RE_SMART_DEL if smart else RE_DEL
        sub_del_rule = RE_SMART_SUB_DEL if smart else RE_SUB_DEL
        sub_del2_rule = RE_SMART_SUB_DEL2 if smart else RE_SUB_DEL2
        sub_rule = RE_SUB

        if delete:
            md.inlinePatterns.add("del", SimpleTagPattern(delete_rule, "del"), "<not_strong")
            if subscript:
                md.inlinePatterns.add("sub_del", DoubleTagPattern(sub_del_rule, "sub,del"), "<del")
                md.inlinePatterns.add("sub_del2", DoubleTagPattern(sub_del2_rule, "sub,del"), "<del")
                md.inlinePatterns.add("sub", SimpleTagPattern(sub_rule, "sub"), ">del" if smart else "<del")
        elif subscript:
            md.inlinePatterns.add("sub", SimpleTagPattern(sub_rule, "sub"), "<not_strong")


def makeExtension(*args, **kwargs):
    return DeleteSubExtension(*args, **kwargs)
