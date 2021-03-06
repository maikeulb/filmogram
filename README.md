# Filmogram

Social network (similar to Instagram) for film photographers. Users share their
favorite photos with other users. Admin users can manage the site content.

There are three branches: 
1. `master` persists the uploaded media files onto the filesystem. 
2. `s3` which persists them onto DigitalOcean Spaces (API is compatible with S3).
3. `redis` (in-progress) is based on the `s3` branch but with a fanout on write feed.


Technology
----------
* Flask
* PostgreSQL
* UI Kit
* List.js
* DataTables
* Noty
* Infinity-Scroll

Infrastructure
----------
* DigitalOcean (virtual machine + object storage)
* Docker
* Lets Encrypt
* Nginx

Screenshots
---
### Landing 
Photo creds to [Trent Parke](https://pro.magnumphotos.com/C.aspx?ERID=24KL534BCY&VF=MAGO31_10_VForm&VP3=CMS3)
![landing](/screenshots/landing.png?raw=true "Feed")
### Feed 
Displays photos from yourself and your following (powered by infinity-scroll). Also get notified when a user likes one of your photos.
![feed](/screenshots/feed.png?raw=true "Feed")
### Profile 
Displays your user profile. The default profile image is a gravatar but users have the ability to upload a photo. Below your profile are your posts, followers, and followings (switch content with tabs).
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

Run (master branch)
---
You will need webpack. If you have webpack installed, then then go ahead and
install the javascript dependencies (e.g. `npm install`).


```
npm run build
docker-compose build
docker-compose up
Go to http://localhost:5000
```

Alternatively, create a database named 'filmogram', open `config.py`
and point the database URI to your server. After configuring the
settings, set the `FLASK_APP` env variable to filmogram.py, and then
install the javascript (e.g `npm install`) and python dependencies
(e.g. `pip install -r requirements.txt`). Be sure to install the
python dependencies using `requirements.txt` located in `./src/`, not
`./src/requirements/` (I'm working on pruning the dev/prod/test
dependencies).

```
flask db upgrade
flask seed-db
npm run build (required for copying assets over to static directory)
npm run start (runs the webpack dev server and flask dev server simultaneously)
Go to http://localhost:5000
```
TODO
----
Prune javascript and python dependencies<br>
Build frontend in Dockerfile<br>
Add Social Auth <br>
