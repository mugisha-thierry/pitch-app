from flask import render_template,request,redirect,url_for,abort
from ..models import User,Pitch,Comment
from . import main
from flask_login import login_required
from .forms import UpdateProfile
from .. import db,photos
from .forms import PitchForm
from flask_login import current_user
# from ..requests import get_news_source,get_news_article

# from ..models import Article,News

# Views
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)  

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

    return render_template('profile/update.html',form =form)    


@main.route('/new_pitch', methods = ['POST','GET'])
@login_required
def add_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        user_id = current_user
        
        
        if form.validate_on_submit():
            new_pitch = Pitch(pitch=pitch,user_id=current_user._get_current_object().id,category=category,title=title)
            db.session.add(new_pitch)
            db.session.commit()
        
        return redirect(url_for('main.index'))
        
    return render_template('pitch.html', form = form)    


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('comment.html', form =form, pitch = pitch,all_comments=all_comments)    