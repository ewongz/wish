


def test_load_data(default_wish):
    item_pool, item_data = default_wish.load_data("tests/test_data")
    assert len(item_pool.keys()) == 3
    assert len(item_pool[4]) == 4
    assert "Sword" in item_pool[3]
    assert item_data["Genshin"]["item_type"] == "characters"

def test_apply_pity(soft_pity_wish):
    soft_pity_wish.apply_pity()
    assert soft_pity_wish.item_probabilities[5] == 0.006 + (1 - 0.006)/(89 - 74)

def test_standard_banner_available_item(standard_banner_wish):
    assert standard_banner_wish.check_available_item("Chongyun") is True


