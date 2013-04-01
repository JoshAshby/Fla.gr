#!/usr/bin/env python
"""
Util for rendering alerts
"""
from views.partials.alerts.alertsTmpl import alertsTmpl


def alert(message, quip="", alertType=""):
    """
    Generates an HTML alert

    :param message: The main body of the alert
    :type message: Str
    :param quip: A bolded title for the alert, shouldn't be too long.
    :type quip: Str
    :param alertType: Defines the color of the alert, can be `info` `success` `warning` or `error`
    :type alertType: Str

    :return: The rendered template with the alert data.
    :rtype: Str
    """
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

