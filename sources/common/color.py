



def hue2rgb(v: float):
    # HUE to RGB transformation function.
    r = (5 + (v * 6)) % 6
    g = (3 + (v * 6)) % 6
    b = (1 + (v * 6)) % 6

    c = lambda k: 1.0 - max( min( [k, 4-k, 1] ), 0 )

    return (int(c(r)), int(c(g)), int(c(b)))

