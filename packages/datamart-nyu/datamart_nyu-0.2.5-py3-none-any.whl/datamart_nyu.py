"""Currently just redirects to datamart-rest.

Might be getting code later, running operations on the client-side.
"""

from datamart_rest import \
    RESTDatamart as NYUDatamart, \
    RESTSearchResult as NYUSearchResult, \
    RESTQueryCursor as NYUQueryCursor
import warnings


__version__ = '0.2.5'


class RESTDatamart(NYUDatamart):
    def __init__(self, *args, **kwargs):
        super(RESTDatamart, self).__init__(*args, **kwargs)

        warnings.warn(
            "datamart_nyu.RESTDatamart is deprecated, use either " +
            "datamart_rest.RESTDatamart (uses common API) or " +
            "datamart_nyu.NYUDatamart (uses NYU's materialization and " +
            "augmentation libraries)",
            FutureWarning,
        )


class RESTSearchResult(NYUSearchResult):
    def __init__(self, *args, **kwargs):
        super(RESTSearchResult, self).__init__(*args, **kwargs)

        warnings.warn(
            "datamart_nyu.RESTSearchResult is deprecated, use either " +
            "datamart_rest.RESTSearchResult (uses common API) or " +
            "datamart_nyu.NYUSearchResult (uses NYU's materialization and " +
            "augmentation libraries)",
            FutureWarning,
        )


__all__ = ['NYUDatamart', 'NYUSearchResult', 'NYUQueryCursor']
