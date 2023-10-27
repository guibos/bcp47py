##########
Quickstart
##########

***********
Basic Usage
***********

.. code-block:: python

   from bcp47py.repository import Repository

   repo = Repository()


A repo instance will provide several methods to get all information or properties to get all information. For more
information for each repo:

#.. autoclass:: repository.Repository
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__

*********************
Provide external data
*********************

BCP47Py have a local copy of:

 - Language Subtag Registry
 - Common Locale Data Repository (TODO)

New versions of previous resource are check regularly by automatic process. It is possible that between a new release
and publish a new version of BCP47Py could delay some time.


Provide alternative data to the constructor
=================================================

You could get the current version of each resource

 - `Language Subtag registry <https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry>`_
 - `Common Locale Data Repository <https://cldr.unicode.org/index/downloads>`_ (TODO)

.. code-block:: python

   from bcp47py.repository import Repository

   repo = Repository(language_subtag_registry='/your/language-subtag-registry/path')


Update data in your virtualenv package
======================================

In some cases provide the paths to the constructor could not be an option. You can force update local data with:

.. code-block:: python

   from bcp47py.downloader_service import DownloaderService

   DownloaderService().download()



.. warning::
   Data updated in virtualenv could be lost if you update your virtualenv. Keep in mind that this solution is not
   recommended and could produce side-effects.



