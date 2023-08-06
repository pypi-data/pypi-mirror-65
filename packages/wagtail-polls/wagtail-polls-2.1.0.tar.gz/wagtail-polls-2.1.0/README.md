# Wagtail Polls

A small polls app that works with Wagtail's snippets and Django Rest Framework for ajax based voting.

This app requires login for voting and limits one vote per user.

# Installation

1. Install `wagtail-polls` via pip
2. Add `polls` to `INSTALLED_APPS`
3. Add `url(r'^polls/', include('polls.urls')),` to urls.py

# Usage

Create polls in wagtail snippets. Embed them wherever Snippets are supported or in Django admin.

## API

It's expected that the api will be used to submit votes (though do what you will)

Check out the self documenting api at `/polls/api/` for more infomation

# HACKING

A docker-compose.yml and demo project is here for quick set up. 

1. Install Docker and Docker compose
2. `docker-compose run --rm web ./manage.py migrate`
3. `docker-compose run --rm web ./manage.py createsuperuser`
4. `docker-compose up`
