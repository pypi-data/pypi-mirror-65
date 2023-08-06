import curses


def get_keys():
    desc = [
        '[h][LEFT]     : Move left one column.',
        '[l][RIGHT]    : Move right one column.',
        '[k][UP]       : Move up one row.',
        '[j][DOWN]     : Move down one row.',
        '[f][PGDN]     : Jump down a page of rows.',
        '[b][PGUP]     : Jump up a page of rows.',
        '[g][HOME]     : Jump to first item.',
        '[G][END]      : Jump to last item.',
        '[#]           : Jump to an item number.',
        '[/]           : Find items via wilcards, regex or range.',
        '[n]           : Jump to next search result.',
        '[p]           : Jump to previous search result.',
        '[CTRL-n]      : Jump to next pick.',
        '[CTRL-p]      : Jump to previous pick.',
        '[r][F5]       : Reset search results and picks.',
        '[z][CTRL-l]   : Recenter current row on screen.',
        '[RET]         : Pick an item.',
        '[;]           : Pick via wildcards, regex or range.',
        '[u]           : Undo the last pick.',
        '[U]           : Undo the last pick and move to it\'s row.',
        '[t]           : Toggle an item.',
        '[SPC]         : Toggle item and go down a row.',
        '[CTRL-SPC]    : Toggle item and go up a row.',
        '[a]           : Toggle all items.',
        '[:]           : Toggle via wildcards, regex or range.',
        '[v]           : View all picks.',
        '[?][F1]       : View this help page.',
        '[w][CTRL-s]   : Save picks to file.',
        '[q][ESC]      : Quit and display all marked paths.',
    ]

    keys = {
        'resize': [
            curses.KEY_RESIZE,
        ],
        'left': [
            ord('h'),
            curses.KEY_LEFT,
        ],
        'right': [
            ord('l'),
            curses.KEY_RIGHT,
        ],
        'down': [
            ord('j'),
            curses.KEY_DOWN,
        ],
        'up': [
            ord('k'),
            curses.KEY_UP,
        ],
        'pgdn': [
            ord('f'),
            curses.KEY_NPAGE,
        ],
        'pgup': [
            ord('b'),
            curses.KEY_PPAGE,
        ],
        'top': [
            ord('g'),
            curses.KEY_HOME,
        ],
        'bottom': [
            ord('G'),
            curses.KEY_END,
        ],
        'goto': [
            ord('#'),
            curses.ascii.ctrl(ord('g')),
        ],
        'find': [
            ord('/'),
        ],
        'next_find': [
            ord('n'),
            curses.ascii.ctrl(ord('s')),
        ],
        'prev_find': [
            ord('p'),
            curses.ascii.ctrl(ord('r')),
        ],
        'next_pick': [
            curses.ascii.ctrl(ord('n')),
        ],
        'prev_pick': [
            curses.ascii.ctrl(ord('p')),
        ],
        'reset': [
            ord('r'),
            curses.KEY_F5,
        ],
        'recenter': [
            ord('z'),
            curses.ascii.ctrl(ord('l')),
        ],
        'pick': [
            ord('\n'),
        ],
        'pick_pattern': [
            ord(';'),
        ],
        'undo': [
            ord('u'),
        ],
        'undo_up': [
            ord('U'),
        ],
        'toggle': [
            ord('t'),
        ],
        'toggle_down': [
            ord(' '),
        ],
        'toggle_up': [
            curses.ascii.ctrl(ord(' ')),
        ],
        'toggle_all': [
            ord('a'),
        ],
        'toggle_pattern': [
            ord(':'),
        ],
        'view_picks': [
            ord('v'),
        ],
        'view_help': [
            ord('?'),
            curses.KEY_F1,
        ],
        'save': [
            ord('w'),
            curses.ascii.ctrl(ord('s')),
        ],
        'quit': [
            ord('q'),
            curses.ascii.ESC,
        ],
    }

    return desc, keys
