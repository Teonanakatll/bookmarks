from django.urls import path

from jquery import views

app_name = 'jquery'

urlpatterns = [
    path('table/', views.table, name='table'),
    path('board/', views.board, name='board'),
    path('simple_disappear/', views.simple_disappear, name='simple_disappear'),
    path('chainable_effects/', views.chainable_effects, name='chainable_effects'),
    path('accordion1/', views.accordion1, name='accordion'),
    path('accordion2/', views.accordion2, name='accordion2'),
    path('animated_hover/', views.animated_hover, name='animated_hover'),
    path('animated_hover2/', views.animated_hover2, name='animated_hover2'),
    path('block_clickable/', views.block_clickable, name='block_clickable'),
    path('collapsible_panels/', views.collapsible_panels, name='collapsible_panel'),
    path('illustrations/', views.illustrations, name='illustrations'),
]
