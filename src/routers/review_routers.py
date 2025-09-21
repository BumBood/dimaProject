from fastapi import APIRouter
from schemas.review_schemas import ReviewAddDTO
from queries.revieworm import ReviewORM

router_reviews = APIRouter()


@router_reviews.post("/reviews", tags=["Reviews"], summary="Создание нового отзыва")
async def post_new_review(rev_data: ReviewAddDTO, authorization: str = Header(None)):
    rev_data.author_id = await Auth.get_user_id(authorization)
    await ReviewORM.insert_review(rev_data)
    return {"ok": True, "message": "Review added successfully"}


@router_reviews.get(
    "/reviews/{id}", tags=["Reviews"], summary="Получение инфы об отзыве"
)
async def get_review(rev_id: int):
    rev_data = await ReviewORM.get_review(rev_id)
    return rev_data


@router_reviews.get(
    "/reviews/{user_id}",
    tags=["Reviews"],
    summary="Получение инфы об отзывах пользователя",
)
async def get_user_reviews(user_id: int):
    rev_data = await ReviewORM.get_all_user_reviews(user_id)
    return rev_data


@router_reviews.get(
    "/reviews/{uni_id}",
    tags=["Reviews"],
    summary="Получение инфы об отзывах университета",
)
async def get_university_reviews(uni_id: int):
    rev_data = await ReviewORM.get_all_university_reviews(uni_id)
    return rev_data


@router_reviews.delete("/reviews", tags=["Reviews"], summary="Удаление отзыва")
async def delete_review(review_id: int, authorization: str = Header(None)):
    user_id = await Auth.get_user_id(authorization)
    if ReviewORM.review_belonging(review_id, user_id):
        await ReviewORM.delete_review(review_id)
        return {"ok": True, "message": "Review deleted successfully"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@router_reviews.put("/reviews", tags=["Reviews"], summary="Изменение отзыва")
async def update_review(review_id: int, review_data: ReviewAddDTO, authorization: str = Header(None)):
    user_id = await Auth.get_user_id(authorization)
    if ReviewORM.review_belonging(review_id, user_id):
        await ReviewORM.change_review(review_id, review_data)
        return {"ok": True, "message": "Review updated successfully"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
