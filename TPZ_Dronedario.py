#!/usr/bin/python

import os
import wx
import csnd6
import libs.topPanel as topPanel
import libs.keybPanel as keybPanel
import libs.actionsPanel as actionsPanel
import libs.stepseqPanel as stepseqPanel
import libs.tuningPanel as tuningPanel


#CSND CODE###########################################################
###################################################################
###################################################################
c = csnd6.Csound()    # create an instance of Csound

file = "csd/Dronedario.csd"

c.Compile(file)     # Compile Orchestra from String

perfThread = csnd6.CsoundPerformanceThread(c)
#performance thread RUN
#perfThread.Play()

#Callback from csound
def callableFunct(c):
	'''to test callbacks'''
	#frame.keypanel.getactivelist()
	return


#GUI CODE###########################################################
###################################################################
###################################################################
#Frame
class TopFrame(wx.Frame):
	"""Main frame"""
	def __init__(self, parent, title):
		super(TopFrame, self).__init__(parent= parent, title = title,
													#size=(960, 390),
													#style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER |wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))#super the subclass
													style=wx.DEFAULT_FRAME_STYLE ^ (wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))#super the subclass
		
		#panel
		self.vboxsizer = wx.BoxSizer(wx.VERTICAL)
		self.vboxsizer.AddSpacer(5,flag=wx.EXPAND)
		#self.vboxsizer.AddSpacer(10,flag=wx.EXPAND)
		self.topp = topPanel.TopPanel(self, -1, cSound=c)
		self.vboxsizer.Add(self.topp, 0,wx.EXPAND)
		self.vboxsizer.AddSpacer(3,flag=wx.EXPAND)
		
		
		
		self.midsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.midsizer.AddSpacer(3,flag=wx.EXPAND)
		
		self.oscisizer = wx.BoxSizer(wx.VERTICAL)
		minmidi = 36
		octaves = 6
		self.keypanel = keybPanel.KeybPanel(self, -1, minpoly=36, maxpoly=minmidi + octaves * 12, cSound=c)
		self.oscisizer.Add(self.keypanel, 0,wx.EXPAND)
		self.oscisizer.AddSpacer(5,flag=wx.EXPAND)
		self.osciactionpanel = actionsPanel.ActionsPanel(self, -1, cSound=c)
		self.oscisizer.Add(self.osciactionpanel, 0,wx.EXPAND)
		
		self.midsizer.Add(self.oscisizer, 0,wx.EXPAND)
		self.midsizer.AddSpacer(3,flag=wx.EXPAND)
		
		self.rightsizer = wx.BoxSizer(wx.VERTICAL)
		self.seq = stepseqPanel.StepseqPanel(self, -1, cSound=c, seqs = 3)
		self.tunpanel = tuningPanel.TuningPanel(self, -1, cSound=c)
		self.rightsizer.Add(self.tunpanel, 0,wx.EXPAND)
		self.rightsizer.AddSpacer(5,flag=wx.EXPAND)
		self.rightsizer.Add(self.seq, -1,wx.EXPAND)
		
		self.midsizer.Add(self.rightsizer, 0,wx.EXPAND)
		
		self.vboxsizer.Add(self.midsizer, 0,wx.EXPAND)
		self.vboxsizer.AddSpacer(5,flag=wx.EXPAND)
		self.SetSizer(self.vboxsizer)
		self.vboxsizer.Fit(self)
		self.Show()


	def OnClose(self, event):
		#stop all the timers created
		#self.topp.timerRefresh.Stop() 
		#self.keypanel.timer.Stop() 
		#destroy
		self.Destroy()
		print "/OnClose"


class AppWithTerm(wx.App):
	"""wx.App subclassed to include csound Thread termination"""
	def OnExit(self):
		#print "Closing csnd Thread"
		perfThread.Stop()
		#print "Stopped csnd Thread"
		perfThread.Join()
		#print "Closed csnd Thread"
		return


app = AppWithTerm(False)#True to redirect stdin/sterr
frame = TopFrame(None, title='Dronedario')

FONT1 = wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
FONT2 = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
SIZE = wx.Size(65,-1)


#callback
#perfThread.SetProcessCallback(callableFunct, c)

#Csound performance thread RUN
perfThread.Play()

#frame.Show()
app.MainLoop()
