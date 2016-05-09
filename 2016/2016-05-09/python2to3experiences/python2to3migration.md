Python 2.7 to 3 migration
=========================

Project
-------

* Python 2.7 project:

  https://github.com/fracpete/python-weka-wrapper

* Python 3 result:

  https://github.com/fracpete/python-weka-wrapper3


Details
-------

Some things have changed:

* renamed `xrange` to `range`

* different format for exceptions (`as` already available in 2.7)
  ```python
  except Exception, e:
  ```
  becomes
  ```python
  except Exception as e:
  ```
* a new library has appeared: `types`
  (creates befuddling error message when you have one yourself)

* iterators have changed slightly
  ```
  __init__
  __iter__
  next
  ```
  becomes
  ```
  __init__
  __iter__
  __next__
  ```

* urlib2 split into urllib.request and urllib.error

  https://docs.python.org/2/library/urllib2.html

* upload of sphinx generated documentation to pypi doesn't work
  (sphinx-pypi-upload is still only Python 2.x)

