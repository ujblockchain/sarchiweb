from datetime import datetime

from django.utils.timezone import utc
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from core.contact.forms import UserMessageForm
from core.newsletters.forms import NewsletterEmailForm
from core.partners.models import Partners

from .models import Blog

# init current time
current_timestamp = datetime.now().replace(tzinfo=utc)


class PostListViews(ListView):
    model = Blog
    queryset = Blog.objects.filter(publish=True, schedule_publish__lte=current_timestamp)
    context_object_name = 'post'
    template_name = 'blog/blog-list.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserMessageForm()
        context['partners'] = Partners.objects.filter(publish=True)
        context['newsletter_form'] = NewsletterEmailForm()

        return context


class PostDetailViews(DetailView):
    model = Blog
    queryset = Blog.objects.filter(publish=True, schedule_publish__lte=current_timestamp)
    context_object_name = 'post'
    template_name = 'blog/blog-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserMessageForm()
        context['partners'] = Partners.objects.filter(publish=True)
        context['newsletter_form'] = NewsletterEmailForm()
        return context
