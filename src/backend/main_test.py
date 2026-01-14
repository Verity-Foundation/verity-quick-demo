import random
import pytest
from src.core.exceptions import VerityValidationError
from . import VerityDemo

def test_is_data_valid_validation_error():
    v = VerityDemo()
    with pytest.raises(VerityValidationError, match="cannot be empty"):
        v.is_data_valid("", "data")
    with pytest.raises(VerityValidationError, match="must not be None"):
        v.is_data_valid(None, "data")
    
def test_list_accounts_empty():
    v = VerityDemo()
    addr, diddoc = v.list_account()
    assert addr == None and diddoc == None

def test_list_accounts():
    v = VerityDemo()
    for _ in range(5):
        v.create_account()
    addr, diddoc = v.list_account()
    assert addr != None and diddoc == {}
    assert len(addr) == 5

def test_select_account_by_index_error():
    v = VerityDemo()
    for _ in range(2):
        v.create_account()
    with pytest.raises(VerityValidationError, match="idx can't be None"):
        v.select_account_by_index(None)
    with pytest.raises(VerityValidationError, match="idx must be an integer"):
        v.select_account_by_index("123")
    selected = v.select_account_by_index(3)
    assert not selected

def test_select_account_by_index():
    v = VerityDemo()
    addr = []
    pass_thresold= 25
    passed = 0
    for _ in range(15):
        t = v.create_account()
        addr.append(t)
    while True:
        n = random.randrange(1, 15)
        selected = v.select_account_by_index(n)
        assert selected
        assert addr[n-1] == v.curr_account()
        passed = passed+1
        if passed == pass_thresold:
            break

def test_select_account():
    v = VerityDemo()
    addr = []
    pass_thresold= 25
    passed = 0
    for _ in range(15):
        t = v.create_account()
        addr.append(t)
    while True:
        n = random.randrange(0, 15)
        selected = v.select_account(addr[n])
        assert selected
        assert addr[n] == v.curr_account()
        passed = passed+1
        if passed == pass_thresold:
            break

