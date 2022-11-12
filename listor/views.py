from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import UserRegisterForm
from .models import Artikel, Lista

def registrera(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            anvandarnamn = form.cleaned_data.get('username')
            messages.success(request, f'Konto skapades för {anvandarnamn}')
            return redirect('loggain')
    else:
        form=UserRegisterForm()

    return render(request, 'listor/registrera.html',{'form':form})

class AllaListor(LoginRequiredMixin,ListView):
    model=Lista
    template_name = 'listor/hem.html'
    context_object_name = 'listor'
    ordering = ['-datum_skapad']

class EnLista(LoginRequiredMixin,ListView):
    model=Artikel
    template_name = 'listor/lista.html'
    context_object_name = 'artiklar'
    #ordering = ['namn']

    def get_queryset(self):
        return Artikel.objects.filter(lista=self.kwargs['pk']).order_by('namn')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['listan'] = Lista.objects.filter(id=self.kwargs['pk'])
        return context

class SkapaLista(LoginRequiredMixin,CreateView):
    model=Lista
    fields=['namn']

    def form_valid(self,form):
        form.instance.forfattare=self.request.user
        return super().form_valid(form)

class UppdateraLista(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Lista
    fields=['namn']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.forfattare:
            return True
        return False

class RaderaLista(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Lista
    success_url='/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.forfattare:
            return True
        return False

class SkapaArtikel(LoginRequiredMixin,CreateView):
    model=Artikel
    fields=['namn', 'antal']

    def form_valid(self,form):
        form.instance.lista=get_object_or_404(Lista,id=self.kwargs.get('l_pk'))
        return super().form_valid(form)

class UppdateraArtikel(LoginRequiredMixin,UpdateView):
    model=Artikel
    fields=['namn', 'antal']

class RaderaArtikel(LoginRequiredMixin,DeleteView):
    model=Artikel

    def get_success_url(self):
        lista = self.object.lista
        return reverse_lazy( 'lista-sida', kwargs={'pk': lista.id})