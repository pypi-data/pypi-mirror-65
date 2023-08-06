# Epiphany-Editor

A graphical Map Editor for the Boulder-Dash clone, Epiphany!

A teratorn software production.

# Install from PyPI

```
pip3 install --user epiphany-editor
```

# Manual Installation

If the above method won't work for you, then the following manual instructions may help.

epiphany-editor depends on python3, pygame, and pygobject. Please install them first.

E.g. on Debian or Ubuntu-based systems try this:

```
sudo apt-get install python3-gi python3-pygame
```

Then you may run the editor:

```
./epiphany-editor
```

Or you may symlink it in to your path, like:

```
ln -s `pwd`/epiphany-editor /usr/bin/
```

Alternatively, use virtualenv to install all the dependencies:

```
git checkout https://github.com/teratorn/epiphany-editor.git
cd epiphany-editor
virtualenv -p python3 venv
venv/bin/pip install --editable .

# and run it with:

venv/bin/epiphany-editor
```
