PyPI Release Process
======================


#. Update HISTORY.rst

#. Commit the changes:

    .. code-block:: bash

        git add HISTORY.rst
        git commit -m "Changelog for upcoming release 0.1.1."

#. Update version number (can also be patch or major)

    .. code-block:: bash

        bump2version minor

#. Install the package again for local development, but with the new version number:

    .. code-block:: bash

        python setup.py develop

#. Run the tests:

    .. code-block:: bash

        py.test

#. Push the commit:

    .. code-block:: bash

        git push

#. Push the tags, creating the new release on both GitHub:

    .. code-block:: bash

        git push --tags

#. Wait for travis to finish running tests to make sure everything's ok. Then release.

	.. code-block:: bash

		make release

#. Check the PyPI listing page to make sure that everything displays properly. If not, try one of these:

    #. Copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.

    #. Check your long_description locally:

        .. code-block:: bash

            pip install readme_renderer
            python setup.py check -r -s

#. Edit the release on GitHub (e.g. https://github.com/mozilla/domain_utils/releases). Paste the release notes into the release's release page, and come up with a title for the release.

About This Checklist
--------------------

This checklist is adapted from https://github.com/audreyr/cookiecutter-pypackage/blob/master/docs/pypi_release_checklist.rst
