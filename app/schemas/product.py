from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime

class ProductBase(BaseModel):
    name:str =Field(...,min_length=1,max_length=100)
    description:str | None = Field(default=None,max_length=500)
    price:float =Field(gt=0)
    stock:int = Field(default=0,ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):

    name:str =Field(default=None,min_length=1,max_length=100)
    description:str | None = Field(default=None,max_length=500)
    price:float =Field(default=None,gt=0)
    stock:int = Field(default=None,ge=0)

class ProductRead(ProductBase):
    id:int
    created_at:datetime
    updated_at:datetime
    

    model_config = ConfigDict(from_attributes=True)    