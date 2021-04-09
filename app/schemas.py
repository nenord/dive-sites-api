from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class Site_in(BaseModel):
    name: str = Field(
        title="Site name: 3-32 characters", min_length=3, max_length=32
    )
    lat: float = Field(ge=-90, le=90, description="Latitide must be between -90 and 90")
    lon: float = Field(ge=-180, le=180, description="Longitude must be between -180 and 180")
    description: str = Field(
        title="The description of the site: 10-1024 characters", min_length=10, max_length=1024
    )
    depth: int = Field(ge=1, le=200, description="Depth in m, must be between 1 and 200")
    park_approach: Optional[str] = Field(
        "Not added yet", title="Parking and site approach", min_length=10, max_length=512
    )

class Site(Site_in):
    id: str = Field(alias='_id')
    #date_created: datetime
    #owner_id: str

class Update_site(BaseModel):
    name: Optional[str] = Field(
        title="Site name: 3-32 characters", min_length=3, max_length=32
    )
    description: Optional[str] = Field(
        title="The description of the site: 10-1024 characters", min_length=10, max_length=1024
    )
    depth: Optional[int] = Field(ge=1, le=200, description="Depth in m, must be between 1 and 200")
    park_approach: Optional[str] = Field(
        title="Parking and site approach", min_length=10, max_length=512
    )

class User(BaseModel):
    user_name: str = Field(
        title="User name: 3-32 characters", min_length=3, max_length=32
    )
    email: str = Field(
        title="User email: 8-32 characters", min_length=8, max_length=32
    )

class User_in(User):
    password: str = Field(
        title="User input passcode: 8-16 characters", min_length=8, max_length=16
    )

class User_out(User):
    id: str = Field(alias='_id')

class User_inDB(User):
    id: str = Field(alias='_id')
    active: bool
    password_hash: str
    #date_registered: datetime

class Update_user(BaseModel):
    user_name: Optional[str] = Field(
        title="User name: 3-32 characters", min_length=3, max_length=32
    )
    email: Optional[str] = Field(
        title="User email: 8-32 characters", min_length=8, max_length=32
    )
