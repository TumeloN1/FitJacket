from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.documents import Account
from .models import Post, Comment, Group, Friendship
from mongoengine.queryset.visitor import Q

@login_required
def social_hub(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Or wherever you want to redirect non-logged-in users

    user_doc = Account.objects.get(username=request.user.username)
    friendships = Friendship.objects(user=user_doc)
    friend_ids = [friendship.friend.id for friendship in friendships]
  
    posts = Post.objects(author__in=[user_doc] + [friendship.friend for friendship in friendships]).order_by('-created_at')
    groups = Group.objects(members=user_doc)

    # Fetch comments for posts
    comments_by_post = {}
    for post in posts:
        comments = Comment.objects(post=post)
        comments_by_post[post.id] = comments

    # Handle adding friends (via POST request)
    if request.method == 'POST' and 'add_friend' in request.POST:
        friend_username = request.POST['friend_username']
        try:
            # Fetch the Account by the username
            friend_user = Account.objects.get(username=friend_username)
            
            # Make sure the logged-in user is not trying to add themselves
            if friend_user != user_doc:
                if not Friendship.objects(user=user_doc, friend=friend_user):
                    Friendship(user=user_doc, friend=friend_user).save()
        except Account.DoesNotExist:
            # Handle the case when the user doesn't exist
            pass
    
    return render(request, 'social/social_hub.html', {
        'posts': posts,
        'comments_by_post': comments_by_post,
        'groups': groups,
    })

@login_required
def add_friend(request, friend_id):
    friend = get_object_or_404(Account, id=friend_id)
    account = request.user
    if friend not in account.friends:
        account.friends.append(friend)
        account.save()
    return redirect('social_hub')

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    account = request.user
    if account not in group.members:
        group.members.append(account)
        group.save()
    return redirect('group_feed', group_id=group_id)

@login_required
def group_feed(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members:
        return redirect('social_hub')  # Only members can view

    posts = Post.objects(group=group).order_by('-created_at')
    comments_by_post = {
        str(post.id): Comment.objects(post=post).order_by('created_at')
        for post in posts
    }

    return render(request, 'social/group_feed.html', {
        'group': group,
        'posts': posts,
        'comments_by_post': comments_by_post,
    })

@login_required
def create_post(request, group_id=None):
    if request.method == 'POST':
        content = request.POST['content']
        account = request.user
        group = Group.objects(id=group_id).first() if group_id else None

        post = Post(author=account, content=content, group=group)
        post.save()

        return redirect('group_feed', group_id=group_id) if group else redirect('social_hub')

    return render(request, 'social/create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    account = request.user
    if account not in post.likes:
        post.likes.append(account)
        post.save()
    return redirect('social_hub')

@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('comment_content')
        post = Post.objects(id=post_id).first()
        if post and content:
            comment = Comment(author=request.user, post=post, content=content)
            comment.save()
    return redirect('social_hub')

