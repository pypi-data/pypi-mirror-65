gocept.webtoken
===============

3.1 (2020-04-08)
----------------

- Migrate to Github.

- Test with Python 3.8 and PyPy3.

- Stop testing with Python 3.5.

3.0 (2018-11-14)
----------------

- Change license from ZPL to MIT.

- Add support for Python 3.7.

- Drop support for Python 3.4.

- Make subject check optional as some systems like Keycloak use a random
  uuid as the subject which is unknown for the decoder.

- Add `audience` parameter which is required to decode tokens generated
  by Keycloak.


2.0 (2018-01-08)
----------------

- Drop support for Python 3.3 but add it for 3.6.

- Make `setup.py` compatible with newer `setuptools` versions by no longer
  using absolute paths.


1.2.1 (2015-10-08)
------------------

- Fix `extract_token` to accept any ``collections.Mapping`` derived object.


1.2 (2015-10-08)
----------------

- Added helper functions to create a Bearer Authorization header and extract
  a token from it.

- Officially support Python 3.5.


1.1 (2015-10-01)
----------------

- Shortened imports for `CryptographicKeys`, `create_web_token` and
  `decode_web_token`, which are now importable directly from `gocept.webtoken`.

- Added documentation.


1.0 (2015-10-01)
----------------

* Add support for Python 3.3 and 3.4.

* Initial release, extracted from internally used package.
