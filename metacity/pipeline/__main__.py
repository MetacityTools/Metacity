from .ui import pick

if __name__ == '__main__':
    selection = pick(['a', 'b', 'c'], 'Pick one:')
    print(selection)
