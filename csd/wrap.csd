<CsoundSynthesizer>
<CsOptions>
; Select audio/midi flags here according to platform
-odac    ;;;realtime audio out
;-iadc    ;;;uncomment -iadc if realtime audio input is needed too
; For Non-realtime ouput leave only the line below:
; -o wrap.wav -W  ;;; for file output any platform
</CsOptions>
<CsInstruments>

sr = 44100 
ksmps = 32 
0dbfs  = 1 
nchnls = 2

instr    1

iout  wrap  p4, 0, 12
print iout

  
endin

</CsInstruments>
<CsScore>

;           
i1  0  1    0 
i1  1  1    1
i1  2  1    11
i1  3  1    12
i1  3  1    -1
e
</CsScore>
</CsoundSynthesizer>
