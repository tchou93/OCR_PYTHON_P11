import pytest
import server
from server import app
from tests.global_var import simu_clubs, simu_competitions, simu_dict_clubs_purchase


# Configure Client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Configure DataBase
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
    mocker.patch.object(server, "dict_clubs_purchase", simu_dict_clubs_purchase)


@pytest.fixture
def new_old_competitions_mocker(mocker):
    competitions_old = [simu_competitions[0], simu_competitions[1]]
    competitions_new = [simu_competitions[2]]
    books_ko = []
    books_ok = [simu_competitions[2]]

    mocker.patch('server.get_possibility_to_book', return_value=(books_ko, books_ok))
    mocker.patch.object(server, "competitions_old", competitions_old)
    mocker.patch.object(server, "competitions_new", competitions_new)


@pytest.fixture
def only_new_competitions_mocker(mocker):
    competitions_old = []
    competitions_new = [simu_competitions[2]]
    books_ko = []
    books_ok = [simu_competitions[2]]
    mocker.patch('server.get_possibility_to_book', return_value=(books_ko, books_ok))
    mocker.patch.object(server, "competitions_old", competitions_old)
    mocker.patch.object(server, "competitions_new", competitions_new)


@pytest.fixture
def only_old_competitions_mocker(mocker):
    competitions_old = [simu_competitions[0], simu_competitions[1]]
    competitions_new = []
    books_ko = []
    books_ok = []

    mocker.patch('server.get_possibility_to_book', return_value=(books_ko, books_ok))
    mocker.patch.object(server, "competitions_old", competitions_old)
    mocker.patch.object(server, "competitions_new", competitions_new)
