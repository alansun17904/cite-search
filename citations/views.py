import json
import threading
import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from citations.forms import QueryCitationForm
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView


# Connect to twilio to email full bibtex document


# Class Based Views
class IndexView(FormView):
    template_name = 'index.html'
    form_class = QueryCitationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            query = form.cleaned_data.get('query')
            return HttpResponseRedirect(
                    reverse_lazy('citations:result', args=[query]) 
            )
        else:
            return render(request, 'index.html')

class GraphView(TemplateView):
    template_name = 'citations/results.html'
    
    def get(self, request, *args, **kwargs):
        doi = kwargs['query']
        meta = requests.get('https://opencitations.net/index/coci/api/v1/metadata/' + doi)
        if meta.status_code == 500:
            return render(request, self.template_name, context={'found':False})

        data = meta.json()
        citations = requests.get('https://opencitations.net/index/coci/api/v1/citations/' + doi)
        citations = citations.json()
        
        if len(citations) == 0:
            return render(request, self.template_name, context={
                'found': True,
                'title': data[0]['title'],
                'author': data[0]['author'],
                'citations': len(citations),
            })

        num_citations = len(citations)
        nodes = []

        cited = []
        def get_citing(doi, i, lock):
            meta = requests.get('https://opencitations.net/index/coci/api/v1/metadata/' + doi)
            if meta.status_code != 200:
                return
            jjson = meta.json()[0]
            title = jjson['title']
            author = jjson['author']
            cites = jjson['citation_count']
            # Get the metadata for the current node.
            lock.acquire()
            nodes.append({'title': title, 'author': author, 'doi': doi, 'cites': cites, 'group': i})
            lock.release()
            # Get nodes that cite the current node.
            citations = requests.get('https://opencitations.net/index/coci/api/v1/citations/' + doi)
            citations = citations.json()
            lock.acquire()
            cited.extend(citations)
            lock.release()
 

        layers = []
        links = []
        for i in range(5):
            lock = threading.Lock()
            threads = []
            cited = [] 
            for i in range(min(20, len(citations))):
                t = threading.Thread(target=get_citing, args=(citations[i]['citing'],i,lock))
                links.append({'source':citations[i]['cited'],'target':citations[i]['citing']})
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()
            _ = [layers.append(v) for v in nodes]
            citations = cited.copy()
            cited = []
            nodes = []
            

        layers.append({'title':data[0]['title'],'author':data[0]['author'],'doi':doi.lower(),'cites':num_citations,'group':6})

        return render(request, self.template_name, context={
                'found': True,
                'title': data[0]['title'],
                'author': data[0]['author'],
                'citations': num_citations,
                'nodes': json.dumps(layers),
                'links': json.dumps(links),
        })
        
