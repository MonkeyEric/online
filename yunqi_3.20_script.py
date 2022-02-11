# coding:utf-8
import time,requests
# def getBeijinTime():
#      try:
#          conn = httplib.HTTPConnection("www.beijing-time.org")
#          conn.request("GET", "/time.asp")
#          response = conn.getresponse()
#          print (response.status, response.reason)
#          if response.status == 200:
#              result = response.read()
#              data = result.split("rn")
#              year = data[1][len("nyear")+1 : len(data[1])-1]
#              month = data[2][len("nmonth")+1 : len(data[2])-1]
#              day = data[3][len("nday")+1 : len(data[3])-1]
#              #wday = data[4][len("nwday")+1 : len(data[4])-1]
#              hrs = data[5][len("nhrs")+1 : len(data[5])-1]
#              minute = data[6][len("nmin")+1 : len(data[6])-1]
#              sec = data[7][len("nsec")+1 : len(data[7])-1]
#
#              beijinTimeStr = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
#              beijinTime = time.strptime(beijinTimeStr, "%Y/%m/%d %X")
#              return beijinTime
#      except Exception,e:
#          print e
#          return None


if __name__=='__main__':
    # print(getBeijinTime())
    res = requests.get("http://www.beijing-time.org")
    content = res.content