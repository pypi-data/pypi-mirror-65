import os
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def create_view(sln_dir="data_sln", res_dir="data_res", types=None, groups=None, title="View of Results", view_html=None):
    '''
    show results in 3d view.
        sln_dir    = directory where sln files (.json) saved, see function "get_sln()", if sln_dir=None, only show sln checked;
        res_dir    = directory where results files (.json) saved, see function "run_check()";
        types      = list of types  of sln to be shown [default=None, show all];
        groups     = list of groups of sln to be shown [default=None, show all];
        view_html  = save view plot to html file [default=None, view only].
    '''
    ## Preparing data
    # ---- check results log
    try:
        with open(f"{res_dir}/_summary.json","r") as f:
            log = json.load(f)
    except:
        print("results not valid!")
        raise
    # ----- filters
    print("\nreading results...")
    all_df = pd.DataFrame(log["summary"])
    all_df["file"] = log["sln"]
    if types is not None:
        all_df = all_df.loc[all_df["type" ].isin(types ),:]
    if groups is not None:
        all_df = all_df.loc[all_df["group"].isin(groups),:]
    # -----
    frm_df = all_df["SLN"].to_frame()
    for k in ["node1","x1","y1","z1", "node2","x2","y2","z2"]:
        frm_df[k] = 0
    sln = []
    for ind,row in all_df.iterrows():
        data = json.load(open(f"{res_dir}/{row['file']}","r"))
        sln += [data]
        frm_df.loc[ind, ["node1","x1","y1","z1"]] = data["node1"].values()
        frm_df.loc[ind, ["node2","x2","y2","z2"]] = data["node2"].values()
    # ----- structural line frame
    print("sorting results...")
    if sln_dir is not None:
        try:
            with open(f"{sln_dir}/_index.json","r") as f:
                log = json.load(f)
        except:
            print("results not valid!")
            raise
        frm_df = pd.DataFrame(log["sln"]).T
    frm_df = frm_df.loc[frm_df["node1"]>0,:]
    frm_df = frm_df.loc[frm_df["node2"]>0,:]
    # ------- values
    x = []
    y = []
    z = []
    grp = []
    val = []
    lab = []
    for s in sln:
        nd1 = np.array([s["node1"]["x"], s["node1"]["y"], s["node1"]["z"]])
        nd2 = np.array([s["node2"]["x"], s["node2"]["y"], s["node2"]["z"]])
        pp = [nd1 + (nd2-nd1)*min(max(0.05, x/s["length"]), 0.95) for x in s["stations"]]
        x += [p[0] for p in pp]
        y += [p[1] for p in pp]
        z += [p[2] for p in pp]
        grp += [f'{s["type"]}{s["group"]}']*len(pp)
        val += [r["rho"] for r in s["results"]]
        lab += [
f'''SLN.{s["id"]} [{s["name"]}]<br>
    s = {s["stations"][i]:5.3f} [{s["sections"][i]["name"]}]<br>
    rho = {s["results"][i]["rho"]:5.3f}<br>
    rho<sub>flexure</sub>={s["results"][i]["rho_flexure"]:5.3f}<br>
    rho<sub>shear  </sub>={s["results"][i]["rho_shear"  ]:5.3f}'''
            for i in range(len(pp))
        ]
    val_df = pd.DataFrame({"x":x,"y":y,"z":z,"grp":grp,"val":val,"lab":lab})
    # -----------------------------
    print("creating elements for view...")
    lines = [
        go.Scatter3d(
            x=[row["x1"],row["x2"]],
            y=[row["y1"],row["y2"]],
            z=[row["z1"],row["z2"]],
            mode= "lines",
            line={"color":'grey',"width":2.5},
            hoverinfo='skip',
            hovertext='none',
            showlegend=False
        ) for _,row in frm_df.iterrows()
    ]
    # values scatters
    ugrp = val_df["grp"].unique()
    points = [go.Scatter3d(
        x=val_df.loc[val_df["grp"]==g,"x"],  
        y=val_df.loc[val_df["grp"]==g,"y"],  
        z=val_df.loc[val_df["grp"]==g,"z"],
        mode="markers",
        marker=dict(
            size=val_df.loc[val_df["grp"]==g,"val"]*100,
            sizemode='area',
            sizeref=2.*100/(40.**2),
            sizemin=4, 
            opacity=0.8, 
            cmin=0,
            cmax=1,
            color=val_df.loc[val_df["grp"]==g,"val"], 
            colorbar={"title":'rho'}, 
            colorscale='Temps'
        ),
        name=f'group {g}',
        hovertext=val_df.loc[val_df["grp"]==g,"lab"],
        hoverinfo='text',
        hoverlabel=dict(bgcolor='white')
    ) for g in ugrp
    ]
    layout = dict(
        title=title,
        scene=dict(
            aspectratio=dict(x=1, y=1, z=1),
            aspectmode='data',
            # bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showspikes=False, showticklabels=False, showbackground=False, title=""),
            yaxis=dict(showgrid=False, showspikes=False, showticklabels=False, showbackground=False, title=""),
            zaxis=dict(showgrid=False, showspikes=False, showticklabels=False, showbackground=False, title="")
        ),
        # showlegend=False,
        legend=dict(x=0,y=1),
        shapes=[]
    )
    fig = go.Figure(data=lines+points, layout=layout)
    if view_html is None:
        fig.show()
    else:
        fig.write_html(view_html, auto_open=True)
    print("done.")
