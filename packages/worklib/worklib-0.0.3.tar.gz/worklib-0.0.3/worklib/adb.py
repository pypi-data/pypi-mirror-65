# -*- coding:utf-8 -*-

import os
def get_udid(executable_path_dict):
	return [i.split("\t")[0].strip() for i in os.popen(executable_path_dict["adb_path"] + "  devices").readlines() if
			"device" in i and "attached" not in i]

class adb(object):
	def __init__(self, udid,initConfigParams):

		self.config = initConfigParams
		self.adb_cmd = self.init_adb_cmd()
		self.aapt_path = self.init_aapt_cmd()

		# self.app_path = initConfigParams["app_path"]
		self.udid = udid

	def init_adb_cmd(self):
		if "adb_path" in self.config.keys():
			return self.config["adb_path"]
		else:
			return "adb"

	def init_aapt_cmd(self):
		if "aapt_path" in self.config.keys():
			return self.config["aapt_path"]
		else:
			return "aapt"

	def command(self, cmd):
		print(type(cmd))
		print(type(self.adb_cmd))
		print()
		text = self.adb_cmd + " -s " + self.udid + "  " + cmd
		print("--adb log------->"+text)
		return os.popen(text).read()

	def install_app(self, path):
		return self.command("install -t" + path)

	def query_system_packagelist(self, ):
		return self.command("shell pm list packages -f")

	def pull(self, systempath, localpath):
		return self.command("pull " + systempath + " " + localpath)

	def push(self, localpath, systempath):
		return self.command("push " + localpath + " " + systempath)

	def logcat(self, savelogpath, level=""):
		self.command("logcat %s  >" % (level) + savelogpath)

	def bugreport(self, savelogpath):

		self.command("bugreport >" + savelogpath)

	def monkey(self, cmd, savelogpath):
		self.command("shell monkey " + cmd + " >" + savelogpath)

	def ps(self, ps_cmd=""):
		return self.command("shell ps " + ps_cmd)

	def kill(self, port):
		self.command("shell kill " + port)

	def get_app_package(self,app_path):
		if os.name == "posix":
			aapt_dump = "%s dump badging %s |grep %s|awk '{print $2}'"
			appPackage = str(os.popen(aapt_dump % (self.aapt_path, app_path, "package")).read()).strip()[6:-1]
			# print(aapt_dump % (aapt_path,app_path, "launchable-activity"))
			try:
				appActivity = str(
					os.popen(aapt_dump % (self.aapt_path, app_path, "launchable-activity")).read()).split()[
								  0].strip()[6:-1]
			except Exception as e:
				appActivity = appPackage + ".main.MainActivity"

		elif os.name == "nt":
			appPackage = os.popen('aapt dump badging  %s |findStr "package:" ' % (app_path)).read().split(" ")[
							 1].strip()[6:-1]
			try:
				appActivity = \
					os.popen('aapt dump badging %s |findStr "launchable-activity"' % (app_path)).read().split(" ")[
						1].strip()[
					6:-1]
			except:
				appActivity = appPackage + ".main.MainActivity"

		return appPackage,appActivity

	def uninstall(self, app_path):
		self.command("uninstall " + self.get_app_package(app_path)[0])

	def dumpsys(self, dumpsys_cmd=""):
		return self.command("shell dumpsys " + dumpsys_cmd)

	def get_meninfo(self,app_path):
		return self.dumpsys("meninfo " + self.get_app_package(app_path)[0])

	def get_app_activity(self):
		pass


# if __name__ == '__main__':
# 	executable_path_dict = {"adb_path": "/Users/zhenghong/Library/Android/sdk/platform-tools/adb",
# 							"aapt_path": "/Users/zhenghong/Library/Android/sdk/build-tools/29.0.3/aapt",
# 							"firefoxdriver": "/Users/zhenghong/work/gitee/AutomationFramework/conf/geckodriver",
# 							"chromedriver": "/Users/zhenghong/work/gitee/AutomationFramework/conf/chromedriver",
# 							"app_path":"/Users/zhenghong/Downloads/1fdb0cf17de2a5738f9c9789aae036f7.apk"}
#
# 	udid = get_udid(executable_path_dict)[0]
# 	print("udid",udid)
# 	adb = adb(udid,executable_path_dict)
# 	# adb.install_app(executable_path_dict["app_path"])
# 	print(adb.get_meninfo(executable_path_dict["app_path"]))

	pass


