from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from blogs.models import BlogPost


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blogpost_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogs/blogpost_list.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse('blogpost_detail', kwargs={'pk': self.object.pk})

class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blogs/blogpost_form.html'

    def get_success_url(self):
        return reverse('blogpost_detail', kwargs={'pk': self.object.pk})

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogs/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogpost_list')
