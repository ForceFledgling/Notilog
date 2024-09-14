# server/app/controllers/dept.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from app.core.crud import CRUDBase
from app.models.admin import Dept, DeptClosure
from app.schemas.depts import DeptCreate, DeptUpdate
from app.core.database import get_session  # Импортируйте функцию для получения сессии
from app.log import logger
from app.core.database import SessionLocal

class DeptController(CRUDBase[Dept, DeptCreate, DeptUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Dept, session=session)

    async def get_dept_tree(self, name: str = None):
        async with SessionLocal() as session:
            q = select(Dept).filter_by(is_deleted=False)
            if name:
                q = q.filter(Dept.name.contains(name))
            all_depts = await session.execute(q)
            all_depts = all_depts.scalars().all()

            # Вспомогательная функция для рекурсивного построения дерева департаментов
            def build_tree(parent_id):
                return [
                    {
                        "id": dept.id,
                        "name": dept.name,
                        "desc": dept.desc,
                        "order": dept.order,
                        "parent_id": dept.parent_id,
                        "children": build_tree(dept.id),  # Рекурсивное построение дочерних департаментов
                    }
                    for dept in all_depts
                    if dept.parent_id == parent_id
                ]

            # Начать построение дерева департаментов с корневого уровня (parent_id=0)
            dept_tree = build_tree(0)
            return dept_tree

    async def get_dept_info(self):
        # Реализуйте логику получения информации о департаменте
        pass

    async def update_dept_closure(self, obj: Dept):
        async with self.session() as session:
            parent_depts = await session.execute(
                select(DeptClosure).filter_by(descendant=obj.parent_id)
            )
            parent_depts = parent_depts.scalars().all()
            
            dept_closure_objs = []
            # Вставить родительские отношения
            for item in parent_depts:
                dept_closure_objs.append(DeptClosure(ancestor=item.ancestor, descendant=obj.id, level=item.level + 1))
            # Вставить собственные отношения
            dept_closure_objs.append(DeptClosure(ancestor=obj.id, descendant=obj.id, level=0))
            # Создать отношения
            session.add_all(dept_closure_objs)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                logger.error("Failed to update dept closure")

    async def create_dept(self, obj_in: DeptCreate):
        async with self.session() as session:
            async with session.begin():
                # Создание
                if obj_in.parent_id != 0:
                    await session.execute(select(Dept).filter_by(id=obj_in.parent_id).one())
                
                new_obj = Dept(**obj_in.dict())
                session.add(new_obj)
                await session.commit()
                await self.update_dept_closure(new_obj)

    async def update_dept(self, obj_in: DeptUpdate):
        async with self.session() as session:
            async with session.begin():
                dept_obj = await session.execute(select(Dept).filter_by(id=obj_in.id).one())
                dept_obj = dept_obj.scalar()
                
                # Обновление отношений департаментов
                if dept_obj.parent_id != obj_in.parent_id:
                    await session.execute(
                        select(DeptClosure).filter_by(ancestor=dept_obj.id).delete()
                    )
                    await session.execute(
                        select(DeptClosure).filter_by(descendant=dept_obj.id).delete()
                    )
                    await self.update_dept_closure(dept_obj)

                # Обновление информации о департаменте
                for key, value in obj_in.dict(exclude_unset=True).items():
                    setattr(dept_obj, key, value)
                await session.commit()

    async def delete_dept(self, dept_id: int):
        async with self.session() as session:
            async with session.begin():
                # Удаление департамента
                obj = await session.execute(select(Dept).filter_by(id=dept_id).one())
                obj = obj.scalar()
                obj.is_deleted = True
                session.add(obj)
                await session.commit()
                # Удаление отношений
                await session.execute(
                    select(DeptClosure).filter_by(descendant=dept_id).delete()
                )
                await session.commit()

# Получение сессии
session = get_session()  # Предположим, что у вас есть функция для получения сессии
dept_controller = DeptController(session=session)
