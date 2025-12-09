from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from Rogger.download import down
import os

def extract(request):
    if request.method == "POST":
        url = request.POST.get("yt_url")
        if not url:
            return HttpResponse("Paste a YouTube link")

        try:
            filepath = down(url)  # returns full path on server
            filename = os.path.basename(filepath)
            # Send file as download to browser
            return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
        except Exception as e:
            return HttpResponse(f"Download failed: {e}")

    return render(request, "Roggerz/all.html")
