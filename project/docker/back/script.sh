cd /var/www/html;

python3.10 -m pip install --upgrade pip;

python3.10 -m pip install --no-cache-dir --upgrade -r requirements.txt;

echo "--------------------- Starting --------------------------------";

# uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload
pip install geoip2
FLASK_APP=app.app:app flask run --host 0.0.0.0 --port 8080 --debug