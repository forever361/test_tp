import os

from app.application import app
from app.common.libs.DateHelper import getCurrentTime

class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        return "%s%s" % ('http://127.0.0.1:8889', path)

    @staticmethod
    def buildStaticUrl(path):
        path = "/static" + path + "?v=" + UrlManager.getReleaseVersion()
        return UrlManager.buildUrl(path)
	
    @staticmethod
    def buildStaticUrl_no_v(path):
        path = "/static" + path
        return UrlManager.buildUrl(path)	
		

    @staticmethod
    def getReleaseVersion():
        """
        版本管理，开发环境使用时间戳，prod加载版本信息
        :return:
        """
        ver = 'v1'
        #ver = "%s"%(getCurrentTime("%Y%m%d%H%M%S%f"))
        release_path = app.config.get('RELEASE_PATH')
        if release_path and os.path.exists(release_path):
            with open(release_path,'r') as f:
                ver = f.readline()
        return ver

