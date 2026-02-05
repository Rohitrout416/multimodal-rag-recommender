from fastapi import APIRouter, Depends, HTTPException, status
from src.models.user import UserCreate, UserLogin, Token, UserResponse
from src.core.security import get_password_hash, verify_password, create_access_token
from src.db.mongodb import get_database

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_in: UserCreate, db = Depends(get_database)):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_in.password)
    
    # Create user
    user_data = {
        "email": user_in.email,
        "username": user_in.username,
        "password": hashed_password,
        "created_at": "now", # TODO: Use datetime
        "preferences": {}
    }
    
    result = await db.users.insert_one(user_data)
    
    # Create token
    access_token = create_access_token(subject=user_in.email)
    
    # Return user + token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(result.inserted_id),
            "email": user_in.email,
            "username": user_in.username,
            "preferences": {}
        }
    }

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db = Depends(get_database)):
    user = await db.users.find_one({"email": login_data.email})
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(subject=user["email"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "username": user["username"],
            "preferences": user.get("preferences", {})
        }
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends("src.api.deps.get_current_user")):
    return current_user
