from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .models import Post, PostForm, Comment, Like
from . import db, month_name
import json

views = Blueprint("views", __name__)

@views.route("/home")
@views.route("/")
@login_required
def home():
	posts = Post.query.all()
	return render_template("home.html", user=current_user, posts=posts, month_name=month_name)

@views.route("/profile/<user>")
@login_required
def profile(user):
	return render_template("user.html", user=current_user)

#Posts

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
	form = PostForm()
	if request.method == "POST":
		title = form.title.data
		text = form.text.data
		post = Post(title=title, text=text, author=current_user.id)

		db.session.add(post)
		db.session.commit()
		flash("Post is created")
		return redirect(url_for("views.home"))
	return render_template("create_post.html", form=form, user=current_user)

@views.route("/post/<int:id>")
@login_required
def post_user(id):
	post = Post.query.filter_by(id=id).first()
	return render_template("post_user.html", user=current_user, post=post, month_name=month_name)

@views.route("/delete-post/<int:id>")
@login_required
def delete_post(id):
	post = Post.query.filter_by(id=id).first()

	if not post:
		flash("Post does not exist", category="error")
	elif post.user.id != current_user.id:
		flash("You do not have permission to delete this post", category="error")
	else:
		db.session.delete(post)
		db.session.commit()
		flash("Post deleted successfully", category="success")
	return redirect(url_for("views.home"))

#End Post

#Comments

@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
	text = request.form["text"]
	if not text:
		flash("Comment can not be emptry!", category="error")
	else:
		post = Post.query.filter_by(id=post_id)

		if post:
			comment = Comment(text=text, author=current_user.id, post_id=post_id)
			db.session.add(comment)
			db.session.commit()
			flash("Comment added successfully", category="success")
		else:
			flash("Post does not exist", category="error")

	return redirect(url_for("views.post_user", id=post_id))


@views.route("/delete-comment/<int:post_id>/<int:comment_id>")
def delete_comment(post_id, comment_id):
	comment = Comment.query.filter_by(id=comment_id).first()
	if not comment:
		flash("Comment does not exist", category="error")
	elif comment.user.id != current_user.id:
		flash("You don't have permission to delete this comment", category="error")
	else:
		db.session.delete(comment)
		db.session.commit()
		flash("Comment deleted successfully", category="success")
	return redirect(url_for("views.post_user", id=post_id))

#Liking

@views.route("/like-post/<int:post_id>", methods=["POST"])
@login_required
def like(post_id):
	post = Post.query.filter_by(id=post_id).first()
	like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

	if not post:
		return jsonify({"error": "Post does not exist"}, 400)
	else:
		if like:
			db.session.delete(like)
		else:
			like = Like(author=current_user.id, post_id=post_id)
			db.session.add(like)

		db.session.commit()

	return jsonify({"likes-count": len(post.likes), "liked": current_user.id in map(lambda x:x.author, post.likes)})
