from django.shortcuts import render

from . import util

from re import search as searchSubstr
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

def search(request):
    if request.method == "GET":
        keyword = request.GET['q']
        entry = util.get_entry(keyword)
        if entry != None:
            return render(request, "encyclopedia/entrypage.html", {
                "title" : keyword.capitalize(),
                "entry": entry
            })

    entries = util.list_entries()
    search_results = []
    for name in entries:
        if searchSubstr(keyword.upper(), name.upper()):
            search_results.append(name)

    return render(request, "encyclopedia/searchResults.html", {
    "title": "Search Results: {}".format(keyword),
    "entries": search_results
    })