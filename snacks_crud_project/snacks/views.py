from django.urls import reverse_lazy
from .models import Snack
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class SnackListView(ListView):
    template_name = "snack_list.html"
    model = Snack


class SnackDetailView(DetailView):
    template_name = "snack_detail.html"
    model = Snack
    context_object_name = "snack_object"


class SnackCreateView(CreateView):
    template_name = "snack_create.html"
    model = Snack
    fields = ["title", "purchaser", "description"]


class SnackUpdateView(UpdateView):
    template_name = "snack_update.html"
    model = Snack
    fields = ["title", "description"]
    template_name_suffix = '_update_form'

class SnackDeleteView(DeleteView):
    template_name = "snack_delete.html"
    model = Snack
    success_url = reverse_lazy('snack_list')