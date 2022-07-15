from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/result')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_id(data)
    posts = Post.get_all()
    return render_template('result.html', posts = posts, user=user)


@app.route("/post/content", methods=["POST"])
def create_review():
    if not Post.validate_post(request.form):
        return redirect('/result')
    data = {
        "user_id":  request.form['user_id'],
        "content": request.form['content']
    }
    Post.create(data)
    return redirect("/result")

@app.route("/post/<int:id>/delete", methods=["POST"])
def delete(id):
    post_data = {
        'id': id
    }
    review = Post.get_one(post_data)
    if(review.user_id != session['user_id']):
        flash(f"Unauthorized access to edit review with id {id}")
        return redirect("/dashboard")
    Post.delete(request.form)
    return redirect('/dashboard')
