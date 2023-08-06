# open-experiment-format
Open Experiment Format is a collection of protobufs that allows you to serialize an Experiment.


## How to deploy
This should be done after your pull request has been merged to master.

### Bump the version in `deepomatic/oef/__init__.py`
If this is a breaking change, modify the middle number. For instance: a new required field in a
protobuf definition. Otherwise, change the last number.

### Tag the commit
Once the pull request is merged, tag the (last) corresponding commit by doing:

```bash
git checkout commit_id
version=0.1.2
git tag -m "Release open-experiment-format v${version}" v${version}
git push origin v${version}
```

### Create a github release
Click "Draft a new release" [here](https://github.com/Deepomatic/open-experiment-format/releases)
Paste the result of:

```bash
git log --pretty=oneline v0.3.0..v0.4.0
```

- Tip 1: keep the whole commit id, it will shorten itself into a little link
- Tip 2: remove the tag from the commit line

### Release the packages for this version on pypi
Simply run `make publish`. You will need to be admin on PyPi for it to work.

You  can check the release here: https://pypi.org/project/deepomatic-oef/#files
