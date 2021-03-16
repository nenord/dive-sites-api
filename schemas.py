from typing import Optional
from pydantic import BaseModel, Field

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

    class Config:
        orm_mode = True

class Site(Site_in):
    id: int
    slug: str = Field(
        title="Url safe site name: 3-32 characters", min_length=3, max_length=32
    )

    class Config:
        orm_mode = True
