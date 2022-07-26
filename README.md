virtualenv -p python3 venv
source venv/bin/activate

install dev environment
```
pyenv install 3.10.4
pyenv virtualenv 3.10.4 venv-audacious
pyenv virtualenvs
pyenv activate venv-audacious
# create a file called .python-version 
# containing the name of venv

pip install --upgrade pip
pip install --upgrade pylama
pip install --upgrade -r requirements.txt

sqlite3 database/database.db
```

export FLASK_CONFIG=development
export FLASK_DEBUG=1
export FLASK_APP=audacious_webui
flask run

# FLASK DATABASSE
## first time
flask db init
flask db migrate -m "Initial migration"
## after
flask db migrate
## every time
flask db upgrade

# FLASK APP

INSERT INTO domains (domain_id, domain_name, domain_type, domain_isactive)
VALUES
  (10, 'tata.com', 'ads', 1),
  (11, 'titi.com', 'ads', 1),
  (12, 'tutu.com', 'porn', 1);

INSERT INTO statistics (stats_domain_id, stats_client_ip, stats_request_count)
VALUES
  (1, '10.0.0.1', 103),
  (1, '10.0.0.2', 112),
  (2, '10.0.0.1', 97),
  (3, '10.0.0.1', 16),
  (3, '10.0.0.2', 1),
  (3, '10.0.0.3', 175);

select * from domains left join statistics on domains.domain_id = statistics.stats_domain_id;
session.query(Model).join(AnotherModel, AnotherModel.model_id == Model.id, isouter=True)


# Docker env

docker build --tag 'dns' .





# Host

certbot
fail2ban
byobu
nginx
gitea


certbot certonly -n --standalone --domain dns.audacious-unicorn.com

certbot renew --standalone --reuse-key

sudo certbot delete
sudo certbot delete --cert-name dot.audacious-unicorn.com