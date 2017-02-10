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
   CourseSection = "course_sections"
   CourseSectionMembers = "course_section_members"

class Student( _Base ):
   __tablename__  = _TableNames.Student

   id = Column( Integer, primary_key = True )
   name = Column( String( 50 ), unique = True, nullable = False )

   course_sections = relationship( "CourseSection", uselist = True, secondary = _TableNames.CourseSectionMembers )

class Course( _Base ):
   __tablename__ = _TableNames.Course

   id = Column( Integer, primary_key = True )
   name = Column( String( 50 ), unique = True, nullable = False )
   description = Column( String( 16000 ), nullable = True )

   sections = relationship( "CourseSection", uselist = True )

class CourseSection( _Base ):
   __tablename__ = _TableNames.CourseSection

   course_id = Column( Integer, ForeignKey( _TableNames.Course + ".id" ), primary_key = True )
   time = Column( Time, primary_key = True )
   id = Column( String( 36 ), nullable = True, default = generate_uuid )

   students = relationship( "Student", uselist = True, secondary = _TableNames.CourseSectionMembers )
   course = relationship( "Course", uselist = False )

class CourseSectionMembers( _Base ):
   __tablename__ = _TableNames.CourseSectionMembers

   course_section_id = Column( Integer, ForeignKey( _TableNames.CourseSection + ".id" ), primary_key = True )
   student_id = Column( Integer, ForeignKey( _TableNames.Student + ".id" ), primary_key = True )
