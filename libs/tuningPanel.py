import wx
import csnd6


class TuningPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(TuningPanel, self).__init__(*a, **k)#super the subclass
		#self.SetBackgroundColour((250, 200, 200))
		siz = wx.Size(60,-1)#size of floatspin
		font_s = wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.temperaT = wx.StaticText(self, -1, "Temperament", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.temperaChoice = ["Pythagorean", "Equally"] 
		self.tempera = wx.ComboBox(self, -1, choices=self.temperaChoice, size=wx.Size(60, 20))
		self.tempera.SetFont(font_s)
		self.tempera.SetValue(self.temperaChoice[0])
		self.Bind(wx.EVT_COMBOBOX, self.setTempera, self.tempera)
		self.cSound.SetChannel("tempera", 0.0)
		
		self.tuningT = wx.StaticText(self, -1, "Tuning", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.tuningChoice = ["8Hz C", "440Hz A"] 
		self.tuning = wx.ComboBox(self, -1, choices=self.tuningChoice, size=wx.Size(60, 20))
		self.tuning.SetFont(font_s)
		self.tuning.SetValue(self.tuningChoice[0])
		self.Bind(wx.EVT_COMBOBOX, self.setTuning, self.tuning)
		self.cSound.SetChannel("tuning", 0.0)
		
		
		self.sizer.Add(self.temperaT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.tempera, -1,flag=wx.EXPAND)
		self.sizer.AddSpacer(2,flag=wx.EXPAND)
		self.sizer.Add(self.tuningT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.tuning, -1,flag=wx.EXPAND)
		
		
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)


	def setTempera(self, evt):
		index = self.tempera.GetSelection()
		self.cSound.SetChannel("tempera", index)	


	def setTuning(self, evt):
		index = self.tuning.GetSelection()
		self.cSound.SetChannel("tuning", index)	
		


