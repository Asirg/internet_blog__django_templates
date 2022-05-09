from email import header
from re import template
from time import process_time_ns
from urllib import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.test import tag
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.views import generic
from dashboard.models import (
    Post, Comment, PostTag, Reaction, Tag
)

from typing import Any, Dict

class IndexView(generic.ListView):
    # model = Post
    template_name = "dashboard/index.html"
    context_object_name = "post_list"

    tags_filter = []

    def get_queryset(self) -> list:
        posts = Post.objects.all()

        search = self.request.GET.get('search')
        if search:
            posts = posts.filter(header__contains=search)

        sort = self.request.GET.get('sort')
        if sort == "Дата публікації за зростанням":
            posts = posts.order_by('-created_at')
        else:
            posts = posts.order_by('created_at')

        self.tags_filter = [ tag for tag in self.request.GET.keys() if tag in Tag.get_all_tags()]
        if self.tags_filter != []:
            result_posts = []
            for post in posts:
                if not set(post.tags()).isdisjoint(set(self.tags_filter)):
                    result_posts.append(post)
        else:
            result_posts = posts

        return result_posts

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        context['search_value'] = self.request.GET.get('search', "")
        context['tags_list'] = [
            {'checked': tag in self.tags_filter, 'value': tag}
            for tag in Tag.get_all_tags()
        ]

        return context

class PostView(generic.DetailView):
    template_name = "dashboard/post.html"
    model = Post

def ReactionView(request, post_id, comment_id, islike):
    post = comment = args = None

    # Проверка на страницу где выставляеться реакция
    if request.META['HTTP_REFERER'].split('dashboard/')[1] == "":
        post = get_object_or_404(Post, pk=post_id)
        path = 'dashboard:index'
    else:
        if islike > 1:
            comment = get_object_or_404(Comment, pk=comment_id)
            islike -= 2
        else:
            post = get_object_or_404(Post, pk=post_id)
        path = "dashboard:post"
        args = (post_id, )

    reaction = Reaction(
            post=post, comment=comment, value=islike
    )
    reaction.save()

    return HttpResponseRedirect(reverse(path, args=args))

def CommentView(request, post_id, parent_comment_id):
    text_value = request.POST['input_text_comment']
    
    comment = Comment(
        post=Post.objects.get(pk=post_id),
        text=text_value
    )
    comment.save()

    return HttpResponseRedirect(reverse("dashboard:post", args=(post_id, )))