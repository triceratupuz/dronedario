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
		

	def openEditFrame(self, evt):
		'''open a midi Configuration frame'''
		#print "open Midi Conf"
		newframe = actionsEditPanel.actionEditFr(self, -1, title="Event Editor", cSound = self.cSound)
		self.openFr.append(newframe)
		newframe.Show()