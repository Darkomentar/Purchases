import pytest

from app.Holders.dao import HoldersDAO


@pytest.mark.parametrize("id,is_present", [(1, True), (2, True), (3324, False)])
async def test_find_holders_by_id(id, is_present):
    holder = await HoldersDAO.find_by_id(id)
    if is_present:
        assert holder.id == id
    else:
        assert not holder
    print(holder)
