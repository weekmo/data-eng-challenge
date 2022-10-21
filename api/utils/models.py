# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 06:41:27 2022

@author: HassaM3
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "tb_regions"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    isocode = Column(String, unique=True, index=True)
   
    countries = relationship("Country", back_populates="region", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Region(id={self.id}, name={self.name}, isocode={self.isocode})"

class Country(Base):
    __tablename__ = "tb_countries"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    isocode = Column(String, unique=True, index=True)
    region_id = Column(Integer, ForeignKey("tb_regions.id"), nullable=False)
    
    region = relationship("Region", back_populates="countries")
    agros = relationship("Agro", back_populates="country", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Country(id={self.id}, name={self.name}, isocode={self.isocode})"
    
class Agro(Base):
    __tablename__ = "tb_agro"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    date_year = Column(Integer, index=True)
    agro_srfc = Column(Float)
    cereal_land = Column(Float)
    cereal_yield = Column(Float)
    country_id = Column(Integer, ForeignKey("tb_countries.id"), nullable=False)
    
    country = relationship("Country", back_populates="agros")
    
    
    def __repr__(self):
        return f"Agro(id={self.id}, year={self.date_year}, cereal_land={self.cereal_land}, cereal_yield={self.cereal_yield}, agro_srfc={self.agro_srfc})"
