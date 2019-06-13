#!/usr/bin/env python3
"""
Greeting function.

"""
def ngreeting():
    """
    Create a colorful greeing string.

    """
    orangeyellow = "\u001b[38;5;214m"

    darkgrey = "\u001b[38;5;246m"
    mediumgrey = "\u001b[38;5;250m"
    lightgrey = "\u001b[38;5;252m"

    reset = "\u001b[0m"

    color1 = mediumgrey
    color2 = darkgrey
    color3 = lightgrey
    color4 = orangeyellow

    mp_logo = [
        "        {}_c{}".format(color1, reset),
        "       {}<Qm {}.QQf  {}_; {}_{}".format(color1, color2, color3, color4, reset),
        "      {}jQQ? {})QF {}_w@` {}dm,{}".format(color1, color2, color3, color4, reset),
        "     {}jQP`  {}jP  {}mQf {}.QQf{}".format(color1, color2, color3, color4, reset),
        "    {}jD^   {}.2  {}.QW` {}=Q({}".format(color1, color2, color3, color4, reset),
        "  {}.J!         {}:Qf  {})^{}".format(color1, color3, color4, reset),
        "  {}-           {}=W'".format(color1, color3, reset),
        "              {})F{}".format(color3, reset),
        "              {}]'{}".format(color3, reset),
        "              {}={}".format(color3, reset)
    ]

    greet = "\n"
    for s in mp_logo:
        greet += "{}\n".format(s)

    return greet

if __name__ == "__main__":
    print(ngreeting())
