
def listLabels(flags, showAll):
    labels = []
    for flag in flags:
        if showAll:
            labels.extend(flag.labels)
        else:
            if flag.visibility:
                labels.extend(flag.labels)
    return labels
