from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import ToDoList, Item
from .forms import ItemForm

import datetime


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        task_list = []
        try:
            todolist = get_list_or_404(ToDoList, user=request.user)
        except Http404:
            todolist = []
        for master in todolist:
            for task in master.item_set.all().order_by('due_date'):
                if task.complete == False:
                    task_list.append(task)

        current_time = datetime.datetime.now()
        ctx = {'tasks': task_list, 'time': current_time}
        return render(request, 'taskmaster/home.html', ctx)

    def post(self, request):
        task_list = []
        try:
            todolist = get_list_or_404(ToDoList, user=request.user)
        except Http404:
            todolist = []
        for master in todolist:
            for task in master.item_set.all().order_by('due_date'):
                if not task.complete:
                    task_list.append(task)

        if request.POST.get("update"):
            for task in task_list:
                if request.POST.get('t' + str(task.id)) == "completed":
                    task.complete = True
                task.save()

        current_time = datetime.datetime.now()
        ctx = {'tasks': task_list}
        return render(request, 'taskmaster/home.html', ctx)


class MasterView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            master_lists = get_list_or_404(ToDoList, user=request.user)
        except Http404:
            master_lists = []

        ctx = {'masters': master_lists}
        return render(request, 'taskmaster/master.html', ctx)


class TaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task_list = []
        try:
            master = get_object_or_404(ToDoList, id=pk, user=request.user)
        except Http404:
            master = []
        for task in master.item_set.all().order_by('due_date'):
            task_list.append(task)
        ctx = {'master': master, 'tasks': task_list}
        return render(request, 'taskmaster/item_list.html', ctx)


class InboxView(LoginRequiredMixin, View):
    def get(self, request):
        task_list = []
        try:
            todolist = get_list_or_404(ToDoList, user=request.user)
        except Http404:
            todolist = []
        for master in todolist:
            for task in master.item_set.all().order_by('due_date'):
                task_list.append(task)

        current_time = datetime.datetime.now()
        ctx = {'tasks': task_list, 'time': current_time}
        return render(request, 'taskmaster/inbox.html', ctx)

    def post(self, request):
        task_list = []
        try:
            todolist = get_list_or_404(ToDoList, user=request.user)
        except Http404:
            todolist = []

        for master in todolist:
            for task in master.item_set.all().order_by('due_date'):
                task_list.append(task)

        ctx = {'tasks': task_list}
        if request.POST.get("update"):
            for task in task_list:
                if request.POST.get('t' + str(task.id)) == "completed":
                    task.complete = True
                else:
                    task.complete = False
                task.save()
        return render(request, 'taskmaster/inbox.html', ctx)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('taskmaster:inbox')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Item 


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('taskmaster:inbox')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MasterDetailView(LoginRequiredMixin, DetailView):
    model = ToDoList 

    def post(self, request):
        task_list = []
        try:
            todolist = get_list_or_404(ToDoList, user=request.user)
        except Http404:
            todolist = []
        for master in todolist:
            for task in master.item_set.all().order_by('due_date'):
                if not task.complete:
                    task_list.append(task)

        if request.POST.get("update"):
            for task in task_list:
                if request.POST.get('t' + str(task.id)) == "completed":
                    task.complete = True
                task.save()

        ctx = {'tasks': task_list}
        return render(request, 'taskmaster/home.html', ctx)


class MasterCreateView(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ['name']
    success_url = reverse_lazy('taskmaster:master')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MasterUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoList
    fields = ['name']
    success_url = reverse_lazy('taskmaster:master')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MasterDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList
    fields = '__all__'
    success_url = reverse_lazy('taskmaster:master')
