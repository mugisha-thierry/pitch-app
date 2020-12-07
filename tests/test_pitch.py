import unittest
from app.models import Pitch,User
from app import db

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.user_thierry = User(username = 'thierry',email = 'thierry@ms.com',secure_password = 'howareyou',bio= 'am a student', profile_pic_path='https://image.tmdb.org/t/p/w500/jdjdjdjn')
        self.new_pitch = Pitch(id=12345,title='tell the world',pitch="love you self",category='hobbies',user_id= self.user_thierry.id, time="2020/2/3 13:20" )

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.id,12345)
        self.assertEquals(self.new_pitch.title,'tell the world')
        self.assertEquals(self.new_pitch.pitch,"love you self")
        self.assertEquals(self.new_pitch.category,'hobbies')
        self.assertEquals(self.new_pitch.user_id,self.user_thierry.id)
        self.assertEquals(self.new_pitch.time,'2020/2/3 13:20')

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()    