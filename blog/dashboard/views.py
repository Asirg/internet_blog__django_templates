from re import template
from urllib import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.views import generic
from dashboard.models import (
    Post, Comment, PostTag, Reaction, Tag
)

class IndexView(generic.ListView):
    template_name= "dashboard/index.html"
    context_object_name = "post_list"

    def get_queryset(self) -> list:
        return Post.objects.all()

class PostView(generic.DeleteView):
    template_name = "dashboard/post.html"
    model = Post

def ReactionView(request, post_id, comment_id, islike):
    post = comment = args = None

    print("*"*100)

    # Проверка на страницу где выставляеться реакция
    if request.META['HTTP_REFERER'].split('dashboard/')[1] == "":
        post = get_object_or_404(Post, pk=post_id)
        path = 'dashboard:index'
    else:
        if islike > 1:
            ...
            # comment = get_list_or_404(Comment, pk=comment_id)
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