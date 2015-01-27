.. KA Lite documentation master file, created by
   sphinx-quickstart on Tue Jan 20 11:55:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to KA Lite's documentation!
===================================

I just want to give an example here of how documentation can be organized. Be sure to check out the source and the `rst primer`_ and `toctree directive`_!

.. _rst primer: http://sphinx-doc.org/rest.html
.. _toctree directive: http://sphinx-doc.org/markup/toctree.html

.. screenshot::
   :url: /a/test/url

.. screenshot::
   :url: /another/test/url
   :focus: just_the_id
   :user-role: admin

.. screenshot:: joy_web_logo.png
   :url: /another/test/url/2
   :focus: the_id and the annotation
   :alt: alt text here
   :class: is_this_a_list of css_classes
   :user-role: admin
   :navigation-steps: ['click #css-selector', 'submit #css-selector-form']

Contents:

.. toctree::
   :maxdepth: 1

   You can specify titles like this <topic_dir/topic1>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

