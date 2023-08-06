import pytest
from bocks_ds import Client, DSQueryError, DSTargetError

client = Client("starfinder")


class TestNested:
    def test_get(self):
        query = [
            "name",
            {
                "effect_ranges": ["name", "description"],
            }
        ]

        all_spells = client.spells.get(query)
        assert all_spells.status_code == 200
        assert type(all_spells.json()) is dict

        all_list = all_spells.json()['data']['spells']
        assert type(all_list) is list
        assert len(all_list) > 20
        assert all_list[0]['name']
        assert all_list[0]['effect_ranges']

class TestNestedExceptions:
    def test_fields_list(self):
        query = "Not a list"
        with pytest.raises(TypeError) as error:
            client.spells.get(query)
            assert error.status_code == 400
            assert error.errors >= 1

    def test_fields_dict(self):
        query = ['name', ['not', 'a', 'dict']]
        with pytest.raises(TypeError) as error:
            client.spells.get(query)
            assert error.status_code == 400
            assert error.errors >= 1
