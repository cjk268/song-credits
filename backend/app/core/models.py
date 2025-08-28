from pydantic import BaseModel

class RoleModel(BaseModel):
    title: str


class ContributorModel(BaseModel):
    id: int
    name: str
    uri: str
    image_uri: str


class CreditModel(BaseModel):
    role: RoleModel
    contributor: ContributorModel
    
    
class TrackModel(BaseModel):
    id: str
    name: str
