import wx
import csnd6
import fsm
import language
import actionsEditPanel

class ActionsPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(ActionsPanel, self).__init__(*a, **k)#super the subclass
		
		self.parent = self.GetParent()
		siz = wx.Size(70,-1)#size of floatspin
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#KILLALL
		self.killallB = wx.Button(self, -1, label='Kill All')
		self.Bind(wx.EVT_BUTTON, self.killAll, self.killallB)
		
		#MULTIPLY VOLUME
		self.volmultip = fsm.Fsm(parent=self, id=-1,
										digits=3,
										min_val = 0.0,
										max_val = 3.0,
										increment=0.01,
										value = 1.0,
										mousev = 1,
										size = siz)
		self.multipB = wx.Button(self, -1, label='Volume Mul')
		self.Bind(wx.EVT_BUTTON, self.multipAll, self.multipB)
		
		'''
		#Create Serie
		self.seriecode = wx.TextCtrl(self, -1)
		#buttons to scroll hystory
		self.oldB = wx.Button(self, -1, label='^', size=wx.Size(30,-1))
		self.newB = wx.Button(self, -1, label='v', size=wx.Size(30,-1))
		self.Bind(wx.EVT_BUTTON, self.hystscroll, self.oldB)
		self.Bind(wx.EVT_BUTTON, self.hystscroll, self.newB)
		
		self.serieB = wx.Button(self, -1, label='Do Serie')
		self.Bind(wx.EVT_BUTTON, self.doSerie, self.serieB)
		'''
		self.editorB = wx.Button(self, -1, label='Event Edit')
		self.Bind(wx.EVT_BUTTON, self.openEditFrame, self.editorB)
		
		'''
		self.openMem()
		self.hystindex = len(self.memory) - 1
		'''
		self.sizer.Add(self.killallB, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(15,flag=wx.EXPAND)
		self.sizer.Add(self.volmultip, 0,flag=wx.EXPAND)
		self.sizer.Add(self.multipB, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(15,flag=wx.EXPAND)
		'''
		self.sizer.Add(self.seriecode, -1,flag=wx.EXPAND)
		self.sizer.Add(self.oldB, 0,flag=wx.EXPAND)
		self.sizer.Add(self.newB, 0,flag=wx.EXPAND)
		self.sizer.Add(self.serieB, 0,flag=wx.EXPAND)
		'''
		self.sizer.Add(self.editorB, -1,flag=wx.EXPAND)

		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
		
		self.openFr=[]
		
		self.timers_storage = []
		self.timers_actions = []
		self.timeMultip = 0.0
		self.futureItem = []


	def OnClose(self, evt):
		'''kill stored timers kill open windows'''
		for timer in self.timers_storage:
			timer.Stop()
		for item in self.openFr:
			self.openFr.remove(item)
		self.Destroy()
		
	
	def killAll(self, evt):
		'''kill all active oscillators
		PROBLEM: resetting lowest oscillator to wrong value'''
		parent = self.GetParent()
		for osc in parent.keypanel.oscillators:
			if osc.isAlive:
				osc.vol.SetValue(0.0)
				osc.vol.emitValue(evt)
		


	def multipAll(self, evt):
		'''change the volume for all active oscillators'''
		parent = self.GetParent()
		multip = self.volmultip.GetValue()
		for osc in parent.keypanel.oscillators:
			if osc.isAlive:
				val = osc.vol.GetValue()
				newval = val * multip 
				if newval > 1.0:
					newval = 1.0
				elif newval < 0.001:
					newval = 0.0
				osc.vol.SetValue(newval)
				osc.vol.emitValue(evt)
		
		
	"""
	def doSerie(self, evt):
		'''list separated by space'''
		parent = self.GetParent()
		string = self.seriecode.GetValue().encode()
		self.memory.append(string)
		#print self.memory
		f = open("save/actmem","a")
		f.write(string+"\n")
		f.close()
		self.hystindex = len(self.memory) - 1
		list = language.divideGroups(string)
		for item in list:
			if parent.keypanel.minpoly < item[0] < parent.keypanel.maxpoly:
				#calculate base time (60 / BpM)
				#print "command"
				#print item
				if item[4] > 0.0:
					'''start timer'''
					#print "timed futureItem"
					self.timeMultip = item[4]
					self.futureItem = item
					#print self.futureItem 
					self.timerActionStart()
					#pass
				else:
					print "UNtimed"
					if item[1] >= 0.0:
						vol = item[1]
						if vol > 1.0:
							vol = 1.0
						parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].vol.SetValue(vol)
						parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].vol.emitValue(evt)
					else:
						vol = parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].vol.GetValue()
					if item[2] >= 0.0:
						parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].pan.SetValue(item[2])
						parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].pan.emitValue(evt)
					if item[3] >= 0:
						spe=parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].speedList[item[3]]
						parent.keypanel.oscillators[item[0]  - parent.keypanel.minpoly].speedvalue.SetValue(spe)
						self.cSound.SetChannel("spe_"+str(item[0]), item[3])
		
	
	def openMem(self):
		'''load the list of commands'''
		f = open("save/actmem","r")
		self.memory =[]
		for line in f:
			self.memory.append(line.rstrip('\n'))
		f.close()


	def hystscroll(self,evt):
		'''to navigate between old commands'''
		button = evt.GetEventObject().GetLabel()
		if button == "^":
			self.hystindex = self.hystindex - 1
			if self.hystindex < 0:
				self.hystindex = len(self.memory) - 1
		else:
			self.hystindex = self.hystindex + 1
			if self.hystindex > len(self.memory) - 1:
				self.hystindex = 0
		#print "index : %d lenght %d" % (len(self.memory), self.hystindex)
		str = self.memory[self.hystindex]
		self.seriecode.SetValue(str)




	def timerActionStart(self):
		'''start a timer for future event'''
		#obj = evt.GetEventObject.GetParent()
		parentpanel = self.GetParent()
		time = int(1000 * self.timeMultip * 60 / parentpanel.topp.bpm.GetValue())#calculate time
		timer = wx.Timer(self, -1)
		self.Bind(wx.EVT_TIMER, self.timerActionStop, timer)
		self.timers_storage.append(timer)
		self.timers_storage[len(self.timers_storage)-1].Start(time)
		#print 'timerActionStart'
		#print self.futureItem
		self.timers_actions.append(self.futureItem)
		
	
	def timerActionStop(self, evt):
		'''do event and stop a timer'''
		obj = evt.GetEventObject()
		ind = self.timers_storage.index(obj)
		#print "stopping %d" % ind
		self.timers_storage[ind].Stop()
		#print self.timers_actions[ind]
		#print "timed command"
		parent = self.GetParent()
		note = self.timers_actions[ind][0]
		vol = self.timers_actions[ind][1]
		pan = self.timers_actions[ind][2]
		mod = self.timers_actions[ind][3]
		if vol >= 0.0:
			if vol > 1.0:
				vol = 1.0
			parent.keypanel.oscillators[note  - parent.keypanel.minpoly].vol.SetValue(vol)
			parent.keypanel.oscillators[note  - parent.keypanel.minpoly].vol.emitValue(evt)
		else:
			vol = parent.keypanel.oscillators[note  - parent.keypanel.minpoly].vol.GetValue()
		if pan >= 0.0:
			parent.keypanel.oscillators[note  - parent.keypanel.minpoly].pan.SetValue(pan)
			parent.keypanel.oscillators[note  - parent.keypanel.minpoly].pan.emitValue(evt)
		if mod >= 0:
			spe=parent.keypanel.oscillators[note  - parent.keypanel.minpoly].speedList[mod]
			parent.keypanel.oscillators[note  - parent.keypanel.minpoly].speedvalue.SetValue(spe)
			self.cSound.SetChannel("spe_"+str(note), mod)
		#parent.keypanel.find_lowest_oscillator_single(note,vol)	
		#delete timer
		del self.timers_storage[ind]
		#delete action
		del self.timers_actions[ind]
	"""

	def openEditFrame(self, evt):
		'''open a midi Configuration frame'''
		print "open Midi Conf"
		newframe = actionsEditPanel.actionEditFr(self, -1, title="Event Editor", cSound = self.cSound)
		self.openFr.append(newframe)
		newframe.Show()