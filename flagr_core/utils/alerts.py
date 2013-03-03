#!/usr/bin/env python
"""
Util for rendering alerts

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from views.partials.alerts.alertsTmpl import alertsTmpl


def alert(message, quip="", alertType=""):
    if alertType == "info":
        alertType = "alert-%s"%alertType
        icon = "info-sign"
    elif alertType == "success":
        alertType = "alert-%s"%alertType
        icon = "thumbs-up"
    elif alertType == "warning":
        alertType = ""
        icon = "excalmation-mark"
    elif alertType == "error":
        alertType = "alert-%s"%alertType
        icon = "warning-sign"

    tmpl = alertsTmpl()
    tmpl.alertType = alertType
    tmpl.quip = quip
    tmpl.message = message
    tmpl.icon = icon

    return str(tmpl)

