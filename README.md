# Tech Challenge 03 <!-- omit in toc -->

- [Local ENV](#local-env)
  - [Create](#create)
  - [Active](#active)
- [Run local](#run-local)

## Local ENV

### Create

```bash
python -m venv .venv
```

### Active

```bash
source .venv/bin/activate
```

## Run local

> Before run copy `.env.sample` and rename to `.env`. Replace the variables with the correct values.

```bash
pip install -r requirements.txt
python src/main.py
```
