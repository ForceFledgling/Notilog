from pydantic import BaseModel, Field


class BaseDept(BaseModel):
    name: str = Field(..., description="Название отдела", example="Центр исследований и разработок")  # Описание: Название отдела
    desc: str = Field("", description="Примечание", example="Центр исследований и разработок")  # Описание: Примечание
    order: int = Field(0, description="Порядок")  # Описание: Порядок
    parent_id: int = Field(0, description="ID родительского отдела")  # Описание: ID родительского отдела


class DeptCreate(BaseDept):
    ...


class DeptUpdate(BaseDept):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})  # Исключаем ID при обновлении
