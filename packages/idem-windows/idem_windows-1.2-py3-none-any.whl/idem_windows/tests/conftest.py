import pop.hub
import pytest
import sys
import unittest.mock as mock


@pytest.fixture(scope="session")
def hub():
    """
    provides a full hub that is used as a reference for mock_hub
    """
    hub = pop.hub.Hub()

    # strip pytest args
    with mock.patch.object(sys, "argv", sys.argv[:1]):
pass

    return hub
