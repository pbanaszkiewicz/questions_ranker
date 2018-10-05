from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from ranker import views as ranker_views

urlpatterns = [
    # path(
    #     "about/",
    #     TemplateView.as_view(template_name="pages/about.html"),
    #     name="about",
    # ),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # User management
    # path(
    #     "users/",
    #     include("questions_ranker.users.urls", namespace="users"),
    # ),

    # login-related stuff
    path("accounts/", include("allauth.urls")),

    # ranker views
    path("", ranker_views.home, name="home"),
    path("rank/",
         TemplateView.as_view(template_name="pages/rank.html"),
         name="rank_page",
    ),
    path("data_privacy_policy/",
         TemplateView.as_view(template_name="pages/data_privacy_policy.html"),
         name="data_privacy_policy",
    ),
    re_path(
        r'^rank/(?P<hash_id>[a-z0-9]+)/$',
        ranker_views.rank_start,
        name="rank_start",
    ),
    # special case of stage for answering email, draw and paper questions
    re_path(
        r'^rank/(?P<hash_id>[a-z0-9]+)/1/$',
        ranker_views.rank_email,
        name="rank_email",
    ),
    # special case of stage for answering demographic questions
    re_path(
        r'^rank/(?P<hash_id>[a-z0-9]+)/4/$',
        ranker_views.rank_demographic,
        name="rank_demographic",
    ),
    re_path(
        r'^rank/(?P<hash_id>[a-z0-9]+)/(?P<stage>\d+)/$',
        ranker_views.rank_stage,
        name="rank_stage",
    ),

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
