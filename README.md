# Blog Platform

A personal blog platform aimed at sharing my own thoughts, trips, knowledges through posts

## Launch project with `poetry` package manager

1. Make sure that the package manager `poetry` is installed in your machine. If it's not installed, go to official documentation for more info.

2. Activate a virtual environment with `poetry`

```shell
poetry shell
```

3. Install project needed packages with following command

```shell
poetry install --no-root
```

4. Create `.env` file in the project root directory and set project virtual variables for your own like the example in `.env-example` file

5. Migrate database to create db tables

```shell
python manage.py migrate
```

6. Run the project with command below

```shell
python manage.py runserver
```

7. Move to `http://127.0.0.1:8000/blog/` to open the page of blog posts


## Launch project with `pip` package manager

1. Create a virtual environment

```shell
python3 -m venv venv
```

2. Activate virtual environment depends on your OS

3. Install all project dependencies with command

```shell
pip install -r requirements.txt
```

For next steps follow the instruction above (Launch project with `poetry` package manager) begining from 4th step.


## Run tests

Enter the command below to run project tests

```shell
pytest -s -v
```
