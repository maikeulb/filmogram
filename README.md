# Filmogram

Instagram/Flickr clone where users share their favorite photos with other
users. Admin users can manage the site content.

Technology
----------
* Flask
* PostgreSQL
* UI Kit
* List.js
* DataTables
* Noty
* Infinity-Scroll

Screenshot
---
### Feed 
Displays photos from yourself and your following (powered by infinity-scroll). Also get notified when a user likes one of your photos.
![feed](/screenshots/feed.png?raw=true "Feed")
### Profile 
Displays your user profile and below that: your posts, followers, and followings (switch with tabs).
![profile](/screenshots/daido.png?raw=true "Profile")
### Post
Upload photos (from your filesystem) with captions.
![post](/screenshots/post.png?raw=true "Post")
### Discover 
Discover other users to follow/unfollow (client-side searching powered by
list.js).
![discover](/screenshots/discover.png?raw=true "Discover")
### Favorites 
Displays your liked photos.
![favorites](/screenshots/favorites.png?raw=true "Discover")
### Admin
Admin users may remove photos (admin interface powered by DataTables).
![admin](/screenshots/admin.png?raw=true "Admin")

Run
---
If you have docker installed,
```
TODO
```

Create a database titled 'filmogram', open `config.py` and point the database
URI to your server. After configuring the settings, set the
`FLASK_APP` env variable to filmogram.py, and then install the javascript
and python dependencies (e.g. `npm install` and `pip install -r
requirements.txt`). 

`cd` to `./src` and run the following:
```
flask db upgrade
flask seed-db
npm run start (runs the webpack dev server and flask dev server simultaneously)
Go to http://localhost:5000
```
TODO
----
Secure APIs  
Dockerfile  
Configure Webpack
