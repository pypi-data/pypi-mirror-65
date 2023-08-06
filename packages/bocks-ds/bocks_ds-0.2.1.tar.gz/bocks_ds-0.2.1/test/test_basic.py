import pytest
from bocks_ds import Client, DSQueryError, DSTargetError

client = Client("starfinder")

class TestBasic:

    def test_get(self):
        all_armor = client.armor.get(['name', 'price'])
        assert all_armor.status_code == 200
        assert type(all_armor.json()) is dict

        all_list = all_armor.json()['data']['armor']
        assert type(all_list) is list
        assert len(all_list) > 20
        assert all_list[0]['name']
        assert all_list[0]['price']

    def test_set_arguments(self):
        client.armor.set_arguments({"name_like":"basic"})
        client.armor.set_arguments({"price_min":200, "price_max":2000})
        limited_armor = client.armor.get(['name', 'price'])
        assert limited_armor.status_code == 200
        assert type(limited_armor.json()) is dict

        limited_list = limited_armor.json()['data']['armor']
        assert type(limited_list) is list
        assert len(limited_list) < 20
        assert limited_list[0]['name']
        assert limited_list[0]['price'] >= 200
        assert limited_list[-1]['price'] <= 2000

class TestBasicExceptions:
    def test_client_exception(self):
        with pytest.raises(DSTargetError) as error:
            Client("does_not_exist")
            assert error.status_code == 400
            assert error.errors >= 1


    def test_get_exception(self):
        with pytest.raises(DSQueryError) as error:
            client.armor.set_arguments({"name_min":200, "name_max":2000})
            client.armor.get(['name', 'price'])
            assert error.status_code == 400
            assert error.errors >= 1
