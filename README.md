# About

This is test task implementation for some employer.

## How to Run ==

I'm using Fedora with docker installation

copy docker-compose.yml file somewhere,
after what run `docker-compose pull && docker-compose up --build`

this will create 2 containers: 1 for PostgreSQL and 1 for this
source tree. an this test server will listen at 8080 port

there is primitive client `client_main.py`: I starting it with `python3 ./client_main.py localhost:8080` command

this is all

beers
