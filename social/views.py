from django.shortcuts import render, redirect
from mongoengine.queryset.visitor import Q
from .models import Post, Group, Comment
from accounts.documents import Account  # Import Account model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# User Feed View (personal posts)
@login_required  # Ensure that only logged-in users can access the feed
def user_feed(request):
    # Fetch posts from the logged-in user
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            content = request.POST.get('comment_content')
            post_id = request.POST.get('post_id')
            if content and post_id:
                post = Post.objects(id=post_id).first()
                if post:
                    Comment(
                        content=content,
                        author=request.user,  # Use the logged-in user
                        post=post
                    ).save()
            return redirect('user_feed')  # Update this to your feed URL name

    # Fetch comments by post
    comments_by_post = {}
    for comment in Comment.objects.order_by('created_at'):
        post_key = str(comment.post.id)
        if post_key not in comments_by_post:
            comments_by_post[post_key] = []
        comments_by_post[post_key].append(comment)

    return render(request, 'social/feed.html', {
        'posts': posts,
        'comments_by_post': comments_by_post
    })

# Group Feed View (posts for a specific group)
@login_required
def group_feed(request, group_id):
    group = Group.objects.get(id=group_id)
    posts = Post.objects(group=group).order_by('-created_at')  # Fetch posts in the group, ordered by date
    return render(request, 'social/group_feed.html', {'posts': posts, 'group': group})

# Create Post View (either personal or group post)
@login_required
def create_post(request, group_id=None):
    if request.method == 'POST':
        content = request.POST['content']
        
        # Explicitly get the Account object from the logged-in user
        account = request.user

        if group_id:
            group = Group.objects.get(id=group_id)
            post = Post(author=account, content=content, group=group)
        else:
            post = Post(author=account, content=content)
        
        post.save()
        return redirect('user_feed')  # Redirect to user feed after posting

    return render(request, 'social/create_post.html')

# Like Post View (to like a post)
@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    account = request.user  # request.user is the Account instance
    
    if account not in post.likes:
        post.likes.append(account)
        post.save()

    return redirect('user_feed')  # Redirect to user feed after liking the post

# Join Group View (to join a group)
@login_required
def join_group(request, group_id):
    group = Group.objects.get(id=group_id)
    account = request.user  # request.user is the Account instance
    
    if account not in group.members:
        group.members.append(account)
        group.save()
        account.groups.append(group)  # Add group to user's list of groups
        account.save()

    return redirect('group_feed', group_id=group_id)  # Redirect to group feed after joining
