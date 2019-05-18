#!/usr/bin/env python3
"""
Greeting function.

"""
# [==- )a, -=================]
# [==- )/#L, -===============]
# [==- v("###a -=============]
# [==- vv,"####a, -==========]
# [==- vv( 4#####L, -========]
# [=- =vvv  !!4#####a -======]
# [=- =vv>       !!!##a,. -==]
# [=- =v> sXXXXXXXsssss**- -=]
# [=- %>_XXXXXXXX7"""" -=====]
# [=- vJ7"""" -==============]

import shutil


def ngreeting():
    """
    Create a colorful greeing string.

    """
    # colors
    blue = "\u001b[38;5;61m"
    green = "\u001b[38;5;107m"
    orange = "\u001b[38;5;209m"

    reset = "\u001b[0m"

    color1 = blue
    color2 = green
    color3 = orange

    left = "  {}".format(reset)

    cotri = [
        "{}  {}){}a,".format(left, color1, color3),
        "{}  {})/{}#L,".format(left, color1, color3),
        "{}  {}v({}\"###a".format(left, color1, color3),
        "{}  {}vv,{}\"####a,".format(left, color1, color3),
        "{}  {}vv( {}4#####L,".format(left, color1, color3),
        "{} {}=vvv  {}!!4#####a".format(left, color1, color3),
        "{} {}=vv>       {}!!!##a,.".format(left, color1, color3),
        "{} {}=v> {}sXXXXXXXsssss*{}{}*-".format(left, color1, color2, reset, color3),
        "{} {}%>{}_XXXXXXXX7\"\"\"\"".format(left, color1, color2),
        "{} {}v{}J7\"\"\"\"           {}mp".format(left, color1, color2, reset)
    ]
    greet = "\n"
    for s in cotri:
        greet += "{}\n".format(s)

    return greet

def greeting(text=None):
    """
    Create a colorful greeting string.

    Can add a small string of max 10 characters.

    """
    # colors
    blue = "\u001b[38;5;61m"
    green = "\u001b[38;5;107m"
    orange = "\u001b[38;5;209m"

    reset = "\u001b[0m"

    color1 = blue
    color2 = green
    color3 = orange

    light_grey = "\u001b[38;5;255m"
    grey       = "\u001b[38;5;248m"
    dark_grey  = "\u001b[38;5;242m"

    term_width = shutil.get_terminal_size((80, 23)).columns
    if term_width > 80:
        term_width = 80         # no need to get wider

    multiplier = int((term_width - 28) / 6)  # width of image by 6
    space_padding = " " * multiplier
    padding = "=" * multiplier

    left_long = "{}{}[{}=={}{}-".format(space_padding, dark_grey, grey, padding,
                                        light_grey)
    left_short = "{}{}[{}={}{}-".format(space_padding, dark_grey, grey, padding,
                                        light_grey)
    right = "{}-{}={}".format(light_grey, grey, padding)

    if text:
        tlen = len(text)
        if tlen > 10:
            raise ValueError("Greeting name cannot be longer that 10 characters")
        slen = 10 - tlen
        microtext = "{} {}{}{} ".format("="*slen, light_grey, text, grey)
    else:
        microtext = "=" * 12

    cotri4 = [
        "{} {}){}a, {}================{}]".format(left_long, color1, color3,
                                                  right, dark_grey),
        "{} {})/{}#L, {}{}=={}]".format(left_long, color1, color3, right,
                                        microtext, dark_grey),
        "{} {}v({}\"###a {}============{}]".format(left_long, color1, color3,
                                                   right, dark_grey),
        "{} {}vv,{}\"####a, {}========={}]".format(left_long, color1, color3,
                                                   right, dark_grey),
        "{} {}vv( {}4#####L, {}======={}]".format(left_long, color1, color3,
                                                  right, dark_grey),
        "{} {}=vvv  {}!!4#####a {}====={}]".format(left_short, color1, color3,
                                                   right, dark_grey),
        "{} {}=vv>       {}!!!##a,. {}={}]".format(left_short, color1, color3,
                                                   right, dark_grey),
        "{} {}=v> {}sXXXXXXXsssss*{}{}*- {}{}]".format(left_short, color1,
                                                       color2, reset, color3,
                                                       right, dark_grey),
        "{} {}%>{}_XXXXXXXX7\"\"\"\" {}===={}]".format(left_short, color1,
                                                       color2, right,
                                                       dark_grey),
        "{} {}v{}J7\"\"\"\" {}======== {}mp{} ={}]{}".format(left_short, color1,
                                                             color2, right,
                                                             light_grey, grey,
                                                             dark_grey, reset)
    ]

    greet = "\n"

    for i in cotri4:
        greet += "{}\n".format(i)

    return greet


if __name__ == "__main__":
    print(ngreeting())
    print(greeting("flte"))
