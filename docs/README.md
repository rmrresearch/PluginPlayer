PluginPlayer Documentation
==========================

This folder contains the source code for the PluginPlayer documentation. The
documentation is hosted on GitHub pages and should be built automatically when
the `master` branch of PluginPlayer is updated.

If you would like to build a local copy the following instructions should
suffice (commands are assumed to be run in this directory):

```.bash
python3 -m venv virt_env
source virt_env/bin/activate
pip3 install -r requirements.txt
make html
```

The result will be a directory `build`. Navigating your web browser to
`file://path/to/build/html/index.html` should allow you to view the local
documentation in its HTML glory.
