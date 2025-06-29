import atexit
import flask
from flask import Flask, request, render_template, session, redirect, url_for
from entity import *

from repository import Repository
from pymongo import MongoClient
import math
from flask import request
import os
from icecream import ic
from datetime import datetime
from functools import wraps
app = Flask(__name__)


app.secret_key = "i7tbiuztifuertlbjh234qat"

username = "tua37646"
password = username + "_secret"
auth_source = username
host = "im-vm-005"
port = 27017

try:
    client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}", serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    print("Verbindung zu MongoDB aufgebaut")
    db = client[f"{auth_source}"]
except:
    print("Keine Verbindung zur Datenbank (VPN-Verbindung an?!?)")
    exit(0)

#Repo-Objekts
user_repo = Repository[User](db["users"], User, primary_key="username")
movie_repo = Repository[Movie](db["movies"], Movie)
genre_repo = Repository[Genre](db["genres"], Genre)
adress_repo = Repository[Adress](db["adresses"], Adress)
like_repo = Repository[Like](db["likes"], Like)
comment_repo = Repository[Comment](db["comments"], Comment)
profile_repo = Repository[Profile](db["profiles"], Profile)



#PERMISSION REQUIRED FUNCTION
def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = session["role"]

            if not user_role:
                flask.flash("Please log in first.", "info")
                return redirect(url_for("login"))

            if user_role not in required_roles:
                flask.flash("You do not have permission to access this page.", "error")
                return redirect(url_for("mainpage"))

            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/')
def mainpage(): 
    movies = movie_repo.find_all()
    return render_template('pages/index.html',movies=movies)



#AUTHENTICATIOON START
@app.route('/authentication/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_profile =  Profile(comments=[],favorite_movies=[])
        
        profile_id = profile_repo.save(user_profile)
        
        new_user = User(request.form.get("username"), request.form.get("password"), profile_id=profile_id)
     
        user_repo.save(new_user)
        flask.flash(f"You {request.form.get('username')} have registered", category="success")
        return redirect(url_for("login"))
    return render_template("authentication/register.html")

@app.route('/authentication/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_from_db = user_repo.find_by_id(request.form.get("username"))
        if user_from_db != None:
            if user_from_db.password == request.form.get("password"):
             
           
                user_from_db.date_time_last_login = datetime.now()

                user_repo.save(user_from_db)
      
                
                session["profile_id"] = str(user_from_db.profile_id)
                session["eingeloggter_username"] = user_from_db.username
                
                profile = profile_repo.find_by_id(user_from_db.profile_id)
                
                session["role"] = profile.role
                
                

                flask.flash(f"You {user_from_db.username} have logged in", category="success")
                return redirect(url_for('mainpage'))

        flask.flash("Username or password is false", category="error")
    return render_template('authentication/login.html')


@app.route('/authentication/logout',methods=['GET'])
def logout():
    if session["eingeloggter_username"]:
        session["eingeloggter_username"]  = ''
        session["profile_id"] = ''
        session["role"] = ''
        
    return redirect(url_for('mainpage'))


#AUTHENTICATIOON END

#GENRES START
@app.route('/genres/',methods=['GET'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def genres_list():
    genres = genre_repo.find_all()
    return render_template("genres/genres_list.html",genres=genres)

@app.route('/genres/create',methods=['GET', 'POST'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def genres_create():
    if request.method == 'POST':
        genre_name = request.form.get("name")
        if genre_name:
           
            new_genre = Genre(name=genre_name, related_movies=[])
            genre_id = genre_repo.save(new_genre)
           
           
            flask.flash(f"Genre '{genre_name}' created successfully", category="success")
            return redirect(url_for('genres_list'))
        flask.flash("Genre name can not be empty", category="error")
    return render_template("genres/genres_create.html")



@app.route('/genres/update/<string:id>',methods=['GET', 'POST'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def genres_update(id):
    
    object_id = ObjectId(id)
    
    genre = genre_repo.find_by_id(ObjectId(id))
   
    if genre:
        if request.method == 'POST':
            genre.name = request.form.get("name")
            genre_repo.save(genre)
            flask.flash(f"Genre '{genre.name}' updated successfully", category="success")
            return redirect(url_for('genres_list'))
       
        return render_template("genres/genres_update.html",genre = genre)
    flask.flash("Genre is not found", category="error")
    return redirect(url_for('mainpage'))
    



@app.route('/genres/delete/<string:id>',methods=['GET'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def genres_delete(id):
    genre = genre_repo.find_by_id(ObjectId(id))
    if genre:
        movies = movie_repo.find_all()
        for movie in movies:
            if genre.id in movie.genres:
                movie.genres.remove(genre.id)
                movie_repo.save(movie)
                
        genre_repo.delete_by_id(ObjectId(id))
        flask.flash(f"Genre '{genre.name}' deleted successfully", category="success")
        return redirect(url_for('genres_list'))
    flask.flash("Genre is not found", category="error")
    return redirect(url_for('mainpage'))

#GENRES END


#MOVIES START

@app.route('/movies/',methods=['GET'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def movies_list():
    movies = movie_repo.find_all()
    return render_template('movies/movies_list.html',movies = movies)

@app.route('/movies/create',methods=['GET', 'POST'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def movies_create():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = file.filename
            filepath = os.path.join('static', 'images/movies', filename)
            file.save(filepath)

    
            title = request.form.get('title')
            description = request.form.get('description')
            runtime_in_minutes = request.form.get('runtime_in_minutes')
            rating = request.form.get('rating')
            
            released_in_str = request.form.get("released_in")  
            released_in_date = datetime.strptime(released_in_str, "%Y-%m-%d").date()
            
            release_datetime = datetime.combine(released_in_date, datetime.min.time())
            
            genres = request.form.getlist('genres') 
            genres_ids = []
        
            for genre in genres:
                genres_ids.append(ObjectId(genre))
                
                
            
            movie = Movie(
                title=title,
                description=description,
                runtime_in_minutes=int(runtime_in_minutes),
                released_in=release_datetime,
                rating=float(rating),
                image_url=filepath,  
                genres=genres_ids
            )

            movie_id  = movie_repo.save(movie)
            
            
            
            flask.flash(f"Movie '{title}' creataed successfully", category="success")
            return redirect(url_for("movies_list"))
    
    genres = genre_repo.find_all()
    return render_template("movies/movies_create.html", genres=genres)
    

@app.route('/movies/<string:id>',methods=['GET', 'POST'])
def movies_detail(id):
    object_id = ObjectId(id)
    
    movie = movie_repo.find_by_id(object_id)
    likes = like_repo.find_all()
    likes_count = 0
    for like in likes:
        if like.movie_id == object_id:
            likes_count = likes_count + 1
    comments = []
    for comment_id in movie.comments:
        comment = comment_repo.find_by_id(comment_id)
        comments.append(comment)    
    
    if movie:
        genres = []
        for genre in movie.genres:
            genre_object = genre_repo.find_by_id(genre)
            genres.append(genre_object)
            
        return render_template("movies/movies_detail.html",movie = movie, genres=genres,likes_count=likes_count, comments = comments)
    flask.flash("Movie is not found", category="error")
    return redirect(url_for('mainpage'))

@app.route('/movies/update/<string:id>',methods=['GET', 'POST'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def movies_update(id):
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    if not movie:
        flask.flash(f"Movie  is not found successfully", category="error")
        return redirect(url_for("mainpage"))
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = file.filename
            filepath = os.path.join('static', 'images/movies', filename)
            file.save(filepath)
            movie.image_url = filepath
    
        title = request.form.get('title')
        movie.title = title
            
        description = request.form.get('description')
        movie.description = description
            
        runtime_in_minutes = request.form.get('runtime_in_minutes')
        movie.runtime_in_minutes = int(runtime_in_minutes)
        rating = request.form.get('rating')
        movie.rating = float(rating)
            
        released_in_str = request.form.get("released_in")  
        released_in_date = datetime.strptime(released_in_str, "%Y-%m-%d").date()
        release_datetime = datetime.combine(released_in_date, datetime.min.time())
        movie.released_in = release_datetime            
            
        genres = request.form.getlist('genres') 
        genres_ids = []
    
        for genre in genres:
            genres_ids.append(ObjectId(genre))
                
        movie.genres  = genres_ids
            
        movie_repo.save(movie)
            
            
            
            
            
        flask.flash(f"Movie '{title}' updated successfully", category="success")
        return redirect(url_for("movies_list"))

    genres = genre_repo.find_all()
    return render_template("movies/movies_update.html", genres=genres,movie = movie)

@app.route('/movies/delete/<string:id>',methods=['GET'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def movies_delete(id):
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    
    if movie:  
        for comment_id in movie.comments:
            comment = comment_repo.find_by_id(comment_id)
            
            user_profile = profile_repo.find_by_id(comment.author_id)
            user_profile.comments.remove(comment_id) 
            profile_repo.save(user_profile)
            comment_repo.delete_by_id(comment_id)
            
        movie_repo.delete_by_id(object_id)
        flask.flash(f"Movie '{movie.title}' deleted successfully", category="success")
        return redirect(url_for('movies_list'))
    flask.flash("Genre is not found", category="error")
    return redirect(url_for('mainpage'))



#MOVIES END

#FAVORITES START

@app.route('/movies/favorites/add/<string:id>',methods=['GET'])
def favorites_add(id):
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    user = user_repo.find_by_id(session["eingeloggter_username"])
    user_profile = profile_repo.find_by_id(user.profile_id)
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    if movie: 
        if movie.id in user_profile.favorite_movies:
            flask.flash("Movie already in your favorites", category="info")
            return redirect(url_for('movies_detail',id=id))
        user_profile.favorite_movies.append(movie.id)
        profile_repo.save(user_profile)
        
      
    
        flask.flash(f"Movie '{movie.title}' added to favorites successfully", category="success")
        
        return redirect(url_for('movies_detail',id=id))
    flask.flash("Movie is not found", category="error")
    return redirect(url_for('mainpage'))

@app.route('/movies/favorites/',methods=['GET'])
def favorites_list():
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    user = user_repo.find_by_id(session["eingeloggter_username"])
    user_profile = profile_repo.find_by_id(user.profile_id)
    favorites = []
    for movie_id in user_profile.favorite_movies:
        movie_object = movie_repo.find_by_id(movie_id)
        favorites.append(movie_object)

    return render_template("pages/favorite_movies.html",movies = favorites)


@app.route('/movies/favorites/delete/<string:id>',methods=['GET'])
def favorites_delete(id):
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    user = user_repo.find_by_id(session["eingeloggter_username"])
    user_profile = profile_repo.find_by_id(user.profile_id)
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    if movie: 
        if movie.id not in user_profile.favorite_movies:
            flask.flash("This movie not in your favorites", category="error")
            return redirect(url_for('movies_detail',id=id))
        user_profile.favorite_movies.remove(movie.id)
        profile_repo.save(user_profile)
        
      
    
        flask.flash(f"Movie '{movie.title}' removed from favorites successfully", category="success")
   
        return redirect(url_for('favorites_list'))
    flask.flash("Movie is not found", category="error")
    return redirect(url_for('mainpage'))

#FAVORITES END

#LIKES START 
@app.route('/movies/like/<string:id>',methods=['GET'])
def like(id):
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    user = user_repo.find_by_id(session["eingeloggter_username"])
    
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    if movie: 
        like = like_exists(object_id,user.profile_id)
        if(like):
            like_repo.delete_by_id(like.id)
            return redirect(url_for('movies_detail',id=id))
        like = Like(movie_id=object_id,user_profile_id = user.profile_id)
        like_repo.save(like)
        return redirect(url_for('movies_detail',id=id))
    flask.flash("Movie is not found", category="error")
    return redirect(url_for('mainpage'))

def like_exists(movie_id, user_profile_id):
    likes = like_repo.find_all()
    for like in likes:
        if like.movie_id == movie_id and like.user_profile_id == user_profile_id:
            return like
    return False

#LIKES END

#COMMENTS START
@app.route('/movies/<string:id>/comment',methods=['POST','GET'])
def add_comment(id):
    if request.method == "GET":
        return redirect(url_for('movies_detail',id=id))
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    user = user_repo.find_by_id(session["eingeloggter_username"])
    user_profile = profile_repo.find_by_id(user.profile_id)
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    if movie: 
        content = request.form.get("content")
        comment = Comment(
            content=content,
            author_id=user.profile_id,
            movie_id=object_id,
            created_at=datetime.now(),
            author_name=user.username
            
        )
        comment_id = comment_repo.save(comment)
        movie.comments.append(comment_id)
        movie_repo.save(movie)
        user_profile.comments.append(comment_id)
        profile_repo.save(user_profile)
        flask.flash("You added comment successfully",category="success")
        return redirect(url_for('movies_detail',id=id))
    flask.flash("Movie is not found", category="error")
    return redirect(url_for('mainpage'))


@app.route('/movies/<string:id>/comment/<string:comment_id>/delete',methods=['POST','GET'])
def delete_comment(id,comment_id):
    if request.method == "GET":
        return redirect(url_for('movies_detail',id=id))
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    user = user_repo.find_by_id(session["eingeloggter_username"])
    user_profile = profile_repo.find_by_id(user.profile_id)
    object_id = ObjectId(id)
    movie = movie_repo.find_by_id(object_id)
    comment_id = ObjectId(comment_id)
    comment = comment_repo.find_by_id(comment_id)
    if movie and comment: 
        if comment.id not in movie.comments:
            flask.flash("This movie doest have this comment", category="error")
            return redirect(url_for('movies_detail',id=id))
        if comment.id  not in user_profile.comments and session['role']==Role.User.value :
            flask.flash("You can not delete others comments",category="error")
            return redirect(url_for('movies_detail',id=id))
        
        
        comment_repo.delete_by_id(comment_id)
        
        movie.comments.remove(comment_id)
        movie_repo.save(movie)
        user_profile.comments.remove(comment_id)
        profile_repo.save(user_profile)
        flask.flash("You deleted comment successfully",category="success")
        return redirect(url_for('movies_detail',id=id))
    flask.flash("Movie or comment are not found", category="error")
    return redirect(url_for('mainpage'))



@app.route('/comments/',methods=['GET'])
@role_required([Role.ADMIN.value,Role.SUPERUSER.value])
def comments_list():
    comments = comment_repo.find_all()
    return render_template('comments/comments_list.html',comments = comments)


#COMMENTS END

#PROFILES START

@app.route('/profile/<string:id>',methods=['GET'])
def profile_detail(id):
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    profile_id = ObjectId(id)
    current_user = user_repo.find_by_id(session["eingeloggter_username"])
    if current_user.profile_id != profile_id:
        flask.flash(f"You can not access to others account", category="error")
        return redirect(url_for('mainpage'))
    profile = profile_repo.find_by_id(profile_id)
    adress = adress_repo.find_by_id(profile.adress)
    return render_template("profiles/profile_detail.html",profile = profile,adress=adress)

@app.route('/profile/update/<string:id>',methods=['GET',"POST"])
def profile_update(id):
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    profile_id = ObjectId(id)
    current_user = user_repo.find_by_id(session["eingeloggter_username"])
    if current_user.profile_id != profile_id:
        flask.flash(f"You can not access to others account", category="error")
        return redirect(url_for('mainpage'))
    
    profile = profile_repo.find_by_id(profile_id)
    adress = adress_repo.find_by_id(profile.adress)
    if request.method == 'POST':
        email = request.form.get('email')
        profile.email = email
        mobile_number = request.form.get('mobile_number')
        profile.mobile_number = mobile_number
        
        street = request.form.get('street')
        postal_code = request.form.get('postal_code')    
        country = request.form.get('country')
        house_number = request.form.get('house_number')
        
        if not adress:
            adress = Adress(street=street,postal_code=postal_code,country=country,house_number=house_number)
        
        adress.street = street
        adress.country = country
        if house_number == '':
            adress.house_number = None
        
        adress.postal_code = postal_code
        adress_id = adress_repo.save(adress)   
        
        profile.adress = adress_id
        profile_repo.save(profile)
        flask.flash(f"You updated profile successfully", category="success")
        return redirect(url_for('profile_detail',id=id))
            
        
        
    
    return render_template("profiles/profile_update.html",profile = profile,adress=adress)

#END COMMENTS

#START USERS

@app.route('/users/',methods=['GET'])
@role_required([Role.SUPERUSER.value])
def users_list():
    users = user_repo.find_all()
    profiles = profile_repo.find_all()
    users_profiles = zip(users, profiles)
    return render_template('users/users_list.html',users_profiles = users_profiles)


@app.route('/users/<string:id>/role/update',methods=['GET','POST'])
@role_required([Role.SUPERUSER.value])
def users_role_update(id):
    if not session["eingeloggter_username"]:
        flask.flash(f"You should first log in", category="info")
        return redirect(url_for('login'))
    profile_id = ObjectId(id)
    profile = profile_repo.find_by_id(profile_id)
    users = user_repo.find_all()
    
    for user_object in users:
        if user_object.profile_id == profile_id:
            user = user_object
    if request.method == 'POST':
        new_role = request.form.get('role')
        profile.role = new_role
        profile_repo.save(profile)
        flask.flash("User role updated successfully", "success")
        return redirect(url_for('users_list'))
        
    return render_template('users/user_role_update.html',profile = profile,user=user)

#END USERS

@atexit.register
def shutdown_hook():
    print("Close MongoDB-Connection...")
    client.close()

if __name__ == '__main__':
    app.run()
