from dashboard.models import Post, Comment, Tag, PostTag, Reaction
from django.contrib import admin

class PostTagInLine(admin.TabularInline):
    model = PostTag
    extra = 1

class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0

class ReactionInLine(admin.TabularInline):
    model = Reaction
    extra = 0

class PostAdmin(admin.ModelAdmin):
    fields = [
        'header', 'number_of_views', 'content' 
    ]

    inlines = [
        PostTagInLine, 
        CommentsInLine, 
        ReactionInLine
    ]

    list_filter = [
        'created_at'
    ]

    list_display = [
        'header', 'number_of_views', 'update_at', 'created_at'
    ]

    search_field = [
        'header'
    ]

class CommentAdmin(admin.ModelAdmin):
    fields = [
        'post', 'parent_comment', 'text'
    ]

    inlines = [
        ReactionInLine
    ]

    list_filter = [
        'created_at'
    ]

    list_display = [
         'post', 'text', 'update_at', 'created_at'
    ]

    search_field = [
        'post'
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)