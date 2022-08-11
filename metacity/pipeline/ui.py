import os
import re
import readline
import textwrap
from typing import List

from colored import attr, bg, fg

COMMANDS = ['extra', 'extension', 'stuff', 'errors',
            'email', 'foobar', 'foo']

RE_SPACE = re.compile('.*\s+$', re.M)

class Colors:
    pink_bg = bg('#FE5E87')
    white_fg = fg(15)
    gray_bg = bg(236)
    purple_bg = bg('#6308df')
    reset = attr('reset')
    light_purple_bg = bg('#9933cc')
    dim = attr('dim')


def len_no_ansi(string):
    return len(re.sub(
        r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', string))


def processing_sequence_start():
    message = "Let me work on it..."
    width = os.get_terminal_size().columns
    free_space = width - len_no_ansi(message)
    print(f"\n{Colors.dim}{Colors.gray_bg}{message}{free_space * ' '}{Colors.reset}{Colors.dim}")   


def processing_sequence_end():
    print(f"Done!{Colors.reset}")


def print_intro_bar(left_text: str, center_text: str, right_text: str):
    size = os.get_terminal_size()
    prompt = f"{Colors.pink_bg}{Colors.white_fg} {left_text} {Colors.gray_bg} {center_text}"
    prompt_end = f"{Colors.purple_bg} {right_text} "
    free_space = size.columns - len_no_ansi(prompt) - len_no_ansi(prompt_end)
    
    print(prompt, end='')
    print(free_space * ' ', end='')
    print(prompt_end, end='')
    print(Colors.reset)


def format_message(message: str):
    message = re.sub(r'\s+', ' ', message)
    message = message.removeprefix(' ')
    message = textwrap.fill(message, width=60)
    message = textwrap.indent(message, '    ')
    message = f"\n{Colors.dim}{message}{Colors.reset}\n"
    return message


def print_message(message: str):
    message = format_message(message)
    print(message)
    
    
def prompt_task(title: str):
    prompt = f"{Colors.pink_bg}{Colors.white_fg} {title} "
    width = os.get_terminal_size().columns
    free_space = width - len_no_ansi(prompt)
    print(f"{prompt}{Colors.gray_bg}{free_space * ' '}{Colors.reset}")


class Completer(object):
    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_extra(self, args):
        "Completions for the 'extra' command."
        if not args:
            return self._complete_path('./')
        # treat the last arg as a path and complete it
        return self._complete_path(args)

    def complete(self, text, state):
        "Generic readline completion entry point."
        line = readline.get_line_buffer()
        return self.complete_extra(line)[state]
        

def get_path(title: str):
    comp = Completer()
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)
    path = input(title)
    readline.parse_and_bind('set disable-completion on')
    readline.parse_and_bind('C-a: overwrite-mode')
    return path

def get_yes_no(title: str):
    while True:
        answer = input(title)
        print("Please answer y or n.")