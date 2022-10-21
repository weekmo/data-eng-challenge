# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:34:20 2022

@author: weekm
"""
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from utils import crud, schemas, database
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

errore_message = "Couldn't retrieve data, please try again later."
@app.get("/", response_class=RedirectResponse)
async def index():
    return "/docs"


@app.get("/countries", response_model=List[schemas.Country])
async def get_all_countries(db: Session = Depends(get_db)):
    """Returns all the countries in a given region, as a list"""
    countries = await crud.get_all_countries(db)
    if countries == None:
        raise HTTPException(status_code=500, detail=errore_message)
    return countries


@app.get("/countries/{region}", response_model=List[schemas.Country])
async def get_countries(region:str, db: Session = Depends(get_db)):
    """Returns all the countries in a given region, as a list"""
    countries = await crud.get_countries(db, region)
    if countries == None:
        raise HTTPException(status_code=500, detail=errore_message)
    return countries
    
@app.get("/countrieswithcode", response_model=List[schemas.CountriesWithRegions])
async def get_all_countries_with_code(db: Session = Depends(get_db)):
    countries = await crud.get_all_countries_with_region(db)
    if countries == None:
        raise HTTPException(status_code=500, detail=errore_message)
    return countries

@app.get("/agro-surface/{country}", response_model=List[schemas.AgroSurface])
async def get_agro_land_srfc_all_years(country:str, db: Session = Depends(get_db)):
    """Returns a country’s agricultural land surface (in sq. km)..."""
    return await crud.get_agro_srfc(db, country)

@app.get("/agro-surface/{country}/{year}")
async def get_agro_land_srfc(country:str, year:int, db: Session = Depends(get_db)):
    """Returns a country’s agricultural land surface (in sq. km) for a given
    year, as a float."""
    return await crud.get_agro_surface_year(db, country, year)

@app.get("/cereal-yield/{country}", response_model=List[schemas.CerealYield])
async def get_cereal_yield_all_years(country:str, db: Session = Depends(get_db)):
    """Returns list of all available years..."""
    return await crud.get_cereal_yield(db, country)

@app.get("/cereal-yield/{country}/{year}")
async def get_cereal_yield(country, year:int, db: Session = Depends(get_db)):
    """Returns the cereal yield of a country for a given year (in kg/hectare, as
    an integer."""
    return await crud.get_cereal_yield_year(db, country, year)

@app.get("/cereal-land/{country}",  response_model=List[schemas.CerealLand])
async def get_cereal_land_all_years(country:str, db: Session = Depends(get_db)):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    return await crud.get_cereal_land(db, country)
    
@app.get("/cereal-land/{country}/{year}")
async def get_cereal_land(country, year:int, db: Session = Depends(get_db)):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    return await crud.get_cereal_land_year(db, country, year)


""" Scatter """
@app.get("/cereal-land-yield", response_model=List[schemas.AgroCerealYieldLandAll])
async def get_cereal_land_yield(db: Session = Depends(get_db)):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    return await crud.get_cereal_yiel_land_all(db)


@app.get("/cereal-land-yield/{country}",  response_model=List[schemas.AgroCerealYieldLand])
async def get_cereal_land_yield_all(country:str, db: Session = Depends(get_db)):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    return await crud.get_cereal_yiel_land(db, country)

# Stack Bar
@app.get("/cereal-land-yield-bar/{year}", response_model=List[schemas.CerealYielLandBar])
async def get_cereal_land_yield_bar_reg(year:int, db: Session = Depends(get_db)):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    return await crud.get_cereal_yiel_land_for_bar_reg(db, year)

@app.get("/cereal-land-yield-bar/{reg_code}/{year}", response_model=List[schemas.CerealYielLandBar])
async def get_cereal_land_yield_bar(reg_code:str, year:int, db: Session = Depends(get_db)):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    return await crud.get_cereal_yiel_land_for_bar(db, reg_code, year)