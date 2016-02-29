import wx
import csnd6
import fsm



class OscillatorPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.counter= k.pop('counter', None)
		self.title= k.pop('title', None)
		super(OscillatorPanel, self).__init__(*a, **k)#super the subclass
		
		self.parent = self.GetParent()
		self.isLowest = False
		self.isAlive = False
		
		siz = wx.Size(65,-1)#size of floatspin
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		font_s = wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		
		self.note = wx.Button(self, -1, label=str(self.counter) + " " + self.title, size = wx.Size(65,20))
		self.Bind(wx.EVT_BUTTON, self.setLowest, self.note)
		self.note.SetFont(font_s)
		
		self.setColourBack()
		
		
		self.vol_previous_val=0.0	
		self.vol = fsm.FsmTs(parent=self, id=-1,
									digits=3,
									min_val = 0.0,
									max_val = 1.0,
									increment=0.01,
									value = 0.0,
									size = siz,
									cSound = self.cSound,
									ftable = 100,
									indxn = self.counter)
		self.cSound.TableSet(100, self.counter, 0)		
	
		
		self.pan = fsm.FsmCs(parent=self, id=-1,
									digits=3,
									min_val = 0.0,
									max_val = 1.0,
									increment=0.01,
									value = 0.5,
									mousev = 0,
									size = siz,
									cSound = self.cSound,
									channel = "pan_"+str(self.counter))
		self.cSound.SetChannel("pan_"+str(self.counter), 0.5)		
		
		self.speedList = ["0.0", "0.03125","0.0625", "0.125", "0.25", "0.333", "0.5", "0.666", "0.75", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"] 
		self.speedvalue = wx.ComboBox(self, -1, choices=self.speedList, size=wx.Size(60, 20))
		self.speedvalue.SetValue("0.0")
		self.Bind(wx.EVT_COMBOBOX, self.setSpeed, self.speedvalue)
		self.cSound.SetChannel("spe_"+str(self.counter), 0.0)
		
		
		self.sizer.Add(self.note, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(1,flag=wx.EXPAND)
		self.sizer.Add(self.vol, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(1,flag=wx.EXPAND)
		self.sizer.Add(self.pan, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(1,flag=wx.EXPAND)
		self.sizer.Add(self.speedvalue, 0,flag=wx.EXPAND)
		
		
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
		
		
	def setColourBack(self):
		if self.isLowest:
			self.note.SetBackgroundColour((255, 0, 0))
		elif self.isAlive:
			self.note.SetBackgroundColour((0, 255, 100))
			if "#" in self.title:
				self.note.SetForegroundColour((0,0,0))
			else:
				self.note.SetForegroundColour((255,255,255))
		else:
			if "#" in self.title:
				self.note.SetBackgroundColour((0, 0, 0))
				self.note.SetForegroundColour((250,250,250))
			else:
				self.note.SetBackgroundColour((250, 250, 250))
				self.note.SetForegroundColour((0,0,0))
		#self.sizer.Layout()
		#self.Layout()
	
	
	def setSpeed(self, evt):
		"""set the speed multiplier"""
		speed = float(self.speedList[self.speedvalue.GetSelection()])
		self.cSound.SetChannel("spe_"+str(self.counter), speed)
		
		
	def setLowest(self, evt):
		'''set lowest'''
		prevlowest = self.parent.lowest
		if prevlowest <> self.counter:
			self.isLowest = True
			self.parent.oscillators[prevlowest - self.parent.minpoly].isLowest = False
			self.setColourBack()
			self.parent.oscillators[prevlowest - self.parent.minpoly].setColourBack()
			self.parent.lowest = self.counter
			self.cSound.SetChannel("lowest", self.counter)