# flask-fahrzeug-status

Simple Website to display vehicle status. Pulling its' data from a postgres DB created with fireboard-scraper

# Running
Create test.env similar to this:
```
DB_NAME="<name_of_db>"
DB_HOST="<ip_of_db_server>"
DB_USER="<db_user_name>"
DB_PASSWORD="<db_password>"
DB_PORT=<db_port>
```
create virtual environment, with python3 and activate it
```
python3 -m venv .venv
source .venv/bin/activate
```
Upgrade pip and install requirements
```
pip install --upgrade pip
pip install -r requirements.txt
```
Finally start the app
```
uvicorn app.run:app --reload
```

Note that this app is expecting a created DB that is filled with data from another source for now. As an example you can use this [Project](https://github.com/Freiwillige-Feuerwehr-Weingarten/fireboard-scraper) to scrape fireboard.net for vehicle data, if you have it available there.
Example of how this could be depoyed to debian can be found on [Medium.com](https://ashfaque.medium.com/deploy-fastapi-app-on-debian-with-nginx-uvicorn-and-systemd-2d4b9b12d724)