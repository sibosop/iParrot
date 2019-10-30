#!/usr/bin/env python
import os
import sys
os.environ['DISPLAY']=":0.0"
os.chdir(os.path.dirname(sys.argv[0]))
pname = sys.argv[0]
home = os.environ['HOME']
sys.path.append("sibcommon")
defaultSpecPath = "%s/%s"%("speclib","raspmus.json")

import datetime
import time
import recog
import recorder
import anal
import blanket


if __name__ == '__main__':
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  print(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

  it = recorder.inputThread()
  it.setDaemon(True)

  rt = recog.recogThread(it)
  rt.setDaemon(True)

  analt = anal.analThread(rt)
  analt.setDaemon(True)

  pst = blanket.phraseSender(analt)
  pst.setDaemon(True)

  it.start()
  rt.start()
  analt.start()
  pst.start()
  while True:
    try:
      time.sleep(2)
    except KeyboardInterrupt:
      print(pname+": keyboard interrupt")
      it.close()
      break
    except Exception as e:
      syslog.syslog(pname+":"+str(e))
      it.close()
      break

  printpname+" exiting")
  exit(0)

