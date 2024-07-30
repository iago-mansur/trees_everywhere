# trees_everywhere

The "Trees Everywhere" project aims to create a database of trees planted by volunteers around the world. A user can join an account with other users so that everyone can see all the trees that were planted by the group of users on the same account.

## Instructions to run the app

- [Install Docker and Docker Compose](https://docs.docker.com/compose/install/)
- On terminal
    - sudo chmod 666 /var/run/docker.sock
    - docker build .
    - docker-compose build
    - docker-compose run --rm app sh -c "python manage.py migrate"
    - docker-compose up