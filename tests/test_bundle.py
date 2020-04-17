import unittest
import bcolz
import os
import datetime

class TestBundle(unittest.TestCase):
   
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(self.base_dir,'bundle/')
    def test_isExist(self): 
        """验证指定路径下是否存在文件夹bundle"""
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.exists(os.path.join(self.path,'stocks.bcolz')))
        self.assertTrue(os.path.exists(os.path.join(self.path,'futures.bcolz')))
        self.assertTrue(os.path.exists(os.path.join(self.path,'indexes.bcolz')))
        self.assertTrue(os.path.exists(os.path.join(self.path,'funds.bcolz')))
    
    def test_isUpdated(self):
        """测试数据是否已经更新"""
        table = bcolz.open(os.path.join(self.path,'stocks.bcolz'),'r')        
        self.assertIsNotNone(table)
        index = table.attrs['line_map']
        self.assertIsNotNone(index)
        fields = table.names[1:]
        self.assertIsNotNone(fields)
        lastdate = table.cols['date'][-1]
        self.assertIsNotNone(lastdate)
        lastdate = datetime.datetime.strptime(str(lastdate), '%Y%m%d')
        print("The updated date of bundle:{}".format(lastdate))
        self.assertTrue(datetime.datetime.__eq__(lastdate,datetime.datetime.now().date()))
        
        

        
        
if __name__ == '__main__':
    unittest.main()       
