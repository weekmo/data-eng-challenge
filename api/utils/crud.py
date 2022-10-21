# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 07:32:52 2022

@author: HassaM3
"""

from sqlalchemy.orm import Session

from utils import models, schemas

sql_template = """
SELECT {indicator},date_year
from tb_agro agro
INNER JOIN tb_countries ctr on ctr.id = agro.country_id
where ctr.isocode = upper(:isocode)
"""


def get_regions(db: Session):
    return db.query(models.Region).all()

def get_region(db:Session, reg_isocode:str):
    return db.query(models.Region).filter(models.Region.isocode==reg_isocode).first()


async def get_countries(db: Session, reg_isocode:str):
    reg = get_region(db,reg_isocode)
    return reg.countries

def get_country(db:Session, country_isocode:str):
    return db.query(models.Country).filter(models.Country.isocode==country_isocode).first()

""" For scatter plot per country"""
async def get_cereal_yiel_land(db:Session, country_code:str):
    sql_qury = """
    select ag.cereal_land, ag.cereal_yield, ag.date_year
    from tb_agro ag
    INNER join tb_countries ct on ct.id=ag.country_id
    WHERE ct.isocode = upper(:countrycode)
    """
    result = []
    for row in db.execute(sql_qury, {"countrycode":country_code}):
        result.append(schemas.AgroCerealYieldLand(
            date_year=row["date_year"],
            cereal_yield = row["cereal_yield"],
            cereal_land = row["cereal_land"]
            ))
    return result

""" For scatter plot all countries"""
async def get_cereal_yiel_land_all(db:Session):
    sql_qury = """
    select ag.cereal_land, ag.cereal_yield, ag.agro_srfc, ag.date_year,
    ct.name country_name,ct.isocode country_code, reg.name region_name, reg.isocode region_code
    from tb_agro ag
    INNER join tb_countries ct on ct.id=ag.country_id
    INNER JOIN tb_regions reg on reg.id = ct.region_id
    """
    result = []
    for row in db.execute(sql_qury):
        result.append(schemas.AgroCerealYieldLandAll(
            date_year=row["date_year"],
            cereal_yield = row["cereal_yield"],
            cereal_land = row["cereal_land"],
            country = row["country_name"],
            region = row["region_name"],
            region_code = row["region_code"],
            country_code = row["country_code"],
            agro_srfc = row["agro_srfc"]
            ))
    return result

async def get_cereal_yiel_land_for_bar(db:Session, reg_code:str, year:int):
    sql_qury = """
    select 
    sum(ag.agro_srfc) data_value, 
    "Agricultural Land Surface" data_type, 
    ct.name area
    from tb_agro ag
    INNER join tb_countries ct on ct.id=ag.country_id
    INNER JOIN tb_regions reg on reg.id = ct.region_id
    where ag.date_year = :year and reg.isocode = :reg_code
    group by ct.name
    UNION
    select 
    sum(ag.cereal_land) data_value, 
    "Cereal Land" data_type, 
    ct.name area
    from tb_agro ag
    INNER join tb_countries ct on ct.id=ag.country_id
    INNER JOIN tb_regions reg on reg.id = ct.region_id
    where ag.date_year = :year and reg.isocode = :reg_code
    group by ct.name
    """
    result = []
    for row in db.execute(sql_qury, {"reg_code":reg_code, "year":year}):
        result.append(schemas.CerealYielLandBar(
            value = row["data_value"],
            data_type = row["data_type"],
            area = row["area"]
            ))
    return result

async def get_cereal_yiel_land_for_bar_reg(db:Session, year:int):
    sql_qury = """
    select 
    sum(ag.agro_srfc) data_value, 
    "Agricultural Land Surface" data_type, 
    reg.name area
    from tb_agro ag
    INNER join tb_countries ct on ct.id=ag.country_id
    INNER JOIN tb_regions reg on reg.id = ct.region_id
    where ag.date_year = :year
    group by reg.name
    UNION
    select 
    sum(ag.cereal_land) data_value, 
    "Cereal Land" data_type, 
    reg.name area
    from tb_agro ag
    INNER join tb_countries ct on ct.id=ag.country_id
    INNER JOIN tb_regions reg on reg.id = ct.region_id
    where ag.date_year = :year
    group by reg.name
    """
    result = []
    for row in db.execute(sql_qury, {"year":year}):
        result.append(schemas.CerealYielLandBar(
            value = row["data_value"],
            data_type = row["data_type"],
            area = row["area"]
            ))
    return result

async def get_all_countries(db: Session):
    return db.query(models.Country).all()

async def get_all_countries_with_region(db: Session):
    sql_qury = """
    SELECT ctr.name country, ctr.isocode countryisocode, reg.name region, reg.isocode regioniscode
    from tb_countries ctr
    inner join tb_regions reg on reg.id = ctr.region_id
    """
    result = []
    for row in db.execute(sql_qury):
        result.append(schemas.CountriesWithRegions(
            country=row["country"],
            countryisocode = row["countryisocode"],
            region = row["region"],
            regioniscode = row["regioniscode"]
            ))
    return result

async def get_agro_srfc(db: Session, country_code:str):
    result = []
    for row in db.execute(sql_template.format(indicator="agro_srfc"), {"isocode":country_code}):
        result.append(schemas.AgroSurface(
            date_year=row["date_year"],
            agro_srfc = row["agro_srfc"]
            ))
    return result

async def get_agro_surface_year(db: Session, country_code:str, date_year: int):
    result = db.execute(sql_template.format(indicator="agro_srfc")+" and agro.date_year = :year", {"isocode":country_code, "year":date_year}).scalar()
    return result

async def get_cereal_yield(db: Session, country_code:str):
    result = []
    for row in db.execute(sql_template.format(indicator="cereal_yield"), {"isocode":country_code}):
        result.append(schemas.CerealYield(
            date_year=row["date_year"],
            cereal_yield = row["cereal_yield"]
            ))
    return result

async def get_cereal_yield_year(db: Session, country_code:str, date_year: int):
    result = db.execute(sql_template.format(indicator="cereal_yield")+" and agro.date_year = :year", {"isocode":country_code, "year":date_year}).scalar()
    return result

async def get_cereal_land(db: Session, country_code:str):
    result = []
    for row in db.execute(sql_template.format(indicator="cereal_land"), {"isocode":country_code}):
        result.append(schemas.CerealLand(
            date_year=row["date_year"],
            cereal_land = row["cereal_land"]
            ))
    return result

async def get_cereal_land_year(db: Session, country_code:str, date_year: int):
    result = db.execute(sql_template.format(indicator="cereal_land")+" and agro.date_year = :year", {"isocode":country_code, "year":date_year}).scalar()
    return result

def get_region_data(db:Session, reg_isocode:str,sart_year=None, end_year=None):
    if sart_year == None and end_year == None:
        reg = get_region(db,reg_isocode)
        return reg.countries.agros
    return 

def get_country_data(db:Session, country_isocode:str,sart_year=None, end_year=None):
    return 

def get_data_by_date(sart_year=None, end_year=None):
    return 

def add_agro_data(db: Session, date_year:int, agro_srfc:float, cereal_land:float, cereal_yield:float, count_isocode:str):
    agro_data = models.Agro(
        date_year = date_year,
        agro_srfc = agro_srfc,
        cereal_land = cereal_land,
        cereal_yield = cereal_yield
        )
    country = db.query(models.Country).filter(models.Country.isocode== count_isocode).first()
    if country:
        country.agros.append(agro_data)
        db.add(country)
        db.commit()
        db.refresh(agro_data)
        return agro_data
    return None

def add_country(db: Session, name:str, country_isocode:str, reg_isocode:str):
    country = models.Country(
        name = name,
        isocode = country_isocode
        )
    region = db.query(models.Region).filter(models.Region.isocode == reg_isocode).first()
    if region:
        region.countries.append(country)
        db.add(country)
        db.commit()
        db.refresh(country)
        return country
    return None

def add_region(db: Session, name:str, isocode:str):
    region = models.Region(
        name = name,
        isocode = isocode
        )
    db.add(region)
    db.commit()
    db.refresh(region)
    return region
