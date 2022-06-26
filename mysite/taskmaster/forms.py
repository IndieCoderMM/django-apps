from django import forms
from .models import ToDoList, Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'due_date', 'todolist', 'priority']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['todolist'].queryset = self.fields['todolist'].queryset.filter(user=user)

