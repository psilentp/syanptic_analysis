# coding= utf-8
import read_header_2 as rh
import numpy as np
import ephys as ep
import pylab as plb
from params import *


def md_fig(cennum):
    #plb.box(on='off')
    import quantities as quan
    traces = load_cell(cennum)
    if cennum > 32:
        vh = [-90,60,-75,45,-60, 30,-45,15,-30, 0,-15]
    else:
        vh = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60]
        #vh = [-75, -60, -45, -30, -15,   0,  15,  30,  45,  60]
    current_list = list()
    
    vh = [v-15.0 for v in vh]
    for i,trace in enumerate(traces):
        epoch = trace.ts(725.0,975.0,tunits = 'ms')
        swp = trace.ts(725.0,975.0,tunits = 'ms')
        epoch = epoch.sub_baseline(0,100,tunits = 'ms')
        chtr = epoch.integrate(100,250,tunits = 'ms')
        chtr = chtr/quan.Quantity(100,'ms')
        chtr.units = 'pA'
        epoch.set_yunits('pA')
        swp.set_yunits('pA')
        if i > 10:
            i=np.mod(i,11)
        current_list.append((vh[i],chtr,epoch,swp))
        #current_list.append(epoch)
    
    num_trials = len(current_list)/11
    f = plb.figure(figsize=(12,8))
    ###scatter plot
    a1 = make_axes(0.55,0.9,0.1,0.5)
    colors = ['Green','Maroon','Olive','Teal','Purple','SaddleBrown','DarkSeaGreen','AquaMarine','DarkOrchid','RosyBrown','RoyalBlue','Chocolate','LightSlateGray','YellowGreen','SteelBlue']
    for n in range(2):
        #print n
        #c = colors[n]
        c = 'k'
        #print c
        [plb.plot(i[0],i[1],'o',color = c) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    
    ###regression
    xs = [i[0] for i in current_list]
    ys = [i[1] for i in current_list]
    from scipy import stats
    slope,intercept,r_value,p_value,std_err = stats.linregress(xs,ys)
    r_pot = u"Vrev: %.2f mV"%(-1*intercept/slope)
    cond = u"Conductance:%.2f±%.2f pS"%(slope*1000,std_err*1000)
    pval = u"p-value:%.4f"%(p_value)
    st = r_pot + '\n' + cond + '\n' + pval
    fv = lambda v:slope*v + intercept
    plb.plot(np.sort(vh[:11]),[fv(v) for v in np.sort(vh[:11])],color = 'k',lw=2,alpha = 0.6)
    a1.set_xbound([-120,70])
    a1.set_ybound([-5,20])
    xlims = a1.get_xlim()
    ylims = a1.get_ylim()
    t = plb.text(xlims[0],ylims[1]*0.8,st)
        
    ###baseline subtracted current plot
    a2 = make_axes(0.1,0.45,0.1,0.45,frameon = False)
    for n in range(1):
        c = colors[n]
        [i[2].get_low_filter(2000).plot(color = c, alpha = 0.9,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    
    ###stimax for subtracted current plot
    stimax = make_axes(0.1,0.45,0.45,0.47,frameon = False)
    plb.plot([0,0.1,0.1,0.25],[0,0,1,1])
    format_phys(a2,0.05,2.0)
    format_stim(stimax)
    format_iv(a1)
    
    ###unsubtracted plot
    a3 = make_axes(0.1,0.9,0.5,0.85,frameon = False)
    for n in range(1):
        c = colors[n]
        c = 'k'
        [i[3].get_low_filter(2000).plot(color = c, alpha = 0.5,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    a3.set_ybound([-100,50])
    format_phys(a3,0.025,10.0)
    a3.set_ybound([-100,50])
    stimax2 = make_axes(0.1,0.9,0.85,0.87,frameon = False,sharex = a3)
    #plb.plot([0,0.225,0.225,0.725,0.725,0.900],[0,0,1,1,0,0])
    plb.plot([0,0.1,0.1,0.25],[0,0,1,1])
    format_stim(stimax2)
    #plb.savefig("cell_%s.png"%(cennum))
    #plb.close()
    #fi = open('output.txt','a')
    #fi.write("%s\t%s\t%s\t%s\t%s\n"%(cennum,-1*intercept/slope,slope*1000,std_err*1000,p_value))
    #fi.close()
    
def ssm_fig(cennum):
    #plb.box(on='off')
    import quantities as quan
    traces = load_cell(cennum)
    if cennum > 32:
        vh = [-90,60,-75,45,-60, 30,-45,15,-30, 0,-15]
    else:
        vh = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60]
        #vh = [-75, -60, -45, -30, -15,   0,  15,  30,  45,  60]
    current_list = list()
    
    vh = [v-15.0 for v in vh]
    for i,trace in enumerate(traces):
        epoch = trace.ts(725.0,975.0,tunits = 'ms')
        swp = trace.ts(725.0,975.0,tunits = 'ms').get_low_filter(2000)
        epoch = epoch.sub_baseline(0,100,tunits = 'ms')
        chtr = epoch.integrate(100,250,tunits = 'ms')
        chtr = chtr/quan.Quantity(100,'ms')
        chtr.units = 'pA'
        epoch.set_yunits('pA')
        swp.set_yunits('pA')
        if i > 10:
            i=np.mod(i,11)
        current_list.append((vh[i],chtr,epoch,swp))
        #current_list.append(epoch)
    
    #max = np.max(np.array([np.max(trace[3]) for trace in current_list]))
    #min = np.min(np.array([np.min(trace[3]) for trace in current_list]))
    #print max
    #print min
    num_trials = len(current_list)/11
    f = plb.figure(figsize=(12,4))
    
    ###scatter plot
    a1 = make_axes(0.55,0.9,0.1,0.85)
    colors = ['Green','Maroon','Olive','Teal','Purple','SaddleBrown','DarkSeaGreen','AquaMarine','DarkOrchid','RosyBrown','RoyalBlue','Chocolate','LightSlateGray','YellowGreen','SteelBlue']
    for n in range(2):
        #print n
        #c = colors[n]
        c = 'k'
        #print c
        [plb.plot(i[0],i[1],'o',color = c) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    
    ###regression
    xs = [i[0] for i in current_list]
    ys = [i[1] for i in current_list]
    from scipy import stats
    slope,intercept,r_value,p_value,std_err = stats.linregress(xs,ys)
    r_pot = u"Vrev: %.2f mV"%(-1*intercept/slope)
    cond = u"Conductance:%.2f±%.2f pS"%(slope*1000,std_err*1000)
    pval = u"p-value:%.4f"%(p_value)
    st = r_pot + '\n' + cond + '\n' + pval
    fv = lambda v:slope*v + intercept
    plb.plot(np.sort(vh[:11]),[fv(v) for v in np.sort(vh[:11])],color = 'k',lw=2,alpha = 0.6)
    a1.set_xbound([-120,70])
    a1.set_ybound([-5,15])
    xlims = a1.get_xlim()
    ylims = a1.get_ylim()
    t = plb.text(xlims[0],ylims[1]*0.8,st)
        
    ####baseline subtracted current plot
    #a2 = make_axes(0.1,0.45,0.1,0.45,frameon = False)
    #for n in range(1):
    #    c = colors[n]
    #    [i[2].get_low_filter(2000).plot(color = c, alpha = 0.9,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    
    ###stimax for subtracted current plot
    #stimax = make_axes(0.1,0.45,0.45,0.47,frameon = False)
    #plb.plot([0,0.1,0.1,0.25],[0,0,1,1])
    #format_phys(a2,0.05,2.0)
    #format_stim(stimax)
    format_iv(a1)
    
    ###unsubtracted plot
    a3 = make_axes(0.1,0.50,0.1,0.85,frameon = False)
    for n in range(1):
        c = colors[n]
        c = 'k'
        [i[3].plot(color = c, alpha = 0.5,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
        max = np.max(np.array([np.max(i[3]) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]))
        min = np.min(np.array([np.min(i[3]) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]))
        #[i[3].get_low_filter(2000).plot(color = c, alpha = 0.5,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    print max
    print min
    #a3.set_ybound([-60,50])
    format_phys(a3,0.025,10.0)
    #a3.set_ybound([-50,60])
    a3.set_ybound([min,max])
    stimax2 = make_axes(0.1,0.5,0.85,0.87,frameon = False,sharex = a3)
    #plb.plot([0,0.225,0.225,0.725,0.725,0.900],[0,0,1,1,0,0])
    plb.plot([0,0.1,0.1,0.25],[0,0,1,1])
    format_stim(stimax2)
    return current_list
    
    
def plot_summary():
    """plots conductance vs r-potential for the different groups using the ohmic fits
    found in the file 'conductance_ohmic_fits.txt'"""
    #25-first cell,36-wrong cell,67-probe trials
    import sys
    #sys.path.append('/Volumes/Storage/psilentp/pybin')
    from Salines import salines
    cmap = plb.cm.Paired
    interal = salines.internal.buffCa.lowCl
    external = salines.ext.tets.highCa
    nersts = salines.saline_nersts(external,interal)
    e_cl = nersts['Cl-']
    groups = {
    'AVA_AVB_l1':[26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59],
    'AVB_AVA_l1':[60,61,62,63,64,65,66,68,69,70,71,72,73,74,75],
    'AVB_AVA_ttx':[96,97,98,99,100,103,104,105,106,107],
    'AVB_AVA':[60,61,62,63,64,65,66,68,69,70,71,72,73,74,75,96,97,98,99,100,103,104,105,106,107],
    'ASH_AVB_l1':[88,89,90,92,93,94,95]
    }
    from collections import OrderedDict
    
    #ordered_groups = OrderedDict()
    #for key in ['AVA_AVB_l1','AVB_AVA_l1','AVB_AVA_ttx','ASH_AVB_l1']:
    #ordered_groups.update({key:groups[key]})
    fi = open('conductance_ohmic_fits.txt','r')
    lns = fi.readlines()
    calcdict = dict()

    for l in lns:
        data = [float(x) for x in l.split()]
        calcdict.update({int(data[0]):{'rpot':data[1],'cond':data[2],'std_err':data[3],'p_val':data[4]}})
    #print calcdict[59]
    fig = plb.figure(figsize = (6.0,11))
    for i,key in enumerate(['AVA_AVB_l1','AVB_AVA_l1','AVB_AVA_ttx','ASH_AVB_l1']):
        group = groups[key]
        xs = [calcdict[cennum]['rpot'] for cennum in group]
        #xs = [np.random.rand()*5+20 for cennum in group]
        ys = [calcdict[cennum]['cond'] for cennum in group]
        yerr = [calcdict[cennum]['std_err'] for cennum in group]
        pval = [calcdict[cennum]['p_val'] for cennum in group]
        alpha_level = 0.05/len(ys)
        sig_rps = list()
        ax = plb.subplot(4,1,i+1)
        n_sig = 0
        n_not_sig = 0
        for x,y,er,pv in zip(xs,ys,yerr,pval):
            if pv > alpha_level:
                c = cmap(0.5)
                n_not_sig += 1
            else:
                sig_rps.append(x)
                c = cmap(0.1)
                n_sig += 1
            plb.errorbar(x,y,yerr=er,marker='o',ls='None',color = c)
        mean_rp = np.mean(sig_rps)
        from scipy import stats
        sterr_rp = stats.sem(sig_rps)
        print("%s:%.2f"%(key,mean_rp)) 
        print("%s:%.2f"%(key,sterr_rp))
        print('not sig: ' + str(n_not_sig))
        print('sig: ' + str(n_sig))
        #ax = plb.gca()
        plb.title(key)
        format_iv(ax)
        ax.set_xbound([-130,50])
        ax.set_ybound([-50,210])
        ax.tick_params(top=False,right=False)
        ax.spines['left'].set_position('zero')
        y_start = -40
        y_axis_space = 15
        plb.arrow(mean_rp,y_start,0,-1*y_start-y_axis_space,shape='full',length_includes_head = True,head_length=10,head_width=2,color = cmap(0.1))
        plb.arrow(float(e_cl),y_start,0,-1*y_start-y_axis_space,shape='full',length_includes_head = True,head_length=10,head_width=2,color = cmap(0.3))
        #plb.savefig('/Volumes/Storage/psilentp/Desktop/'+key+'.pdf')
    return calcdict


def stats_for_shawn():
    """test if the AVA->AVB conxns is different than AVB->AVA conxn"""
    calcdict = plot_summary()
    #get AVA-AVB conns with cond greater than 0
    AVA_AVB_l1 = [26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
    AVB_AVA_l1 = [60,61,62,63,64,65,66,68,69,70,71,72,73,74,75]
    AVB_AVA = [60,61,62,63,64,65,66,68,69,70,71,72,73,74,75,96,97,98,99,100,103,104,105,106,107]
    AVB_AVA_ttx = [96,97,98,99,100,103,104,105,106,107]

    from scipy import stats
    #stats summary
    print("stats summary:")
    print("AVB->AVA in lite-1 bkgrnd vs. AVA->AVB in lite-1 bkgrnd")
    atob = [calcdict[cell]['cond'] for cell in AVA_AVB_l1]# if calcdict[cell]['cond'] > 0]
    btoa = [calcdict[cell]['cond'] for cell in AVB_AVA_l1]# if calcdict[cell]['cond'] > 0]
    print("mann whitney U comparisons")
    print(("\tU=%0.2f P=%0.5f")%stats.mannwhitneyu(atob,btoa))
    print("t test on log transformed data:")
    print("\tt=%0.2f P=%0.5f")%stats.ttest_ind(atob,btoa)
    #print("\tt=%0.2f P=%0.5f")%stats.ttest_ind(np.log(atob),np.log(btoa))
    print("Untransformed means:")
    print(u"AVB->AVA:%0.3f\u00B1%0.3f     AVA->AVB:%0.3f\u00B1%0.3f")%(np.mean(btoa),stats.sem(btoa),np.mean(atob),stats.sem(atob))
    print("Log transformed means:")
    print(u"AVB->AVA:%0.3f\u00B1%0.3f     AVA->AVB:%0.3f\u00B1%0.3f")%(np.mean(np.log(btoa)),stats.sem(np.log(btoa)),np.mean(np.log(atob)),stats.sem(np.log(atob)))
    print('')
    print('')
    print("AVB->AVA in ttx-3 bkgrnd vs. AVA->AVB in lite-1 bkgrnd")
    atob = [calcdict[cell]['cond'] for cell in AVA_AVB_l1 if calcdict[cell]['cond'] > 0]
    btoa = [calcdict[cell]['cond'] for cell in AVB_AVA_ttx if calcdict[cell]['cond'] > 0]
    print("mann whitney U comparisons")
    print(("\tU=%0.2f P=%0.5f")%stats.mannwhitneyu(atob,btoa))
    print("t test on log transformed data:")
    print ("\tt=%0.2f P=%0.5f")%stats.ttest_ind(np.log(atob),np.log(btoa))
    print(u"AVB->AVA:%0.3f\u00B1%0.3f     AVA->AVB:%0.3f\u00B1%0.3f")%(np.mean(btoa),stats.sem(btoa),np.mean(atob),stats.sem(atob))
    print("Log transformed means:")
    print(u"AVB->AVA:%0.3f\u00B1%0.3f     AVA->AVB:%0.3f\u00B1%0.3f")%(np.mean(np.log(btoa)),stats.sem(np.log(btoa)),np.mean(np.log(atob)),stats.sem(np.log(atob)))
    print('')
    print('')
    print("AVB->AVA with the lite-1 and ttx-3 bkgrnds pooled together vs. AVA->AVB in lite-1 bkgrnd vs.")
    atob = [calcdict[cell]['cond'] for cell in AVA_AVB_l1 if calcdict[cell]['cond'] > 0]
    btoa = [calcdict[cell]['cond'] for cell in AVB_AVA if calcdict[cell]['cond'] > 0]
    print("mann whitney U comparisons")
    print(("\tU=%0.2f P=%0.5f")%stats.mannwhitneyu(atob,btoa))
    print("t test on log transformed data:")
    print ("\tt=%0.2f P=%0.5f")%stats.ttest_ind(np.log(atob),np.log(btoa))
    print(u"AVB->AVA:%0.3f\u00B1%0.3f     AVA->AVB:%0.3f\u00B1%0.3f")%(np.mean(btoa),stats.sem(btoa),np.mean(atob),stats.sem(atob))
    print("Log transformed means:")
    print(u"AVB->AVA:%0.3f\u00B1%0.3f     AVA->AVB:%0.3f\u00B1%0.3f")%(np.mean(np.log(btoa)),stats.sem(np.log(btoa)),np.mean(np.log(atob)),stats.sem(np.log(atob)))
    print('')
    print('')
    print("comparison of AVB->AVA connection in ttx-3 vs lite-1 background")
    grp1 = [calcdict[cell]['cond'] for cell in AVB_AVA_l1 if calcdict[cell]['cond'] > 0]
    grp2 = [calcdict[cell]['cond'] for cell in AVB_AVA_ttx if calcdict[cell]['cond'] > 0]
    print("mann whitney U comparisons")
    print(("\tU=%0.2f P=%0.5f")%stats.mannwhitneyu(grp1,grp2))
    print("t test on log transformed data:")
    print ("\tt=%0.2f P=%0.5f")%stats.ttest_ind(np.log(grp1),np.log(grp2))
    print(u"AVB->AVA_l1:%0.3f\u00B1%0.3f     AVB_AVA_ttx:%0.3f\u00B1%0.3f")%(np.mean(grp1),stats.sem(grp1),np.mean(grp2),stats.sem(grp1))
    print("Log transformed means:")
    print(u"AVB->AVA_l1:%0.3f\u00B1%0.3f     AVA->AVA_ttx:%0.3f\u00B1%0.3f")%(np.mean(np.log(grp1)),stats.sem(np.log(grp1)),np.mean(np.log(grp2)),stats.sem(np.log(grp2)))
    
    atob = [calcdict[cell]['cond'] for cell in AVA_AVB_l1 if calcdict[cell]['cond'] > 0]
    btoa = [calcdict[cell]['cond'] for cell in AVB_AVA_l1 if calcdict[cell]['cond'] > 0]
    btoattx = [calcdict[cell]['cond'] for cell in AVB_AVA_ttx if calcdict[cell]['cond'] > 0]
    groups = {'atob':atob,'btoa':btoa,'btoattx':btoattx}
    contrasts = {'atob_vs_btoa':{'atob':-2.0,'btoa':1.0,'btoattx':1.0},'ttx_effect':{'atob':0.0,'btoa':1.0,'btoattx':-1.0}}
    import anova
    aov = anova.ANOVA(groups = groups,contrasts = contrasts)
    print(aov)
	
	
def make_movie(files):
    downs_factor = 2
    from PIL import Image
    im2 = Image.open(files[0])
    counter = 3
    frame = 0
    for f in files[1:]:
        counter += 1
        im = im2
        im2 = Image.open(f)
        im2 = Image.blend(im,im2,0.2)
        if counter % downs_factor == 0:
            fname = 'b_tmp%05d.png'%frame
            s_image = im2.resize((1400,500),Image.ANTIALIAS)
            s_image.save(fname)
            frame += 1
            print "saving" + fname
    import os
    os.system("ffmpeg -r 50 -qscale  -i b_tmp%05d.png test.mp4")

def get_pul(f):
    head = rh.BundleHeader(f)
    head.load(f)
    for bi in head.oBundleItems:
        if str(bi.oExtension)[0:4] == '.pul':
            pul = rh.PULFile(f,bi)
    return pul
    
def load_cell(cennum):
    censtr = "%03d"%(cennum)
    filepath = basepath + "CEN%s/%s"%(str(censtr),datamap[censtr][fn])
    #print filepath
    f = open(filepath,'rb')
    pul = get_pul(f)
    celldata = list()
    for route in datamap[censtr][r]:
        #print(route)
        tree_obj = pul.tree['children'][route[1]]
        [celldata.append(l) for l in rh.getleafs(tree_obj,f)]
    f.close()
    return celldata

def make_axes(xstart,xstop,ystart,ystop,**kwargs):
    l = xstart
    b = ystart
    w = xstop-xstart
    h = ystop-ystart
    return plb.axes([l,b,w,h],**kwargs)

def format_phys(ax,xscale,yscale):
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    x0 = xlims[0]+(xlims[1]-xlims[0])*0.1
    y0 = ylims[0]+(ylims[1]-ylims[0])*0.1
    yshift = yscale + xlims[0]+(xlims[1]-xlims[0])*0.1
    xshift = xscale + xlims[0]+(xlims[1]-xlims[0])*0.1
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    #ax.tick_params(top=False,right=False,bottom=False,left=False)
    #ax.tick_params(visible=False)
    #ax.set_yticks([y0,y0+yscale])
    #ax.set_xticks([x0,x0+xscale])
    #ax.set_xticklabels([0,xscale])
    #ax.set_yticklabels([0,yscale])
    ax.plot([x0,x0+xshift],[y0,y0],color = 'k')
    ax.plot([x0,x0],[y0,y0+yshift],color = 'k')
    ylbl = "%.2f pA"%yscale
    xlbl = "%.2f s"%xscale
    ax.text(x0,y0+yshift+(ylims[1]-ylims[0])*0.01,
            ylbl,
            horizontalalignment='center',
            verticalalignment='center')
    ax.text(x0+xshift,y0+(ylims[1]-ylims[0])*0.01,
            xlbl,
            horizontalalignment='center')
            
def format_iv(ax,s=None):
    ax.tick_params(top=False,right=False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    
    
def format_stim(ax):
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_ybound([-0.1,1.1])

def run_calc():
    """run calc_currents_ohmic on the group"""
    for cennum in datamap.keys():  #range(93,108):
        try:
            calc_currents_ohmic(int(cennum))
        except Exception, e:
            print e
            plb.close()

def comp_syn_to_zero(cennum):
    from scipy import stats
    current_list_zero = calc_zero_current_hold(cennum)
    current_list_syn = calc_synaptic_currents(cennum)
    syn_xs = [x[0] for x in current_list_syn]
    syn_ys = [x[1] for x in current_list_syn]
    zer_xs = [x[0] for x in current_list_zero]
    zer_ys = [x[1] for x in current_list_zero]
    slope,intercept,r_value,p_value,std_err = stats.linregress(zer_xs,zer_ys)
    zer_cur_pot = (-1*intercept/slope)
    slope,intercept,r_value,p_value,std_err = stats.linregress(syn_xs,syn_ys)
    rpot_syn = (-1*intercept/slope)
    return (zer_cur_pot,rpot_syn,p_value)
    0
    
def calc_zero_current_hold(cennum):
    """calculate the reversal potential using an ohmic model, save a summary figure
     of the family and the reversal potentials"""
    #plb.box(on='off')
    import quantities as quan
    traces = load_cell(cennum)
    if cennum > 32:
        vh = [-90,60,-75,45,-60, 30,-45,15,-30, 0,-15]
    else:
        vh = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60]
        #vh = [-75, -60, -45, -30, -15,   0,  15,  30,  45,  60]
    current_list = list()
    vh = [v-15.0 for v in vh]
    for i,trace in enumerate(traces):
        epoch = trace.ts(725.0,975.0,tunits = 'ms')
        #swp = trace.ts(600.0,1550.0,tunits = 'ms')
        #epoch = epoch.sub_baseline(0,100,tunits = 'ms')
        chtr = epoch.integrate(0,100,tunits = 'ms')
        chtr = chtr/quan.Quantity(100,'ms')
        chtr.units = 'pA'
        epoch.set_yunits('pA')
        #rswp.set_yunits('pA')
        if i > 10:
            i=np.mod(i,11)
        current_list.append((vh[i],chtr))
        #current_list.append(epoch)
        num_trials = len(current_list)/11
        
    return current_list
    
def calc_synaptic_currents(cennum):
    """calculate the reversal potential using an ohmic model, save a summary figure
     of the family and the reversal potentials"""
    #plb.box(on='off')
    import quantities as quan
    traces = load_cell(cennum)
    if cennum > 32:
        vh = [-90,60,-75,45,-60, 30,-45,15,-30, 0,-15]
    else:
        vh = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60]
        #vh = [-75, -60, -45, -30, -15,   0,  15,  30,  45,  60]
    current_list = list()
    vh = [v-15.0 for v in vh]
    for i,trace in enumerate(traces):
        epoch = trace.ts(725.0,975.0,tunits = 'ms')
        #swp = trace.ts(600.0,1550.0,tunits = 'ms')
        epoch = epoch.sub_baseline(0,100,tunits = 'ms')
        chtr = epoch.integrate(100,200,tunits = 'ms')
        chtr = chtr/quan.Quantity(100,'ms')
        chtr.units = 'pA'
        epoch.set_yunits('pA')
        #rswp.set_yunits('pA')
        if i > 10:
            i=np.mod(i,11)
        current_list.append((vh[i],chtr))
        #current_list.append(epoch)
        num_trials = len(current_list)/11
    return current_list
    
    #num_trials = len(current_list)/11
    #f = plb.figure(figsize=[12,8])
    ###scatter plot
    #a1 = make_axes(0.55,0.9,0.1,0.5)
    #colors = ['Green','Maroon','Olive','Teal','Purple','SaddleBrown','DarkSeaGreen','AquaMarine','DarkOrchid','RosyBrown','RoyalBlue','Chocolate','LightSlateGray','YellowGreen','SteelBlue']
    #for n in range(num_trials):
    #    #print n
    #   c = colors[n]
    #    #print c
    #    [plb.plot(i[0],i[1],'o',color = c) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
        
        
    
def calc_currents_ohmic(cennum):
    """calculate the reversal potential using an ohmic model, save a summary figure
     of the family and the reversal potentials"""
    #plb.box(on='off')
    import quantities as quan
    traces = load_cell(cennum)
    if cennum > 32:
        vh = [-90,60,-75,45,-60, 30,-45,15,-30, 0,-15]
    else:
        vh = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60]
        #vh = [-75, -60, -45, -30, -15,   0,  15,  30,  45,  60]
    current_list = list()
    
    vh = [v-15.0 for v in vh]
    for i,trace in enumerate(traces):
        epoch = trace.ts(725.0,975.0,tunits = 'ms')
        swp = trace.ts(600.0,1550.0,tunits = 'ms')
        epoch = epoch.sub_baseline(0,100,tunits = 'ms')
        chtr = epoch.integrate(100,250,tunits = 'ms')
        chtr = chtr/quan.Quantity(100,'ms')
        chtr.units = 'pA'
        epoch.set_yunits('pA')
        swp.set_yunits('pA')
        if i > 10:
            i=np.mod(i,11)
        current_list.append((vh[i],chtr,epoch,swp))
        #current_list.append(epoch)
    
    num_trials = len(current_list)/11
    f = plb.figure(figsize=[12,8])
    ###scatter plot
    a1 = make_axes(0.55,0.9,0.1,0.5)
    colors = ['Green','Maroon','Olive','Teal','Purple','SaddleBrown','DarkSeaGreen','AquaMarine','DarkOrchid','RosyBrown','RoyalBlue','Chocolate','LightSlateGray','YellowGreen','SteelBlue']
    for n in range(num_trials):
        #print n
        c = colors[n]
        #print c
        [plb.plot(i[0],i[1],'o',color = c) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    
    ###regression
    xs = [i[0] for i in current_list]
    ys = [i[1] for i in current_list]
    from scipy import stats
    slope,intercept,r_value,p_value,std_err = stats.linregress(xs,ys)
    r_pot = u"Vrev: %.2f mV"%(-1*intercept/slope)
    cond = u"Conductance:%.2f±%.2f pS"%(slope*1000,std_err*1000)
    pval = u"p-value:%.4f"%(p_value)
    st = r_pot + '\n' + cond + '\n' + pval
    fv = lambda v:slope*v + intercept
    plb.plot(np.sort(vh[:11]),[fv(v) for v in np.sort(vh[:11])],color = 'k',lw=2,alpha = 0.6)
    a1.set_xbound([-120,70])
    a1.set_ybound([-5,20])
    xlims = a1.get_xlim()
    ylims = a1.get_ylim()
    t = plb.text(xlims[0],ylims[1]*0.8,st)
        
    ###baseline subtracted current plot
    a2 = make_axes(0.1,0.45,0.1,0.45,frameon = False)
    for n in range(num_trials):
        c = colors[n]
        [i[2].get_low_filter(2000).plot(color = c, alpha = 0.9,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    
    ###stimax for subtracted current plot
    stimax = make_axes(0.1,0.45,0.45,0.47,frameon = False)
    plb.plot([0,0.1,0.1,0.25],[0,0,1,1])
    format_phys(a2,0.05,0.05)
    format_stim(stimax)
    format_iv(a1)
    
    ###unsubtracted plot
    a3 = make_axes(0.1,0.9,0.5,0.85,frameon = False)
    for n in range(num_trials):
        c = colors[n]
        [i[3].get_low_filter(2000).plot(color = c, alpha = 0.5,lw=0.5) for i in current_list[(n)*len(current_list)/num_trials:(n+1)*len(current_list)/num_trials]]
    a3.set_ybound([-100,50])
    format_phys(a3,0.2,10.0)
    a3.set_ybound([-100,50])
    stimax2 = make_axes(0.1,0.9,0.85,0.87,frameon = False,sharex = a3)
    plb.plot([0,0.225,0.225,0.725,0.725,0.900],[0,0,1,1,0,0])
    format_stim(stimax2)
    plb.savefig("./cell_summaries/cell_%s.png"%(cennum))
    plb.close()
    fi = open('output.txt','a')
    fi.write("%s\t%s\t%s\t%s\t%s\n"%(cennum,-1*intercept/slope,slope*1000,std_err*1000,p_value))
    fi.close()


def plot_cell2(cennum):
    import quantities as pq
    vh = [-90,60,-75,45,-60, 30,-45,15,-30, 0,-15]
    vh = [v-15.0 for v in vh]
    ave_num = 6
    a = 1
    fig = plb.figure(figsize=(6,6))
    stimtrace = {'y':[0,0,1,1],'x':[0,0.14,0.14,0.5]}
    ax = plb.axes([0.05,0.9,0.55,0.1])
    plb.plot(stimtrace['x'],stimtrace['y'])
    ax.set_ybound([-0.05,1.05])
    ax.set_frame_on(False)
    ax.set_xticklabels('')
    ax.set_xticks([])
    ax.set_yticks([])
    for i,cennum in enumerate([41,72,98,94]):
        celldata = load_cell(cennum)
        current_list = list()
        for j,trace in enumerate(celldata[:11]):
            #get the data
            epoch = trace.ts(725.0,975.0,tunits = 'ms')
            swp = trace.ts(725.0,975.0,tunits = 'ms')
            epoch = epoch.sub_baseline(0,100,tunits = 'ms')
            chtr = epoch.integrate(100,250,tunits = 'ms')
            chtr = chtr/pq.Quantity(100,'ms')
            chtr.units = 'pA'
            epoch.set_yunits('pA')
            swp.set_yunits('pA')
            current_list.append((vh[j],chtr,epoch,swp))
        xs = [item[0] for item in current_list[:11]]
        ys = [item[1] for item in current_list[:11]]
        from scipy import stats
        slope,intercept,r_value,p_value,std_err = stats.linregress(xs,ys)
        r_pot = u"Vrev: %.2f mV"%(-1*intercept/slope)
        cond = u"Conductance:%.2f±%.2f pS"%(slope*1000,std_err*1000)
        pval = u"p-value:%.4f"%(p_value)
        st = r_pot + '\n' + cond + '\n' + pval
        fv = lambda v:slope*v + intercept
        ax2 = plb.axes([0.65,0.7-(i*0.21),0.3,0.2])
        plb.plot(xs,ys,'o')
        plb.plot(np.sort(vh[:11]),[fv(v) for v in np.sort(vh[:11])],color = 'k',lw=2,alpha = 0.6)
        ax2.set_xbound([-120,70])
        ax2.set_ybound([-10,30])
        xlims = ax2.get_xlim()
        ylims = ax2.get_ylim()
        format_iv(ax2)
        #t = plb.text(xlims[0],ylims[1]*0.8,st)
    
        ax3 = plb.axes([0.05,0.7-(i*0.21),0.55,0.2],sharex = ax)
        [trace.ts(0.7,1.2)[::10].plot(color = 'k') for trace in celldata[:11]]
        ax3.set_ybound([70e-12,-60e-12])
        #format_phys(ax3,5e-12,2.0)
    
def plot_cell(cennum):
    ave_num = None
    a = 0.4
    celldata = load_cell(cennum)
    fig = plb.figure(figsize=(20,6))
    #stim trace
    stimtrace = {'y':[0,0,1,1,0,0],'x':[0,30,30,60,60,90]}
    ax = plb.axes([0.05,0.8,0.9,0.15])
    plb.plot(stimtrace['x'],stimtrace['y'])
    ax.set_frame_on(False)
    ax.set_xticklabels('')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ybound([-0.05,1.05])
    #data trace
    ax = plb.axes([0.05,0.07,0.9,0.7])
    
    [trace[::10].sub_baseline(0,30,tunits='s').plot(color = 'k', alpha = a,lw=0.5) for trace in celldata[:ave_num]]
    if not(ave_num) or (ave_num > 1):
        tr0 =  celldata[0].sub_baseline(0,30,tunits='s')
        for tr in celldata[1:ave_num]:
            tr0 += tr.sub_baseline(0,30,tunits='s')
        tr0 /= len(celldata[:ave_num])
        tr0[::10].plot(color='r',lw=0.2)
    plb.plot([0,10],[-20e-12,-20e-12],color='k',lw=2)
    plb.plot([0,0],[-20e-12,-10e-12],color='k',lw=2)
    ax.set_xticks([])
    ax.set_frame_on(False)
    ax.set_ybound([-20e-12,20e-12])
    ax.set_yticks([])
    ax.text(-2, -15e-12,"10pA",{'fontsize':20},
       horizontalalignment = 'left',
       verticalalignment = 'center',
       rotation = 90,
       clip_on = False)
    ax.text(5, -22e-12,"10s",{'fontsize':20},
       horizontalalignment = 'left',
       verticalalignment = 'center',
       clip_on = False)
    plb.savefig("/Users/lab/Documents/Data/itx/CEN%s/%s"%(str(cennum),"cellsum.png"))
    plb.close(fig)
    
    
def load_data(dmap):
    fn = 'fn'
    r = 'r'

    def get_pul(f):
        head = rh.BundleHeader(f)
        head.load(f)
        for bi in head.oBundleItems:
            if str(bi.oExtension)[0:4] == '.pul':
                pul = rh.PULFile(f,bi)
        return pul

    {114:[[0,15]]}
    {125:[[0,11],[0,15],[0,19],[0,23],[0,27],[0,31]]}

    #filepath = "/Volumes/BigGuy/CELLS/CEN%s/%s"%(str(key),datamap[cennum][p])

    for cennum in dmap.keys():
        filepath = basepath + "CEN%s/%s"%(str(cennum),dmap[cennum][fn])
        print filepath
        celldata = list()
        f = open(filepath,'rb')
        pul = get_pul(f)
        for route in datamap[cennum][r]:
            tree_obj = pul.tree['children'][route[1]]
            celldata.append(rh.getleafs(tree_obj,f)[0])
        f.close()
        dmap[cennum].update({'d':celldata})
        #datamap[cennum]['d'][0][::10].sub_baseline(0,30,tunits='s').plot(color = 'k', alpha = 0.3)
    return dmap


def summary_fig():
    fig = plb.figure(figsize=(5,10))
    cennums = [153,151,150,149,148,147,146,145,144,143,142,141,139,138,137,136,135,134,133]
    cennums  = [str(c) for c in cennums]
    dmap = dict()
    [dmap.update({cennum:datamap[cennum]}) for cennum in cennums]
    dmap = load_data(dmap)
    stimtrace = {'y':[0,0,1,1,0,0],'x':[0,30,30,60,60,90]}
    ax = plb.subplot(len(cennums)+1,1,1)
    plb.plot(stimtrace['x'],stimtrace['y'])
    ax.set_ybound([-0.1,1.1])
    ax.set_yticks([0,1])
    ax.set_yticklabels([0,1])
    ax.set_frame_on(False)
    for n,l in enumerate(ax.get_xticklines()):
        l.set_visible(False)
    for n,l in enumerate(ax.get_yticklines()):
        if np.mod(n,2):
            l.set_visible(False)
    ax.set_xticklabels([''])

    ave_num = 3

    for i,cennum in enumerate(cennums):
        ax = plb.subplot(len(cennums)+1,1,i+2)
        if ave_num:
            a = 1/ave_num
        else:
            a = 1
        print('here')
        [trace[::10].sub_baseline(0,30,tunits='s').plot(color = 'k', alpha = a) for trace in dmap[cennum]['d'][:ave_num]]
        tr0 =  dmap[cennum]['d'][0].sub_baseline(0,30,tunits='s')

        if ave_num > 1:
            for tr in dmap[cennum]['d'][1:ave_num]:
                tr0 += tr.sub_baseline(0,30,tunits='s')
            tr0 /= ave_num
            tr0[::10].plot(color='r',alpha = 0.5)
        
        ax.set_ybound([-20e-12,20e-12])
        ax.set_yticks([-15e-12,15e-12])
        ax.set_yticklabels([-15,15])
        ax.set_frame_on(False)
        for n,l in enumerate(ax.get_xticklines()):
            if np.mod(n,6) and np.mod(n-1,6):
                l.set_visible(False)
        for n,l in enumerate(ax.get_yticklines()):
            if np.mod(n,2):
                l.set_visible(False)
        if i<len(cennums)-1:
            ax.set_xticklabels([''])
            ax.set_ybound([-20e-12,20e-12])
            ax.set_yticks([])
            ax.set_yticklabels('')
            ax.set_frame_on(False)
        else:
            ax.set_ybound([-20e-12,20e-12])
            ax.set_yticks([-20e-12,20e-12])
            ax.set_yticklabels([-15,15])
        ax.text(1.01, 0.5, str(cennum),
               horizontalalignment = 'left',
               verticalalignment = 'center',
               transform = ax.transAxes,
               clip_on = False)
    
def cell_plots(datamap):
    a = 0.4
    ave_num = None
    cennums = datamap.keys()
    for i,cennum in enumerate(cennums[:]):
        fig = plb.figure(figsize=(20,6))
        #stim trace
        stimtrace = {'y':[0,0,1,1,0,0],'x':[0,30,30,60,60,90]}
        ax = plb.axes([0.05,0.8,0.9,0.15])
        plb.plot(stimtrace['x'],stimtrace['y'])
        ax.set_frame_on(False)
        ax.set_xticklabels('')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ybound([-0.05,1.05])
        #data trace
        ax = plb.axes([0.05,0.07,0.9,0.7])
        
        [trace[::10].sub_baseline(0,30,tunits='s').plot(color = 'k', alpha = a,lw=0.5) for trace in datamap[cennum]['d'][:ave_num]]
        if not(ave_num) or (ave_num > 1):
            tr0 =  datamap[cennum]['d'][0].sub_baseline(0,30,tunits='s')
            for tr in datamap[cennum]['d'][1:ave_num]:
                tr0 += tr.sub_baseline(0,30,tunits='s')
            tr0 /= len(datamap[cennum]['d'][:ave_num])
            tr0[::10].plot(color='r',lw=0.2)
        plb.plot([0,10],[-20e-12,-20e-12],color='k',lw=2)
        plb.plot([0,0],[-20e-12,-10e-12],color='k',lw=2)
        ax.set_xticks([])
        ax.set_frame_on(False)
        ax.set_ybound([-20e-12,20e-12])
        ax.set_yticks([])
        ax.text(-2, -15e-12,"10pA",{'fontsize':20},
           horizontalalignment = 'left',
           verticalalignment = 'center',
           rotation = 90,
           clip_on = False)
        ax.text(5, -22e-12,"10s",{'fontsize':20},
           horizontalalignment = 'left',
           verticalalignment = 'center',
           clip_on = False)
        plb.savefig("/Users/lab/Documents/Data/itx/CEN%s/%s"%(str(cennum),"cellsum.png"))
        plb.close(fig)
                #ax.set_yticklabels(['-15','15'])


"""
scratch code
        #v = float(-2*10**(10))
        #ax.spines['bottom'].set_position(('data',v))
        #ax.spines['left'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        #ax.spines['top'].set_visible(False)
        #lbs = ax.get_yticklabels()
        #tks = ax.get_yticklines()
        #[l.set_visible(False) for l in lbs]
        #[t.set_color('w') for t in txs]
        #files = []
        #print('here')
        #set_tup = (1-2000/(apos-300),200+2000/(apos-300))
            #for i,apos in enumerate(np.arange(1,2000,100)):
            #fname = '%s_tmp%03d.png'%(key,i)
            #print apos
            #set_tup = (1-2000/(apos*0.2),200+2000/(apos*0.2))
            #ax.spines['bottom'].set_position(('data',set_tup[0]))
            
            #ax.set_ybound(set_tup[0]-20,set_tup[1])
            #print-2*10**(apos/10.0)
            #print 1*10**(apos/10.0)
            #plb.draw()
        #    #plb.show()
            #print 'Saving frame', fname
            #fig.savefig(fname)
            #files.append(fname)
            #ax.spines['left'].set_visible(True)
        #[l.set_visible(True) for l in lbs]
            #[t.set_color('k') for t in txs]
        #ax.set_xbound(-200,100)
        #ax.set_ybound(-20,200)
        #print 'Making movie animation.mpg - this make take a while'
        #import os
        #compression = 0
        #q = str(int(max(0, min(1, compression)) * 30.0 + 1))
        #make_movie(files)
        #os.system("ffmpeg -r 50 -qscale 31 -i %s_tmp*.png %s_test.mp4"%(key,key))
        #os.system("mencoder 'mf://%s_tmp*.png' -mf fps=20 -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=1600 -oac copy -o %s_animation.avi"%(key,key))
        #os.system("mencoder 'mf://%s_tmp*.png' -mf fps=20 -ovc lavc -lavcopts vcodec=mjpeg -oac copy -o %s_animation.avi"%(key,key))
        #os.system("mencoder 'mf://%s_tmp*.png' -mf type=png:fps=10 -ovc raw -oac copy -o animation.mpg"%(key))
"""