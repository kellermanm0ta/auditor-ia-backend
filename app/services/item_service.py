from app.schemas.item import ItemCreate, ItemResponse


class ItemService:
    def __init__(self):
        self._items: dict[int, ItemResponse] = {}
        self._counter = 0

    def create(self, data: ItemCreate) -> ItemResponse:
        self._counter += 1
        item = ItemResponse(id=self._counter, **data.model_dump())
        self._items[item.id] = item
        return item

    def list_all(self) -> list[ItemResponse]:
        return list(self._items.values())

    def get(self, item_id: int) -> ItemResponse | None:
        return self._items.get(item_id)
