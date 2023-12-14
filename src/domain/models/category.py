class Category:
    def __init__(self, id: int) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f'Category(id={self.id})'
