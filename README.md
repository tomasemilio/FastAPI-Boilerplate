# FastAPI-Boilerplate

FastAPI Starter: A simple and intuitive example repository showcasing basic functionality and best practices for building web APIs with FastAPI. Use this as a template or reference for accelerating your FastAPI projects

## How to get started

Create a .env file following the example `example.env`

`app/config.py` has 3 sets of configurations: Test, Dev, and Prod.

```bash
touch .env
```

Run the following command to install dependencies. `runtime.txt` specifies the runtime version used.

```bash
bash reset.sh
```

## Run the app locally

```bash
python run.py
```

## Run tests.

We use the `TestConfig` to run tests

```bash
bash test.sh
```

### Features

- Routes / Crud.
- Base models with database persistence and relationships.
- Multiple configuration files.
- User authentication, authorization, and route protection.
- Logging
