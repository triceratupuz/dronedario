import wx
import csnd6
import fsm



class StepseqPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.seqs = k.pop('seqs', None)
		super(StepseqPanel, self).__init__(*a, **k)#super the subclass
		self.gridSizer = wx.GridBagSizer(vgap=2, hgap=5)
		#TAGS
		spe = wx.StaticText(self, -1, "Speed", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(spe, pos=(1,0))
		durr = wx.StaticText(self, -1, "Duration", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(durr, pos=(2,0))
		ste = wx.StaticText(self, -1, "Steps", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(ste, pos=(3,0))
		miv = wx.StaticText(self, -1, "min V", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(miv, pos=(4,0))
		mav = wx.StaticText(self, -1, "Max V", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(mav, pos=(5,0))		
		octt = wx.StaticText(self, -1, "Octave", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(octt, pos=(6,0))
		pio = wx.StaticText(self, -1, "Sequence", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(pio, pos=(7,0))
		#SEQUENCERS
		for val in range(0, self.seqs):
			seq = Stepseq(parent = self, cSound = self.cSound, istance = val + 1)
			for vert_position in range(0, len(seq.stuff)):
				item = seq.stuff[vert_position]
				if vert_position < 8:
					self.gridSizer.Add(item, span=(1,2), pos=(vert_position,1 + val * 2))
				elif 8 <= vert_position < len(seq.stuff) - 8:
					self.gridSizer.Add(item, pos=(vert_position, 1 + val * 2))
				else:
					self.gridSizer.Add(item, pos=(vert_position - 8, 2 + val * 2))
		#Set sizer
		self.SetSizer(self.gridSizer)
		self.gridSizer.Fit(self)



class Stepseq():
	def __init__(self, parent, cSound, istance):
		self.parent = parent
		self.cSound = cSound
		self.istance = istance
		self.stuff =[]
		siz = wx.Size(65,-1)#size of floatspin
		font_s = wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		#ON OFF button
		self.startstopB = wx.ToggleButton(self.parent, -1, label='Stopped', size = siz)
		self.startstopB.SetFont(font_s)
		self.startstopB.Bind(wx.EVT_TOGGLEBUTTON, self.doStartStop)
		self.stuff.append(self.startstopB)
		#speed
		self.speedList = ["0.03125","0.0625", "0.125", "0.25", "0.333", "0.5", "0.666", "0.75", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"] 
		self.speedvalue = wx.ComboBox(self.parent, -1, choices=self.speedList, size= siz)
		self.speedvalue.SetFont(font_s)
		self.speedvalue.SetValue("1.0")
		self.speedvalue.Bind(wx.EVT_COMBOBOX, self.setSpeed)
		self.cSound.SetChannel("seqspe_"+str(self.istance), 1.0)
		self.stuff.append(self.speedvalue)
		#duration
		self.duration = fsm.FsmCs(parent=self.parent, id=-1,
											digits=3,
											min_val = 0.0,
											max_val = 1.0,
											increment=0.01,
											value = 0.5,
											size = siz,
											cSound = self.cSound,
											channel = "duration_"+str(self.istance))
		self.cSound.SetChannel("duration_"+str(self.istance), 0.5)
		self.stuff.append(self.duration)
		#number of steps
		self.steps = fsm.FsmCs(parent=self.parent, id=-1,
											digits=0,
											min_val = 1.0,
											max_val = 16.0,
											increment=1.0,
											value = 16.0,
											size = siz,
											cSound = self.cSound,
											channel = "steps_"+str(self.istance))
		self.cSound.SetChannel("steps_"+str(self.istance), 16.0)
		self.stuff.append(self.steps)
		#min vol
		self.minv = fsm.FsmCs(parent=self.parent, id=-1,
											digits=3,
											min_val = 0.0,
											max_val = 1.0,
											increment=0.001,
											value = 0.5,
											size = siz,
											cSound = self.cSound,
											channel = "minv_"+str(self.istance))
		self.cSound.SetChannel("minv_"+str(self.istance), 0.5)	
		self.stuff.append(self.minv)
		#max vol
		self.maxv = fsm.FsmCs(parent=self.parent, id=-1,
											digits=3,
											min_val = 0.0,
											max_val = 1.0,
											increment=0.001,
											value = 0.5,
											size = siz,
											cSound = self.cSound,
											channel = "maxv_"+str(self.istance))
		self.cSound.SetChannel("maxv_"+str(self.istance), 0.5)	
		self.stuff.append(self.maxv)
		#octave transposition
		self.octt = fsm.FsmCs(parent=self.parent, id=-1,
											digits=0,
											min_val = -2.0,
											max_val = 2.0,
											increment=1.0,
											value = 0.0,
											size = siz,
											cSound = self.cSound,
											channel = "octt_"+str(self.istance))
		self.cSound.SetChannel("octt_"+str(self.istance), 0.0)	
		self.stuff.append(self.octt)		
		#pitch scanning
		self.seqmodes = ["L to H","H to L", "B and F","Random"] 
		self.seqqua = wx.ComboBox(self.parent, -1, choices=self.seqmodes, size=siz)
		self.seqqua.SetValue("L to H")
		self.seqqua.Bind(wx.EVT_COMBOBOX, self.setPitSeq)
		self.cSound.SetChannel("seqqua_"+str(self.istance), 0)
		self.stuff.append(self.seqqua)
		#step checkboxes
		steps =[]
		for count in range(0, 16):
			ckb = wx.CheckBox(self.parent, -1, style=wx.CHK_2STATE, label=str(count))
			self.stuff.append(ckb)
			self.stuff[len(self.stuff)-1].Bind(wx.EVT_CHECKBOX, self.doCheckbox)
			
		
	def doStartStop(self, evt):
		"""launch record instrument"""
		obj = evt.GetEventObject()
		ispressed = obj.GetValue()
		if ispressed:
			obj.SetLabel('Playing')
			self.cSound.InputMessage('i %f 0 -1 %d\n' % (20 + 0.1 * self.istance, self.istance))
		else:
			obj.SetLabel('Stopped')
			self.cSound.InputMessage('i %f 0 -1\n' % (-20 - (0.1 * self.istance)))
			
	def setSpeed(self, evt):
		"""set the speed multiplier"""
		speed = float(self.speedList[self.speedvalue.GetSelection()])
		self.cSound.SetChannel("seqspe_"+str(self.istance), speed)
		
	def doCheckbox(self,evt):
		'''self.GetLabel()'''
		obj = evt.GetEventObject()
		step = int(obj.GetLabel())
		state = obj.IsChecked()
		#print step
		#write in a csound ftable
		if state:
			val = 1.0
		else:
			val = 0.0
		self.cSound.TableSet(10 + self.istance, step, val)
		
	def setPitSeq(self, evt):
		"""set the pitch scanning method"""
		order = self.seqqua.GetSelection()
		self.cSound.SetChannel("seqqua_"+str(self.istance), order)

		
		
