import pytest
import server
from server import app
from tests.global_var import simu_clubs, simu_competitions

########### Configure Client ###########
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

########### Configure DataBase ###########
@pytest.fixture
def competitions_test():
    return simu_competitions

@pytest.fixture
def clubs_test():
    return simu_clubs

@pytest.fixture
def data_base_mocker(mocker):
    mocker.patch.object(server, "clubs", simu_clubs)
    mocker.patch.object(server, "competitions", simu_competitions)
