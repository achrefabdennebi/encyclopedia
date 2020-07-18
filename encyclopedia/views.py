import random
from django import forms
from django.shortcuts import render, HttpResponseRedirect, reverse
from . import util
from re import search as searchSubstr

class NewPageForm(forms.Form): 
    title = forms.CharField(label="New entry")
    type_view = forms.CharField(widget=forms.HiddenInput(), 
    required = False, initial="add")
    content = forms.CharField(widget=forms.Textarea(
        attrs={"cols":5, "rows":5, "placeholder": "Content of entry"}))

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

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            type_view = form.cleaned_data["type_view"]
            is_existed_title = util.get_entry(title)
            if is_existed_title != None and type_view == "add":
                msg = "Existed page name, please try again."
                return  render(request, "encyclopedia/add.html", {
                            "title": "Add entry",
                            "form": NewPageForm(),
                            "Error": msg
                        })
            else: 
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entryPage", args=[title]))


    return render(request, "encyclopedia/add.html", {
        "title": "Add entry",
        "form": NewPageForm()
    })

def edit(request, title):
    entry = util.get_entry(title)
    form = NewPageForm({'title': title, 'content': entry, 'type_view': 'edit'})
    return render(request, "encyclopedia/add.html",{
        "title": "Edit entry",
        "form": form
    })

def random_link(request): 
    random_title  = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entryPage", args=[random_title]))
