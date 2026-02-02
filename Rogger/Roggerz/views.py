from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from Rogger.download import down,san
import os

def extract(request):
    if request.method == "POST":
        url = request.POST.get("yt_url")
        if not url:
            return HttpResponse("Paste a YouTube link")

        try:
            filepath = down(url) 
            filename = os.path.basename(filepath)
            return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
        except Exception as e:
            print("e:",e)
            return HttpResponse(f"Download failed: {e}")

    return render(request, "Roggerz/all.html")