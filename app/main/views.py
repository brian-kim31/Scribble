from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm, UpdateProfile, CommentForm, UpdateProfile
from flask_login import login_required, current_user
from ..models import User, Post, Comment, Upvote, Downvote
from .. import db,photos



# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    message = "Welcome to Scribble"
    title = 'Scribble'
    click_bait = 'In life, you only have 60 seconds to impress someone. 1 minute can make or break you. How do we make sure that you use your 1 minute to actually say something meaningful?'
    return render_template('index.html',  title = title, message = message, click_bait = click_bait)


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():

    '''
    View scribble page function that returns the scribble details page and its data
    '''
    title = 'Scribble'

    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        post_obj = Post(post=post, title=title, category=category, user_id=user_id)
        post_obj.save()
        return redirect(url_for('main.index'))
    return render_template('pitch.html', form=form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


# Added stuff
@main.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    likes = Upvote.query.all()
    
    return render_template('pitch_display.html', posts=posts, likes=likes, user=user)



@main.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    user = User.query.all()
    comments = Comment.query.filter_by(post_id=post_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment,
            post_id=post_id,
            user_id=user_id
            )

        new_comment.save()
        new_comments = [new_comment]
        print(new_comments)
        return redirect(url_for('.comment', post_id=post_id))
    return render_template('comment.html', form=form, post=post, comments=comments, user=user)


@main.route('/user')
@login_required
def user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return ('not found')
    return render_template('profile.html', user=user)


@main.route('/user/<name>/update_profile', methods=['POST', 'GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username=name).first()
    if user is None:
        error = 'The user does not exist'
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile', name=name))
    return render_template('profile/update_profile.html', form=form)


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    post = Post.query.get(id)
    vote_mpya = Upvote(post=post, upvote=1)
    vote_mpya.save()
    return redirect(url_for('main.posts'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    post = Post.query.get(id)
    vm = Downvote(post=post, downvote=1)
    vm.save()
    return redirect(url_for('main.posts'))