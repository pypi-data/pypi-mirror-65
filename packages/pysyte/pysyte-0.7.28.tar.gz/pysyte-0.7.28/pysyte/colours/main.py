import os
from pysyte.colours import ansi_escapes
from pysyte.colours import colour_numbers
from pysyte.colours.texts import colour_initials


def test():
    return ansi_escapes.foreground_string(
        'hello', colour_numbers.html_to_int('0x00FF00'))


def main():
    for b in range(8):
        print(ansi_escapes.background(b), end='')
        for f in range(8):
            print('%s%s%s%s%s' % (
                ansi_escapes.foreground(f),
                ansi_escapes.bold(),
                'hello ',
                ansi_escapes.no_bold(),
                'world'), end='')
        print(ansi_escapes.no_colour())

    term = os.environ.get('TERM', '')
    if '256' in term or term == 'linux':
        for foregound in ['8b4513', '00ff7f', 'ff1493']:
            print(ansi_escapes.foreground_string(
                'hello', colour_numbers.html_to_int(foregound)))
        print(ansi_escapes.no_colour())
    print(colour_initials(['Hello ', 'World'], 'red').colour('!', 'green'))


if __name__ == '__main__':
    main()

