Dialup modem (V.34) start-up signalling sequence: Spectral perspective
######################################################################
:date: 2012-03-29 22:42
:author: sauravtuladhar
:category: signalprocessing
:slug: spectrgram-view-of-the-v34-start-up-signalling
:status: published

If you are one of those who jumped onto the internet bandwagon from the days of dial-up connection, then you must be familiar with a sequence of sounds  the modem makes before the connection was established with the ISP. I started my internet surfing days listening to that peculiar sound. Back in those days I had a vague idea that the modem was actually transferring data over the copper pair line that was only being used for voice before that. But I was I didnt' know what the strange sequence of sound was.

**V.34** is the standard protocol recommended by ITU for modems operating on legacy copper pair. The V.34 allows upto 33.8 kbit/s bidirectional data transfer. ( `Refer <https://en.wikipedia.org/wiki/V.34>`__ to Wikipedia for more )

Today I came across a recording of the V.34 dialup modem startup signalling audio sequence (`here <http://www.dspcsp.com/wavefiles/4v34.wav>`__) and I decided to take a look at its spectral content. The figure below shows the temporal and spectrogram plot of ~18s of of signalling sequence. ( The total startup time for V.34 modem is about 10 - 13s)

|Spectrogram|

Then I looked up the start up signalling sequence for V.34 protocol and found this `paper <http://www.doc.ic.ac.uk/~costa/cn_slides/v34.pdf>`__. Briefly the startup signalling involves four phases which can be summarized infollowing steps ( focus on frequency content of signalling signals ):

Phase I ( Network interaction )

-  A 2100Hz  answer tone modulated with 15Hz sine wave is exchanged. ( The 15Hz modulated sine wave is not distinct in the spectrogram, but I will take faith on the specification for V.34 that it is present )

Phase II ( Ranging and probing )

-  This phase involves three steps :  Initial information exchange [INFO0], Probing & Rangin and a second information exchange [INFO2]
-  The information exchange is done at 600bps using DPSK modulated FDM tones at 1200Hz and 2400Hz
-  Probing is used to estimate channel characteristic. The probing signals consists of set of tones 150Hz apart starting from 150Hz to 3750Hz. However, tones at 900, 1200, 1800 and 2400Hz are omitted.

Phase III ( Equalize and training )

-  This phase consists of a series of signals transmitted between the calling and the answering modem. The exchange consists of a sequence of scrambled binary 1s for fine tuning of the equalizer and echo canceller, and a repeating 16-bit scrambled sequence indicating the constellation size that will be used during. These scrambled sequences are transmitted using a four-point constellation.  The scrambled sequence occupies the entire channel bandwidth.

Phase IV (Final duplex training )

-  This phase consists of a sequence of scrambled binary 1s  using either a 4- or 16-point QAM constellation.

I have tired to identify these sequence of events in the spectrogram above ( `Larger version <http://sauravtuladhar.files.wordpress.com/2012/03/v34_specgram_large.png>`__ ). All of the signalling sequences listed above can be identified in the spectrogram.  There was at least two set of signalling tones that I could not associate with the specification on V.34 protocol.

( Spent couple of hours this afternoon doing this exercise. Coming around more than 10 years after the days of dialup, this was a nice trip down the memory lane and moreover I can see what was going on the scene everytime my modem dialed up to the ISP )

.. |Spectrogram| image:: http://sauravtuladhar.files.wordpress.com/2012/03/v34_specgram_large1.png?w=1024
   :class: wp-image-141
   :width: 614px
   :height: 446px
   :target: http://sauravtuladhar.files.wordpress.com/2012/03/v34_specgram_large1.png
