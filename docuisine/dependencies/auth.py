from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

OAuth2_Scheme = OAuth2PasswordBearer(tokenUrl="token")


AuthToken = Annotated[str, Depends(OAuth2_Scheme)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]
