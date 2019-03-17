# LAB

## Dev Guides

### Packages

```bash
pip install -r requirements.txt
```

### venv

We need to create a virtual environment at the first time.

> It's fine if you wanna install those things globally.
> I suggest you to create a virtual environment if you don't want to mess your environment up :)

```bash
python3 -m venv python
```

After this creation

In Linux or Mac

```bash
source python/bin/activate
```

### config

The configuration file is located at /config.json. The template configuration file is at `config.templete.json`. The format of the file is JSON.

### Run

You need to make a `config.json` at project root in order to run it.

```bash
python main.py
```

### Dev flow

If you want to change something. Please open a new branch from branch `dev` and commit you changes at the new branch you just created. After finished all changes, make a pull request and set the target branch to `dev`, then wait for someone's approval.
