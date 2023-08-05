CornerstoneCMS
==============

CornerstoneCMS is a really simple content management system for churches. It has only two components to it, pages and
sermons. Sermons are hosted on Simplecast.


Installing
----------

Install and update using `pip`_::

   $ pip install -U CornerstoneCMS


Set up
------

To set up CornerstoneCMS for your site, you can either manually create a configuration file, or run a configuration
wizard.

Configuration wizard
~~~~~~~~~~~~~~~~~~~~

CornerstoneCMS comes with a short configuration wizard which will create a configuration file for you::

   $ python -m cornerstone.conf

Manual configuration
~~~~~~~~~~~~~~~~~~~~
Set up CornerstoneCMS by creating a configuration file like ``cornerstone.conf``:

.. code-block:: ini

   [flask]
   secret_key = <create a secret for sessions etc>

   [sqlalchemy]
   database_uri = sqlite:///cornerstone.sqlite

   [cornerstone]
   title = My Church Name


Deploying to Production
-----------------------

CornerstoneCMS is a WSGI application, and needs to be deployed to a WSGI server. Create a file called ``wsgi.py`` and
point your WSGI server to the file.

.. code-block:: python

   from cornerstone.app import create_app

   application = create_app('/path/to/yourfile.conf')


Links
-----

* Website: https://cornerstonecms.org/
* License: https://gitlab.com/cornerstonecms/cornerstonecms/blob/master/LICENSE
* Issue tracker: https://gitlab.com/cornerstonecms/cornerstonecms/issues


.. _pip: https://pip.pypa.io/
