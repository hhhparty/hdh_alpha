import unittest
import os
import datetime
import sys



class TestSettings(unittest.TestCase):
    """Test the lazzySetting process of global_settings and settings """
    def setUp(self):
        sys.path.append("..")
        from hdh_alpha.conf import settings 
        self.settings = settings
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 设置环境变量
        os.environ.setdefault('HDH_ALPHA_SETTINGS_MODULE', 'hdh_alpha.settings')
        
    def test_isExistSettingfiles(self):
        """验证是否存在文件global_settings和settings"""
        self.assertTrue(os.path.exists(os.path.join(self.base_dir,'hdh_alpha/global_settings.py')))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir,'hdh_alpha/settings.py')))
        
    def test_isExistSettings(self):
        """验证是否能够正常延迟加载文件中的设置。"""                  
        self.assertTrue(os.environ.get('HDH_ALPHA_SETTINGS_MODULE'))
        self.assertEqual(self.settings.LANGUAGE_CODE,'zh-hans')
        
        
        
        