ZERO_WIDTH_CHARS = ["\u200b", "\u200c", "\u200d", "\ufeff", "\u2060"]

# Visual homoglyph \u2192 Latin equivalent \u2014 lowercase only (normalize() lowercases before applying this)
CONFUSABLES = {
    # Greek lowercase
    "\u03b1": "a",  # \u03b1
    "\u03b5": "e",  # \u03b5
    "\u03b7": "h",  # \u03b7 (looks like h)
    "\u03b9": "i",  # \u03b9
    "\u03ba": "k",  # \u03ba
    "\u03bf": "o",  # \u03bf
    "\u03c4": "t",  # \u03c4
    "\u03c5": "u",  # \u03c5
    "\u03c7": "x",  # \u03c7
    # Cyrillic lowercase
    "\u0430": "a",  # \u0430
    "\u0435": "e",  # \u0435
    "\u043d": "h",  # \u043d (looks like h)
    "\u043e": "o",  # \u043e
    "\u0440": "p",  # \u0440 (looks like p)
    "\u0441": "c",  # \u0441 (looks like c)
    "\u0445": "x",  # \u0445
    "\u0443": "y",  # \u0443 (looks like y)
}
