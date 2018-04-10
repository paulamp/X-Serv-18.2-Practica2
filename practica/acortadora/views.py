from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Url


def redirigir(request,id):
	try:
		redirecion = Url.objects.get(short_url="http://localhost:8000/"+str(id))
		return HttpResponseRedirect(redirecion.url)
	except:
		response = "<html><body><h2>Recurso no disponible</h2><br>"
		response += "<a href='/'>Inicio</a></body></html>"
		return HttpResponse(response,status=400)

def imprimir_urls_guardadas():
	urls = Url.objects.all()
	response = ""
	for url in urls:
		response += "URL real: <a href=" + url.url
		response += ">" + url.url + "</a>"
		response += " -> URL acortada: <a href=" + url.short_url
		response += ">" + url.short_url + "</a><br>"
	return response

@csrf_exempt
def acortar (request):
	response = ""
	if request.method == "GET":
		formulario="""
		<form action="/" method="post">
		<p>Introduce la Url <input type="text" name="url"/></p>
		<p><input type="submit" value="Enviar"/></p>
		</form>
		"""
		urls_acortadas=imprimir_urls_guardadas()
		response = "<html><body>" + formulario + urls_acortadas + "</body></html>"

	elif request.method == "POST":
		valor_url = request.POST.get('url')
		response = ""
		if valor_url:
			if not "http://" in valor_url and not "https://" in valor_url:
				valor_url = "http://" + valor_url
			url = Url.objects.filter(url=valor_url)
			if not url:
				url = Url()
				url.url = valor_url
				url.short_url = "http://localhost:8000/"+ str(Url.objects.all().count())
				url.save()
			response += "URL real: <a href=" + url.url
			response += ">" + url.url + "</a>"
			response += " -> URL acortada: <a href=" + url.short_url
			response += ">" + url.short_url + "</a><br>"
			response += "<a href='/'>Introducir otra Url</a></body></html>"
		else:
			response = "<html><body>URL no valida<br>"
			response += "<a href='/'>Inicio</a></body></html>"
			return HttpResponse(response,status=400)
	else:
		response = "invalid method"
		return HttpResponse(response,status=400)
	return HttpResponse(response)

