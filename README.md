## cyclrr-py

cyclrr-py is Simple Cyclic Remeinder by email.

## Usage

### 1. Register your account

[![main](https://github.com/masayuki038/cyclrr-py/raw/master/screenshots/register.png)](https://github.com/masayuki038/cyclrr-py/raw/master/screenshots/register.png)

### 2. Register your contents that you want to remember cyclicly

[![main](https://github.com/masayuki038/cyclrr-py/raw/master/screenshots/contents.png)](https://github.com/masayuki038/cyclrr-py/raw/master/screenshots/contents.png)

### 3. Set schedule to send a content to you (ex. daily)

```
FLASK_APP=cli.py flask job sendmail
```

## Environment Vars

- DATABASE_URL: Database URL (SQLAlchemy)
- SENDGRID_API_KEY: API Key of SendGrid
- SENDMAIL_FROM: From Address