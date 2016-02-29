import wx
import csnd6
import fsm


class TopPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(TopPanel, self).__init__(*a, **k)#super the subclass
		
		#self.SetBackgroundColour((250, 200, 200))
		siz = wx.Size(65,-1)#size of floatspin
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.bpmT = wx.StaticText(self, -1, "BpM", style= wx.ALIGN_CENTER | wx.TE_RICH)
		
		self.bpm = fsm.FsmCs(parent=self, id=-1,
									digits=2,
									min_val = 1.0,
									max_val = 500.0,
									increment=0.1,
									value = 60.0,
									size = siz,
									cSound = self.cSound,
									channel = "bpm")
		self.cSound.SetChannel("bpm", 60.0)		
		
		self.speedvalueT = wx.StaticText(self, -1, "Speed", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.speedList = ["0.0", "0.125", "0.25", "0.333", "0.5", "0.666", "0.75", "1.0", "2.0", "3.0", "4.0", "5.0"] 
		self.speedvalue = wx.ComboBox(self, -1, choices=self.speedList, size=wx.Size(60, 20))
		self.speedvalue.SetValue("1.0")
		self.Bind(wx.EVT_COMBOBOX, self.setSpeedPorta, self.speedvalue)
		self.cSound.SetChannel("porta", 0.0)
		
		self.osciVT = wx.StaticText(self, -1, "OscVol", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.osciV = fsm.FsmCs(parent=self, id=-1,
									digits=3,
									min_val = 0.0,
									max_val = 2.0,
									increment=0.001,
									value = 1.0,
									size = siz,
									cSound = self.cSound,
									channel = "osciV")
		self.cSound.SetChannel("osciV", 1.0)
		
		self.sequVT = wx.StaticText(self, -1, "SeqVol", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.sequV = fsm.FsmCs(parent=self, id=-1,
									digits=3,
									min_val = 0.0,
									max_val = 2.0,
									increment=0.001,
									value = 1.0,
									size = siz,
									cSound = self.cSound,
									channel = "sequV")
		self.cSound.SetChannel("sequV", 1.0)
		
		self.revT = wx.StaticText(self, -1, "Reverb", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.rev_feed = fsm.FsmCs(parent=self, id=-1,
									digits=3,
									min_val = 0.0,
									max_val = 1.0,
									increment=0.001,
									value = 0.5,
									size = siz,
									cSound = self.cSound,
									channel = "reverbFe")
		self.cSound.SetChannel("reverbFe", 0.5)
		
		self.revdampFT = wx.StaticText(self, -1, "dampF", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.rev_fco = fsm.FsmCs(parent=self, id=-1,
									digits=1,
									min_val = 10.0,
									max_val = 15000.0,
									increment=0.1,
									value = 5000.0,
									size = siz,
									cSound = self.cSound,
									channel = "reverbFr")
		self.cSound.SetChannel("reverbFr", 5000.0)
		
		self.revdwT = wx.StaticText(self, -1, "DW", style= wx.ALIGN_CENTER | wx.TE_RICH)	
		self.rev_dw = fsm.FsmCs(parent=self, id=-1,
									digits=3,
									min_val = 0.0,
									max_val = 1.0,
									increment=0.01,
									value = 0.5,
									size = siz,
									cSound = self.cSound,
									channel = "reverbDW")
		self.cSound.SetChannel("reverbDW", 0.5)
		self.rev_hpT = wx.StaticText(self, -1, "hpIn", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.rev_hp = fsm.FsmCs(parent=self, id=-1,
									digits=1,
									min_val = 10.0,
									max_val = 15000.0,
									increment=0.1,
									value = 10.0,
									size = siz,
									cSound = self.cSound,
									channel = "reverbLFr")
		self.cSound.SetChannel("reverbLFr", 10.0)		
	
		self.vuT = wx.StaticText(self, -1, "dB", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_outL = wx.TextCtrl(self, -1, size=(60,20))
		self.vumeter_outR = wx.TextCtrl(self, -1, size=(60,20))
		
		
		#Timer Update MUST BE STOPPED IN MAIN FRAME
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(50)
		self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timerRefresh)
		
		self.recB = wx.ToggleButton(self, -1, label='Record')
		self.Bind(wx.EVT_TOGGLEBUTTON, self.doRecord, self.recB)
		
		
		self.sizer.Add(self.bpmT, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(2,flag=wx.EXPAND)
		self.sizer.Add(self.bpm, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(10,flag=wx.EXPAND)
		self.sizer.Add(self.speedvalueT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.speedvalue, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(10,flag=wx.EXPAND)
		self.sizer.Add(self.osciVT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.osciV, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.sequVT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.sequV, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.revT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.rev_feed, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.revdampFT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.rev_fco, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.rev_hpT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.rev_hp, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.revdwT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.rev_dw, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.vuT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.vumeter_outL, 0,flag=wx.EXPAND)
		self.sizer.Add(self.vumeter_outR, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(3,flag=wx.EXPAND)
		self.sizer.Add(self.recB, 0,flag=wx.EXPAND)
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
		
		
	def OnClose(self, evt):
		#stop all the timers created
		self.timerRefresh.Stop() 
		#destroy
		self.Destroy()

		
		
	def setSpeedPorta(self, evt):
		"""set the speed multiplier"""
		speed = float(self.speedList[self.speedvalue.GetSelection()])
		self.cSound.SetChannel("porta", speed)		
		
	def timerUpdate(self, evt):
		"""update the vumeters"""
		self.dbL = self.cSound.GetChannel("outVUmeterL")
		self.dbR = self.cSound.GetChannel("outVUmeterR")
		if self.dbL < -1.0:
			self.vumeter_outL.SetForegroundColour((100,250, 100))
		elif -1.0<= self.dbL < 0.0:
			self.vumeter_outL.SetForegroundColour((250, 200, 0))
		else:
			self.vumeter_outL.SetForegroundColour((250, 10, 10))
		self.vumeter_outL.SetValue(str(self.dbL))
		if self.dbR < -1.0:
			self.vumeter_outR.SetForegroundColour((100,250, 100))
		elif -1.0<= self.dbR < 0.0:
			self.vumeter_outR.SetForegroundColour((250, 200, 0))
		else:
			self.vumeter_outR.SetForegroundColour((250, 10, 10))
		self.vumeter_outR.SetValue(str(self.dbR))
		
		
	def doRecord(self, evt):
		"""launch record instrument"""
		obj = evt.GetEventObject()
		ispressed = obj.GetValue()
		if ispressed:
			obj.SetLabel('Recording')
			self.cSound.InputMessage('i 101 0 -1\n')
		else:
			obj.SetLabel('Stopped')
			self.cSound.InputMessage('i -101 0 -1\n')