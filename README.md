# Handoff-simulation
This project simulates some handoff algrithms for wireless communications.

To understand the effect of various parameters like handoff initiation power value, movement of mobile devices, the number of channels per base station,
etc., on the handoff requests, we need a tool which helps visualize and show statistics regarding call drops, 
successful call drops, etc. I have developed a tool which simulates different handoff schemes namely:

1. Non-priority handoff scheme
2. Priority handoff scheme
3. Handoff call queuing scheme

The theory for the handoff schemes was referenced from **CHAPTER 1 Handoff in Wireless Mobile Networks, QING-AN ZENG, and DHARMA
P. AGRAWAL, Department of Electrical Engineering and Computer Science, University of Cincinnati**

The filenames and their uses are:

**Filename** | **Scheme**
------------| -------------
class1.py | Non-priority handoff scheme
class2.py | Priority handoff scheme
class3.py | Handoff call queuing scheme
handoff.py | TKinter GUI for the handoff visualisation
