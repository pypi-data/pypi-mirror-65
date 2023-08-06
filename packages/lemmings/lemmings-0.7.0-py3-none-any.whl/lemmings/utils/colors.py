from lemmings.utils.utils import ignore_exception


class Color:
    e = "\033[0m"  # End of color
    m = "\033[1m"  # bold
    i = "\033[3m"  # cursive
    s = "\033[4m"  # cursive
    black, red, green, yellow, blue, magenta, cyan, white = 0, 1, 2, 3, 4, 5, 6, 7

    @classmethod
    def _(cls, typ, color, bright):
        b = ";1" if bright else ""
        return f"\033[{typ}{color}{b}m"

    @classmethod
    def _foreground(cls, color, bright=False):
        return cls._(3, color, bright)

    @classmethod
    def _light(cls, color, bright=False):
        return cls._(9, color, bright)

    @classmethod
    def _background(cls, color, bright=False):
        return cls._(4, color, bright)

    @classmethod
    @ignore_exception
    def execute(cls, cmd, msg):
        return cmd + str(msg) + cls.e

    @classmethod
    def bold(cls, msg):
        return Color.execute(cls.m, msg)

    @classmethod
    def cursive(cls, msg):
        return Color.execute(cls.i, msg)

    @classmethod
    def underline(cls, msg):
        return Color.execute(cls.s, msg)

    @classmethod
    def mark(cls, color, msg):
        return Color.execute(Color._foreground(color), msg)

    @classmethod
    def back(cls, color, msg):
        return Color.execute(Color._background(color), msg)

    @classmethod
    @ignore_exception
    def print_full(cls, back, color, msg, comment="", prefix=""):
        print(prefix + cls.b[back % len(Color.b)] + cls.c[color % len(Color.c)] + str(msg) + cls.e + str(comment))

    @classmethod
    def print(cls, color, msg, comment="", prefix=""):
        Color.print_full(color, color, msg, comment, prefix)


Color.b = (
    Color._background(Color.black),
    Color._background(Color.black),
    Color._background(Color.red),
    Color._background(Color.yellow),
)
Color.c = (
    # C.fore(C.red),
    # C.back(C.red)+C.light(C.white, True),
    Color._foreground(Color.green),
    Color._light(Color.white),
    Color._foreground(Color.blue),
    Color._foreground(Color.black),
)

if __name__ == '__main__':
    for i in range(len(Color.c)):
        Color.print(i, f" test color#{i}")
