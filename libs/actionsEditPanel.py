import wx
import csnd6
import os
import fsm
import language


class ActionsPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(ActionsPanel, self).__init__(*a, **k)#super the subclass
		
		#self.SetBackgroundColour((250, 200, 200))
		siz = wx.Size(70,-1)#size of floatspin
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		#target object
		par = self.GetParent()
		parr = par.GetParent()
		self.target = parr.GetParent()

		
		#File field
		self.filename = self.retriveLastFile()
		self.filesizer = wx.BoxSizer(wx.HORIZONTAL)
		self.newB = wx.Button(self, -1, label='New')
		self.Bind(wx.EVT_BUTTON, self.doNewF, self.newB)
		self.filesizer.Add(self.newB, 0,flag=wx.EXPAND)
		self.openB = wx.Button(self, -1, label='Open')
		self.Bind(wx.EVT_BUTTON, self.doOpenF, self.openB)
		self.filesizer.Add(self.openB, 0,flag=wx.EXPAND)
		self.saveasB = wx.Button(self, -1, label='SaveAs')
		self.Bind(wx.EVT_BUTTON, self.doSaveAsF, self.saveasB)
		self.filesizer.Add(self.saveasB, 0,flag=wx.EXPAND)
		
		
		self.fileT = wx.StaticText(self, -1, "File: " + self.filename, style= wx.ALIGN_CENTER | wx.TE_RICH)
		#self.file = wx.TextCtrl(parent = self, id = -1, style = wx.TE_READONLY|wx.TE_AUTO_URL)
		#Hystory field
		self.hystoryT = wx.StaticText(self, -1, "History", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.hystory = wx.TextCtrl(parent = self, id = -1, size = (300, 500), style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL)
		
		
		#Create Serie
		self.seriecodeT = wx.StaticText(self, -1, "Command", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.seriecode = wx.TextCtrl(self, -1)
		
		self.serieB = wx.Button(self, -1, label='Do')
		self.Bind(wx.EVT_BUTTON, self.doSerie, self.serieB)
		self.openMem()
		self.hystindex = len(self.memory) - 1
		
		self.sizer.AddSpacer(5,flag=wx.EXPAND)
		self.sizer.Add(self.filesizer, 0,flag=wx.EXPAND)
		self.sizer.Add(self.fileT, 0,flag=wx.EXPAND)
		self.sizer.AddSpacer(5,flag=wx.EXPAND)
		self.sizer.Add(self.hystoryT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.hystory, -1,flag=wx.EXPAND)
		self.sizer.AddSpacer(5,flag=wx.EXPAND)
		self.sizer.Add(self.seriecodeT, 0,flag=wx.EXPAND)
		self.sizer.Add(self.seriecode, 0,flag=wx.EXPAND)
		self.sizer.Add(self.serieB, 0,flag=wx.EXPAND)


		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
		
		self.timers_storage = []
		self.timers_actions = []
		self.timeMultip = 0.0
		self.futureItem = []


	def OnClose(self, evt):
		'''kill stored timers'''
		for timer in self.timers_storage:
			timer.Stop()
		self.Destroy()
		
	
		
		
	
	def doSerie(self, evt):
		'''list separated by space'''
		string = self.seriecode.GetValue().encode()
		self.memory.append(string)
		#print self.memory
		f = open("save/" + self.filename,"a")
		f.write(string+"\n")
		f.close()
		self.hystory.AppendText(string+'\n')#add to hystory
		self.hystindex = len(self.memory) - 1
		list = language.divideGroups(string)
		for item in list:
			if self.target.keypanel.minpoly < item[0] < self.target.keypanel.maxpoly:
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
					#print "UNtimed"
					if item[1] >= 0.0:
						vol = item[1]
						if vol > 1.0:
							vol = 1.0
						self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].vol.SetValue(vol)
						self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].vol.emitValue(evt)
					else:
						vol = self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].vol.GetValue()
					if item[2] >= 0.0:
						self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].pan.SetValue(item[2])
						self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].pan.emitValue(evt)
					if item[3] >= 0:
						spe=self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].speedList[item[3]]
						self.target.keypanel.oscillators[item[0]  - self.target.keypanel.minpoly].speedvalue.SetValue(spe)
						self.cSound.SetChannel("spe_"+str(item[0]), item[3])

	def retriveLastFile(self):
		'''read the last file used'''
		f = open("save/DoNoteDeleteMe","r")
		data="".join(line.rstrip() for line in f)
		f.close()
		return data


	def setLastFile(self):
		f = open("save/DoNoteDeleteMe","w")
		f.write(self.filename)
		f.close()


	
	def openMem(self):
		'''load the list of commands'''
		f = open("save/" + self.filename,"r")
		self.memory =[]
		for line in f:
			self.memory.append(line.rstrip('\n'))
		f.close()
		for line in self.memory:
			self.hystory.AppendText(line+'\n')



	def timerActionStart(self):
		'''start a timer for future event'''
		#obj = evt.GetEventObject.GetParent()
		parentpanel = self.GetParent()
		time = int(1000 * self.timeMultip * 60 / self.target.topp.bpm.GetValue())#calculate time
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
		note = self.timers_actions[ind][0]
		vol = self.timers_actions[ind][1]
		pan = self.timers_actions[ind][2]
		mod = self.timers_actions[ind][3]
		if vol >= 0.0:
			if vol > 1.0:
				vol = 1.0
			self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].vol.SetValue(vol)
			self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].vol.emitValue(evt)
		else:
			vol = self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].vol.GetValue()
		if pan >= 0.0:
			self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].pan.SetValue(pan)
			self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].pan.emitValue(evt)
		if mod >= 0:
			spe = self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].speedList[mod]
			self.target.keypanel.oscillators[note - self.target.keypanel.minpoly].speedvalue.SetValue(spe)
			self.cSound.SetChannel("spe_"+str(note), mod)
		#parent.keypanel.find_lowest_oscillator_single(note,vol)	
		#delete timer
		del self.timers_storage[ind]
		#delete action
		del self.timers_actions[ind]
		


	def doSaveAsF(self, event):
		saveFileDialog = wx.FileDialog(self, "Save As", "save/", "", 
					"Text files (*.txt)|*.txt", 
					wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		saveFileDialog.ShowModal()
		p = saveFileDialog.GetPath()
		head, tail = os.path.split(p)
		#copy in new file
		fr = open("save/" + self.filename, "r")
		fw = open("save/" + tail, "w")
		fw.write(fr.read())
		fr.close()
		fw.close()
		#new filename
		self.filename = tail
		self.hystory.Clear()
		#update record
		self.setLastFile()
		#update the label
		self.fileT.SetLabel("File: " + self.filename)
		self.sizer.Layout()
		saveFileDialog.Destroy()



	def doOpenF(self, event):
		openFileDialog = wx.FileDialog(self, "Open", "save/", "", 
					"Text files (*.txt)|*.txt", 
					wx.FD_OPEN | wx.FD_OVERWRITE_PROMPT)
		openFileDialog.ShowModal()
		p = openFileDialog.GetPath()
		head, tail = os.path.split(p)
		self.filename = tail
		#clear the text
		self.hystory.Clear()
		#load the data
		self.openMem()
		#update record
		self.setLastFile()
		#update the label
		self.fileT.SetLabel("File: " + self.filename)
		self.sizer.Layout()
		#kill dialog
		openFileDialog.Destroy()



	def doNewF(self, event):
		'''create and set a new file'''
		self.filename = "unsaved"
		self.hystory.Clear()
		f = open("save/" + self.filename,"w")
		f.close()
		self.setLastFile()
		self.fileT.SetLabel("File: " + self.filename)
		self.sizer.Layout()
		


class actionEditFr(wx.Frame):
	"""Main frame"""
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(actionEditFr, self).__init__(*a, **k)#super the subclass
		self.Bind(wx.EVT_CLOSE, self.on_close)
		
		panel = ActionsPanel(self, -1, cSound=self.cSound)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(panel, 0,wx.EXPAND)
		self.SetSizer(sizer)
		sizer.Fit(self)
		self.Show()
	
	def on_close(self, evt):
		'''remove itself from the parent list of open istances
		then destroy itself'''
		for item in self.GetParent().openFr:
			if item == self:
				self.GetParent().openFr.remove(item)
		#self.saveVals()
		self.Destroy()
		


if __name__ == '__main__':
	app = wx.App(False)#True to redirect stdin/sterr
	frame = actionEditFr(None, title='test')
	app.MainLoop()