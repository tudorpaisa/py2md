"""File contains the Convert class. With input from Parser it converts to markdown"""

import re

class Convert:
    """Convert source file into a .md file"""

    def __init__(self, source: list, parsed_text: list, meta: dict = None):
        """Class constructor"""

        self.new_file = []
        self.source = source.copy()

        if meta:
            self.new_file.append(self.convert_metadata(self.source, meta))

        for i in parsed_text:
            if i[2] == 'text':
                self.new_file.append(self.convert_text(self.source, i))
                # self.new_file.append('\n')
            elif i[2] == 'code':
                code = self.convert_code(self.source, i)
                self.new_file.append(code)
                # self.new_file.append('\n')

        # self.source = source
        # self.source = self.convert_metadata(self.source, meta)
        # self.source = self.convert_text(self.source, text)
        # self.source = self.convert_code(self.source, code)

    def convert_text(self, source: list, text: list):
        """Convert text to markdown"""

        t_start = text[0]
        t_stop = text[1]

        source[text[0]] = re.sub('^"""', '\n', source[text[0]])
        source[text[1]] = re.sub('"""', '\n', source[text[1]])

        return ''.join(source[text[0]:text[1]+1])

    def convert_code(self, source: list, code: list):
        """Convert code to markdown code blocks"""

        c_start = code[0]
        c_stop = code[1]

        if c_start - c_stop == 0:

            return ''.join(['```python\n', source[c_start], '\n```\n'])

        else:
            new_code = source[c_start:c_stop+1].copy()
            new_code.insert(0, '```python\n')
            new_code.append('\n```\n')

            return ''.join(new_code)

    def convert_metadata(self, source: list, meta: dict):

        dat = []

        # FIXME for I am ugly code
        if meta['__title__'] != -1:
            title = re.sub('__title__ *= *', '',
                           source[meta['__title__']])
            dat.append('title: ' + title)

        if meta['__author__'] != -1:
            author = re.sub('__author__ *= *', '',
                            source[meta['__author__']])
            dat.append('author: ' + author)

        if meta['__date__'] != -1:
            date = re.sub('__date__ *= *', '',
                          source[meta['__date__']])
            dat.append('date: ' + date)

        if meta['__keywords__'] != -1:
            keywords = re.sub('__keywords__ *= *', '',
                              source[meta['__keywords__']])
            dat.append('keywords: ' + keywords)

        dat.insert(0, '---\n')
        dat.append('---\n\n')

        return ''.join(dat)

    def convert_file(self, source: list, parsed_text: list, meta = None):

        new_file = []

        if meta:
            new_file.append(self.convert_metadata(source, meta))

        for i in parsed_text:
            if i[2] == 'text':
                new_file.append(self.convert_text(source, i))
            elif i[2] == 'code':
                new_file.append(self.convert_code(source, i))

        return '\n'.join(new_file)
