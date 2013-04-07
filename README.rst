Installation and setup
======================

Create a new virtualenv::

    $ virtualenv --no-site-packages tg2env.

Go into that environment and activate it::

    $ cd tg2env && source bin/activate

Install the dependencies required to bootstrap the site::

    $ easy_install -i http://tg.gy/current tg.devtools

Now, clone the website's repository::

    $ git clone git://github.com/Erebot/www.erebot.net.git

This will create a directory named "www.erebot.net" in the current directory.

Go into that directory and "develop" the project::

    $ cd www.erebot.net &&  python setup.py develop -i http://tg.gy/current

This will download all required dependencies in the virtual environment
that we just created.

We will now finalize the installation.
To do so, we will first create a new configuration file.
You may start off by copying the example configuration file provided with
the git clone::

    $ cp -f erebot/config/deployment.ini_tmpl development.ini

Now use whatever editor you like to adapt development.ini
to suit your environment.

Second, we must create machine object (.mo) files from the translations
catalogs that ship with Erebot's website::

    $ python setup.py compile_catalog

Last but not least, we will create the (local, SQLite-based) database
for the website::

    $ paster setup-app development.ini

You're now ready to go.


Testing changes locally
=======================

Go to your local clone::

    $ cd .../www.erebot.net/

Activate the virtual environment::

    $ source ../bin/activate

Start the paste http server::

    $ paster serve development.ini

This will display some information on the console, like so::

    Starting server in PID 10920.
    serving on http://127.0.0.1:5000

You may now browse to the address displayed (here, ``http://127.0.0.1:5000``)
to test your changes.

While developing you may want the server to reload after changes
in package files (or its dependencies) are saved.
This can be achieved easily by adding the ``--reload`` option
to the ``serve`` command::

    $ paster serve --reload development.ini


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
    A pull request with no tests has less chances of being accepted than one
    that is fully tested and properly documented.

