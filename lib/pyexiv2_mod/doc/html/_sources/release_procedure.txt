pyexiv2 release procedure
=========================

.. highlight:: bash

Release branch
##############

Set the version number to release::

  export VERSION=0.3.1
  export D=pyexiv2-$VERSION

Branch to release::

  bzr branch lp:pyexiv2 $D
  cd $D

Bump the version number: change the value of ``version_info`` in
``src/pyexiv2/__init__.py``.

Bump the version number in the Windows installer script: change the value of
``PYEXIV2_VERSION`` in ``win32-installer.nsi``.

Commit the changes::

  bzr commit -m "Bumped version number to $VERSION."

Update the ``NEWS`` file with the changes since the last release:

* dependencies
* changes
* bugs fixed
* contributors

Commit and push the changes::

  bzr commit -m "Updated NEWS."
  bzr push lp:~osomon/pyexiv2/$D

Source tarball
##############

Build pyexiv2::

  scons

Build the HTML documentation::

  scons doc
  mv doc/_build doc/html

Create the tarball and sign it::

  cd ..
  tar cvvjf $D.tar.bz2 $D --exclude-vcs \
      --exclude=build --exclude=.doctrees --exclude=.buildinfo \
      --exclude=objects.inv --exclude=.sconsign.dblite --exclude=*.pyc
  gpg --armor --sign --detach-sig $D.tar.bz2
  cd $D

Windows installer
#################

Cross-compile::

  ./cross-compile.sh

Build the installer and sign it::

  makensis win32-installer.nsi
  gpg --armor --sign --detach-sig pyexiv2-$VERSION-setup.exe

Publication
###########

* Create a release for the milestone
  (e.g. at https://launchpad.net/pyexiv2/+milestone/0.3.1/+addrelease)
* Upload the source tarball and the windows installer
  e.g. at https://launchpad.net/pyexiv2/0.3.x/0.3.1/+adddownloadfile
* Change the status of all the bugs marked as "Fix Committed" in the milestone
  to "Fix Released"

Communication
#############

* Write an announcement
  `on Launchpad <https://launchpad.net/pyexiv2/+announce>`_
* Send a mail to the
  `pyexiv2-developers mailing list <pyexiv2-developers@lists.launchpad.net>`_
* Send a mail to the current distribution packagers
  (Debian, Ubuntu, Fedora, ...)
* Write about the release on the
  `exiv2 forums <http://dev.exiv2.org/projects/exiv2/boards>`_
* Send a mail to the
  `Python announce mailing list <python-announce-list@python.org>`_
* Blog about the release (optional)

Web site
########

The branch for the website is at
`lp:~osomon/pyexiv2/website <https://code.launchpad.net/~osomon/pyexiv2/website>`_.

* Update the download page with the new release
* Update the online documentation

Final
#####

Merge back the release branch in the master branch and tag it::

  cd <local/path/to/master/>
  bzr merge lp:~osomon/pyexiv2/$D
  bzr commit -m "Merge the $VERSION release."
  bzr tag release-$VERSION
  bzr push

