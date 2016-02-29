<CsoundSynthesizer> 
<CsOptions>
-odac
</CsOptions> 
<CsInstruments> 
sr = $SRATE
ksmps = $KRATE
nchnls = 2
0dbfs = 1
zakinit 4, 1
;TUNING
;MIDI 0 = 8Hz


;											0		1	2	 3b	3   4  5b   5    6b
ginumer ftgen 1, 0, 16, -2, 1, 256, 9, 32, 81, 4, 1024, 3, 128, 27, 16, 243 
gidenom ftgen 2, 0, 16, -2, 1, 243, 8, 27, 64, 3, 729, 2, 81, 16, 9, 128
gibasicNotes ftgen 3, 0, 16, -2, 8, 8*256/243, 8*9/8, 8*32/27, 8*81/64, 8*4/3, 8*1024/729, 8*3/2, 8*128/81, 8*27/16, 8*16/9, 8/243/128

giWave ftgen 6, 0, 16384, 10, 1

giActive ftgen 10, 0, 128, -2, 0

giSeq1 ftgen 11, 0, 16, -2, 0
giSeq2 ftgen 12, 0, 16, -2, 0
giSeq3 ftgen 13, 0, 16, -2, 0


chn_k "bpm", 1
gkbpm init 60
chn_k "porta", 1
gkporta init 0
chn_k "lowest", 1
gklowest init 0
;tuning
chn_k "tempera", 1
gktempera init 0
chn_k "tuning", 1
gktuning init 0


;reverb channels
chn_k "reverbFe", 1
chn_k "reverbFr", 1
chn_k "reverbDW", 1
chn_k "reverbLFr", 1

instr 1
gkbpm chnget "bpm"
gkporta chnget "porta"
gklowest chnget "lowest"
gktempera chnget "tempera"
gktuning chnget "tuning"

;calculate lowest frequency
klowc init 8
if gktuning == 0 then
	klowc = 8
else
	klowc = 8.176
endif

if gktempera == 0 then
	klowest_oct = int(gklowest / 12)
	klowest_sem = gklowest % 12
	klowest_num tab klowest_sem, ginumer
	klowest_den tab klowest_sem, gidenom
	gklowest_Hz = klowc * (2 ^ klowest_oct) * klowest_num / klowest_den
else
	gklowest_Hz = klowc
endif

;start output instrument
event_i "i", 100, 0, -1
printk2 gklowest
endin



instr 10;Split Synth
;TUNING
;p4 midi note
if gktempera == 0 then
	kdiff = p4 - gklowest
	kdiff_oct = int(kdiff / 12)
	kdiff_sem = kdiff % 12
	kdiff_sem wrap kdiff_sem, 0, 12
	kdiff_num tab kdiff_sem, ginumer
	kdiff_den tab kdiff_sem, gidenom
	kfreq = gklowest_Hz * (2 ^ kdiff_oct) * kdiff_num / kdiff_den
else
	kfreq = gklowest_Hz * semitone(p4)
endif

kfreqport line 0.0001, 0.01, 1.0
kfreqp portk kfreq, 0.009 + kfreqport * gkporta * 60 / gkbpm

ScannelVol sprintf "vol_%d", p4
ScannelPan sprintf "pan_%d", p4
ScannelSpe sprintf "spe_%d", p4

kvol chnget ScannelVol
kpan chnget ScannelPan
kspe chnget ScannelSpe

kpanp portk kpan, 0.05 + gkporta * 60 / gkbpm
kvolp portk kvol, 0.05 + gkporta * 60 / gkbpm
kspep portk kspe, 0.05 + gkporta * 60 / gkbpm

kenv linsegr 0, 0.02, 1.0, 0.35, 0

kfreq1 = kfreqp + kspep * .5 * gkbpm / 60
kfreq2 = kfreqp - kspep * .5 * gkbpm / 60
ao1 oscil kvolp, kfreq1, giWave
ao2 oscil kvolp, kfreq2, giWave
al1 limit ao1, 0, 1
al2 limit ao2, -1, 0
aout = (al1 + al2) * kvolp * kenv * .25
aL, aR pan2 aout, kpanp
zawm aL, 0
zawm aR, 1

endin



instr 20;step sequencer
Sspeed sprintf "seqspe_%d", p4
kspeed chnget Sspeed
Sduration sprintf "duration_%d", p4
kduration chnget Sduration
Ssteps sprintf "steps_%d", p4
ksteps chnget Ssteps
Sminv sprintf "minv_%d", p4
kminv chnget Sminv
Smaxv sprintf "maxv_%d", p4
kmaxv chnget Smaxv
Soctt sprintf "octt_%d", p4
koctt chnget Soctt
Smetho sprintf "seqqua_%d", p4
kmetho chnget Smetho


kstep_index init 0
knote_index init 0;giActive
knoteqty_index init 0
kpitdirection init 1
ktrig metro kspeed * gkbpm / 60
if ktrig == 1 then
	kstep_index = (kstep_index + 1) % ksteps
	kstp tab kstep_index, 10 + p4
	if kstp == 1 then
		knoteqty tab knoteqty_index, 10
		;how to read list of pitch
		if kmetho == 0 then;low to high
			knote_index = (knote_index + 1) % knoteqty
			knote tab knote_index + 1, 10
		elseif kmetho == 1 then;high to low da rivedere limiti
			knote_index wrap (knote_index - 1), 0, knoteqty
			knote tab knote_index + 1, 10
		elseif kmetho == 2 then;back and forth
			knote_index wrap (knote_index + kpitdirection), 0, knoteqty
			if (knote_index == 0) || (knote_index == knoteqty - 1) then
				kpitdirection = -1 * kpitdirection
			endif
			knote tab knote_index + 1, 10
		else;random
			knote_index random 0, knoteqty - 1
			knote_index = int(knote_index)
			knote tab knote_index + 1, 10
		endif
		kvol random kminv, kmaxv
		event "i", 25 + 0.1 * p4 + 0.001 * kstep_index, 0, kduration * kspeed * 60 / gkbpm, kvol, knote, koctt
	endif
endif
endin

instr 25;sequencer audio
;envelope
iatt init 0.06
idec init 0.03 + p4 * 0.02
kenvelopeatt linseg 0, iatt, p4, idec, p4 * 0.7
kenveloperel line 1, p3, 0
kenvelope = kenvelopeatt * kenveloperel
;tuning
itempera = i(gktempera)
ilowest_Hz = i(gklowest_Hz)
if itempera == 0 then
	ilowest = i(gklowest)
	idiff = p5 - ilowest
	idiff_oct = int(idiff / 12)
	idiff_sem = idiff % 12
	idiff_sem wrap idiff_sem, 0, 12
	idiff_num tab_i idiff_sem, ginumer
	idiff_den tab_i idiff_sem, gidenom
	ifreqb = ilowest_Hz * (2 ^ idiff_oct) * idiff_num / idiff_den
else
	ifreqb = ilowest_Hz * semitone(p5)
endif
;octave
if p6 == -2 then
	ioctmul = 0.25
elseif p6 == -1 then
	ioctmul = 0.5
elseif p6 == 1 then
	ioctmul = 2.0
elseif p6 == 2 then
	ioctmul = 4.0
else
	ioctmul = 1.0
endif

ifreq = ioctmul * ifreqb

;synthesis
acarrier oscil kenvelope, ifreq, giWave
aL zar 0
aR zar 1
aaudio = acarrier * (aL + aR) * kenvelope * 3

;random panning
aoutL, aoutR pan2 aaudio * kenvelope, 0.5 + birnd(0.3)

;output
zawm aoutL, 2
zawm aoutR, 3
endin


instr 100
aL10 zar 0
aR10 zar 1
aLSE zar 2
aRSE zar 3
;reverb
kosciV chnget "osciV"
kseqV chnget "sequV"
kosciVp portk kosciV, 0.05 + gkporta * 60 / gkbpm
kseqVp portk kseqV, 0.05 + gkporta * 60 / gkbpm




kinsnum init 10
kactive10 active kinsnum
kactive10p port kactive10, 0.5

aL = aL10 * sqrt(kactive10p + 1) * kosciVp + aLSE * kseqVp
aR = aR10 * sqrt(kactive10p + 1) * kosciVp + aRSE * kseqVp


;reverb
kfblvl chnget "reverbFe"
kfco chnget "reverbFr"
krdw chnget "reverbDW"
khp chnget "reverbLFr"
kfblvlp port kfblvl, 0.05
kfcop portk kfco, 0.05 + gkporta * 60 / gkbpm
krdwp portk krdw, 0.05 + gkporta * 60 / gkbpm
khpp portk khp, 0.05 + gkporta * 60 / gkbpm


denorm aL, aR
alhr, arhr reverbsc aL, aR, kfblvlp, kfcop
alhr buthp alhr, khpp
arhr buthp arhr, khpp

apoL = aL * cos(krdwp * $M_PI_2) + alhr * sin(krdwp * $M_PI_2)
apoR = aR * cos(krdwp * $M_PI_2) + arhr * sin(krdwp * $M_PI_2)

outs apoL, apoR
zacl 0, 3

ktrigVUmeter metro 3
koutVU_rmsL max_k apoL, ktrigVUmeter, 1
koutVU_rmsL_db = dbfsamp(koutVU_rmsL)
chnset koutVU_rmsL_db, "outVUmeterL"
koutVU_rmsR max_k apoR, ktrigVUmeter, 1
koutVU_rmsR_db = dbfsamp(koutVU_rmsR)
chnset koutVU_rmsR_db, "outVUmeterR"

;printk2 kactive10
;printk2 gklowest
endin



instr 101;record output
aL, aR monitor
idata date
Sfile sprintf "recordings/%i_recording.wav", idata
fout Sfile, 14, aL, aR
endin




</CsInstruments> 
<CsScore> 
;test
;i 10 0 1 55




;Run
i1 0 1000
</CsScore> 
</CsoundSynthesizer> 
