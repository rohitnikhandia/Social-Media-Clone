# My Social Media App

My Social Media App is a web application built using HTML, CSS, JavaScript, Python Django, SQLite3, Django ORM, and Django templating tags. The app provides features such as user registration, authentication, user profiles, follower and following sections, post options, update and delete post options, and search.

## Table of Contents

* Features
* Installation
* Usage
* Endpoints
* Contributing

## Features
* User registration and authentication system.
* User profiles with options to update and delete posts.
* Follower and following sections.
* Post options: users can create, update and delete their own posts.
* Search functionality.
* Secure password storage using.

## Installation
To run this app, you need to have Python 3 and SQLite3 installed on your system. To install, clone this repository and install the requirements using pip.
```
git clone https://github.com/<username>/<repository>.git
cd <repository>
pip install -r requirements.txt
```

## Usage
To use this app, run the following command in your terminal:

```
python manage.py runserver
```
The app will start running on http://localhost:8000.

## Endpoints
* /settings/: User settings page.
* /upload/: Post upload page.
* /follow/: Follow user endpoint.
* /search/: Search functionality.
* /profile/<str:pk>/: User profile page.
* /like-post/<uuid:post_id>/: Like post endpoint.
* /signup/: User registration endpoint.
* /signin/: User login endpoint.
* /signout/: User logout endpoint.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
