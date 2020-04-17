import unittest
import os
import datetime

class TestStore(unittest.TestCase):
   
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(self.base_dir,'data/csv/')
        self.today = datetime.datetime.today().date().strftime("%Y%m%d")
    def test_isExistCSV(self): 
        """验证指定路径下是否存在文件夹data/csv文件目录"""
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.exists(os.path.join(self.path,'stockbasicinfo'+self.today+'.csv')))
        
if __name__ == '__main__':
    unittest.main()       
