# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:50:54 2022

@author: HassaM3
"""
from pydantic import BaseModel
from typing import Union

class Agro(BaseModel):
    date_year: int
    agro_srfc: float
    cereal_land: float
    cereal_yield: float
    country_code: str
    region_code: str
    class Config:
        orm_mode = True
        
class Country(BaseModel):
    name: str
    isocode: str
    class Config:
        orm_mode = True
        
class CountriesWithRegions(BaseModel):
    country: str
    countryisocode: str
    region: str
    regioniscode: str
    
    class Config:
        orm_mode = True

class AgroData(BaseModel):
    date_year: int
    class Config:
        orm_mode = True

class AgroSurface(AgroData):
    agro_srfc: Union[float, None]

class CerealYield(AgroData):
    cereal_yield: Union[float, None]

class CerealLand(AgroData):
    cereal_land: Union[float, None]
    
class AgroCerealYieldLand(BaseModel):
    date_year: int
    cereal_land: Union[float, None]
    cereal_yield: Union[float, None]
    
    class Config:
        orm_mode = True
        
class AgroCerealYieldLandAll(AgroCerealYieldLand):
    country: str
    #country_code: str
    region: str
    region_code:str
    agro_srfc: Union[float, None]
    
class CerealYielLandBar(BaseModel):
    value: Union[float, None]
    data_type: str
    area: str
