from bot import GrotemServerConnector
import settings


def test_check_connection():
    grotem_bot = GrotemServerConnector()
    res = grotem_bot.check_connection()
    assert res


def test_get_lic_info():
    grotem_bot = GrotemServerConnector()
    res = grotem_bot.get_lic_info('')
    # assert type(res) == dict
    assert res
    assert grotem_bot.error_code == 0
    assert grotem_bot.error_description == ''
    assert type(grotem_bot.data) == dict
    assert 'TotalLicenses' in grotem_bot.data
    print(grotem_bot.data)


def test_set_lic_count():
    grotem_bot = GrotemServerConnector()
    res = grotem_bot.set_lic_count(solution_name='', lic_count=1000)
    assert res
    assert grotem_bot.error_code == 0
    assert grotem_bot.error_description == ''
    assert grotem_bot.data == 'ok'


def test_reset_lic_count():
    grotem_bot = GrotemServerConnector()
    res = grotem_bot.reset_lic_count(solution_name='')
    assert res
    assert grotem_bot.error_code == 0
    assert grotem_bot.error_description == ''
    assert grotem_bot.data == 'ok'


def test_load_settings_file():
    result = settings._load_settings_file()
    assert type(result) == dict


def test_load_env_settings():
    result = settings._load_env_settings()
    assert type(result) == dict


def test_get_settings():
    result = settings.get_settings()
    assert type(result) == dict
