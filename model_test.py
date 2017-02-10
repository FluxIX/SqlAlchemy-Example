from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid

_Base = declarative_base()

def generate_uuid():
   # From: http://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
   return str( uuid.uuid1() )

def create_tables( engine ):
   DbSession = sessionmaker( bind = engine )
   db_session = DbSession()

   _Base.metadata.create_all( engine )

   db_session.commit()

class _TableNames:
   Student = "students"
   Course = "courses"
   CourseOffering = "course_offerings"
   CourseMember = "course_members"

class Student( _Base ):
   __tablename__  = _TableNames.Student

   id = Column( Integer, primary_key = True )
   name = Column( String( 50 ), unique = True, nullable = False )

   course_sections = relationship( "CourseOffering", secondary = _TableNames.CourseMember )

class Course( _Base ):
   __tablename__ = _TableNames.Course

   id = Column( Integer, primary_key = True )
   name = Column( String( 50 ), unique = True, nullable = False )
   description = Column( String( 16000 ), nullable = True )

class CourseOffering( _Base ):
   __tablename__ = _TableNames.CourseOffering

   course_id = Column( Integer, ForeignKey( _TableNames.Course + ".id" ), primary_key = True )
   time = Column( Time, primary_key = True )
   id = Column( String( 36 ), nullable = True, default = generate_uuid )

   students = relationship( "Student", secondary = _TableNames.CourseMember )
   course = relationship( "Course", uselist = False )

class CourseMembers( _Base ):
   __tablename__ = _TableNames.CourseMember

   course_offering_id = Column( Integer, ForeignKey( _TableNames.CourseOffering + ".id" ), primary_key = True )
   student_id = Column( Integer, ForeignKey( _TableNames.Student + ".id" ), primary_key = True )
