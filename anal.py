#!/usr/bin/env python
import threading
from Queue import Queue
import time


chooseLen=6
debug=True
class analThread(threading.Thread):
  def __init__(self,i):
    super(analThread,self).__init__()
    self.name = "analThread"
    self.queue = Queue()
    self.source = i

  def run(self):
    print("starting: "+self.name)
    while True:
      input = self.source.get()
      if debug: print(self.name+" got "+ input)
      for w in input.split():
        if debug: print(self.name+"test:"+w)
        if len(w) > chooseLen:
          if debug: print(self.name+"CHOSE: "+w)
          self.queue.put(w)

  def get(self):
    return self.queue.get()

  
