from flask import render_template,request,redirect,url_for,abort
from ..models import User,Pitch,Comment,Upvote,Downvote
from . import main
from flask_login import login_required
from .forms import UpdateProfile
from .. import db,photos
from .forms import PitchForm,CommentForm
from flask_login import current_user

# Views
@main.route('/')
def index():
    pitch = Pitch.query.all()
    hobbies = Pitch.query.filter_by(category = 'Hobbies').all() 
    experiences = Pitch.query.filter_by(category = 'Experiences').all()
    skills = Pitch.query.filter_by(category = 'Skills').all()
    title ='Pitch'
    return render_template('index.html', hobbies = hobbies, experiences = experiences, pitch = pitch, skills= skills, title=title)

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



@main.route('/upvote/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_upvote = Upvote(user = current_user, pitch_id=id)

    db.session.add(new_upvote)
    db.session.commit()

    return redirect(url_for('main.index',id=id))

@main.route('/downvote/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    pitches = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in pitches:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, pitch_id=id)

    db.session.add(new_downvote)
    db.session.commit()
    
    return redirect(url_for('main.index',id = id))
