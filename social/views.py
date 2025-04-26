from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.documents import Account
from .documents import Post, Comment, Group, Friendship, FriendRequest
from mongoengine.queryset.visitor import Q
from bson import ObjectId
from .models import Milestones, Badge
from workouts.models import WorkoutLog
from dashboard.models import WeightLog
from goals.models import FitnessGoal


@login_required
def social_hub(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_doc = Account.objects.get(username=request.user.username)

    search_results = []
    incoming_requests = FriendRequest.objects(receiver=user_doc, status='pending')
    outgoing_requests = FriendRequest.objects(sender=user_doc, status='pending')
    request_message = ""  # message to show in template

    if request.method == 'POST':
        if 'search_user' in request.POST:
            query = request.POST['search_query']
            friendships = Friendship.objects(user=user_doc)
            friend_ids = [friendship.friend.id for friendship in friendships]

            # Search users by username, exclude friends AND yourself
            search_results = Account.objects(username__icontains=query).filter(
                id__nin=friend_ids + [user_doc.id]
            )

        elif 'send_request' in request.POST:
            target_id = request.POST['target_id']
            try:
                target_user = Account.objects.get(id=ObjectId(target_id))
                existing_request = FriendRequest.objects(
                    (Q(sender=user_doc) & Q(receiver=target_user)) |
                    (Q(sender=target_user) & Q(receiver=user_doc))
                ).first()

                if not existing_request:
                    FriendRequest(sender=user_doc, receiver=target_user).save()
                    request_message = f"Friend request sent to {target_user.username}."
                else:
                    request_message = f"You have already sent a friend request to {target_user.username}."
            except Exception as e:
                print("Send request error:", e)
                request_message = "Something went wrong sending the friend request."

        elif 'accept_request' in request.POST:
            req_id = request.POST['request_id']
            try:
                fr = FriendRequest.objects.get(id=ObjectId(req_id), receiver=user_doc)
                fr.status = 'accepted'
                fr.save()
                Friendship(user=user_doc, friend=fr.sender).save()
                Friendship(user=fr.sender, friend=user_doc).save()
            except Exception as e:
                print("Accept request error:", e)

        elif 'reject_request' in request.POST:
            req_id = request.POST['request_id']
            try:
                fr = FriendRequest.objects.get(id=ObjectId(req_id), receiver=user_doc)
                fr.status = 'rejected'
                fr.save()
            except Exception as e:
                print("Reject request error:", e)

    friendships = Friendship.objects(user=user_doc)
    friend_ids = [friendship.friend.id for friendship in friendships]
    friends = Account.objects(id__in=friend_ids)

    posts = Post.objects(author__in=[user_doc] + [friendship.friend for friendship in friendships]).order_by('-created_at')
    groups = Group.objects(members=user_doc)
    group_search_results = []
    group_message = ""

    if request.method == 'POST':
        if 'search_group' in request.POST:
            group_query = request.POST['group_query']
            group_search_results = Group.objects(title__icontains=group_query).filter(members__ne=user_doc)

        elif 'join_group' in request.POST:
            group_id = request.POST['group_id']
            group = Group.objects(id=ObjectId(group_id)).first()
            if group and user_doc not in group.members:
                group.members.append(user_doc)
                group.save()
                group_message = f"You joined the group: {group.title}"
            else:
                group_message = "You are already in this group."

        elif 'create_group' in request.POST:
            group_title = request.POST['group_title']
            if not Group.objects(title=group_title).first():  # Prevent duplicate names
                group = Group(title=group_title, members=[user_doc])
                group.save()
                group_message = f"Group '{group_title}' created and joined!"
            else:
                group_message = "A group with this name already exists."
        elif 'leave_group' in request.POST:
            group_id = request.POST['group_id']
            group = Group.objects(id=ObjectId(group_id)).first()
            if group and user_doc in group.members:
                if group.creator != user_doc:
                    group.members.remove(user_doc)
                    group.save()
                    group_message = f"You left the group: {group.title}"
                else:
                    group_message = "You cannot leave a group you created. You can delete it instead."

        elif 'delete_group' in request.POST:
            group_id = request.POST['group_id']
            group = Group.objects(id=ObjectId(group_id)).first()
            if group and group.creator == user_doc:
                group.delete()
                group_message = f"The group '{group.title}' has been deleted."


    comments_by_post = {}
    for post in posts:
        comments = Comment.objects(post=post)
        comments_by_post[str(post.id)] = comments

    # Badge Checking
    milestones = Milestones.objects.all()
    active_days = WorkoutLog.objects.filter(user=request.user).values('date').distinct().count()
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('date')
    goals = [goal.goal_type for goal in FitnessGoal.objects.filter(user=request.user)]
    weight_changes = [
        weight_logs[i].weight - weight_logs[i - 1].weight
        for i in range(1, len(weight_logs))
    ]
    milestones_met = []
    for milestone in milestones:
        if milestone.target_category == "active_days" and active_days >= int(milestone.target_metric):
            milestones_met.append(milestone)
        if len(weight_changes) > 0:
            if milestone.target_category == "lose_weight" and 'lose_weight' in goals:
                if any(change < 0 and abs(change) >= int(milestone.target_metric) for change in weight_changes):
                    milestones_met.append(milestone)
            if milestone.target_category == "gain_muscle" and 'gain_muscle' in goals:
                if any(change > 0 and change >= int(milestone.target_metric) for change in weight_changes):
                    milestones_met.append(milestone)
        
    for milestone in milestones_met:
        if not Badge.objects.filter(user=request.user, milestone=milestone).exists():
            Badge.objects.create(
                user=request.user,
                name=milestone.name,
                icon="🫡",
                milestone=milestone,
            )

    user_badges = Badge.objects.filter(user=request.user)


    return render(request, 'social/social_hub.html', {
        'search_results': search_results,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'posts': posts,
        'comments_by_post': comments_by_post,
        'groups': groups,
        'friends': friends,
        'request_message': request_message,
        'group_search_results': group_search_results,
        'group_message': group_message,
        'user_badges': user_badges,
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