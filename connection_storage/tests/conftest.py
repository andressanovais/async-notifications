import sys
from unittest.mock import MagicMock

import mock_redis_repository

sys.modules['repository.redis_keys'] = MagicMock()
sys.modules['repository.redis_repository'] = mock_redis_repository
sys.modules['secrets_manager'] = MagicMock()
