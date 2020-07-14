from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request, title):
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "title": "{}: Entry not found".format(title.capitalize()),
            "error" : "Oops ! entry not exited, please enter an existing entry."
        })

    return render(request, "encyclopedia/entrypage.html", {
        "title" : title.capitalize(),
        "entry": entry
    })

