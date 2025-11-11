# Converted from: https://web.archive.org/web/20081204104047/http://www.electri-fire.com/drumvolumekill.htm

### The` Drum kill ` mod 

How to kill sk-1 drum sounds:

This boardscan has the speaker on the right side.  
The drumsounds leave the cpu (square chip) at pin 97. This pin seems unconnected, but runs beneath the cpu and emerges in the right lower corner to the small jumper 1cm to the right.

Gray is Percussion (drums)

The Raw waves from the CPU, pre envelope and pre filter. 

Green CPU pin 93 is Melody 

Pink is CPU pin 94 Melody or Obbligato /all latter in Chord MODE setting

White is CPU pin 95 Melody or Chord

Blue is CPU pin 96 Bass or Melody 

![](../images/sk1%20sound%20lines.JPG)

The next picture shows the other side of the board. I´ll have to make new one, as the drum mod has not yet been done on this board . 

The jumper between the orange and blue wires is the AutoPowerOff line. [How to disable AutoPowerOff here.](../guides/diasbleAutoOff.md)

Up and left between white and red, not relevant for this page. 

Then left of that, partly behind the capacitor, the smaller jumper is the Drum wave. This could be replaced for drum kill or volume mods. 

![](../images/sk-1%20pin%2061-88%20jumpers\.JPG)

So, the drum jumper... 

There are several options here. 

Classic Drum kill would simply replace the jumper with a switch. 

I´ve tried several other schemes... 

For DRUM volume DISCONNECT the jumper and insert a 100k linear pot. Middle lug takes the cpu side (upper side in above picture), left lug to ground for zero volume , right lug for max. volume to the other side of the jumper. 

Bypassing the filter section gets really loud and snappy . When I used to be more into the drum side of the sk1 I had the raw wave at a momentary switch connecting to a point post filter for unfiltered accents. I forgot the exact location, but as you can see it´s a small aerea. You´ll find it easily. 

I´ve tried connecting the raw drum wave to other points in the filter/amp aerea for filter and envelope effects. In above boardscan this aerea is at the right side of the board. There are several interesting options. 

You may want to see the [Envelope circuits page](../guides/envelopeCircuits.md). Play a note in Chord Mode and do some poking with the raw drum/percussion wave (or other raw waveforms) in the envelope aereas. This lets you apply other rhytms (and filtering) to the waves. 

WARNING: transistors in these aereas fry easily. Do precision poking and avoid stationary voltages. 

