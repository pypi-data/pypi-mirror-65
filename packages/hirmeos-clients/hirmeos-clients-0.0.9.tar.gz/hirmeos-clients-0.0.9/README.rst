HIRMEOS Clients
===============

Python clients for interacting with APIs that were developed as part of the
HIRMEOS project.

Once this has been shown to be working properly, and able to integrate with the
HIRMEOS drivers it can be moved to a HIRMEOS/OPERAS PyPI Repo.


Until CI is ready
-----------------
  .. code-block:: bash

    $ python3 setup.py sdist bdist_wheel
    $ twine upload dist/*


Note: We are still in the early stages of this project so there will be many
breaking changes as we go along.

Release Notes:
==============

[0.0.9] - 2020-04-06
---------------------
Added
 - translator: Reference variables for work types and URI schemes.
 - translator: Check if a work exists.
 - translator: Fetch all URIs associated with a work.
 - translator: Post new work.


[0.0.8] - 2020-03-06
---------------------
Changed
 - Make requirements for flexible to avoid conflicts with other packages.


[0.0.7] - 2020-03-06
---------------------

Added
 - Release notes

Changed
 - Strip trailing slash from TranslatorClient API base.
