from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from db.database import Base


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    address = Column(String)
    country_id = Column(Integer, ForeignKey("country.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    city_id = Column(Integer, ForeignKey("city.id"))


class Country(Base):
    __tablename__ = "country"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)


class Region(Base):
    __tablename__ = "region"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)
    country_id = Column(Integer, ForeignKey("country.id"))


class City(Base):
    __tablename__ = "city"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)
    region_id = Column(Integer, ForeignKey("region.id"))

class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    id_role = Column(Integer, ForeignKey("role.id"))

class School(Base):
    __tablename__ = "school"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)
    address = Column(String)
    country_id = Column(Integer, ForeignKey("country.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
    rut = Column(String, unique=True)

class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    country_id = Column(Integer, ForeignKey("country.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
    rut = Column(String, unique=True)

class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    patente = Column(String, unique=True)
    driver_id = Column(Integer, ForeignKey("driver.id"))

class Parent(Base):
    __tablename__ = "parent"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    country_id = Column(Integer, ForeignKey("country.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
    rut = Column(String, unique=True)
    type_parent_id = Column(Integer, ForeignKey("type_parent.id"))

class TypeParent(Base):
    __tablename__ = "type_parent"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    country_id = Column(Integer, ForeignKey("country.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
    rut = Column(String, unique=True)
    school_id = Column(Integer, ForeignKey("school.id"))
    parent_id = Column(Integer, ForeignKey("parent.id"))
    birthdate = Column(Date)

class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    driver_id = Column(Integer, ForeignKey("driver.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"))
    school_id = Column(Integer, ForeignKey("school.id"))
    parent_id = Column(Integer, ForeignKey("parent.id"))
    student_id = Column(Integer, ForeignKey("student.id"))

