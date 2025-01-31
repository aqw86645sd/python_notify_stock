import datetime

class TimeHelper:
    """負責時間處理"""

    @staticmethod
    def get_timezone(offset):
        """根據時區偏移量獲取當前時間"""
        gmt = datetime.timezone(datetime.timedelta(hours=offset))
        return datetime.datetime.now(tz=gmt).strftime('%Y/%m/%d %H:%M:%S')