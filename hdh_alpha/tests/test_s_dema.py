import unittest 

__config__ = {
    "base": {
        "start_date": "2008-07-01",
        "end_date": "2017-01-01",
        "frequency": "1d",
        "matching_type": "current_bar",
        "benchmark": "000001.XSHE",
        "accounts": {
            "stock": 100000
        }
    },
    "extra": {
        "log_level": "error",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        },
        "sys_funcat": {
            "enabled": True,
            "show": True,
        },
    },
}
@unittest.skip("class TestStrategy is empty now.")
class TestStrategy(unittest.TestCase):
    def test_dema(self):
        pass
        
if __name__ == "__main__":
    unittest.main()