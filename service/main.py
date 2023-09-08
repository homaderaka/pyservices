from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from middleware import JSONMiddleware
import uvicorn
import repo
from dbconfig import DBConfig


class UserHandler:
    def __init__(self, app, repo: repo.Repository):
        self.app = app
        self.repo = repo


# Define a Pydantic model for user credentials
class UserCredentials(BaseModel):
    username: str
    password: str


# Create a FastAPI app instance
app = FastAPI()
app.add_middleware(JSONMiddleware)

db_config = DBConfig()

# Create an instance of the 'Repository' class from the 'repo' module
userRepo = repo.Repository(db_config)

# Create an instance of the 'UserHandler' class, passing the app and the repository instance
uh = UserHandler(app, userRepo)


# Define a route to create a new user
@app.post("/user/create")
def create_user(user_data: UserCredentials):
    userRepo.create_user(user_data)
    return {"message": "User created successfully"}

# Define a route to get users
@app.get("/user/get/all")
def get_user_by_username():
    users, err = userRepo.get_users()
    if err is not None:
        raise HTTPException(status_code=500, detail=err)
    return users


# Define a route to get user information by username
@app.get("/user/get/id/{id}")
def get_user_by_id(id: str):
    user, err = userRepo.get_user_by_id(id)
    if err is not None:
        print('failed to get_user_by_username:', str(err))
        if type(err) is repo.EntityNotFound:
            raise HTTPException(status_code=404, detail=str(err))
        raise HTTPException(status_code=500)
    return user


# Define a route to get user information by username
@app.get("/user/get/username/{username}")
def get_user_by_username(username: str):
    user, err = userRepo.get_user_by_username(username)
    if err is not None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Define a route to update user information by username
@app.put("/user/update/{username}")
def update_user(username: str, updated_user_data: UserCredentials):
    # TODO: add update check
    user = {'username': username, 'password': updated_user_data.password}
    userRepo.update_user(user)
    return {"message": "User updated successfully"}


# Define a route to delete a user by username
@app.delete("/user/delete/id/{id}")
def delete_user(id: str):
    # TODO: add deletion check
    userRepo.delete_user(id)
    return {"message": "User deleted successfully"}


# Define a route to authenticate a user
@app.post("/user/auth")
def auth_user(credentials: UserCredentials):
    ok = userRepo.auth_user(credentials)
    if not ok:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"message": "User is authenticated"}


# Run the FastAPI app using uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
