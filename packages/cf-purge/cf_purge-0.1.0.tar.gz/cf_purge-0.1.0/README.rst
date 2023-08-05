========
cf_purge
========

::
    usage: cf_purge.py [-h] [-a ACCESS_KEY] [-s SECRET_KEY] -d DISTRIBUTION
                       [-c CALLER_REFERENCE] [-t] [-v]
                       paths [paths ...]

    Invalidate AWS CloudFront's cache.

    positional arguments:
      paths

    optional arguments:
      -h, --help            show this help message and exit
      -a ACCESS_KEY, --access-key ACCESS_KEY
      -s SECRET_KEY, --secret-key SECRET_KEY
      -d DISTRIBUTION, --distribution DISTRIBUTION
      -c CALLER_REFERENCE, --caller-reference CALLER_REFERENCE
                            Unique identifier for invalidation request, default
                            is a timestamp.
      -t, --track           Wait until the end of purge.
      -v, --verbose
