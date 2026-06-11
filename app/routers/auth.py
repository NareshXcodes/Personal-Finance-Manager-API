from fastapi import APIRouter , HTTPException , status , Response ,Depends
from app.db.deps import SessionDep
from app.schemas.User import UserCreate , UserResponse
from app.models.user import User
from app.utils.hashing import verify_password , hash_password 
from app.utils.jwt import create_access_token , verify_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils.oauth2 import get_current_user
from app.schemas.User import TokenResponse

router = APIRouter(prefix="/auth" ,tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(db:SessionDep,user_credential : OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="Invalid Crediantial")

    if not verify_password(user_credential.password,user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="Invalid Crediantial")

    access_token = create_access_token(data = {"sub": user.email})

    return {"access_token" : access_token , "token_type" : "bearer"}
    

    

@router.post("/register", response_model=UserResponse, status_code = status.HTTP_201_CREATED)
def register(db:SessionDep , new_user : UserCreate):
    existing_user = db.query(User).filter(User.email == new_user.email).first()

    if existing_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail="Email already taken")

    new_user.password = hash_password(new_user.password)
    user = User(**new_user.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me",response_model=UserResponse)
def current_logged_in_status(current_user : User = Depends(get_current_user)):
    return current_user



