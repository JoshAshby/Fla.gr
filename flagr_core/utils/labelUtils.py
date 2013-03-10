
def listLabels(flags):
    labels = []
    for flag in flags:
        labels.extend(flag.labels)
    return labels
