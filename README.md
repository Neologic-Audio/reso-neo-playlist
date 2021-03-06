

<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Neologic-Audio/reso-neo-playlist">
    <img src="https://github.com/Neologic-Audio/reso-neo-playlist/blob/main/playlist/static/img/logo2.png" alt="Logo" width="800px">
  </a>

<h3 align="center">Neologic Audio</h3>

  <p align="center">
    A recommendation tool to find the most popular tracks for each tag.
    <br />
    <a href="https://github.com/Neologic-Audio/reso-neo-playlist"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://neologic-audio.herokuapp.com/">View on Heroku</a>
    ·
    <a href="https://github.com/Neologic-Audio/reso-neo-playlist/issues">Report Bug</a>
    ·
    <a href="https://github.com/Neologic-Audio/reso-neo-playlist/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
## Table of Contents
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <ul>
        <li><a href="#how-to-setup-locally-">How to Setup Locally</a></li>
        <li><a href="#how-to-deploy-to-heroku">How to Deploy to Heroku</a></li>
      </ul>
      </ul>
    </li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>


<!-- ABOUT THE PROJECT -->
## About The Project

This project provides a Resonate.is listener an upgraded experience by allowing users to search for the most popular tracks for a given tag and being able to also find convenient recommendations from different tags through an upgraded user interface. Through this improved search algorithm, people can explore new recommended tracks and add what they like to a personalized playlist through our responsive web application. The playlist is stored via Neo4j to provide an easy-to-use query experience that works seamlessly for the user and allows the engineer to graphically maintain and update connections in a concise manner.

### Built With

#### Technologies
* [Python](https://www.python.org/)
* [Django Web Framework](https://www.djangoproject.com/)
* [Neo4j Graph Database](https://neo4j.com)
* [Django-Neomodel Plugin](https://github.com/neo4j-contrib/django-neomodel)
* [Bootstrap](https://getbootstrap.com)
* [HTML](https://html.spec.whatwg.org/)
* [CSS](https://www.w3.org/Style/CSS/)
* [JavaScript](https://www.javascript.com/)
* [jQuery](https://jquery.com)

#### IDEs / Code Editors
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [Visual Studio](https://visualstudio.microsoft.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Create a free listener account with [Resonate.is](https://resonate.is/join/)

 * Install [Python 3.9](https://www.python.org/downloads/)
	  ```sh
	  python --version
	  ```
* Django 3.2.5
* Neo4j Database

#### Create your Neo4j Database <!--the first step to do-->

You can manage your own database locally using [Neo4j Desktop](https://neo4j.com/download-center/#desktop), or go to [Neo4j Aura](https://neo4j.com/cloud/aura/) for a fully managed cloud database.

#### Initial Data Import
Before you start, install the [APOC Library plugin.](https://neo4j.com/developer/neo4j-apoc/#installing-apoc) <!--installs automatically when accessing plugins Neo4j Desktop-->

#### Create Constraints <!--in Neo4j Browser-->

```
CREATE CONSTRAINT ON (a:Ruser) ASSERT a.uuid IS UNIQUE;
CREATE CONSTRAINT ON (a:TrackGroup) ASSERT a.uuid IS UNIQUE;
CREATE CONSTRAINT ON (a:Track) ASSERT a.uuid IS UNIQUE;
```
<!--all commands below in Neo4j Browser-->
#### Add the first page of Playlists (a type of TrackGroup) 

```
WITH 'https://api.resonate.coop/v2/' AS uri
CALL apoc.load.json(uri + 'trackgroups?type=playlist') // in this example, grabbing listener-generated playlists
YIELD value
UNWIND value["data"] as data
MERGE (u:RUser {uuid:toString(data["user"]["id"])})
MERGE (t:TrackGroup {uuid:toString(data["id"])})
MERGE (u)-[:OWNS]->(t)
SET t.title = data["title"]
SET t.type = data["type"]
SET t.slug = data["slug"]
SET t.tracks_imported = false
```

#### Add more TrackGroups

```
WITH 'https://api.resonate.coop/v2/' AS uri
CALL apoc.load.json(uri + 'trackgroups') // in this example, grabbing listener-generated playlists
YIELD value
UNWIND value["data"] as data
MERGE (u:RUser {uuid:toString(data["user"]["id"])})
MERGE (t:TrackGroup {uuid:toString(data["id"])})
MERGE (u)-[:OWNS]->(t)
SET t.title = data["title"]
SET t.type = data["type"]
SET t.slug = data["slug"]
SET t.tracks_imported = false
```

#### Add the tracks

```
CALL apoc.periodic.commit(
"MATCH (tg:TrackGroup)
WHERE NOT tg.tracks_imported 
SET tg.tracks_imported = true
WITH tg limit $limit
WITH 'https://api.resonate.coop/v2/' AS uri, tg.uuid as tg_id
CALL apoc.load.json(uri + 'trackgroups/' + tg_id )
yield value
UNWIND value['data']['items'] as items
MERGE (u:RUser {uuid:toString(items['track']['creator_id'])})
MERGE (track:Track {uuid:toString(items['track']['id'])})
MERGE (tg)-[:HAS_TRACK]->(track)
MERGE (track)<-[:CREATED]-(u)
SET track.title = items['track']['title']
SET track.tags_imported = false
RETURN count(*)
",
{limit:10});
```

#### Double-check track-adding

```
CALL apoc.periodic.commit(
"
match (tg:TrackGroup)-[:HAS_TAG]-(t:Tag)
where not (tg)-[:HAS_TRACK]-(:Track)
WITH tg limit $limit
WITH 'https://api.resonate.coop/v2/' AS uri, tg.uuid as tg_id, tg
CALL apoc.load.json(uri + 'trackgroups/' + tg_id )
yield value
UNWIND value['data']['items'] as items
MERGE (u:RUser {uuid:toString(items['track']['creator_id'])})
MERGE (track:Track {uuid:toString(items['track']['id'])})
MERGE (tg)-[:HAS_TRACK]->(track)
MERGE (track)<-[:CREATED]-(u)
SET track.title = items['track']['title']
SET track.tags_imported = false
RETURN count(tg)",
{limit:1});
```

#### The Tags

```
CALL apoc.periodic.commit(
"
MATCH (u:RUser)-[:CREATED]->(track:Track)
WHERE not u.uuid  in ['7212','4315','4414'] // bad data
AND NOT track.tags_imported
SET track.tags_imported = true
WITH u as artist, u.uuid as user_id, count(DISTINCT track) as tracks,'https://api.resonate.coop/v2/' as uri
ORDER BY tracks desc
LIMIT $limit
CALL apoc.load.json(uri + 'artists/' + user_id + '/releases') // grabbing all
YIELD value
UNWIND value['data'] as data
UNWIND data['tags'] as tags
MERGE (t:TrackGroup {uuid:toString(data['id'])})
MERGE (user:RUser {uuid:toString(user_id)})-[:OWNS]->(t)
MERGE (tag:Tag {name:toLower(tags)})
MERGE (tag)<-[:HAS_TAG]-(t)
SET tag.uuid=apoc.create.uuid()
SET t.title = data['title']
SET t.type = data['type']
RETURN count(*)
",
{limit:5});
```

#### Twitter 

```
CALL apoc.periodic.commit(
"
MATCH (u:RUser)
WHERE u.twitter_checked=false
WITH u.uuid as user_id, 'https://stream.resonate.coop/api/v2/' as uri, u as artist
LIMIT $limit
CALL apoc.load.json(uri + 'artists/' + user_id) // grabbing all
YIELD value
UNWIND value['data']['links'] as links
WITH apoc.data.url(links['href']) as unwound_links, artist as artist,links
WHERE unwound_links.host='twitter.com'
SET artist.twitter=toLower(substring(unwound_links.path,1))
SET artist.twitter_checked=true
RETURN count(artist)",
{limit:100});

```
	
### Installation
#### How to Setup Locally <!--can also download the code directly-->

1. Clone the repository
  ```sh
   git clone https://github.com/Neologic-Audio/reso-neo-playlist.git
   ```



#### Creating a virtual environment


<details>
<summary>
Option 1: Using command-line
</summary>

```
1. Open up the terminal to the base level of the project folder

2. Type the following commands
* python(python3) -m venv venv <!--different for mac-->
* source venv/bin/activate (Unix OS and macOS)
** venv/bin/activate (Windows)
* pip install -r requirements.txt

3. The packages should be installed
```
</details>

<details>
<summary>
Option 2: Use an IDE (Similar setup depending on the IDE)
</summary>

```
In PyCharm (example of setup):

1. Go to File Settings

2. In the Python Interpreter tab, click the gear Icon

3. Click Add (new interpreter)

4. On the virtual environment page, click to create a new environment
* Keep the project location as the base project filepath
* Make sure to use the Python source your Operating System is using <!-- python 3.9 for mac -->
** If you have multiple installations of Python, use "where python" (for Windows) or "which python3" (for mac) in your terminal to find the correct file location
* Keep inheritance and availability unchecked, since it's better to go on a project by project basis

5. Click OK

6. You should be good to run the application afterwards
* note: if your installation is using any version of Django 4.0, then the dependencies will be broken and conflict.
```
</details>

<p align="right">(<a href="#top">back to top</a>)</p>


  
#### Environment Variables  
  
Environment variables can be used for configuration. They must be set before running the project to avoid receiving a server error. This can be configured either through your IDE or PATHs. #should configure by itself when py manage.py migrate
  
Neo4j Desktop:  
```shell  
export NEO4J_BOLT_URL=bolt://neo4j:password@host-or-ip:port
```  

For Neo4j Aura:  
```shell  
export NEO4J_BOLT_URL=neo4j+s://neo4j:password@host-or-ip:port
```  
  
#### Running the Django Server  <!--geos for Windows (brew install geos for macOS)-->
Run migrations and create your superuser (for the admin, this is using an SQLite database)  
  

<details>
<summary>
Option 1: Windows
</summary>

```python  
py manage.py migrate 
py manage.py createsuperuser
py manage.py runserver
```  
</details>
<details>
<summary>
Option 2: Mac
</summary>

```python  
python3 manage.py migrate
python3 manage.py createsuperuser #only for the first time
python3 manage.py runserver
```  
</details>

<p align="right">(<a href="#top">back to top</a>)</p>  
  
<!-- USAGE EXAMPLES -->  
## How to Deploy to Heroku  
  
Go to your Heroku dashboard and create a new app and add its git remote to your local clone of this app.  
  
Go your Heroku's app's settings and add the `NEO4J_BOLT_URL` environment variable with the correct credentials:  
  
```NEO4J_BOLT_URL="bolt://neo4j:password@host-or-ip:port"```  

Follow the deployment instructions inside your Heroku app.

```Adding gunicorn to your project for web deployment```

(https://devcenter.heroku.com/articles/python-gunicorn)

Now you can push to Heroku:  
  
```shell  
git push heroku master/main (depending on how project's original git branch is named)
```  

Noted issues that can interfere with deployment:

``` Libgeos C DLL missing ```

To fix:

```
"This is ultimately because Shapely is currently an install requirement of Neomodel. Shapely requires a C lib to be installed which may/may not be present on your OS.
On UNIX you can simply install this with 'apt-get install libgeos-dev'"

To actually install via Heroku requires several steps:
1. You would need to include a Heroku buildpack into your application (https://github.com/heroku/heroku-buildpack-apt)
2. Create an Aptfile in your root directory and add 'libgeos-dev' as its contents (similar problem here https://stackoverflow.com/questions/34104909/heroku-python-app-with-custom-package-in-aptfile-no-python-packages-installed)
3. Make sure that Gunicorn is installed so that this works
4. Push to Heroku
```

```Application only loads HTML, no Javascript or CSS```

To fix:

```
1. Add Whitenoise to your application (https://devcenter.heroku.com/articles/django-assets)
2. Use Postgresql provided by Heroku application and add to project settings (extract credentials necessary via clicking on the DB in Heroku)
```
  
<p align="right">(<a href="#top">back to top</a>)</p>  
  
  
<!-- LICENSE -->  
## Authors  
  
* Ariel Fainstain (Team Lead)  
* Adejsha Francis  
* Samuel Parker  
* Maxim Stroganov  
* Gabrielle White
<p align="right">(<a href="#top">back to top</a>)</p>  
  
  
  
  
<!-- ACKNOWLEDGMENTS -->  
## Acknowledgments  
  
* [The SilverLogic](https://tsl.io/) for sponsoring this project
* [Florida Atlantic University - College of Engineering and Computer Science](https://www.fau.edu/engineering/)
* [reso-tag-charts](https://github.com/whatSocks/reso-tag-charts) 
* [Resonate.is](https://resonate.is/)
  
<p align="right">(<a href="#top">back to top</a>)</p>
