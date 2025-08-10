from app.dal.base_repository import BaseRepository
from app.dal.models.tags import Tags

class TagsRepository(BaseRepository):
    _table_name = "tags"
    _columns = [
        "id", "name"
    ]
    _columns_insertion = [
        "name"
    ]

    @classmethod
    def create_tags(cls, tags: Tags) -> bool:
        norm_data = {
            'name' : tags.name,
        }
        tag_id = cls.insert(table_name=cls._table_name, columns=cls._columns_insertion, data=norm_data)
        return tag_id

    @classmethod
    def find_tags_exists(cls, tag_name: str) -> bool :
        return cls.find_by_something(id=tag_name, something="name", what="id") != None
        