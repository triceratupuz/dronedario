import wx
import csnd6
import fsm
import oscillatorPanel



class KeybPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.maxpoly = k.pop('maxpoly', None)
		self.minpoly = k.pop('minpoly', None)
		super(KeybPanel, self).__init__(*a, **k)#super the subclass
		#self.SetBackgroundColour((0, 253, 0))
		siz = wx.Size(70,-1)#size of floatspin
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		self.oscillators =[]
		for item in range(self.minpoly, self.maxpoly):
			notetext = notes[item % 12]
			oscillo = oscillatorPanel.OscillatorPanel(self, -1, counter = item, title = notetext, cSound=self.cSound)
			self.oscillators.append(oscillo)
		
		perRow = 11
		row =1
		maxrows = (self.maxpoly - self.minpoly) / perRow
		col = 0
		self.gridSizer  = wx.GridBagSizer(vgap=5, hgap=5)
		for count in range(0, len(self.oscillators)):
			self.gridSizer.Add(self.oscillators[count], pos=(maxrows - row,col))
			if col == perRow:
				col = 0
				row += 1
			else:
				col +=1
		#print maxrows	
		#print row	
		self.minoscillator = self.minpoly
		self.SetSizer(self.gridSizer)
		self.gridSizer.Fit(self)
			
		self.oldactivelist =[]
			
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.find_active_oscillators, self.timer)
		self.timer.Start(20)
		self.indcall = 0
		
		#Lowest oscillator
		self.lowest = self.minpoly


	def OnClose(self, evt):
		#stop all the timers created
		self.timer.Stop() 
		#destroy
		self.Destroy()
		
	

	def find_active_oscillators(self, evt):
		'''called by csound to have active instruments'''
		newactivelist = []
		for n in range(0, 128):
			st = self.cSound.TableGet(101, n)
			if st > 0:
				newactivelist.append(n)
		if (newactivelist <> self.oldactivelist):
			sumlist = list(newactivelist)
			sumlist.extend(x for x in self.oldactivelist if x not in sumlist)
			if len(newactivelist) > 0:#there are active oscillators
				message = "f 10 0 128 -2 %d" % len(newactivelist)
				#print newactivelist
				for value in newactivelist:
					message = message + (" %d" % value)
				#send the list to csound for sequencers
				#print message
				self.cSound.InputMessage(message + "\n")
				for item in sumlist:
					if item in newactivelist and item not in self.oldactivelist:
						self.oscillators[item - self.minpoly].isAlive = True
						#self.oscillators[item - self.minpoly].isLowest = False
						self.oscillators[item - self.minpoly].setColourBack()
						# visualizza come attivo
					if item not in newactivelist and item in self.oldactivelist:
						self.oscillators[item - self.minpoly].isAlive = False
						#self.oscillators[item - self.minpoly].isLowest = False
						self.oscillators[item - self.minpoly].setColourBack()
						# visualizza come disattivato
			elif len(newactivelist) <= 0:
				for item in self.oldactivelist:
					self.oscillators[item - self.minpoly].isAlive = False
					#self.oscillators[item - self.minpoly].isLowest = False
					self.oscillators[item - self.minpoly].setColourBack()
					# visualizza come disattivato
				message = "f 10 0 128 -2 0"
				self.cSound.InputMessage(message + "\n")
			self.oldactivelist = list(newactivelist)
		


