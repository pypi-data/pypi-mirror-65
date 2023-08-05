import getopt
import os
import sys

app_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(app_root)

import ct


def show_all():
    for k in ct.registered:
        getattr(ct, k)()


def prt_styles():
    for i, v in enumerate(ct.registered):
        if len(v) == 1:
            getattr(ct, v)()


def prt_usg():
    ct.g(f'''USAGE: python {__file__} -s <style_color:Bg> -t <text>
    ''')
    ct.By('''two rules:
    - styles require alphabet order
    - styles go before colors
    ''')
    print()
    ct.Bg('<STYLES>: use with alphabet order')
    for k, v in ct.STYLE_HELPER.items():
        ct.g(f'\t{k} == {v}')
    print()
    ct.Bg('<COLORS>: <fg> on <bg>')
    for k, v in ct.COLOR_HELPER.items():
        ct.g(f'\t{k} == {v}')
    sys.exit(0)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'haVs:t:', ['styles=', 'text=', 'all'])
    except getopt.GetoptError:
        prt_usg()

    if not opts:
        prt_usg()

    style = text = ''
    for opt, arg in opts:
        if opt == '-h':
            prt_usg()
        elif opt in ('-V', '--version'):
            ct.BI(f'sgr-ansi VERSION: {ct.VERSION}')
            sys.exit(0)
        elif opt in ('-a', '--all'):
            show_all()
            sys.exit(0)
        elif opt in ('-s', '--styles'):
            style = arg
        elif opt in ('-t', '--text'):
            text = arg

    getattr(ct, style)(text)


if __name__ == '__main__':
    main(sys.argv[1:])
