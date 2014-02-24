

from django.conf.urls import patterns,  url


urlpatterns = patterns('createNote.views',
    url(r'^$','v_search_home'),
    url(r'^content/id_([\d]+)/$','v_show_content'),
    url(r'^content/edit_([\d]+)/$','v_edit_content'),
    url(r'^add_content/$','v_add_content'),
    url(r'^logout/$','v_logout'),
    url(r'^login/$','v_login'),
    
)
