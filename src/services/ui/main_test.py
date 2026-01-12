import json
import pytest
from .main import api_create_account, api_create_diddoc, api_list_accounts, api_list_diddocs, api_select_account


@pytest.mark.asyncio
async def test_create_account():
    pytest.skip()
    res = await api_create_account()
    assert res.status_code == 201
    data = json.loads(res.body)
    assert data['status'] == "success"

@pytest.mark.asyncio
async def test_select_account():
    pytest.skip()
    res = await api_create_account()
    assert res.status_code == 201
    data = json.loads(res.body)
    acc1 = data['address']
    res = await api_create_account()
    data2 = json.loads(res.body)
    acc2 = data2['address']
    res = await api_select_account(acc2)
    assert res.status_code == 200
    res = await api_select_account(acc1)
    assert res.status_code == 200

@pytest.mark.asyncio 
async def test_create_diddoc():
    pytest.skip()
    res = await api_create_account()
    data2 = json.loads(res.body)
    acc2 = data2['address']
    res = await api_create_diddoc(
        "ghana","org",
        "aren", "US", "S",acc2,None,"1","0"
    )
    pass
def test_sign_diddoc():
    pass

@pytest.mark.asyncio 
async def test_list_diddoc():
    pytest.skip()
    res = await api_create_account()
    data2 = json.loads(res.body)
    acc2 = data2['address']
    res = await api_create_diddoc(
        "ghana","org",
        "aren", "US", "S",acc2,None,"1","0"
    )
    res = await api_select_account(acc2)
    assert res.status_code == 200
    res = await api_list_diddocs()
    d = json.loads(res.body)
    print(d)
    assert res == ""