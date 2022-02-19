import pytest


# set the prefix for all the routes being tested
@pytest.fixture(scope='module')
def app_client(base_app_client):
    base_app_client.base_url += "/pokemon/"
    yield base_app_client


def test_get_pokemon_by_name(app_client):
    pokemon_name = "mewtwo"
    response  = app_client.get(f"{pokemon_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Pokemon name is {pokemon_name}"}


def test_get_pokemon_by_name_translated(app_client):
    pokemon_name = "mewtwo"
    response  = app_client.get(f"translated/{pokemon_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Pokemon name is {pokemon_name}"}