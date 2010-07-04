def humanize_list(l, conj):
    if len(l) < 1:
        return ''
    elif len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return "%s %s %s" % (l[0], conj, l[1])
    else:
        return "%s, %s %s" % (', '.join(l[:-1]), conj, l[-1])
