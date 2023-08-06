"""
Gitlab Pipelines helper libs
"""

from navio.gitlab._gitlab import Gitlab

import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)

__all__ = [
    'Gitlab',
]
