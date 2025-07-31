cd /var/www/html;

python3.10 -m pip install --upgrade pip;

python3.10 -m pip install --no-cache-dir --upgrade -r app/requirements.txt;

echo "--------------------- Starting --------------------------------";
tail -f /dev/null
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload