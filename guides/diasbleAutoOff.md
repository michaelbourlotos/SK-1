# Converted from: https://web.archive.org/web/20081204105041/http://www.electri-fire.com/sk1autopoweroff.htm

# [Electri-fire's Site](https://web.archive.org/web/20081204105041/http://www.electri-fire.com/)

### Disable the sk-1 auto power off 

The sk-1 turns itself off when no key or button is pressed for approximately 7 minutes. This is called the auto power off function. 

Disabling this function is usefull for those that want to leave their sk-1 unattended for a while and keep it on to remain in the state they left it. 

**How does the auto power off work?**

By a voltage at PO1 pin 86 that goes Low after 7-8 minutes (schematic can be found in the service manual).

This is the auto power off signal that turns the sk-1 off. The trace leaving this pin needs to be kept High to disable auto power off.   
  
As the cpu works with a ground voltage of -5 volt and 0 volt as a "positive" , Low is -5V , High is 0 Volts.   
Disconnect PO1 from it's trace , connect the trace at 0 volt instead. No more auto power down.   
  
**How can this be done easily?**

No need to grind through the trace. There's a jumper that can be disconnected.   
  
PO1 at pin 86 runs along the top of the PCB (solderside, speaker left).   
The topmost THIN trace underneeth the Fat trace that leads to a jumper.  
Remove this jumper, wire left side to 0 Volt.   
For 0V I used the solder point most left/down of the board . At he green and blue wires.

![](../images/sk1AutoPowerOffDisable.JPG)


