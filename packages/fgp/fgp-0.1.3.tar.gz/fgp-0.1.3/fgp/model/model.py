from typing import List, Dict

class FGField:
    name: str = None
    type: str = None
    nullable: bool = None
    size: int = None

    def __init__(self, name: str, type: str, nullable: bool = None, size: int = None):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.size = size

    @classmethod
    def from_dict(cls, d) -> 'FGField':
        return cls(
            name=d.get('name'),
            type=d.get('type'),
            nullable=d.get('nullable', None),
            size=d.get('size', None)
        )


class FGModel:
    name: str = None
    fields: Dict[str, FGField] = None

    def __init__(self, name: str):
        self.name = name
        self.fields = dict()

    @classmethod
    def from_object(cls, name, fields: List[dict]) -> 'FGModel':
        m = cls(name=name)
        for f in fields:
            f_obj = FGField.from_dict(f)
            m.fields[f_obj.name] = f_obj
        return m
