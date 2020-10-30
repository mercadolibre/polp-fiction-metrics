#!/bin/bash
docker container run --rm --network=host -v $(pwd):/srv contre95/alembic downgrade base &&
docker container run --rm --network=host -v $(pwd):/srv contre95/alembic upgrade head
