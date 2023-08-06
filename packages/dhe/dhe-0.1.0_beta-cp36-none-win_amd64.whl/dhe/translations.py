import gettext

APP = "dhe"
gettext.bindtextdomain(APP, "lang")
gettext.textdomain(APP)
__ = gettext.gettext
