MoWAKi - Python utilities
#########################

This package provides several common utilities for MoWAKi_ apps.

.. _MoWAKi: https://www.mowaki.org


Storage
=======

Provides a common abstraction for file storage.

Currently supports storing data in:

- memory (mostly for testing)
- local filesystem (mostly for local development)
- s3 buckets


Config
======

Convenience functions for loading configuration from environment variables:


.. code-block:: python

    import os
    from mowaki.config import Config


    class AppConfig(Config):
        SECRET_KEY: str
        DATABASE_URL: str
        ENABLE_FEATURE_1: bool = False


    cfg = AppConfig(os.environ)

    # Access loaded configuration
    cfg.SECRET_KEY
