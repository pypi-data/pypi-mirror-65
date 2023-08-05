import uuid
from math import log,exp,sqrt

_node = uuid.getnode()

class Material:
    '''
    genenral base
    '''
    id       = 0 
    _type    = None
    LC       = None
    FC       = 1
    rho      = 0
    gamma    = 1
    Emod     = 0
    Gmod     = 0
    nv       = 0
    # # concrete
    # fck      = 0
    # t        = 0
    # s        = 0
    # alpha_cc = 0
    # alpha_ct = 0
    # v1       = 0
    # fcd      = 0
    # fcvd     = 0
    # fctd     = 0
    # eps_c1   = 0
    # eps_c2   = 0
    # eps_c3   = 0
    # eps_cu1  = 0
    # eps_cu2  = 0
    # eps_cu3  = 0
    # Crdc     = 0
    # # steel
    # fyk      = 0
    # ftk      = 0
    # fyd      = 0
    # fywd     = 0
    # ftd      = 0
    # epst     = 0
    # # masonry
    # mt       = 0
    # name     = None
    # f        = 0
    # fv0      = 0
    # tau0     = 0
    # fd       = 0
    # taur     = 0
    def __repr__(self):
        return '<Material - {}>'.format(self._type)


class Concrete(Material):
    ''' 
    define Concrete properties - ref. EN1992-1-1: Table 3.1 - Eq.(3.15-3.16) 
        fck = [MPa]  characteristic cylinder strength [Default = 30]
        t   = [days] age of the concrete [Default = 28]
        s   = [-]    coefficient which depends on the type of cement [Default = 0.25]
            = 0.20 for cement of strength Classes CEM 42,5 R, CEM 52,5 N and CEM 52,5 R (Class R)
            = 0.25 for cement of strength Classes CEM 32,5 R, CEM 42,5 N (Class N) 
            = 0.38 for cement of strength Classes CEM 32,5 N (Class S)
        gamma     = partial coefficient of concrete [Default = 1.5]
        alpha_cc  = coefficient taking account of long term effects on the compressive strength [Default = 0.85]
        alpha_ct  = coefficient taking account of long term effects on the tensile strength [Default = 1.0]
        v1        = strength reduction for cracked [Default = 0.6*(1-fck/200)]
        rho       = [kg/m3] density [Default = 2400]
        nv        = poisson's ratio [Default = 0.2]
        LC        = knowledge level (Livello di Conoscenza) of existing structure (ref.NTC) [Default = None]
    '''
    def __init__(self, fck=30, t=28, s=0.25, gamma=1.5, alpha_cc=0.85, alpha_ct=1.00, v1=None, rho=2400, nv=0.2, LC=None):
        self._type = "Concrete"
        self.id  = uuid.uuid1(_node).int
        self.fck = fck
        self.t   = t
        self.s   = s
        self.gamma  = gamma
        self.alpha_cc = alpha_cc
        self.alpha_ct = alpha_ct
        self.v1  = v1 or 0.6*(1-fck/250)
        self.rho = rho
        self.nv  = nv
        self.LC  = LC
        self.FC  = factorConfidence(LC=LC)
        # EN 1992-1-1
        fcm = fck+8
        if fck<=50:
            fctm = 0.30*fck**(2/3)
        else:
            fctm = 2.12*log(1+(fcm/10))
        Ecm = 22*(fcm/10)**0.3 *1e3    # [MPa]
        bcc = exp(s*(1-sqrt(28/t)))    # coefficient which depends on the age
        fcm = bcc*fcm
        a = 2/3
        if t<28:
            fck = fcm - 8
            a = 1
        fctm = bcc**a  *fctm
        Ecm  = bcc**0.3 *Ecm
        Gcm  = Ecm/2/(1+nv)
        # Store parameters
        self.fck_cube  = 2.8
        self.fcm       = fcm
        self.fctm      = fctm
        self.fctk_05   = 0.7*fctm
        self.fctk_95   = 1.3*fctm
        self.Emod      = Ecm
        self.Gmod      = Gcm
        self.eps_c1    = min(0.7*fcm**0.31, 2.8)*1e-3
        self.eps_cu1   = (2.8+27*((98-fcm)/100)**4)*1e-3
        self.eps_c2    = (2.0+0.085*(fck-50)**0.53)*1e-3
        self.eps_cu2   = (2.6+35*((90-fck)/100)**4)*1e-3
        self.n         = (1.4+23.4*((90-fck)/100)**4)
        self.eps_c3    = (1.75+0.55*((fck-50)/40))*1e-3
        self.eps_cu3   = (2.6+35*((90-fck)/100)**4)*1e-3
        if fck<50: 
            self.eps_cu1 = 3.5*1e-3 
            self.eps_c2  = 2.0*1e-3
            self.eps_cu2 = 3.5*1e-3
            self.n       = 2.0 
            self.eps_c3  = 1.75*1e-3
            self.eps_cu3 = 3.5*1e-3
        # design values
        self.fc    = alpha_cc*fck
        self.fcd   = self.fc/gamma
        self.fctd  = alpha_ct*self.fctk_05/gamma
        self.Crdc  = 0.18/gamma
        self.fcvd  = self.fcd
        # modification for existing structure FC>0
        if self.FC is not None:
            self.fcd  = fck / self.FC
            self.fcvd = self.fcd /gamma
            self.Crdc = 0.18/gamma / self.FC

class Steel(Material):
    '''
    define Steel/Rebar properties - ref. EN1992-1-1
        fyk = [MPa]  characteristic yielding strength [Default = 450]
        ftk = [MPa]  characteristic tensile strength [Default = fyk*1.15]
        gamma   = partial coefficient of steel reinforcement [Default = 1.15]
        rho     = [kg/m3] density [Default = 7850]
        Es      = [MPa] elastic modulus [Default = 210000]
        nv      = poisson's ratio [Default = 0.3]
        epst    = ultimate strain [Default = 0.075*0.9 = 0.0675]
        LC      = knowledge level (Livello di Conoscezna) of existing structure (ref.NTC) [Default = None]
    '''
    def __init__(self, fyk=450, ftk=None, gamma=1.15, rho=7850, Emod=210000.0, nv=0.3, epst=0.075*0.9, LC=None):
        self._type = "Steel"
        self.id  = uuid.uuid1(_node).int
        self.fyk = fyk
        self.ftk = ftk or fyk*1.15  # bars class C
        self.gamma   = gamma
        self.rho     = rho
        self.Emod    = Emod
        self.nv      = nv
        self.Gmod    = Emod/2/(1+nv)
        self.epst    = epst
        self.LC  = LC
        self.FC      = factorConfidence(LC=LC)
        self.fyd    = self.fyk/gamma
        self.ftd    = self.ftk/gamma
        self.fywd   = self.fyk/gamma
        if self.FC is not None:
            self.fyd    = fyk/self.FC
            self.ftd    = fyk/self.FC
            self.fywd   = fyk/gamma/self.FC

class Masonry(Material):
    '''
    define Masonry properties by tabled values - ref. Murature by NTC2018
        mt = type of masonry defined in NTC [Default = 9]
            1  - Muratura in pietrame disordinata
            2  - Muratura a conci sbozzati, con paramenti di spessore disomogeneo
            3  - Muratura a conci sbozzati, con paramenti di spessore disomogeneo (*contatti migliorati) 
            4  - Muratura in pietre a spacco con buona tessitura 
            5  - Muratura irregolare di pietra tenera
            6  - Muratura a conci regolari di pietra tenera
            7  - Muratura a blocchi lapidei squadrati 
            8  - Muratura in mattoni pieni e malta di calce
            9  - Muratura in mattoni pieni e malta di calce (***spessore di giunti superiore a 13mm)
            10 - Muratura in mattoni semipieni con malta cementizia
        f    = [Mpa] compression strength [Default = None if not in table]
        tau0 = [MPa] cracked shear strength [Default = None if not in table]
        fv0  = [MPa] shear strength [Default = None if not in table]
        gamma   = partial coefficient of masonry [Default = 2.0]
        rho     = [kg/m3] density [Default = None if not in table]
        Em      = [MPa] elastic modulus [Default = None if not in table]
        Gm      = [MPa] shear modulus   [Default = None if not in table]
        LC      = knowledge level (1/2/3) for existing structure (ref.NTC) [Default = None]
    '''
    def __init__(self, mt=0, f=None, fv0=None, tau0=None, Emod=None, Gmod=None, rho=None, gamma=2.0, LC=None):
        self._type = "Masonry"
        self.id  = uuid.uuid1(_node).int
        self.gamma   = gamma      
        self.LC      = LC
        # -----------------------------------------------------------
        # NTC-2018, Tab.C8.5.I - Valori di riferimento dei parametri meccanici della muratura
        # -----------------------------------------------------------
        # row = [Tipo_muratura, f_min, f_max, tau0_min, tau0_max, fv0_min, fv0_max, E_min, E_max, G_min, G_max, w_min, w_max, ]
        # Unit [MPa, kN/m3]
        ms_tab = {
            0 :["user-defined", 0,0,0,0, 0,0,0,0, 0,0,0,0],
            1 :["Muratura in pietrame disordinata (ciottoli, pietre erratiche e irregolari)",1.0,2.0,0.018,0.032,None,None,690,1050,230,350,19,19],
            2 :["Muratura a conci sbozzati, con paramenti di spessore disomogeneo",2.0,2.0,0.035,0.051,None,None,1020,1440,340,480,20,20],
            3 :["Muratura a conci sbozzati, con contatti migliorati",2.4,2.4,0.042,0.0612,None,None,1020,1440,340,480,20,20],
            4 :["Muratura in pietre a spacco con buona tessitura",2.6,3.8,0.056,0.071,None,None,1500,1980,500,660,21,21],
            5 :["Muratura irregolare di pietra tenera (tufo, calcarenite, ecc.)",1.4,2.2,0.028,0.042,None,None,900,1260,300,420,13,16],
            6 :["Muratura a conci regolari di pietra tenera (tufo, calcarenite, ecc.)",2.0,3.2,0.04,0.08,0.1,0.19,1200,1620,400,500,13,16],
            7 :["Muratura a blocchi lapidei squadrati",5.8,8.2,0.09,0.12,0.18,0.28,2400,3300,800,1100,22,22],
            8 :["Muratura in mattoni pieni e malta di calce",2.6,4.3,0.05,0.13,0.13,0.27,1200,1800,400,600,18,18],
            9 :["Muratura in mattoni pieni con giunti con spessore superiore a 13 mm",1.82,3.01,0.035,0.091,0.091,0.189,960,1440,320,480,18,18],
            10:["Muratura in mattoni semipieni con malta cementizia (es,: doppio UNI foratura  40%)",5.0,8.0,0.08,0.17,0.2,0.36,3500,5600,875,1400,15,15]
        }
        # ------------------------------------------------------------
        if mt not in range(11):
            mt = 0 
        self.mt = mt
        row = ms_tab[mt]
        self.name = row[0]
        f_min    = row[1]
        f_max    = row[2]
        tau0_min = row[3]
        tau0_max = row[4]
        fv0_min  = row[5] or 0
        fv0_max  = row[6] or 0
        E_min    = row[7]
        E_max    = row[8]
        G_min    = row[9]
        G_max    = row[10]
        w_min    = row[11]
        w_max    = row[12]
        # default values
        # if self.name is not None:
        self.f    = f    if f    is not None else (f_min + f_max)/2
        self.fv0  = fv0  if fv0  is not None else (fv0_min + fv0_max)/2
        self.tau0 = tau0 if tau0 is not None else (tau0_min + tau0_max)/2
        self.Emod = Emod if Emod is not None else (E_min+E_max)/2
        self.Gmod = Gmod if Gmod is not None else (G_min+G_max)/2
        self.rho  = rho  if rho  is not None else (w_min+w_max)/2*100
        if LC==1:
            self.f    = f    if f    is not None else f_min
            self.fv0  = fv0  if fv0  is not None else fv0_min
            self.tau0 = tau0 if tau0 is not None else tau0_min
        # design value
        self.FC = factorConfidence(LC=LC)
        if self.FC is not None:
            self.taur = self.tau0 / self.FC / self.gamma
        else:
            self.taur = self.tau0 / self.gamma
        self.fd = self.f/self.gamma
    

def factorConfidence(LC=None):
    '''
    Factor of Confidence (FC) according to knowledge level (LC=1,2,3) on existing structure by NTC2018
    '''
    fc_tab = {1: 1.35, 2: 1.20, 3: 1.00}
    if LC not in [1,2,3]:
        return None
    else:
        return fc_tab[LC]