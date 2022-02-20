# pokedex-api

An API that returns your own personalized Pokedex!

## Prerequisites

To run this project, ensure that you have both `docker` and `docker-compose` installed. To install `docker`, see the
official docs [here](https://docs.docker.com/get-docker/). To install `docker-compose`, see the official docs
[here](https://docs.docker.com/compose/install/).

To check if `docker` and `docker-compose` are installed, run `docker -v` and `docker-compose -v`, respectively.

## Project setup

To start the api, clone the project run `docker-compose up` in the root directory
(ensure that the docker daemon is running first). You should see output similar to:

```
pokedex-api_1  | INFO:     Will watch for changes in these directories: ['/pokedex-api']
pokedex-api_1  | INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
pokedex-api_1  | INFO:     Started reloader process [1] using statreload
pokedex-api_1  | INFO:     Started server process [8]
pokedex-api_1  | INFO:     Waiting for application startup.
pokedex-api_1  | INFO:     Application startup complete.
```

To check whether the api is running, visit http://localhost/health, which should respond with

```json
{
  "status": "ok"
}
```

Whenever you want to stop the server, run `docker-compose down`.

## Docs

The documentation for this api can be found at http://localhost/docs.

The OpenAPI json spec can be found at http://localhost/openapi.json.

## Future improvements

There are many improvements that could be made to this api:

#### Security

- If this api was not running on a VPC beneath a private subnet, then I would implement user authentication
  (e.g. using something like json web tokens). I would also then implement user authorization if necessary.
- I would mask sensitive data in the logs.
- In the docker image, I would create a user that only has the permissions to run apps.

#### Logging

- I would implement a middleware to log the time of each request and potentially flag any requests that are taking a
  long time.

#### Code improvements

- I would use a prefix like `/api/v1` to enable api versioning (the structure for this is already in place, but
  implementing it would mean that the api no longer conforms to the design document).
- I would refactor the custom wrapper client in `app/utils/external_api_client`. Namely, I would implement better error
  handling (e.g. use error schemas from the external apis and map those errors to my own custom error schema).
- I would refactor the tests to make fixtures more reusable and reduce some duplicate code.
- I would use the [semantic release](https://github.com/semantic-release/semantic-release) project to automatically
  create versions for the api based off of commit messages.

#### Performance improvements

- For a production image, I would try to slim down the image by not copying over unnecessary files (like testing files)
  and I would not install all the dev dependencies in the `requirements.txt` file.
- I would cache the result of the external api calls.
