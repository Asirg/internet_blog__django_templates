from django.db import models
from django.contrib import admin

from typing import List

class Post(models.Model):
    header = models.CharField(max_length=200, verbose_name="Post header")
    content = models.JSONField(verbose_name="Post content")
    number_of_views = models.SmallIntegerField(default=0, verbose_name="Post number of views")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Update at")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def description(self) -> str:
        desc = self.content.get('description')
        if desc:
            return desc
        else:
            return self.content.get('text1')[:200]
    
    def number_of_likes(self) -> int:
        return len(self.reaction_set.filter(value=True))

    def number_of_dislikes(self) -> int:
        return len(self.reaction_set.filter(value=False))

    def number_of_comments(self) ->int:
        return len(self.comment_set.all())

    def tags(self) -> List[str]:
        tags = self.posttag_set.all()
        tags = [tag.tag_key.value for tag in tags]
        return tags

    def __str__(self) -> str:
        return (
            f"{self.header}"
        )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Comment(models.Model):
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, verbose_name="Comment on post"
    )
    parent_comment = models.ForeignKey(
        to='self', on_delete=models.CASCADE, verbose_name="Parent comment", null=True
    )
    text = models.CharField(max_length=200, verbose_name="Comment text")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Update at")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self) -> str:
        return (
            f"{self.post.header}:{self.text}"
        )

    def number_of_likes(self) -> int:
        return len(self.reaction_set.filter(value=True))

    def number_of_dislikes(self) -> int:
        return len(self.reaction_set.filter(value=False))
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class Reaction(models.Model):
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, null=True, verbose_name="Reaction on post"
    )
    comment = models.ForeignKey(
        to=Comment, on_delete=models.CASCADE, null=True, verbose_name="Reaction on comment"
    )
    value = models.BooleanField(verbose_name="Like or dislike")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self) -> str:
        source = self.post.header if not self.post.header is None else self.comment.text
        like_dislike = 'like' if self.value else 'dislike'
        return (
            f"{source}:{like_dislike}"
            )

    class Meta:
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"

class Tag(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def get_all_tags():
        return [tag.value for tag in Tag.objects.all()]

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    
class PostTag(models.Model):
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, verbose_name="Tag for post"
    )
    tag_key = models.ForeignKey(
        to=Tag, on_delete=models.CASCADE, verbose_name="Value tag for post"
    )

    def __str__(self) -> str:
        return (
            f"{self.post.header}:{self.tag_key.value}"
        )

    class Meta:
        verbose_name = "Post tag"
        verbose_name_plural = "Post tags"

