EdxNotes Django App
+++++++++++++++++++

To run Django tests use:
`paver test_system -t common/djangoapps/edxnotes/tests.py`

Usage
-----

To use this application, course staff must opt-in by doing the following:

* Login to [Studio](http://studio.edx.org/).
* Go to *Course Settings* -> *Advanced Settings*
* Find the ```Enable Notes``` policy key and set it to `true`.
* Save the course settings.
