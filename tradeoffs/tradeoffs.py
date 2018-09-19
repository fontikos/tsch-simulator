#!/usr/bin/env python3

import sys, os
import matplotlib.pyplot as plt
import matplotlib

# add library directory to path
SELF_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SELF_DIR, '..', "core"))

import sim

PRINTTOFILE = True
MAX_SLOT = 10
REPETITIONS = 100
NODES = 4


######################################

def simulate(packetsPerGw, prrlist, adaptive, slots):  
    stats = sim.Statistics(packetsPerGw)
    sim.simulateDedicated(stats, packetsPerGw, prrlist, adaptive, slots, MAX_SLOT)
    return stats

def printReport(stats, adaptive):
    print("Report")

    if adaptive == True:
        print("Adaptive Static Scheduling")
    else:
        print("Static Scheduling")

    for gw in stats.gwlist:
        print(gw.id, gw.u, gw.aslot)

    print(stats.pdr, stats.asn, stats.txrx, stats.sleeping, stats.idlelistening, stats.collisionsRx)

    print(stats.energy())
    print(stats.enef())   
    print("")

def run4nodes(p,t,a,slots):
    repeat = REPETITIONS
    N = NODES
    traffic = [t] * N
    prr = [p] * N
    adaptive = a

    sstats = sim.SuperStatistics(repeat)

    for i in range(0,sstats.repeat):
        sstats.stats[i] = simulate(traffic, prr, adaptive, slots)
        sstats.stats[i].adaptive = adaptive
        sstats.stats[i].prr = prr
        sstats.stats[i].tr = traffic

    return sstats


######################################################

def motivating_enef(t,filename):

    maxTraffic = MAX_SLOT
    lists = [None] * maxTraffic

    plist = [0.5, 0.6, 0.7, 0.8, 0.9]

    matplotlib.rcParams.update({'font.size': 18})
    plt.figure(figsize=(8,6))

    for p in plist:
        for i in range(0,maxTraffic):
            lists[i] = run4nodes(p,t,False,i+2)


        slots = [None] * len(lists)
        enef = [None] * len(lists)

        for i in range(len(lists)):
            slots[i] = lists[i].stats[0].gwlist[0].aslot
            enef[i] = lists[i].AverageEnef()
            #print(lists[i].StdEnef() / lists[i].AverageEnef())

        plt.plot(slots,enef, linestyle="-")

    plt.legend(["PRR = 0.5","PRR = 0.6","PRR = 0.7","PRR = 0.8","PRR = 0.9"])
    plt.grid()
    plt.xlabel("Active Slots")
    plt.ylabel("Energy per Reliably Delivered Packet (mJ)")
    plt.xlim([2,10])

    if PRINTTOFILE == True:
        plt.savefig(filename)
    else:    
        plt.show()

def motivating_enco(t,filename):

    maxTraffic = MAX_SLOT
    lists = [None] * maxTraffic

    plist = [0.5, 0.6, 0.7, 0.8, 0.9]

    matplotlib.rcParams.update({'font.size': 18})
    plt.figure(figsize=(8,6))

    for p in plist:
        for i in range(0,maxTraffic):
            lists[i] = run4nodes(p,t,False,i+2)


        slots = [None] * len(lists)
        enco = [None] * len(lists)

        for i in range(len(lists)):
            slots[i] = lists[i].stats[0].gwlist[0].aslot
            enco[i] = lists[i].AverageEnco()
            #print(lists[i].StdEnef() / lists[i].AverageEnef())

        plt.plot(slots,enco, "-")

    plt.legend(["PRR = 0.5","PRR = 0.6","PRR = 0.7","PRR = 0.8","PRR = 0.9"])
    plt.grid()
    plt.xlabel("Active Slots")
    plt.ylabel("Energy per Packet (mJ)")
    plt.xlim([2,10])

    if PRINTTOFILE == True:
        plt.savefig(filename)
    else:    
        plt.show()

def motivating_pdr(t,filename):

    maxTraffic = MAX_SLOT
    lists = [None] * maxTraffic

    plist = [0.5, 0.6, 0.7, 0.8, 0.9]

    matplotlib.rcParams.update({'font.size': 18})
    plt.figure(figsize=(8,6))

    for p in plist:
        for i in range(0,maxTraffic):
            lists[i] = run4nodes(p,t,False,i+1)


        slots = [None] * len(lists)
        pdrl = [None] * len(lists)

        for i in range(len(lists)):
            slots[i] = lists[i].stats[0].gwlist[0].aslot
            pdrl[i] = lists[i].AveragePDR()
            #print(lists[i].StdEnef() / lists[i].AverageEnef())

        plt.plot(slots,pdrl,"-")

    plt.legend(["PRR = 0.5","PRR = 0.6","PRR = 0.7","PRR = 0.8","PRR = 0.9"])
    plt.grid()
    plt.xlabel("Active Slots")
    plt.ylabel("PDR (%)")
    plt.xlim([2,10])
    
    if PRINTTOFILE == True:
        plt.savefig(filename)
    else:    
        plt.show()

######################################
print("running")
motivating_pdr(4,"pdr-4ppf.pdf")
print("done")
#motivating_pdr(2,"pdr-2ppf.pdf")
#print("done")
motivating_enef(4,"enef-4ppf.pdf")
print("done")
motivating_enco(4,"enco-4ppf.pdf")
print("done")
#sim.main()
