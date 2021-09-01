import pytest
import sys
sys.path.insert(0,"./src")
from src import main


@pytest.fixture(scope="module")
def default_wish():
    return main.Wish("tests/test_data")

@pytest.fixture(scope="module")
def soft_pity_wish():
    wish = main.Wish("tests/test_data")
    wish.five_star_pity_counter = 74
    return wish

@pytest.fixture(scope="module")
def standard_banner_wish():
    wish = main.StandardBanner(data_path="tests/test_data")
    return wish