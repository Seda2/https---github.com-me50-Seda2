from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from . import util
import random
import markdown2
from markdown2 import Markdown
import secrets
import wiki
from django.db import models
from django.forms import ModelForm, Textarea


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries()        
    })

def title(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/title.html", {
            "entry": markdowner.convert(entryPage),
            "entryTitle": entry
        })


def search(request):
    if request.method == "POST":
        query = request.POST['q'] 
        entries = util.list_entries()
        results = [ ]
        if query in entries:
            return render(request, "encyclopedia/title.html", {
                "entry": markdown2.markdown(util.get_entry(query)),
                "title": query
                })
        else:
            for entry in entries:
                 if query.lower() in entry.lower():
                    results.append(entry)
                    return render(request, "encyclopedia/searchsubstring.html", { 
                    "results": results
    })
    
class NewPageForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def createNewPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("title", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "existing": True,
                "entry": title
                })
        else:
            return render(request, "encyclopedia/newpage.html", {
            "form": form,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/newpage.html", {
            "form": NewPageForm(),
            "existing": False
        })    

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html" )
    else:
        form = NewPageForm()
        form.fields["title"].initial = entry     
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newpage.html", {
            "form": form
        })        
            

def Random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("title", kwargs={'entry': randomEntry}))

