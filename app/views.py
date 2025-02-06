from django.shortcuts import redirect


def redirect_to_docs(self):
    return redirect("/api/docs")
