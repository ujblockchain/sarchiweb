from django.utils.timezone import datetime
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from csp.decorators import csp_exempt
from contact.forms import UserMessageForm
from facilitators.models import Facilitators
from newsletters.forms import NewsletterEmailForm
from partners.models import Partners
from program.models import Event
from projects.models import Projects
from repository.models import RepoInfo
from settings.models import UpcomingEvent
from .github_api import get_github_commits

# init current time, timezone aware
current_timestamp = datetime.now()


# index page view
@method_decorator([never_cache, csp_exempt], name='dispatch')
class HomeView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = UserMessageForm()

        ## facilitators context
        context['facilitators'] = Facilitators.objects.filter(publish=True)

        # get only the latest repo info
        latest_repo_info = RepoInfo.objects.order_by('-date_created')[0]

        # init commit info
        get_commit_info = ''

        try:
            get_commit_info = get_github_commits(latest_repo_info.active_repo)

            # update repo info
            RepoInfo.objects.update(
                id=latest_repo_info.id,
                sha=get_commit_info['sha'],
                node_id=get_commit_info['node_id'],
            )
        except:
            # if error, it means github api request limit reached

            # read from model instance
            get_commit_info = {
                'node_id': latest_repo_info.node_id,
                'sha': latest_repo_info.sha,
            }

        # set commit context
        context['commit'] = get_commit_info
        context['repo'] = RepoInfo.objects.order_by('-date_created').all()[0]

        # partner context
        context['partners'] = Partners.objects.filter(publish=True)

        # project context; only get the latest
        context['project'] = Projects.objects.order_by('-date_created').filter(
            publish=True, schedule_message__lte=current_timestamp)[0]

        # newsletter form
        context['newsletter_form'] = NewsletterEmailForm()
        # event
        context['upcoming_event'] = UpcomingEvent.objects.order_by(
            'last_update').first()

        return context


# index page view
@method_decorator([
    never_cache,
], name='dispatch')
class EventView(TemplateView):
    template_name = 'pages/mb.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['events'] = Event.objects.all()[0:1]

        return context
