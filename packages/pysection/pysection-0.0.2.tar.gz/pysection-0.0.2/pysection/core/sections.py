
from math import log,exp,sqrt,cos,sin,atan2,pi
import os
import uuid
import numpy as np
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
from .materials import Concrete, Steel, Masonry
from .mpl_plots import sectionShape, RCdomains
from . import sect_utils as sg # import Area, rcShape, rcRebar, rcShear, plotGeometry

_node = uuid.getnode()

# functions 
def get_float(entry, unit=1, default=None):
    # get value in float from database entry
    try:
        r = float(entry)*unit
    except ValueError:
        r = default
    return r


def get_profile_list(lib_db=None, table=None):
    if lib_db is None:
        lib_db = "../data/steel_profiles.db"
    if table is None:
        table = "ProfilesEU"
    path0 = os.path.abspath(os.path.dirname(__file__))
    path_db = os.path.join(path0, lib_db)
    db = sql.connect(path_db)
    cur = db.cursor()
    cur.execute(f'SELECT Designation FROM {table}')
    data = []
    for row in cur.fetchall():
        data.append(row[0])
    return data
    

def get_profile(name='IPE 100', lib_db=None, table=None):
    '''
    Standard Steel Profile (European) section defined by: 
        name = (string) label of standard profile, like 'IPE 100', 'HE 100 A', 'CHS 139.7 x 6.3'
    '''
    # get dimensions and properties from db
    if lib_db is None:
        lib_db = "../data/steel_profiles.db"
    if table is None:
        table = "ProfilesEU"
    path0 = os.path.abspath(os.path.dirname(__file__))
    path_db = os.path.join(path0, lib_db)
    db = sql.connect(path_db)
    cur = db.cursor()
    cur.execute(f'PRAGMA TABLE_INFO({table})')
    names = [tup[1] for tup in cur.fetchall()]
    cur.execute(f'SELECT * FROM  {table}  WHERE Designation="{name}"')
    entry = cur.fetchone()
    db.close()
    if entry:
        # print("profile %s found in database" % name)
        # dimensions
        h = get_float(entry[names.index("h")])
        b = get_float(entry[names.index("b")])
        tw= get_float(entry[names.index("tw")])
        tf= get_float(entry[names.index("tf")])
        t = get_float(entry[names.index("t")])
        r = get_float(entry[names.index("r")])
        r1= get_float(entry[names.index("r1")])
        r2= get_float(entry[names.index("r2")])
        # properties
        A    = get_float(entry[names.index("A")])
        Avz  = get_float(entry[names.index("Avz")],100)
        Iyy  = get_float(entry[names.index("ly")],10000)
        Izz  = get_float(entry[names.index("lz")],10000)
        Iyz  = get_float(entry[names.index("lyz")],10000,0)
        Wely = get_float(entry[names.index("Wely")],1000,0)
        Welz = get_float(entry[names.index("Welz")],1000,0)
        Wply = get_float(entry[names.index("Wply")],1000,0)
        Wplz = get_float(entry[names.index("Wplz")],1000,0)
        It   = get_float(entry[names.index("lt")],10000,0)
        Cw   = get_float(entry[names.index("lw")],1000000000,0)
        I11  = get_float(entry[names.index("lu")],10000)
        I22  = get_float(entry[names.index("lv")],10000)
        theta = get_float(entry[names.index("α")],1,0)
        I11 = I11 or Iyy
        I22 = I22 or Izz
        # ----------------------------
    else:
        print("profile {} does not exist in library!!!".format(name))
        return None
    # common profiles sections
    inner_points = []
    if any(s in name for s in ["IPE", "HE", "HL", "HD", "HP"]):
        points = sg.DoubleT(h, b, tf, tw, r)
        Avy = 2*b *tf
    elif any(s in name for s in ["IPN"]):
        points = sg.IPN(h, b, tf, tw, r1, r2)
        Avy = 2*b *tf
    elif any(s in name for s in ["UPE"]):
        points = sg.PFC(h, b, tf, tw, r)
        Avy = 2*b *tf  
    elif any(s in name for s in ["UPN","U"]):
        points = sg.UPN(h, b, tf, tw, r1, r2)
        Avy = 2*b *tf   
    elif any(s in name for s in ["L"]):
        points = sg.Angle(h, b, t, r1, r2)     
        Avy = b *t
        Avz = h *t
    elif any(s in name for s in ["RHS","SHS"]):
        points, inner_points = sg.RHS(h, b, t, r1, r2)  
        Avy = A*b/(b+h)
        Avz = A*h/(b+h)
    elif any(s in name for s in ["CHS"]):
        points, inner_points = sg.CHS(h, t)    
        Avy = A*2/pi
        Avz = A*2/pi
    else:
        return None
    
    profile = {
        "name":name, "h":h, "b":b, "tw":tw, "tf":tf, "t":t, "r":r, "r1":r1, "r2":r2, "I11":I11, "I22":I22, "theta":theta,
        "A":A, "Avz":Avz, "Avy":Avy, "Iyy":Iyy, "Izz":Izz, "Iyz":Iyz, "Wely":Wely, "Welz":Welz, "Wply":Wply, "Wplz":Wplz, "It":It, "Cw":Cw,
        "points": [points], "inner_points":[inner_points], "bounds":sg.Polygons([points]).bounds
    }
    return profile


class Section:
    '''
    For 'RC' section of Reinforced Concrete:
        mat = Concrete type material, e.g. Concrete(fck=20, LC=1)
        mrf = Steel type reinforcing material, e.g. Steel(fyk=450, LC=1)
        shape = polygon of concrete
            = 'rect'  = rectangle, defined by depth d and width b;
            = 'circ'  = circle, defined by diameter d;
            = 'angle' = angle(L), defined by depth d, width b, horizontal leg thickness t, vertical leg thickness t1;
            = 'tee'   = tee(T), defined by depth d, width b, flange thickness t, web thickness t1
            = 'user'  = input via polygons [[(y, z),...],...]
        rebar = [dict(y, z, d),...]  
            list of rebar position and diameter, or simple definitions in dictionary:
            - perimetric distributed with maximum spacing of (smax) (and limited by length of side of concrete shape): 
                rebar = dict(
                    type = 'peri',    
                    d    =     16,   # [mm] diameter
                    cc   =     40,   # [mm] clear cover from concrete edge
                    smax =    200,   # [mm] maximum spacing allowed to distribute rebars
                    )
            - circular distributed with total number of (n):
                rebar = dict(
                    type = 'circ',
                    d    =     16,   # [mm] diameter
                    r    =    150,   # [mm] radius from cenctroid ceneter of concrete 
                    n    =      8,   # [mm] total number of rebars 
                    )
            - symmetrically linear distributed along geometric limits of concrete:
                !! only for concrete shape of rectangle without rotation !!
                rebar = dict(
                    type = 'symx', or 'symy',
                    d    =     16,   # [mm] diameter
                    cc   =     40,   # [mm] clear cover from concrete bounds
                    n    =      4,   # [mm] number of rebars on each side
                    )
        stirr = [(y, z, d, n, s, beta, bw, alpha, theta), ...]  
            list of ref-position, diameter, legs, spacing, direction, effective with, inclination, strut
            or simple stirrup in x and y directions in dictionary:
                stirr = dict(
                    d    =   16,
                    s    =  200,
                    nx   =    2,
                    ny   =    2,
                    )

    For 'ST' section of Steel Beam:
        mat = Steel type material, Steel(fyk=300, gamma=1.05)
        profile = name of standard profile, e.g. 'IPE 200', 'HE 300 A', or
            = 'user' with difinition in polygons = [[(y, z),...],...]

    For 'MS' section of Masonry Wall:
        mat = Masonry type material, e.g. Masonry(mt=9, LC=2)
        shape = as per RC section above, or 
            = 'user' with polygons = [[(y, z),...],...] 
    '''

    def __init__(self, name=None, mat=None, mrf=None, 
                    shape=None, d=None, b=None, t=None, r=None, b1=None, t1=None, r1=None, 
                    rebar=None, stirr=None, polygons=None, profile=None):

        self.id    = uuid.uuid1(_node).int
        if shape in ["rect","Rect","RECT"]:
            shape_name = f"{shape}_{b:.0f}x{d:.0f}"
        elif shape in ["circ","Circ","CIRC"]:
            shape_name = f"{shape}_{d:.0f}"
        elif shape in ["angle","L"]:
            shape_name = f"{shape}_{b:.0f}x{t:.0f}_{d:.0f}x{t1:.0f}"
        elif shape in ["tee","T"]:
            shape_name = f"{shape}_{b:.0f}x{t:.0f}_{d:.0f}x{t1:.0f}"
        else:
            shape_name = None
        self.name  = name or profile or shape_name      
        self._type = None
        # default values
        self.mat      = {}
        self.mrf      = {}
        self.Emod     = 0
        self.Gmod     = 0
        self.gam      = 0
        self.A        = 0
        self.As       = 0
        self.Avy      = 0
        self.Avz      = 0
        self.Avym     = 0
        self.Avzm     = 0
        self.yc       = 0
        self.zc       = 0
        self.It       = 0
        self.I11      = 0
        self.I22      = 0
        self.Iyy      = 0
        self.Izz      = 0
        self.Iyz      = 0
        self.Wely     = 0
        self.Welz     = 0
        self.Wply     = 0
        self.Wplz     = 0
        self.theta    = 0
        self.theta_origin = 0
        self.points   = []
        self.inner_points = []
        self.bounds  = [0,0,0,0]
        self.rebar   = []
        self.stirr   = []
        self.profile = None
        self.shape_inputs = {"shape":shape, "d":d, "b":b, "t":t, "r":t, "b1":b1, "t1":t1, "r1":r1}
        self.reinf_inputs = {"rebar":rebar,"stirr":stirr}
        # not dummy instance
        if self.name is not None:
            if mat is None:
                mat = Concrete()
            if isinstance(mat, (Concrete, Steel, Masonry)):
                mat = mat.__dict__
            if mrf is None and mat["_type"] =="Concrete":
                mrf = Steel()
            if isinstance(mrf, (Concrete, Steel, Masonry)):
                mrf = mrf.__dict__
            self.mat   = mat 
            self.mrf   = mrf 
            self.Emod  = self.mat["Emod"]
            self.Gmod  = self.mat["Gmod"]
            # type of section
            if self.mat["_type"]=='Concrete':
                self._type = 'RC'
            elif self.mat["_type"]=='Steel':
                self._type = 'ST'
            elif self.mat["_type"]=='Masonry':
                self._type = 'MS'
            # get shape and properties, reinforcements
            #   from input 'polygons' list of lists of points [[(x1, y1),...],...]
            #   from input 'profile' standard steel section library
            #   from input 'shape' and dimensions d,b,t,...
            self.set_shape(points=polygons, profile=profile, shape=shape, d=d, b=b, t=t, r=r, b1=b1, t1=t1, r1=r1)
            self.set_reinforcements()
            self.theta_origin = self.theta
            self.yc_origin = self.yc
            self.zc_origin = self.zc
            # get resistance
            self.gam  = self.A * self.mat["rho"] / 1e8  # [kg/m3 * mm2 =>  kN/m] 
            # print(f"-> creating cross section [{self._type} - {self.name}]...")
            self.get_domains()
            self.get_axial_resistance()

    def from_dict(self, vdict):
        self.__dict__.update(vdict)
        return self

    def set_shape(self, points=None, inner_points=None, profile=None, shape='rect', d=500, b=300, t=0, r=0, b1=0, t1=0, r1=0):
        '''
        get sections properties from one of following input in sequence (first valid input):
            #   from input 'points' and 'inner_points' list of lists of points [[(x1, y1),...],...]
            #   from input 'profile' standard steel section library
            #   from input 'shape' and dimensions d,b,t,...
        return dict{}
        '''
        if points is not None:
            # using ponts and inner_points
            polygons = sg.Polygons(points)
            prop = polygons.get_properties_with_holes(inner_points)
        else:
            if profile is not None:
                profile = get_profile(name=profile)
            if profile is not None:
                # steel profile from library
                self.profile = profile["name"]
                prop = profile
            else:
                # read from shape and dimensons
                prop = sg.simple_shape(shape, d, b, t, r, b1, t1, r1)
        if prop is not None:
            self.__dict__.update(prop)


    def set_reinforcements(self, rebar=None, stirr=None, cc=40):
        # cc = 40  # default for plot
        if rebar is None:
            rebar = self.reinf_inputs["rebar"]
        if stirr is None:
            stirr = self.reinf_inputs["stirr"]
        if self._type == 'RC':
            # longitudinal reinforcement
            polygons = sg.Polygons(self.points)
            rebar1, stirr1, cc = sg.simple_reinf(rebar=rebar, stirr=stirr, concr=polygons, cc=cc, dc=self.shape_inputs["d"], beta0=0)
            # assign to section
            self.rebar = rebar1 # sg.Rebar(rebar)
            self.stirr = stirr1 # sg.Stirrup(stirr)
        else:
            self.rebar = {"d":[], "As":[]}
            self.stirr = {"d":[]}
        self.As = np.array(self.rebar["As"]).sum()
        self.cc = cc


    def change_polygons(self, points=None):
        '''
        re-define polygon shape keeping definitions of reinforcements
        '''
        polygons = sg.Polygons(points)
        prop = polygons.get_properties_with_holes()
        self.__dict__.update(prop)
        # update reinforcements
        beta0 = self.theta - self.theta_origin
        rebar1, stirr1, cc = sg.simple_reinf(rebar=self.reinf_inputs["rebar"], stirr=self.reinf_inputs["stirr"], concr=polygons, cc=self.cc, dc=self.shape_inputs["d"], beta0=beta0)
        self.rebar = rebar1
        self.stirr = stirr1
        self.cc    = cc
        # update domains
        self.get_domains()
        self.get_axial_resistance()
        

    def strain_to_force(self, eps=[0], chi=[0], phi=0, concr=None, rebar=None):
        '''
        for RC section, to
        calculate resultant axial and bending forces under section deformation (strain)
        section curvature / strain distribution = eps + v*chi
            eps = [] = list of axial strain at centroid center, (= epsc1- vc1*chi1 from concrete compression edge)
            chi = [] = list of section inclination [1/mm] about axis direction at phi, ( = (epsc1-epsc2)/(vc1-vc2))
                eps and chi must have same numbers of elements!
            phi = 0  = angle (in degrees) of incliation axis (bending axis) direction
        return forces in concrete and reinforcement:
            (Nc, Mc, Ns, Ms) in unit [N, mm]
        '''
        # section curvature / strain distribution = eps1 + [z]*chi1
        if concr is None:
            polygons = sg.Polygons(self.points)
            concr1 = polygons.rotate(angle=-phi)
        else:
            concr1 = concr
        if rebar is None:
            rebar   = sg.Rebars(self.rebar)
            rebar1  = rebar.rotate(angle=-phi, origin=(self.yc, self.zc))
        else:
            rebar1 = rebar
        # deformations
        if type(eps) in [int, float]:
            eps = [eps]
        if type(chi) in [int, float]:
            chi = [chi]
        n = min(len(eps),len(chi))
        Nc = [0]*n
        Mc = [0]*n
        Ns = [0]*n
        Ms = [0]*n
        for i in range(n):
            # forces in concrete
            Nc[i],Mc[i] = concr1.get_concrete_forces(eps=eps[i], chi=chi[i], z0=self.zc, fcd=self.mat["fcd"], ecy=self.mat["eps_c2"], ecu=self.mat["eps_cu2"])
            # forces in rebar, inclinded bi-linear model
            if rebar1 is not None:
                Ns[i],Ms[i] = rebar1.get_forces(eps=eps[i], chi=chi[i], z0=self.zc, fyd=self.mrf["fyd"], ftd=self.mrf["ftd"], Es=self.mrf["Emod"], esu=self.mrf["epst"])
            else:
                Ns[i],Ms[i] = 0,0
        return (Nc, Mc, Ns, Ms)


    def calc_domain(self, phi=0, n=1):
        '''
        This function calculates the ULS bending resistance about axis u-u of fiber section
        concrete prarabolic model, EN1992-1-1: 3.1.7, n=2 
        steel bilinear model,  EN1992-1-1: 3.3.6
          n   = 1 =  interpolation level on domain points
          phi = 0 =  bending axis u-u in direction angle (in degrees)
        '''
        # ----------------------------------------------- construct list of deformation cases
        # coordinates in phi [u v] 
        polygons = sg.Polygons(self.points)
        rebar    = sg.Rebars(self.rebar)
        concr1 = polygons.rotate(angle=-phi)
        rebar1 = rebar.rotate(angle=-phi, origin=(self.yc, self.zc))
        cb = concr1.bounds  # vc = [v[1] for v in concr1] 
        sb = rebar1.bounds  # vs = [v[1] for v in rebar1]
        vc1= cb[3]-self.zc # max(vc) # bottom edge
        vc2= cb[1]-self.zc # min(vc) # top edge
        vs1= sb[3]-self.zc # max(vs) # bottom rebar
        vs2= sb[1]-self.zc # min(vs) # top rebar
        # resulting bending moment reference center
        # vn = 0; # about centroid center of concrete
        # given stress-stain states
        ec2 = self.mat["eps_c2"]
        ecu = self.mat["eps_cu2"]
        esu = self.mrf["epst"]
        # ect = concrete top edge (-)             
        # ecb = concrete bottom edge (+) 
        # ---
        ect = np.linspace(esu, -ecu, 4*n)
        ecb = esu + np.linspace(0, esu+ecu, 4*n)/(vc2-vs1)*(vs1-vc1)
        # ---
        ect = np.append(ect, -ecu*np.ones(4*n))
        ecb = np.append(ecb, np.linspace(esu, min(ecu*3,esu/2), 4*n))
        # ---
        ect = np.append(ect, -ecu*np.ones(4*n))
        ecb = np.append(ecb, np.linspace(min(ecu*3,esu/2), ecu, 4*n))
        # ---
        ect = np.append(ect, -ecu*np.ones(4*n))
        ecb = np.append(ecb, np.linspace(ecu,  0, 4*n)) 
        # ---
        ect = np.append(ect, np.linspace(-ecu, -ec2, 4*n))
        ecb = np.append(ecb, np.linspace(0, -ec2, 4*n))
        # ---
        ect = np.append(ect, np.linspace(-ec2, 0, 4*n))
        ecb = np.append(ecb, np.linspace(-ec2, -ecu, 4*n))
        # ---
        ect = np.append(ect, np.linspace(0,  ecu, 4*n))
        ecb = np.append(ecb, -ecu*np.ones(4*n))
        # ---
        ect = np.append(ect, np.linspace(ecu, min(ecu*3,esu/2), 4*n))
        ecb = np.append(ecb, -ecu*np.ones(4*n))
        # ---
        ect = np.append(ect, np.linspace(min(ecu*3,esu/2), esu, 4*n))
        ecb = np.append(ecb, -ecu*np.ones(4*n))
        # ---
        ect = np.append(ect, esu + np.linspace(esu+ecu,0, 4*n)/(vc1-vs2)*(vs2-vc2))
        ecb = np.append(ecb, np.linspace(-ecu, esu, 4*n))
        # --------
        df = pd.DataFrame({"ect":ect,"ecb":ecb})
        df = df.drop_duplicates()
        df["chi"] = (df["ecb"]-df["ect"])/(vc1-vc2)
        df["eps"] =  df["ecb"]-df["chi"]*vc1
        # ----------------------------------------------- calculate forces
        Nc, Mc, Ns, Ms = self.strain_to_force(eps=df["eps"].tolist(), chi=df["chi"].tolist(), concr=concr1, rebar=rebar1)
        df["Nc"]  = Nc
        df["Mc"]  = Mc
        df["Ns"]  = Ns
        df["Ms"]  = Ms
        df["N"]  = df["Nc"]/1e3 + df["Ns"]/1e3
        df["M"]  = df["Mc"]/1e6 + df["Ms"]/1e6
        # -----------------------------------------------
        return df[["N","M"]].drop_duplicates().values
    

    def plot_domain(self, phi=0, n=1, forces=[], filename=None, fontsize=8, figsize=None, ext='png'):
        filename = filename or 'sect_domain'
        fontsize = fontsize or 8
        figsize = figsize or (8/2.54,8/2.54)
        NM = self.calc_domain(phi=phi, n=n)
        domains = {f"phi={phi}": NM}
        fig_handle = plt.figure(figsize=figsize)
        RCdomains(fig_handle, domains, forces=forces, fontsize=fontsize)
        # save
        if type(filename) in [str]:
            fig_handle.savefig(f"{filename}.{ext}", dpi=300)
        else:
            plt.savefig(filename, format='svg')
        plt.close()


    def get_domains(self, alpha=0):
        if self._type =="RC":
            # calc domain Nx-Mu(phi)
            NMy = self.calc_domain(0-alpha).tolist()
            NMz = self.calc_domain(-90-alpha).tolist()
        else:
            NMy = []
            NMz = []
        self.domains = {"My":NMy, "Mz":NMz}

    def plot_domains(self, filename=None, forces=[], fontsize=8, figsize=None, ext='png'):
        filename = filename or 'sect_domains'
        fontsize = fontsize or 8
        figsize = figsize or (12/2.54,12/2.54)
        fig_handle = plt.figure(figsize=figsize)
        RCdomains(fig_handle, self.domains, forces=forces, fontsize=fontsize)
        # save
        if type(filename) in [str]:
            fig_handle.savefig(f"{filename}.{ext}", dpi=300)
        else:
            plt.savefig(filename, format='svg')
        plt.close()


    def get_axial_resistance(self):
        '''return (Nc, Nt)'''
        if self._type =="RC":
            Nc  = ((self.A - self.As) * self.mat["fcd"] + self.As * self.mrf["fyd"]) / 1000
            Nt  = self.As * self.mrf["fyd"]/ 1000
        elif self._type =="ST":
            Nc  = self.A * self.mat["fyd"] /1000
            Nt  = Nc
        elif self._type =="MS":
            Nc = self.A * self.mat["fd"] /1000
            Nt = 0
        else:
            Nc, Nt = 0, 0
        self.axial_resistances = {"Nc":Nc,"Nt":Nt}
        # return (Nc, Nt)


    def get_flexure_resistance(self, Nx=0, sign_My=0, sign_Mz=0):
        '''return (My, Mz)'''
        if self._type =="RC":
            # calc domain Nx-Mu(phi)
            NMy = self.domains["My"]
            NMz = self.domains["Mz"]
            Nyd = [f[0] for f in NMy]
            Myd = [f[1] for f in NMy]
            Nzd = [f[0] for f in NMz]
            Mzd = [f[1] for f in NMz]
            if Nx < min(Nyd) or Nx > max(Nyd): 
                return (0, 0)
            if Nx < min(Nzd) or Nx > max(Nzd): 
                return (0, 0)
            # domain as polygon
            dmy = sg.Polygons([NMy])
            dmz = sg.Polygons([NMz])
            ty, lsy = dmy.linecut(origin=(Nx, 0), angle=90, r=max(max(Myd),-min(Myd)))
            tz, lsz = dmz.linecut(origin=(Nx, 0), angle=90, r=max(max(Mzd),-min(Mzd)))
            My1 = 0 # positive
            My2 = 0 # negative
            Mz1 = 0 # positive
            Mz2 = 0 # negative
            if ty>0:
                for l in lsy:
                    My1 = max(My1, max(l.coords.xy[1]))
                    My2 = min(My2, min(l.coords.xy[1]))
                    if sign_My>0:
                        Myd = My1
                    elif sign_My<0:
                        Myd = My2
                    else:
                        Myd = min(abs(My1),abs(My2))
            if tz>0:
                for l in lsz:
                    Mz1 = max(Mz1, max(l.coords.xy[1]))
                    Mz2 = min(Mz2, min(l.coords.xy[1]))
                    if sign_Mz>0:
                        Mzd = Mz1
                    elif sign_Mz<0:
                        Mzd = Mz2
                    else:
                        Mzd = min(abs(Mz1),abs(Mz2))
        elif self._type =="ST":
            # elastic limit #TODO
            Myd = (1 - abs(Nx)*1e3 / self.A / self.mat["fyd"]) * self.Wely * self.mat["fyd"] / 1e6
            Mzd = (1 - abs(Nx)*1e3 / self.A / self.mat["fyd"]) * self.Welz * self.mat["fyd"] / 1e6
        elif self._type =="MS":
            # NTC 2018: Eq.7.8.2 # TODO check?
            ly = self.bounds[2] - self.bounds[0]
            lz = self.bounds[3] - self.bounds[1]
            if Nx<0:
                Myd, Mzd = 0, 0 
            else:
                Myd = (lz/1000 * Nx/2) * (1 - Nx*1000 /self.A /0.85 /self.mat["fd"])
                Mzd = (ly/1000 * Nx/2) * (1 - Nx*1000 /self.A /0.85 /self.mat["fd"])
        else:
            Myd, Mzd = 0,0
        return (Myd, Mzd)


    def get_shear_resistance(self, Nx=0, vmin=None, Crdc=None):
        '''return (Vy, Vz)'''
        '''
        Calculates the ULS shear resistance Vrd,z and Vrd,y of rectangular-type section
            Nx      = [kN] axial force on section (tension positive)
            vmin    = [MPa] min shear resistance of concrete
                    = None (default) calculated according to EN1992
        '''
        if self._type =="RC":
            # ----------------------------------------- section dimensions for shear
            rho = 0.5*self.As / self.A   # assuming half reinforcement in tension
            rho = min(rho, 0.02)
            # ----------------------------------------- compression state
            # axial compression
            scp = -Nx*1e3/self.A  # [MPa] compression positive
            # acw [-] coefficient taking account of the state of the stress in the compression chord
            # 1;  for non-prestressed structures
            # (1 + scp/fcd)      for 0 < scp <= 0.25*fcd         (6.11.aN)
            # 1.25               for 0.25*fcd < scp <= 0.5*fcd   (6.11.bN)
            # 2.5*(1 - scp/fcd)  for 0.5*fcd < scp < 1.0*fcd     (6.11.cN)
            if scp>=self.mat["fcvd"]:
                acw = 0.00001
            elif scp>0.5*self.mat["fcvd"]:
                acw = 2.5*(1-scp/self.mat["fcvd"])
            elif scp>0.25*self.mat["fcvd"]:
                acw = 1.25
            elif scp>0:
                acw = 1 + scp/self.mat["fcvd"]
            else:
                acw = 1
            # modify for resistance calculation
            scp = min(scp, 0.2*self.mat["fcvd"])
            # ----------------------------------------- resistance by concrete only
            stirr = sg.Stirrups(self.stirr)
            dy, bwy, dz, bwz = stirr.deff()
            kz  = min(1 + sqrt(200/dz), 2)
            ky  = min(1 + sqrt(200/dy), 2)
            if vmin is None:
                vzmin = 0.035 * kz**(3/2) * sqrt(self.mat["fck"])
                vymin = 0.035 * ky**(3/2) * sqrt(self.mat["fck"])
            else:
                vzmin = abs(vmin)
                vymin = abs(vmin)
            if Crdc is None:
                Crdc = self.mat["Crdc"]
            k1   = 0.15
            Vzc = (max(Crdc *kz *(100*rho*self.mat["fck"])**(1/3), vzmin) + k1*scp) * bwz * dz
            Vyc = (max(Crdc *ky *(100*rho*self.mat["fck"])**(1/3), vymin) + k1*scp) * bwy * dy
            Vzc = max(Vzc, 0)
            Vyc = max(Vzc, 0)
            # ---------------------------------------- resistance with shear reinforcement (strut and tie)
            Vt = stirr.Vrd_tie(fyd=self.mrf["fywd"])       # [N] Vrd,s   (EN)
            Vs = stirr.Vrd_strut(fcvd=self.mat["fcvd"], v1=self.mat["v1"], acw=acw)  # [N] Vrd,max (EN)
            # ---------------------------------------- total resistances 
            if self.mat["FC"] is None:
                # new-design (EN)
                Vy = max(Vyc, min(Vt[0], Vs[0])) 
                Vz = max(Vzc, min(Vt[1], Vs[1])) 
            else:
                # existing structure (NTC-2018, C. 617/2009 - § C8.7.2.5)
                Vy = Vyc + min(Vt[0], Vs[0])
                Vz = Vzc + min(Vt[1], Vs[1])
            Vy = Vy /1000
            Vz = Vz /1000
        elif self._type=="ST":
            Vy = self.mat["fyd"]/sqrt(3) * self.Avy /1000
            Vz = self.mat["fyd"]/sqrt(3) * self.Avz /1000
        elif self._type=="MS":
            sig0 = - Nx*1e3/self.A
            # Turnsek - Cacovic formula
            Vy = self.Avym *self.mat["taur"] *sqrt(1+sig0/self.mat["taur"]/1.5) /1e3
            Vz = self.Avzm *self.mat["taur"] *sqrt(1+sig0/self.mat["taur"]/1.5) /1e3
            Vy = max(Vy, 0)
            Vz = max(Vz, 0)
        else:
            Vy, Vz = 0,0
        return (Vy, Vz)


    def __repr__(self):
        return '<Cross Section {} - {}>'.format(self._type, self.name)
    

    def plot_geometry(self, filename=None, rebar=True, stirr=False, figsize=None, fontsize=None, cc=None, z_inversed=False, ext='png'):
        filename = filename or self.name+'_geometry'
        figsize = figsize or (16/2.54, 8/2.54)
        fontsize = fontsize or 8

        fig_handle = plt.figure(figsize=figsize)
        sectionShape(fig_handle, self.__dict__, rebar=rebar, stirr=stirr, fontsize=fontsize, cc=cc, z_inversed=z_inversed)
        # save
        if type(filename) in [str]:
            fig_handle.savefig(f"{filename}.{ext}", dpi=300)
        else:
            fig_handle.savefig(filename, format='svg')
        plt.close()

