import os
import pickle
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt

from . import sect_utils as sg

def mapZoneSeismic(fig_handle, x, y, annotation="", zones_pkl=None, colors=None, fontsize=None):
    '''
    plot geo location and seismic zone
        x          = coordinates istat WGS84
        y          = coordinates istat WGS84
        annatation = 'Zona ' + str(classification) + '\n' + municipality + '\n' + province + '\n' + region
    '''
    fontsize = fontsize or 8
    if fig_handle is None:
        fig_handle = plt.figure()
    fig_handle.clf()
    axes = fig_handle.add_subplot(111)
    # read simplified zones shapes from pickle (wb) file
    if zones_pkl is None:
        path0 = os.path.abspath(os.path.dirname(__file__))
        zones_pkl = os.path.join(path0, "../data/zone_sismiche_2019_istat_WGS84.pkl")
    with open(zones_pkl,"rb") as f:
        zones = pickle.load(f)
    # colors of zones, including the order of legend
    if colors is None:
        colors = OrderedDict({
            "1"     : "r"             ,
            "12A"   : "tomato"        ,
            "2"     : "chocolate"     ,
            "2A"    : "darkorange"    ,
            "2A2B"  : "sandybrown"    , 
            "2B"    : "peachpuff"     ,
            "2A3A3B": "goldenrod"     ,
            "2B3A"  : "khaki"         ,
            "2-3"   : "gold"          ,
            "3"     : "darkkhaki"     ,
            "3S"    : "yellow"        ,
            "3A"    : "yellowgreen"   ,
            "3A3B"  : "greenyellow"   ,
            "3B"    : "olivedrab"     ,
            "3-4"   : "darkseagreen"  ,
            "4"     : "silver"        ,
        })
    # plot
    for i in range(len(zones)):
        zs = list(zones)[i]
        pp = zones[zs]
        for p in pp:
            axes.fill(p[:,0], p[:,1], color=colors[zs], label=zs, lw=0, rasterized=True, zorder=1)
    # set axis and legend
    axes.set_xlim(      0,1450000) # m( 200000,1450000)
    axes.set_ylim(4000000,5250000)
    axes.set_aspect("equal")
    axes.set_axis_off()
    hdls, labs = axes.get_legend_handles_labels()
    labs, ids = np.unique(labs, return_index=True)
    hdls = [hdls[i] for i in ids]
    inds = [list(colors).index(l) for l in labs]
    inds = sorted(range(len(inds)), key=lambda k: inds[k]) # sort and return index
    axes.legend([hdls[i] for i in inds], [labs[i] for i in inds], 
        loc='upper left', bbox_to_anchor=(1,1), frameon=False, title="zone sismiche", prop={'size':fontsize*0.9})
    # place annotation
    axes.annotate(annotation,
        xy=(x, y), xycoords='data',
        xytext=( 400000, 4000000), textcoords='data',
        size=fontsize, va="bottom", ha="right", color='white',
        bbox=dict(boxstyle="round", fc='royalblue', ec="none"),
        arrowprops=dict(arrowstyle="wedge,tail_width=1.",
            fc='royalblue', ec="none",
            patchA=None, patchB=None, relpos=(0.2, 0.5)))
    axes.scatter(x, y, s=fontsize*1.5, c='royalblue', marker='o', zorder=2)
    axes.set_position([0.05,0.05,0.7,0.9])
    # redraw
    fig_handle.canvas.draw()


def sectionShape(fig_handle, sec, rebar=False, stirr=False, fontsize=None, cc=None, z_inversed=False):
    fontsize = fontsize or 8
    if fig_handle is None:
        fig_handle = plt.figure()
    fig_handle.clf()
    axes = fig_handle.add_subplot(111)
    axes.set_aspect('equal')
    axes.tick_params(labelsize=fontsize*0.8)
    for pp in sec["points"]:
        x = [p[0] for p in pp]
        y = [p[1] for p in pp]
        axes.fill(x, y, color='silver', alpha=0.5)
    if sec["_type"] == "RC":
        # rebar
        if rebar and sec["rebar"]:
            rebar = sg.Rebars(sec["rebar"]).rotate(sec["theta"] - sec["theta_origin"], origin=(sec["yc"],sec["zc"]))
            for i in range(len(rebar.d)):
                c = plt.Circle((rebar.y[i],rebar.z[i]), rebar.d[i]/2, color='blue', alpha=0.9)
                axes.add_artist(c)
                axes.text(rebar.y[i]+rebar.d[i]/2*1.1, rebar.z[i], r'$\phi$' + f"{rebar.d[i]:.0f}", color='grey', va='center', ha='left', fontsize=fontsize)
        # stirr
        if stirr and sec["stirr"]:
            stirr = sg.Stirrups(sec["stirr"])
            cc = cc or sec["cc"]
            if sec["shape_inputs"]["shape"] in ["circ"]:
                pp = sg.Polygons([sg.Rectangle(d=sec["shape_inputs"]["d"]*0.7,b=sec["shape_inputs"]["d"]*0.7,xc=sec["yc"],yc=sec["zc"])])
                stirr.bw = [sec["shape_inputs"]["d"]*0.7]*len(stirr.bw)
            else:
                polygons = sg.Polygons(sec["points"])
                pp = polygons.get_envelope(offset=-1*cc)
            # # (y, z, d, n, s, beta, bw, alpha, theta)
            for i in range(len(stirr.d)):
                p0 = np.array([stirr.y[i], stirr.z[i]])
                d  = stirr.d[i]
                n  = stirr.n[i]
                beta = stirr.beta[i] + sec["theta"] - sec["theta_origin"]
                bw = stirr.bw[i]
                if n>0:
                    p1 = p0 + bw/2 *np.array([np.cos((beta-90)/180*np.pi), np.sin((beta-90)/180*np.pi)]) # np.array(st[0])
                    p2 = p0 + bw/2 *np.array([np.cos((beta+90)/180*np.pi), np.sin((beta+90)/180*np.pi)]) # np.array(st[1])            
                    if n<2:
                        ps = [(p1+p2)/2]
                    else:
                        wd = np.linalg.norm(p2-p1)
                        ps = [p1+(p2-p1)/wd*(cc+d/2+(wd-cc*2-d)*i/(n-1)) for i in range(n)] 
                    # for each leg
                    for p in ps:
                        # find line within comfined area
                        _, ls = pp.linecut(origin=p.tolist(), angle=beta)
                        if len(ls)>0:
                            for l in ls:
                                vv = np.array(l.coords)
                                axes.plot(vv[:,0],vv[:,1], '--', color='green', alpha=0.5, lw=fontsize*0.2)
                        axes.text(p[0], p[1], r'$\phi$' + f"{d:.0f}", color='grey', va='bottom', ha='left', fontsize=fontsize)
    # ----
    elif sec["_type"] =="ST":
        # for interiors
        for pp in sec["inner_points"]:
            x = [p[0] for p in pp]
            y = [p[1] for p in pp]
            axes.fill(x, y, color='silver', alpha=0.5)
    # ----
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    bmax = max(xmax-xmin, ymax-ymin)
    axes.set_xlim([min(xmin,(xmax+xmin)/2-bmax/2), max(xmax,(xmax+xmin)/2+bmax/2)])
    axes.set_ylim([min(ymin,(ymax+ymin)/2-bmax/2), max(ymax,(ymax+ymin)/2+bmax/2)])
    if z_inversed:
        axes.invert_yaxis()
    # redraw
    fig_handle.canvas.draw()


def RCdomains(fig_handle, domains={}, forces=[], fontsize=8):
    if fig_handle is None:
        fig_handle = plt.figure()
    fig_handle.clf()
    axes = fig_handle.add_subplot(111)
    # ----
    axes.set_xlabel('N [kN]')
    axes.set_ylabel('M [kNm]')
    for i,key in enumerate(domains.keys()):
        dmy = np.array(domains[key])
        dmy = np.vstack([dmy, dmy[0,:]])
        axes.plot(dmy[:,0], dmy[:,1], color=f'C{i}', label=key)   
        for ff in forces:
            axes.scatter(ff[0], ff[i+1], s=fontsize, c=f'C{i}', marker='*', zorder=2, label=f"{key}-force")
    axes.grid(True)
    axes.tick_params(labelsize=fontsize*0.8)
    axes.legend(fontsize=fontsize)
    # redraw
    fig_handle.canvas.draw()


def storeyLayout(fig_handle, storey=None, colors=None, styles=None, labels=None, fontsize=None, index_label=True):
    if fig_handle is None:
        fig_handle = plt.figure()
    fig_handle.clf()
    axes = fig_handle.add_subplot(111)
    colors = colors or {"-":'silver', "RC":'g', "MS":'m', "ST":'sienna'}     # varied by materials
    styles = styles or {"Slab":'-', "Column":'-', "Wall":'--',"Bracing":'-'} # varied by types
    labels = labels or {
            "Slab--"    :[ 0,'slab'], 
            "Column-RC" :[ 1,'columns in RC' ], "Column-MS" :[ 2,'columns in MS' ], "Column-ST" :[ 3,'columns in ST' ], 
            "Wall-RC"   :[ 4,'walls in RC'   ], "Wall-MS"   :[ 5,'walls in MS'   ], "Wall-ST"   :[ 6,'walls in ST'   ],
            "Bracing-RC":[ 7,'bracings in RC'], "Bracing-MS":[ 8,'bracings in MS'], "Bracing-ST":[ 9,'bracings in ST'],
            "CenterMass":[10,'mass center'   ], "CenterRigidity":[11,'rigidity center'],
        }
    fontsize = fontsize or 8
    # ------------
    axes.set_aspect("equal")
    axes.set_axis_off()
    for i,el in enumerate(storey["elements"]):
        t = el["_type"]
        m = el["sec_type"] or "-"
        x0 = el["x"]
        y0 = el["y"]
        a0 = el["alpha"] 
        if el["_type"] in ["Bracing"]:
            a0 = el["azimuth"]
            l0 = el["length"] * np.cos(el["elevation"]/180*np.pi) * 0.9
            x = x0 + l0/2 * np.cos(np.array([a0-90,a0+90])/180*np.pi)
            y = y0 + l0/2 * np.sin(np.array([a0-90,a0+90])/180*np.pi)
            axes.plot(x, y, lw=fontsize*0.3, color=colors[m], alpha=0.5, label=t+'-'+m, ls=styles[t])
        for p in el["sec"]["points"]:
            x1 = np.array([v[0]-el["sec"]["yc"] for v in p])
            y1 = np.array([v[1]-el["sec"]["zc"] for v in p])
            x  = x0 + x1*np.cos(a0/180*np.pi) - y1*np.sin(a0/180*np.pi)
            y  = y0 + x1*np.sin(a0/180*np.pi) + y1*np.cos(a0/180*np.pi)
            axes.fill(x, y, color=colors[m], alpha=0.5, label=t+'-'+m, ls=styles[t])
        if index_label:
            if el["_type"] not in ["Slab"]:
                axes.text(x0, y0, f'{i}', color='black', va='center', ha='center', fontsize=fontsize*0.9)
    axes.plot(storey["cmx"], storey["cmy"], "bx", label="CenterMass")
    axes.plot(storey["crx"], storey["cry"], "rx", label="CenterRigidity")
    hdls, labs = axes.get_legend_handles_labels()
    labs, ids = np.unique(labs, return_index=True)
    inds = [labels[l][0] for l in labs]
    inds = sorted(range(len(inds)), key=lambda k: inds[k])
    labs = [labels[l][1] for l in labs]
    hdls = [hdls[i] for i in ids]
    axes.legend([hdls[i] for i in inds], [labs[i] for i in inds], loc='upper left', bbox_to_anchor=(1,1), fontsize=fontsize)
    axes.set_position([0.05,0.05,0.7,0.9])
    # redraw
    fig_handle.canvas.draw()


def buildingShears(fig_handle, building, storey_label=None, shear_label="Shears", fontsize=None):
    if fig_handle is None:
        fig_handle = plt.figure()
    fig_handle.clf()
    ax1 = fig_handle.add_subplot(121)
    ax2 = fig_handle.add_subplot(122,sharey=ax1)
    # fig, [ax1, ax2] = plt.subplots(ncols=2, sharey=True)
    # figsize = figsize or (16/2.54, (2+2*len(self.storeys))/2.54)
    # fig.set_size_inches(*figsize)
    fontsize = fontsize or 8
    # get storey names
    if storey_label is None:
        ss = [s["name"] for s in building["storeys"]]
    else:
        ss = [f"{storey_label}[{i}]" for i in range(len(building['storeys']))]
    smax = max([len(s) for s in ss]) # string length to adjust plot
    # get data
    st = building["results"]
    vm = building["Sa"]
    vs1 = np.array(st["Vsx"    ])
    vr1 = np.array(st["Vrx_red"])
    vs2 = np.array(st["Vsy"    ])
    vr2 = np.array(st["Vry_red"])
    v1   = np.array(st["Sa_x"])   
    v2   = np.array(st["Sa_y"]) 
    vmax = max(vs1.max(),vr1.max(),vs2.max(),vr2.max())
    # plot
    width = 0.4
    inds = np.arange(len(ss))
    indr = inds - width
    # plt.figure(figsize=figsize, dpi=200)
    bar_xs = ax1.barh(inds, vs1, width, align='center', alpha=1, color='C0', label="Vs [kN]")
    bar_xr = ax1.barh(indr, vr1, width, align='center', alpha=1, color='C1', label="Vr [kN]")
    # ax1.barh(inds, vs1, width, align='center', color='None', edgecolor='C0', linewidth=1.5, linestyle='--', label="Vs [kN]")
    # ax1.barh(indr, vr1, width, align='center', color='None', edgecolor='C1', linewidth=1.5, linestyle='-',  label="Vr [kN]")
    ax1.set_xlabel(shear_label + ' in X', fontsize=fontsize)
    ax1.set_xlim([0, vmax*1.5])
    bar_ys = ax2.barh(inds, vs2, width, align='center', alpha=1, color='C0', label="Vs [kN]")
    bar_yr = ax2.barh(indr, vr2, width, align='center', alpha=1, color='C1', label="Vr [kN]")
    # ax2.barh(inds, vs2, width, align='center', color='None', edgecolor='C0', linewidth=1.5, linestyle='--', label="Vs [kN]")
    # ax2.barh(indr, vr2, width, align='center', color='None', edgecolor='C1', linewidth=1.5, linestyle='-',  label="Vr [kN]")
    ax2.set_xlabel(shear_label + ' in Y', fontsize=fontsize)
    ax2.set_xlim([0, vmax*1.5])

    ax1.invert_xaxis()
    ax1.set_yticks((inds+indr)/2)
    ax1.set_yticklabels(ss, fontsize=fontsize)
    ax1.yaxis.tick_right()
    ax2.label_outer()
    ax1.set(xticks=[])
    ax2.set(xticks=[])
    # add value labels to bars
    txt_xs = [None]*len(ss)
    txt_xr = [None]*len(ss)
    txt_ys = [None]*len(ss)
    txt_yr = [None]*len(ss) 
    for i in range(len(ss)):
        txt_xs[i] = ax1.text(vs1[i]+vmax*0.05, inds[i], f"$\\beta V_s={vs1[i]:.0f}kN$", fontsize=fontsize*0.9, va='center', ha='right', color='C0')
        txt_xr[i] = ax1.text(vr1[i]+vmax*0.05, indr[i],  f"$\\psi V_r={vr1[i]:.0f}kN$", fontsize=fontsize*0.9, va='center', ha='right', color='C1')
        ax1.text(vmax*1.50,(inds[i]+indr[i])/2, r"$\dfrac{\psi V_r}{\beta V_s}=$"+"{:.3f}".format(v1[i]), fontsize=fontsize    , ha='left', 
            va='top', fontweight='bold', color='red' if v1[i]==vm else 'k')
        txt_ys[i] = ax2.text(vs2[i]+vmax*0.05, inds[i], f"$\\beta V_s={vs2[i]:.0f}kN$", fontsize=fontsize*0.9, va='center', ha='left', color='C0')
        txt_yr[i] = ax2.text(vr2[i]+vmax*0.05, indr[i],  f"$\\psi V_r={vr2[i]:.0f}kN$", fontsize=fontsize*0.9, va='center', ha='left', color='C1')
        ax2.text(vmax*1.50,(inds[i]+indr[i])/2, r"$\dfrac{\psi V_r}{\beta V_s}=$"+"{:.3f}".format(v2[i]), fontsize=fontsize    , ha='right', 
            va='top', fontweight='bold', color='red' if v2[i]==vm else 'k')
    fig_handle.canvas.draw()
    tr1 = ax1.transData.inverted()  # transform from data to display
    tr2 = ax2.transData.inverted() 
    for i in range(len(ss)):
        v = vs1[i]
        t = txt_xs[i]
        f = tr1.transform(t.get_window_extent())
        if abs(f[1][0] - f[0][0])<=(v-vmax*0.05):
            t.set_position((v-vmax*0.05, t.get_position()[1]))
            t.set_ha('left')
            t.set_color('w')
        v = vr1[i]
        t = txt_xr[i]
        f = tr1.transform(t.get_window_extent())
        if abs(f[1][0] - f[0][0])<=(v-vmax*0.05):
            t.set_position((v-vmax*0.05, t.get_position()[1]))
            t.set_ha('left')
            t.set_color('w')   
        # -------     
        v = vs2[i]
        t = txt_ys[i]
        f = tr2.transform(t.get_window_extent())
        if abs(f[1][0] - f[0][0])<=(v-vmax*0.05):
            t.set_position((v-vmax*0.05, t.get_position()[1]))
            t.set_ha('right')
            t.set_color('w')
        v = vr2[i]
        t = txt_yr[i]
        f = tr2.transform(t.get_window_extent())
        if abs(f[1][0] - f[0][0])<=(v-vmax*0.05):
            t.set_position((v-vmax*0.05, t.get_position()[1]))
            t.set_ha('right')
            t.set_color('w')  
    # ------
    ax1.spines["top"   ].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["left"  ].set_visible(False)
    ax2.spines["top"   ].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right" ].set_visible(False)
    wax = 0.5-0.05-0.15/2*(smax+5)/15
    ax1.set_position([0.05,     0.11, wax, 0.85])
    ax2.set_position([0.95-wax, 0.11, wax, 0.85])
    # redraw
    fig_handle.canvas.draw()


def bfastClass(fig_handle, index_class=1, labels=None, colors=None, inversed=True, fontsize=None):
    # labels and colors are in squence of index_class [1-5]
    if labels is None:
        labels = [            
            ["A", "intervention not necessary"   ],
            ["B", "intervention in long-term"    ],
            ["C", "intervention in medium-term"  ],
            ["D", "intervention in short-term"   ],
            ["E", "intervention extremely urgent"],
        ]
    if colors is None:
        colors = [
            (146/255, 208/255, 80/255),
            (255/255, 255/255,  0/255),
            (255/255, 192/255,  0/255),
            (226/255, 107/255, 10/255),
            (255/255,   0/255,  0/255),
        ]
    fontsize = fontsize or 8
    # figure
    if fig_handle is None:
        fig_handle = plt.figure()
    fig_handle.clf()
    axes = fig_handle.add_subplot(111)
    axes.set_aspect("equal")
    axes.set_axis_off()
    # figsize = (16/2.54, 7/2.54), dpi = 200
    w = 16/2.54*200/1.2 # 10*d
    d =  7/2.54*200/6.0 # fontsize*1.2
    d1= d if inversed else -d
    # plot class list
    for i,p in enumerate(labels):
        if i != index_class -1:
            x = [0, w, w, 0]
            y = [i*d1-d1/2, i*d1-d1/2, i*d1+d1/2, i*d1+d1/2]
            axes.fill(x, y, color=colors[i], alpha=0.5, lw=0)
            axes.text( 0.05*w, i*d1      , p[1], color='grey', va='center', ha='left', size=fontsize)
            axes.text(-0.05*w, i*d1-0.1*d, p[0], color=(0.7,0.7,0.7), va='center', ha='center', size=fontsize*2)
    # highlight current class
    i = index_class -1
    p = labels[i]
    x = [-0.02*w, w*1.02, w*1.02, -0.02*w]
    y = [i*d1-d1/2-0.1*d1, i*d1-d1/2-0.1*d1, i*d1+d1/2+0.1*d1, i*d1+d1/2+0.1*d1]
    axes.fill(x, y, color=colors[i], alpha=1)
    axes.text(0.02*w, i*d1, p[1], fontweight='bold', va='center', ha='left', size=fontsize*1.35)
    # current class index
    axes.text(-0.15*w, i*d1-0.1*d, p[0], va='center', ha='center', fontweight='bold', size=fontsize*4.5, color=colors[i])
    axes.plot(-0.15*w, i*d1, color=colors[i], marker='o', markersize=fontsize*6, fillstyle='none', mew=fontsize*0.3)
    axes.plot(-0.15*w-fontsize*4.5, i*d1, color='w')
    fig_handle.tight_layout()
    # redraw
    fig_handle.canvas.draw()
