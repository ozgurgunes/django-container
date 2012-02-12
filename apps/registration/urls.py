"""
Backwards-compatible URLconf for existing django-registration
installs; this allows the standard ``include('apps.registration.urls')`` to
continue working, but that usage is deprecated and will be removed for
django-registration 1.0. For new installs, use
``include('apps.registration.backends.default.urls')``.

"""

import warnings

warnings.warn("include('apps.registration.urls') is deprecated; use include('apps.registration.backends.default.urls') instead.",
              PendingDeprecationWarning)

from apps.registration.backends.default.urls import *
