# LG-Linter
![Upload Python Package](https://github.com/lgulich/lg-linter/workflows/Upload%20Python%20Package/badge.svg?branch=master)

A simple pre-commit linter for bash, python and c++.

## Installation
Make sure you have `clang-format` and `shellcheck` installed. If not you can install them with
```sh
sudo apt update
sudo apt install -y clang-format shellcheck
```
Next install the linter with
```sh
pip3 install lg-linter
```
**Note:** This will install / overwrite the linter config files in your home directory.

## How to use
Inside your git repo run
```sh
init_lg_linter
```
The linter is now active and will be run before every commit.
If you want to remove the linter from your repo use
```
deinit_lg_linter
```

**Pro Tip:** If the linter complains about stuff which clearly is wrong you can override him with
```
git commit --no-verify
```
Use with care, with great power comes great responsibility!

## Contact
For feature requests or bug reports please drop an issue at https://github.com/lgulich/lg-linter.
