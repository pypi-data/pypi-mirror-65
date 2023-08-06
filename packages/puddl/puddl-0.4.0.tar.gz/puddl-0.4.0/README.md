# Prerequisites
- Python 3.8 (a virtual environment is recommended)
- PostgreSQL


# Installation from Source
```
mkdir ~/puddl
git clone https://gitlab.com/puddl/puddl.git
cd ~/puddl/puddl/
pip install -e .
```

Install completion for bash (for other shells please refer to [the click
documentation][click-completion]):
```
mkdir -p ~/.bash/
_PUDDL_COMPLETE=source_bash puddl > ~/.bash/puddl

cat <<'EOF' >> ~/.bashrc
[[ -f ~/.bash/puddl ]] && source ~/.bash/puddl
EOF

exec $SHELL
```
[click-completion]: https://click.palletsprojects.com/en/7.x/bashcomplete/#activation-script

Initialize the database. The command `puddl config init` will consume the `.env`
file if present in the current working directory.
```
cd ~/puddl/puddl/
./env/dev/generate_env_file.sh > .env
./env/dev/create_database.sh

puddl config init
puddl db health
```

Try it:
```
puddl file index README.md
puddl file ls
puddl db shell
```


# Development
Run flake8 before committing
```
ln -s $(readlink -m env/dev/git-hooks/pre-commit.sample) .git/hooks/pre-commit
```

Basic development workflow:
```
# hack, hack
make
```

Got `psql` installed?
```
source <(puddl db env)
echo "SELECT path, stat->>'st_uid' as uid FROM file.file" | psql
```
