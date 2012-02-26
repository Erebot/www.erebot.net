Installation and setup
======================

Clone the website's repository::

    $ git clone git://github.com/fpoirotte/www.erebot.net.git

This will create a directory named "www.erebot.net" in the current directory.

Go into that directory and create a new virtualenv in it::

    $ cd www.erebot.net/
    $ virtualenv --no-site-packages -p python2.6 .

Replace ``python2.6`` with whatever version of Python you want to use.

Now, run::

    $ bin/python setup.py develop

This will download all required dependencies in the virtual environment
that we just created.

We will now finalize the installation.
To do so, we will first create a new configuration file.
You may start off by copying the example configuration file provided with
the git clone::

    $ cp erebot/config/deployment.ini_tmpl development.ini

Now use whatever editor you like to adapt development.ini
to suit your environment.

Second, we must create machine object (.mo) files from the translations
catalogs that ship with Erebot's website::

    $ bin/python setup.py compile_catalog

Last but not least, we will create the (local, SQLite-based) database
for the website::

    $ bin/paster setup-app development.ini

You're now ready to go.


Testing changes locally
=======================

Go to your local clone::

    $ cd ~/www.erebot.net/

Start the paste http server::

    $ bin/paster serve development.ini

This will display some information on the console, like so::

    Starting server in PID 10920.
    serving on http://127.0.0.1:5000

You may now browse to the address displayed (here, ``http://127.0.0.1:5000``)
to test your changes.

While developing you may want the server to reload after changes
in package files (or its dependencies) are saved.
This can be achieved easily by adding the ``--reload`` option
to the ``serve`` command::

    $ bin/paster serve --reload development.ini


Contributing
============

Once your changes are ready, you may want to contribute them back.
The procedure to do so is quite simple:

#.  Fork the project on GitHub.
#.  Clone your fork's repository locally.
#.  Create a new branch in that clone and apply changes there.
#.  Make sure you have proper tests and documentation for these changes.
#.  Commit the clone to your GitHub fork and send us a pull request.
#.  Please be patient until someone reviews the pull request.
#.  Go to step 3 and repeat. ;)

..  warning::
    A pull request with no tests has less chances to be accepted than one
    that is fully tested and properly documented.

