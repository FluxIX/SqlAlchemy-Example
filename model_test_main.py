from datetime import time
import os, os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model_test import Student, Course, CourseOffering, CourseMembers, create_tables

_session_type = None
def get_session_type( engine_instance ):
   global _session_type
   if _session_type is None:
      _session_type = sessionmaker( bind = engine_instance )

   return _session_type

def get_new_session( engine_instance ):
   return get_session_type( engine_instance )()

def _build_db( engine, db_file_path, ):
   student_names = [ "Alice", "Bob", "Eve" ]
   course_list = [ "Econ 100", "CompSci 243" ]
   times = [ time( *t ) for t in [ [ 8, 0, 0 ], [ 9, 0, 0 ], [ 10, 0, 0 ] ] ]

   if os.path.exists( db_file_path ):
      os.remove( db_file_path )

   create_tables( engine )

   db_session = get_new_session( engine )

   students = [ Student( name = name ) for name in student_names ]
   db_session.add_all( students )

   courses = [ Course( name = name ) for name in course_list ]
   db_session.add_all( courses )

   db_session.commit() # Must commit before adding the dependent records.

   course_offerings = [ CourseOffering( course_id = c.id, time = t ) for c in courses for t in times ]
   db_session.add_all( course_offerings )

   db_session.commit()

   course_members = [ CourseMembers( course_offering_id = c.id, student_id = s.id ) for c in course_offerings for s in students ]
   db_session.add_all( course_members )

   db_session.commit()

def _query_db( engine ):
   db_session = get_new_session( engine )

   print( "Student count: {:d}".format( len( db_session.query( Student ).all() ) ) )

   student = db_session.query( Student ).first()

   print( "Student '{}' course section count: {:d}".format( student.name, db_session.query( CourseOffering ).filter( Course.id == CourseOffering.course_id ).filter( CourseOffering.id == CourseMembers.course_offering_id ).filter( CourseMembers.student_id == student.id ).count() ) )
   for course, offering in db_session.query( Course, CourseOffering ).filter( Course.id == CourseOffering.course_id ).filter( CourseOffering.id == CourseMembers.course_offering_id ).filter( CourseMembers.student_id == student.id ).order_by( CourseOffering.time, Course.name ).all():
      print( "--> {}: {}".format( offering.time.strftime( "%H:%M:%S" ), course.name ) )

   print( "Student '{}' course section count: {:d}".format( student.name, len( student.course_sections ) ) )
   for offering in student.course_sections:
      print( "--> {}: {}".format( offering.time.strftime( "%H:%M:%S" ), offering.course.name ) )

def main():
   db_filename = "model_test_db.sqlite3"

   db_file_path = os.path.normpath( os.path.normcase( db_filename ) )
   if not os.path.isabs( db_file_path ):
      db_file_path = os.path.join( os.getcwd(), db_file_path )

   engine = create_engine( "sqlite:///" + db_file_path )

   _build_db( engine, db_file_path )

   _query_db( engine )
