"""File contains the Parser class. It identifies metadata, code and text location within input"""

import re

class Parser:
    """Identifies location of metadata, code and text within input file"""

    def __init__(self, source: list):
        """Class constructor; Parses, but does not convert"""
        bool_meta = self.bool_metadata(source)

        if bool_meta:
            # Dict containing start, stop location of various
            #  blocks of metadata
            self.meta = self.get_metadata(source)
        else:
            self.meta = None

        # Dict containing start, stop location of various
        #  blocks of text
        self.t_int = self.delim_text(source)
        self.text_rows = self.list_text()
        self.code_rows = self.list_code(source)
        # Dict containing start, stop location of various
        #  blocks of code
        self.c_int = self.delim_code(source)

        self.parsed_text = self.parse_text()

    def bool_metadata(self, source):
        """"Search if file contains module level dunders (AKA metadata)"""

        dunders = ['__title__', '__author__', '__date__', '__keywords__']
        # PEP 8 says that dunder names should be placed after
	#  the module docstring but before any import statements
	#  except from __future__ imports. For this reason
	#  we will look only at 1/4 of the file
        for i in range(int(len(source)/4)):
            for j in dunders:
                if j in source[i]:
                    return True

        return False

    def get_metadata(self, source):
        """Get location of file metadata (module level dunder names; see PEP 8)"""

        dunders = {'__title__': -1,
                   '__author__': -1,
                   '__date__': -1,
                   '__keywords__': -1}

        # Retrieve index of dunders
        for i in dunders.keys():
            for j in range(int(len(source)/4)):
                if i in source[j]:
                    dunders[i] = j

        return dunders

    def delim_text(self, source):
        """Identifies locations {'start': [], 'stop': []} of text"""
        t_int = {'start': [], 'stop': []}
        invert = 1
        for i in range(len(source)):
            if re.search('^""".*"""$', source[i]):
                # IF text is a one-liner
                t_int['start'].append(i)
                t_int['stop'].append(i)
            elif re.search('^"""', source[i]) and invert > 0:
                t_int['start'].append(i)
                invert *= -1
            elif re.search('"""$', source[i]) and invert < 0:
                t_int['stop'].append(i)
                invert *= -1
        return t_int

    def delim_code(self, source):
        """Identifies locations {'start': [], 'stop': []} of code
        on pre-existing indices of text"""
        c_int = {'start': [], 'stop': []}
        invert = -1

        # IF rows are not consecutive, then it signals start/end of code
        #  Iterate from index 1 not 0
        arr = [-1 for i in range(len(self.code_rows))]
        arr[0] = 1

        for i in range(1, len(self.code_rows)):
            if self.code_rows[i] - self.code_rows[i-1] != 1:
                arr[i] = 1
                arr[i-1] = 0

        for i in range(len(self.code_rows)):
            if arr[i] == 1:
                c_int['start'].append(self.code_rows[i])
            elif arr[i] == 0:
                c_int['stop'].append(self.code_rows[i])

        if len(c_int['start']) != len(c_int['stop']):
            c_int['stop'].append(len(source)-1)

        return c_int

    def list_text(self):
        """List all individual rows where text is found"""
        text_rows = []

        for i in range(len(self.t_int['start'])):
            for j in range(self.t_int['start'][i], self.t_int['stop'][i]+1):
                text_rows.append(j)

        return text_rows
    
    def list_code(self, source):
        """List where there is code based on pre-existing indices of text"""
        return [i for i in range(len(source)) if i not in self.text_rows]

    def parse_text(self):
        """Sort text and code intervals"""

        row_types = []

        for i in range(len(self.t_int['start'])):
            row_types.append([self.t_int['start'][i], self.t_int['stop'][i], 'text'])

        for i in range(len(self.c_int['start'])):
            row_types.append([self.c_int['start'][i], self.c_int['stop'][i], 'code'])

        row_types.sort(key=lambda x: x[0])

        return row_types
