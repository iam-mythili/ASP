import sys, os, difflib, re, string
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

AUTHOR_NAME = "TEAM MEMBERS: Mythili | Swathi | Hafiza | Haziqa | Salma |"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title_half_color(text, author_name=""):
    fig = Figlet(font='slant')
    rendered = fig.renderText(text)
    lines = rendered.splitlines()
    nrows = len(lines)
    mid = nrows // 2
    for i, line in enumerate(lines):
        buf = ""
        color = Fore.YELLOW + Style.BRIGHT if i < mid else Fore.BLUE + Style.BRIGHT
        for c in line:
            buf += color + c + Style.RESET_ALL if c != " " else " "
        print(buf)
    if author_name:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + " " * 6 + author_name + Style.RESET_ALL + '\n')

PY_KEYWORDS = [
    'False','None','True','and','as','assert','async','await','break','class','continue','def','del',
    'elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal',
    'not','or','pass','raise','return','try','while','with','yield','print'
]
PY_BUILTINS = [
    'input','len','int','float','str','list','dict','set','tuple','range','type','open','abs','sum',
    'min','max','any','all','super','format','enumerate','sorted','map','filter','help','reversed'
]
PY_LIBRARIES = [
    'os','sys','re','math','statistics','random','datetime','time','json','csv','pdb','copy','shutil','itertools','functools',
    'collections','heapq','bisect','array','subprocess','logging','argparse','pickle','traceback','typing','unittest',
    'string','socket','inspect','glob','gzip','tarfile','zipfile','io','uuid','numpy','np','pandas','pd','matplotlib','plt',
    'scipy','sklearn','seaborn','sns','requests','flask','django','pytest','beautifulsoup4','bs4','lxml','PIL','tqdm',
    'pyplot','torch','tensorflow','keras'
]
ALL_WORDS = set(PY_KEYWORDS + PY_BUILTINS + PY_LIBRARIES)
PY_ALIAS = {
    "dfe":"def", "pritn":"print", "prnit":"print", "improt":"import", "printf":"print",
    "flase":"False", "treu":"True", "nnoe":"None", "clas":"class", "funtion":"function", "contiune":"continue",
    "retun":"return", "wihle":"while", "exepct":"except", "finall":"finally", "fucntion":"function", "lenght":"length",
    "strnig":"string", "dicti":"dict", "tupel":"tuple", "claas":"class", "prnt":"print", "prit":"print", "prnitf":"print",
    "np":"numpy", "nmpy":"numpy", "pd":"pandas", "plt":"matplotlib", "sns":"seaborn", "sp":"scipy", "sk":"sklearn",
    "req":"requests", "bs":"bs4", "tf":"tensorflow", "ss":"sys","is":"os","ps":"os"
}
PAIRS = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}

def autocorrect_func_names(line, keywords, alias):
    def fixfunc(match):
        fname = match.group(1)
        fixed = autocorrect_word(fname, keywords, alias)
        return fixed + '('
    return re.sub(r'\b([A-Za-z_][A-Za-z0-9_]*)\(', fixfunc, line)

def autocorrect_word(word, words, alias):
    lw = word.lower()
    if lw in alias: return alias[lw]
    if word in words or not word.isidentifier() or len(word) < 2: return word
    matches = difflib.get_close_matches(word, words, n=1, cutoff=0.7)
    return matches[0] if matches else word

HIGHLIGHT_MAP = {
    "keyword": Fore.BLUE + Style.BRIGHT,
    "builtin": Fore.LIGHTCYAN_EX + Style.BRIGHT,
    "string": Fore.GREEN + Style.BRIGHT,
    "number": Fore.CYAN + Style.BRIGHT,
    "comment": Fore.LIGHTBLACK_EX + Style.DIM,
    "library": Fore.MAGENTA + Style.BRIGHT,
    "def": Fore.MAGENTA + Style.BRIGHT,
    "import": Fore.LIGHTYELLOW_EX + Style.BRIGHT,
    "from": Fore.LIGHTYELLOW_EX + Style.BRIGHT,
    "class": Fore.RED + Style.BRIGHT,
    "reset": Style.RESET_ALL
}

def syntax_highlight(line):
    def kw_color(w):
        if w in ("def",): return HIGHLIGHT_MAP["def"]
        if w in ("import",): return HIGHLIGHT_MAP["import"]
        if w in ("from",): return HIGHLIGHT_MAP["from"]
        if w in ("class",): return HIGHLIGHT_MAP["class"]
        if w in PY_KEYWORDS: return HIGHLIGHT_MAP["keyword"]
        if w in PY_BUILTINS: return HIGHLIGHT_MAP["builtin"]
        if w in PY_LIBRARIES: return HIGHLIGHT_MAP["library"]
        return ""
    out, i, L = "", 0, len(line)
    while i < L:
        c = line[i]
        if c == "#":
            out += HIGHLIGHT_MAP["comment"] + line[i:] + HIGHLIGHT_MAP["reset"]
            break
        elif c in ("'", '"'):
            quote = c
            j = i+1
            while j < L and (line[j] != quote or (j > i+1 and line[j-1] == '\\')):
                j += 1
            j = min(L-1, j)
            out += HIGHLIGHT_MAP["string"] + line[i:j+1] + HIGHLIGHT_MAP["reset"]
            i = j
        elif c.isdigit():
            j = i
            while j < L and (line[j].isdigit() or line[j] == "."):
                j += 1
            out += HIGHLIGHT_MAP["number"] + line[i:j] + HIGHLIGHT_MAP["reset"]
            i = j-1
        elif c.isalpha() or c == "_":
            j = i
            while j < L and (line[j].isalnum() or line[j]=="_"):
                j += 1
            w = line[i:j]
            color = kw_color(w)
            if color:
                out += color + w + HIGHLIGHT_MAP["reset"]
            else:
                out += w
            i = j-1
        else:
            out += c
        i += 1
    return out

def getch():
    try:
        import msvcrt
        def win_getch():
            while True:
                ch = msvcrt.getwch()
                if ch == '\x13': return 'ctrl+s'
                if ch == '\x1b': return 'esc'
                if ch == '\x03': return 'ctrl+c'
                if ch in ('\r', '\n'): return '\n'
                if ch in ('\x00','\xe0'):
                    k = msvcrt.getwch()
                    if k in 'HPMK': return {'H':'up','P':'down','K':'left','M':'right'}[k]
                    else: continue
                if ch in ('\x08', '\x7f', '\b'):
                    return 'backspace'
                if ch.isprintable():
                    return ch
        return win_getch
    except ImportError:
        import tty, termios
        def unix_getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x13': return 'ctrl+s'
                if ch in ('\r','\n'): return '\n'
                if ch == '\x1b':
                    seq = sys.stdin.read(2)
                    return {'[A':'up','[B':'down','[C':'right','[D':'left'}.get(seq,'')
                if ch == '\x03': return 'ctrl+c'
                if ch in ('\x08', '\x7f', '\b'):
                    return 'backspace'
                if ch.isprintable():
                    return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return unix_getch
getkey = getch()

def render(lines, cur, pos, winlen=24):
    n = len(lines)
    top = max(0, min(cur - winlen // 2, max(0, n - winlen)))
    bottom = min(top + winlen, n)
    clear_screen()
    for i in range(top, bottom):
        l = lines[i]
        pfx = Fore.MAGENTA+">"+Style.RESET_ALL if i == cur else " "
        colored = syntax_highlight(l)
        if i == cur:
            before = syntax_highlight(l[:pos])
            after = syntax_highlight(l[pos:])
            sys.stdout.write(f"{pfx}{str(i+1).rjust(4)} {before}|{after}\n")
        else:
            sys.stdout.write(f"{pfx}{str(i+1).rjust(4)} {colored}\n")

def current_word(buf, pos):
    if not buf: return pos, pos, ""
    start = pos
    while start > 0 and (buf[start-1].isalnum() or buf[start-1] == '_'): start -= 1
    end = pos
    while end < len(buf) and (buf[end].isalnum() or buf[end] == '_'): end += 1
    return start, end, buf[start:end]

def triggers_colon(line):
    # Accepts def hello(), class X, if a==b, else, for a in b, etc. missing colon
    s = line.strip()
    triggers = ['def ', 'class ', 'if ', 'elif ', 'else', 'for ', 'while', 'try', 'except', 'finally', 'with ']
    return any(s.startswith(t) for t in triggers) and not s.endswith(':')

def line_indent(line):
    return len(line) - len(line.lstrip(' '))

def prompt_action():
    print(
        Fore.YELLOW + Style.BRIGHT + "Choose an action:" + Style.RESET_ALL + "\n" +
        Fore.YELLOW + "  1" + Style.RESET_ALL + Fore.CYAN + " - Create new file" + Style.RESET_ALL + "\n" +
        Fore.YELLOW + "  2" + Style.RESET_ALL + Fore.CYAN + " - Edit existing file" + Style.RESET_ALL
    )
    while True:
        print(Fore.YELLOW + "Enter 1 or 2: " + Style.RESET_ALL, end="")
        act = input().strip()
        if act in ('1', '2'): return act

def choose_save_folder():
    return os.getcwd()

def insert_pair(char, buf, pos):
    close = PAIRS[char]
    return buf[:pos] + char + close + buf[pos:], pos + 1

def main():
    clear_screen()
    print_title_half_color("AutoSyntaxPy", AUTHOR_NAME)
    act = prompt_action()
    print(Fore.LIGHTWHITE_EX+"Enter file name: "+Style.RESET_ALL, end="")
    filename = input().strip()
    if not filename.endswith('.py'):
        print(Fore.RED+"Only .py files supported."+Style.RESET_ALL); return
    folder = choose_save_folder()
    clear_screen()
    fullpath = os.path.join(folder, filename)
    if act == "2":
        try:
            with open(fullpath, encoding="utf-8") as f:
                lines = [l.rstrip("\r\n") for l in f]
            if not lines: lines = [""]
        except: lines = [""]
    else:
        lines = [""]

    cur = len(lines) - 1
    pos = len(lines[cur])

    try:
        while True:
            render(lines, cur, pos)
            ch = getkey()
            buf = lines[cur]
            if ch == 'ctrl+s':
                with open(fullpath, "w", encoding="utf-8") as fw:
                    for l in lines: fw.write(l + "\n")
                clear_screen()
                print(Fore.CYAN+Style.BRIGHT+f"Code saved to: {fullpath}"+Style.RESET_ALL)
                sys.exit(0)
            elif ch in ('esc', 'ctrl+c'):
                clear_screen()
                print(Fore.RED+"Exited (not saved)"+Style.RESET_ALL)
                sys.exit(0)
            elif ch == 'up':
                if cur > 0: cur -= 1; pos = min(pos, len(lines[cur]))
            elif ch == 'down':
                if cur < len(lines) - 1:
                    cur += 1; pos = min(pos, len(lines[cur]))
                elif lines[-1] != "":
                    lines.append(""); cur += 1; pos = 0
            elif ch == 'left': pos = max(0, pos - 1)
            elif ch == 'right': pos = min(len(lines[cur]), pos + 1)
            elif ch == 'backspace':
                if pos > 0:
                    lines[cur] = buf[:pos - 1] + buf[pos:]
                    pos -= 1
                elif cur > 0:
                    prev = lines[cur - 1]
                    pos = len(prev)
                    lines[cur - 1] = prev + lines[cur]
                    lines.pop(cur)
                    cur -= 1
            elif ch == ' ':
                s, e, w = current_word(buf, pos)
                if w:
                    fixed = autocorrect_word(w, ALL_WORDS, PY_ALIAS)
                    lines[cur] = buf[:s] + fixed + buf[e:]
                    pos = s + len(fixed)
                    buf = lines[cur]
                lines[cur] = autocorrect_func_names(lines[cur], ALL_WORDS, PY_ALIAS)
                buf = lines[cur]
                lines[cur] = buf[:pos] + ' ' + buf[pos:]
                pos += 1
            elif ch == '\n':
                s, e, w = current_word(buf, pos)
                if w:
                    fixed = autocorrect_word(w, ALL_WORDS, PY_ALIAS)
                    lines[cur] = buf[:s] + fixed + buf[e:]
                    pos = s + len(fixed)
                    buf = lines[cur]
                lines[cur] = autocorrect_func_names(lines[cur], ALL_WORDS, PY_ALIAS)
                buf = lines[cur]
                left = buf[:pos]
                right = buf[pos:]

                prev_strip = left.rstrip()
                prev_indent = line_indent(left)

                # If block keyword but missing colon, insert colon and indent
                if triggers_colon(prev_strip):
                    left = left.rstrip() + ':'
                    newindent = prev_indent + 4
                # If already ends with a colon, just indent
                elif prev_strip.endswith(':'):
                    newindent = prev_indent + 4
                else:
                    newindent = prev_indent

                lines[cur] = left
                lines.insert(cur+1, ' ' * newindent + right.lstrip())
                cur += 1
                pos = newindent
            elif ch in PAIRS:
                lines[cur], pos = insert_pair(ch, buf, pos)
            elif (isinstance(ch, str) and len(ch)==1 and ch.isprintable()):
                lines[cur] = buf[:pos] + ch + buf[pos:]
                pos += 1
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.RED+"\nExited (not saved)"+Style.RESET_ALL)
        sys.exit(0)

if __name__ == "__main__":
    main()
