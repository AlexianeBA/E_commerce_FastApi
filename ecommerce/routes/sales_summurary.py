from fastapi import APIRouter, Depends, HTTPException, status

from routes.auth import get_current_user

router = APIRouter()


async def get_current_active_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )
    return current_user


@router.get("sales_summary", dependencies=[Depends(get_current_active_admin)])
async def sales_summary():
    pass
