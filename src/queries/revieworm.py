from fastapi import HTTPException
from sqlalchemy import  select
from sqlalchemy.exc import IntegrityError
from database import session_factory
from models import Review, User
from schemas.review_schemas import ReviewDTO, ReviewAddDTO


class ReviewORM:
    @staticmethod
    async def insert_review(review_data: ReviewAddDTO):
        async with session_factory() as session:
            try:
                review = Review(
                    author_id=review_data.author_id,
                    university_id=review_data.university_id,
                    text=review_data.text,
                    rating=review_data.rating,
                )

                session.add(review)

                await session.commit()
                return "Отзыв добавлен"
            except IntegrityError:
                await session.rollback()
                return "ti tupoi retern"

    @staticmethod
    async def get_review(review_id: int) -> ReviewDTO:
        async with session_factory() as session:
            review = await session.get_one(Review, review_id)
            if not review:
                raise HTTPException(status_code=404, detail="Такого oтзыва нет")

        return ReviewDTO.model_validate(review)

    @staticmethod
    async def get_all_user_reviews(user_id: int) -> list[ReviewDTO]:
        async with session_factory() as session:
            query = select(Review).filter(Review.author_id == user_id)
            reviews = await session.execute(query)
            if not reviews:
                raise HTTPException(status_code=404, detail="У пользователя нет отзывов")
            return [ReviewDTO.model_validate(_) for _ in reviews]

    @staticmethod
    async def get_all_university_reviews(university_id: int) -> list[ReviewDTO]:
        async with session_factory() as session:
            query = select(Review).filter(Review.university_id == university_id)
            reviews = await session.execute(query)
            if not reviews:
                raise HTTPException(status_code=404, detail="У университета нет отзывов")
            return [ReviewDTO.model_validate(_) for _ in reviews]

    @staticmethod
    async def delete_review(review_id: int):
        async with session_factory() as session:
            review = await session.get_one(Review, review_id)
            await session.delete(review)
            await session.commit()
            if not review:
                raise HTTPException(status_code=404, detail="Такого отзыва нет")
            return "Отзыв удалён"

    @staticmethod
    async def change_review(review_id: int, review_data: ReviewAddDTO):
        async with session_factory() as session:
            review = await session.get_one(Review, review_id)
            if not review:
                raise HTTPException(status_code=404, detail="Такого отзыва нет")
            review.author_id = review_data.author_id
            review.university_id = review_data.university_id
            review.text = review_data.text
            review.rating = review_data.rating

            await session.commit()

            if review is None:
                raise HTTPException(status_code=404, detail="review not found(((")
            return "Отзыв изменён"
    
    @staticmethod
    async def review_belonging(review_id: int, user_id: int):
        async with session_factory() as session:
            review = await session.get_one(Review, review_id)
            if not review:
                raise HTTPException(status_code=404, detail="Такого отзыва нет")
            query = select(Review).filter(Review.author_id == user_id)
            user_reviews = await session.execute(query)
            if any([_ for _ in user_reviews if _==review]):
                return True
            else:
                return False
