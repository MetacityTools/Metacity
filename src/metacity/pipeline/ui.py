import os
import re
import textwrap
from colored import attr, bg, fg

#def bg(color: str):
#    return f""
#
#def fg(color: str):
#    return f""
#
#def attr(color: str):
#    return f""

COMMANDS = ['extra', 'extension', 'stuff', 'errors',
            'email', 'foobar', 'foo']

RE_SPACE = re.compile('.*\s+$', re.M)


def remove_prefix(text: str, prefix: str):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

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
    message = "    Let me work on it..."
    width = os.get_terminal_size().columns
    free_space = width - len_no_ansi(message)
    print(f"{Colors.dim}{Colors.gray_bg}{Colors.white_fg}{message}{free_space * ' '}{Colors.reset}{Colors.dim}")   


def processing_sequence_end():
    message = "    Done!"
    width = os.get_terminal_size().columns
    free_space = width - len_no_ansi(message)
    print(f"{Colors.dim}{Colors.gray_bg}{Colors.white_fg}{message}{free_space * ' '}{Colors.reset}")   

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
    message = remove_prefix(message, ' ')
    message = textwrap.fill(message, width=40)
    message = textwrap.indent(message, '    ')
    message = f"\n{Colors.dim}{message}{Colors.reset}"
    return message


def print_message(message: str):
    message = format_message(message)
    print(message)
    
    
def prompt_task(title: str):
    prompt = f"{Colors.pink_bg}{Colors.white_fg} {title} "
    width = os.get_terminal_size().columns
    free_space = width - len_no_ansi(prompt)
    print(f"\n{prompt}{Colors.gray_bg}{free_space * ' '}{Colors.reset}")
        

def get_path(title: str):
    path = input(">>> " + title + ": ")
    return path


def get_yes_no(title: str):
    while True:
        answer = input(">>> " + title + f" {Colors.dim}[y to apply, blank to skip]{Colors.reset} ")
        if answer.lower() == 'y':
            return True
        return False


supported_suffixes = ('.shp', '.json')


def count_datasets(path: str):
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(supported_suffixes):
                files.append(os.path.join(root, filename))

    if len(files) > 5:
        return files[:5], len(files) - 5 
    return files, 0

def confirm_dataset_selection(datasets: list, extr_count: int):
    print(f"{Colors.dim}", end='')
    if len(datasets) == 0:
        print(f"No datasets found, please try a different directory.{Colors.reset}")
        return False
    
    for dataset in datasets:
        print(f"    {dataset}")
    
    if extr_count > 0:
        print(f"    and {extr_count} extra datasets.")
    print(Colors.reset, end='')
    file_count = len(datasets) + extr_count
    return get_yes_no(f"Load {file_count} dataset{ 's' if file_count > 1 else '' }?")


def get_number(title: str):
    while True:
        answer = input(">>> " + title + ": ")
        try:
            return float(answer)
        except ValueError:
            print(f"{Colors.dim}Please enter a number.{Colors.reset}")

def confirm_tile_size(tile_size: float):
    return get_yes_no(f"Use tile size {tile_size}?")

def validate_path(path):
    if not os.path.exists(path):
        print(f"{Colors.dim}Path {path} does not exist.{Colors.reset}")
        return get_yes_no(f"Create it?")
    else:
        print(f"{Colors.dim}Path {path} exists.{Colors.reset}")
        return get_yes_no(f"Overwrite it?")
