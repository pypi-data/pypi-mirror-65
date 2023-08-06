# Changelog machine

## Getting started

### Install
```bash
pip3 install -i https://test.pypi.org/simple/ changelog-machine
python3 -m changelog-machine -h # will print the help
```

### Create new entry
```bash
python3 -m changelog-machine entry -m "Message of the entry"
```
for further options see:
```bash
python3 -m changelog-machine entry -h
```

### Generate changelog for new release
The new release with its entries will be inserted in the existing `CHNAGELOG.md` or create a new on in order that the highest version will be on top.
```bash
python3 -m changelog-machine changelog --releaseVersion "1.0.0"
```
