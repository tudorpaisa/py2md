import re, argparse
from parser import Parser
from convert import Convert

class Py2md:

    def __init__(self, path, output):
        """Class constructor. Parses, converts, and saves the input file"""

        self.source = self.read_file(path)

        self.parser = Parser(self.source)
        self.parsed_text = self.parser.parsed_text
        self.meta = self.parser.meta
        self.converter = Convert(self.source, self.parsed_text, self.meta)
        self.newfile = self.converter.new_file

        self.newfile = ''.join(self.newfile)
        # In case I went too far with including "\n"s
        # self.newfile = re.sub('\n\n', '\n', self.newfile)
        self.save_file(self.newfile, output)

    def read_file(self, path):
        """Read file and load into memory"""
        with open(path, 'r') as f:
            return f.readlines()

    def save_file(self, source, output):
        """Save the file"""
        with open(output, 'w') as f:
            f.write(source)

# f_loc = input("Enter (relative) path to file: ")
# f_loc = 'test/main.py'

parser = argparse.ArgumentParser()
parser.add_argument('input', type = str, help='Input file')
parser.add_argument('output', type = str, help='Output file; to be saved in the "exports" folder')
args = parser.parse_args()
Py2md(args.input, args.output)
