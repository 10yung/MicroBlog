# MicroBlog
This is a microblog devloped from pythoh flask

# How to use ( development mode )
0. Create environment from `/env.yml` file
    - `conda env create -f env.yml`
1. Setting environment variable
    - `export FLASK_APP=MicroBlog`
    - `export FLASK_ENV=development`
    - `export MAIL_USERNAME=<YOURNAME>@gmail.com`
    - `export MAIL_PASSWORD=<YOURPASSWORD>`
2. Initial Database (If `/migrations` folder is needed to be recreated)
    - `flask db init`
    - `flask db migrate`
    - `flask db upgrade`
    
3. run the application  with `flask run` command

### Reference
- https://flask.palletsprojects.com/en/1.1.x/
- https://uniwebsidad.com/libros/explore-flask/chapter-8/custom-filters
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers
- https://www.amazon.com/Flask-Web-Development-Developing-Applications/dp/1491991739