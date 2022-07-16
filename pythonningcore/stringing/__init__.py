import re

__all__ = ("generateAbreviationFromName",)


def generateAbreviationFromName(name):
    # type: (str) -> str
    """
    Convert the given anme to a shorter version. This is clearly not a perfect
    conversion and would ideally need a manual modification by a human.

    - If contains a "_": "make_soup" -> "msp" ; "video_encoding_test" -> "vett"
    - If camelcase suntax : "makeSoup" -> "msp"; "videoEncondingTest" -> "vett"
    - Else just remove vowels: "makesoup" -> "mksp"

    Args:
        name: string to generate an abbreviation from.

    Returns:
        name but in a shorter version
    """

    if "_" in name:
        buf = name.split("_")
        out = [s[0] for s in buf]
        out = "".join(out).lower()
        out += buf[-1][-1]

    elif re.search(r"[A-Z]", name):
        # SRC: https://stackoverflow.com/a/2279177/13806195
        buf = re.sub(r"([A-Z])", r" \1", name).split()
        out = [s[0] for s in buf]
        out = "".join(out).lower()
        out += buf[-1][-1]

    else:
        out = re.sub(r"[AEIOU]", "", name, flags=re.IGNORECASE)

    return out
