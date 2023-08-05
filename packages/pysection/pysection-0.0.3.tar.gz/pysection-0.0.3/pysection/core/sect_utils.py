# Common Cross Section Shapes and Rebar for Reinforced Concrete
from math import factorial,pi,sin,cos,tan,atan,atan2,sqrt
import numpy as np
from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiPolygon, MultiPoint, box
from shapely.geometry.polygon import orient as PolyOrient
from shapely.ops import linemerge, unary_union, polygonize
from shapely import affinity

def binomial(m:int, n:int):
    '''
    binomial function  = m! / (n! * (m - n)!)
    *note: == math.comb() [for python 3.8]
    '''
    try:
        binom = factorial(m) // factorial(n) // factorial(m-n)
    except ValueError:
        binom = 0
    return binom

# def offset(coordinates, distance):
#     '''
#     coordinates = list of points [(y1, z1), (y2, z2), ...] 
#     distance    = perpendicular from edges (postive towards outside)
#     '''
#     if coordinates is None:
#         return []
#     p0 = Polygon(coordinates)
#     p1 = p0.buffer(distance, join_style=2) 
#     return list(p1.exterior.coords)

class Polygons(MultiPolygon):
    '''
    construct MutliPolygon by list of polygons
    polygons = [[(x1, y1), ...], ...]
    '''
    def __init__(self, polygons):
        if isinstance(polygons, MultiPolygon):
            mp0 = polygons
        mp0 = MultiPolygon([Polygon(p) for p in polygons])
        mp1 = unary_union(mp0)
        mp2 = MultiPolygon([])
        if mp1.geom_type == "Polygon":
            mp2 = MultiPolygon([mp1])
        elif mp1.geom_type == "MultiPolygon":
            mp2 = mp1
        super().__init__([p for p in mp2])
        self.ccx = 0
        self.ccy = 0
        self.moment_xx = 0
        self.moment_yy = 0
        self.moment_xy = 0
        self.moment_11 = 0
        self.moment_22 = 0
        self.principal_angle = 0
        self.get_properties()
        
    def calc_moment(self, p=0, q=0, origin=None):
        '''
        calculate area moment (p, q) = S( S( x^p * y^q * dx * dy))
            = area when p=0, q=0
        '''
        # ref. Carsten Steger, 1996 - On the Calculation of Arbitrary Moments of Polygons
        # TODO 
        # if polygons including holes
        # ...
        if self.is_empty:
            return 0
        else:
            c = 1/(p+q+2)/(p+q+1)/binomial(p+q,p)
            a = 0.0
            origin = origin or (self.centroid.coords.xy[0][0], self.centroid.coords.xy[1][0])
            for pp in self:
                x0 = pp.exterior.coords.xy[0]
                y0 = pp.exterior.coords.xy[1]
                if not pp.exterior.is_ccw:
                    x0 = x0[::-1]
                    y0 = y0[::-1]
                # # move area with centroid to origin
                # pp = transform(poly, xoff=-origin[0], yoff=-origin[1])
                # # rotate are -phi (=rotate the axis +phi)
                # pp = transform(pp, angle=-phi, origin=(0,0))
                for i in range(len(x0)-1):
                    x1 = x0[i] - origin[0]
                    y1 = y0[i] - origin[1]
                    x2 = x0[i+1] - origin[0]
                    y2 = y0[i+1] - origin[1]   
                    d  = x1*y2 - x2*y1
                    v  = 0.0
                    for j in range(p+1):
                        for k in range(q+1):
                            v += binomial(j+k,k) * binomial(p+q-j-k,q-k) * x1**(p-j) * x2**j * y1**(q-k) * y2**k
                    a += d*v
            return c*a
        
    def get_properties(self):
        if not self.is_empty:
            self.ccx = self.centroid.coords.xy[0][0]
            self.ccy = self.centroid.coords.xy[1][0]
            # second area moments about centroid
            # sA  = self.moment(0,0) # check conter-clock-wise or not
            Ixx = self.calc_moment(0,2)
            Iyy = self.calc_moment(2,0)
            Ixy = self.calc_moment(1,1)
            # principal axes direction
            _avg = (Ixx + Iyy)/2
            _dif = (Ixx - Iyy)/2      # signed
            I11 = _avg + sqrt(_dif**2 + Ixy**2)
            I22 = _avg - sqrt(_dif**2 + Ixy**2)
            theta = atan2(-Ixy, _dif)/2
            self.moment_xx = Ixx
            self.moment_yy = Iyy
            self.moment_xy = Ixy
            self.moment_11 = I11 
            self.moment_22 = I22 
            self.principal_angle = theta/pi*180
    
    def get_properties_with_holes(self, holes=None):
        A    = self.area
        yc   = self.ccx
        zc   = self.ccy
        Iyy  = self.moment_xx
        Izz  = self.moment_yy
        Iyz  = self.moment_xy
        inner_points = []
        if holes is not None:
            inner_points = holes
            holes = Polygons(holes)
            A  = A - holes.area
            yc = (self.ccx*self.area - holes.ccx*holes.area)/A
            zc = (self.ccy*self.area - holes.ccy*holes.area)/A
            Iyy  = self.calc_moment(0,2, origin=(yc,zc)) - holes.calc_moment(0,2, origin=(yc,zc))
            Izz  = self.calc_moment(2,0, origin=(yc,zc)) - holes.calc_moment(2,0, origin=(yc,zc))
            Iyz  = self.calc_moment(1,1, origin=(yc,zc)) - holes.calc_moment(1,1, origin=(yc,zc))
        Wely = Iyy/max(abs(self.bounds[1]-zc),abs(self.bounds[3]-zc))
        Welz = Izz/max(abs(self.bounds[0]-yc),abs(self.bounds[2]-yc))
        Wply = 0
        Wplz = 0
        Avy  = 5/6*A
        Avz  = 5/6*A
        Avym = Izz/(Iyy+Izz) * A  # only for masonry shear calculation
        Avzm = Iyy/(Iyy+Izz) * A  # only for masonry shear calculation
        # principal axes direction
        _avg = (Iyy + Izz)/2
        _dif = (Iyy - Izz)/2      # signed
        I11 = _avg + sqrt(_dif**2 + Iyz**2)
        I22 = _avg - sqrt(_dif**2 + Iyz**2)
        theta = atan2(-Iyz, _dif)/2 /pi * 180
        return {
            "A":A, "Avy":Avy, "Avz":Avz, "yc":yc, "zc":zc, "Iyy":Iyy, "Izz":Izz, "Wely":Wely, "Welz":Welz, "Wply":Wply, "Wplz":Wplz, 
            "I11":I11, "I22":I22, "theta":theta, "Avym":Avym, "Avzm":Avzm, "bounds":self.bounds,
            "points":self.get_points(), "inner_points":inner_points
        }

    def rotate(self, angle=0, origin=None, use_radians=False):
        '''
        angle = angle of rotation in degrees (default) or radians by setting use_radians=True. 
            positive angles are counter-clockwise and negative are clockwise rotations.
        origin  = None (default) = the geometry’s centroid, or 
                = (x0, y0) = coordinate tuple 
        '''
        if abs(angle)<1e-3:
            return self
        origin = origin or 'centroid'
        pp = affinity.rotate(self, angle=angle, origin=origin, use_radians=use_radians)
        return Polygons(pp)

    def translate(self, xoff=0, yoff=0):
        '''
        shifted by offsets along x and y
        '''
        pp = affinity.translate(self, xoff=xoff, yoff=yoff)
        return Polygons(pp)

    def get_envelope(self, offset=0):
        '''
        return Polygons of envelope
        '''
        p0 = Polygon(list(self.minimum_rotated_rectangle.exterior.coords))
        if offset!=0:
            p0 = p0.buffer(offset, join_style=2) 
        return Polygons([p0])

    def get_points(self):
        '''
        return list of lists of points
        '''
        points = [list(p.exterior.coords) for p in self]
        return points


    def bandcut(self, ymin=None, ymax=None):
        '''
        get a band part wihtin (ymin ~ ymax) from whole polygons
        '''
        # construct a rectangular to intersect
        if ymin is None:
            ymin = self.bounds[1] 
        if ymax is None:
            ymax = self.bounds[3]
        if ymin>ymax:
            ymin, ymax = ymax, ymin
        bb = box(self.bounds[0], max(self.bounds[1],ymin), self.bounds[2], min(self.bounds[3],ymax))
        # get intersection
        pp = self.intersection(bb)
        if pp.is_empty:
            return Polygons([])
        else:
            if pp.type == 'MultiPolygon':
                return Polygons(pp)
            elif pp.type == 'Polygon':
                return Polygons([pp])
            else:
                return Polygons([])
    
    def linecut(self, origin=None, angle=0, r=9999):
        '''
        get a line part(s) wihtin polygons
        return: (t, c)
            t = total length
            c = list of segments
        '''
        # find width when cut by cutline [(x1,y1),(x2,y2)]
        origin = origin or (self.ccx, self.ccy)
        t = angle/180*pi
        cutline = [(origin[0]-r*cos(t), origin[1]-r*sin(t)), (origin[0]+r*cos(t), origin[1]+r*sin(t))]
        line = LineString(cutline)
        ls = line.intersection(self)
        t = 0
        c = []
        if not ls.is_empty:
            if ls.geom_type=="LineString":
                t = ls.length
                c += [ls]
            if ls.geom_type=="GeometryCollection":
                for l in ls:
                    if l.geom_type=="LineString":
                        t += l.length
                        c += [ls]
        return (t, c)

    def get_concrete_forces(self, eps:float, chi:float, z0=None, fcd=25.0, ecy=0.002, ecu=0.0035):
        '''
        calculate forces on area, as material of concrete-type, under deformation: 
            eps = strain at centroid, compression negative;
            chi = inclination about x-axis (for different angle need to rotate polygons)
        with material characteristics: [ref. stress-strain model EN1992-1-1: 3.1.7]
            fcd  = [MPa] yielding strength
            ecy  = 0.002  (default) = yielding strain, eps_c2 [EN]
            ecu  = 0.0035 (default) = ultimate strain, eps_cu2 [EN]
        return (Nc, Mc)
        '''
        # strain distribution on section (yz system) 
        #     [eps] = eps+chi*[z]   # z postive => tension side
        # stress distribution in 4 zones: 
        # --------------------------------------------------------  zone 3:     [eps]<ecu   - crashed
        #     [sig] = 0
        # --------------------------------------------------------  zone 2: ecu<[eps]<ecy  -  flat yielded
        #     [sig] = fcd
        #         Nc2 = fcd*INT(dy*dz)     = fcd*[A]
        #         Mc2 = fcd*INT([z]*dy*dz) = fcd*[Az]
        # --------------------------------------------------------  zone 1: ecy<[eps]<0     - parabolic
        #     [sig] = fcd*(1-(1-[eps]/ecy).^n);  # n=2
        #         Nc1 = INT([sig]*dy*dz) = fcd * INT(1-(1-[eps]/ecy)^2)*dy*dz) 
        #             = fcd/ecy^2 * ( 
        #                   - chi^2            *[Azz] 
        #                   + 2*chi*(ecy-eps)  *[Az] 
        #                   + (2*ecy*eps-eps^2)*[A]   )
        #         Mc1 = INT([sig]*[z]*dy*dz)
        #             = fcd/ecy^2 * ( 
        #                  - chi^2             *[Azzz] 
        #                  + 2*chi*(ecy-eps)   *[Azz] 
        #                  + (2*ecy*eps-eps^2) *[Az]  )
        # --------------------------------------------------------  zone 0:   0<[eps]       - cracked
        #     [sig] = 0
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        fcd = -abs(fcd)
        ecu = -abs(ecu)
        ecy = -abs(ecy)
        z0  = z0 or self.ccy
        # get strip parts in zones 1 and 2
        if chi ==0:
            if eps<=0 and eps>ecy:        # all zone 1 parabolic
                pp1 = self
                pp2 = Polygons([])
            elif eps<=ecy and eps>=ecu:   # all zone 2 flat
                pp1 = Polygons([])
                pp2 = self
            else:
                return (0, 0)
        else:
            # zones limits = ([eps] - eps) / chi
            v01 = z0+ (ecu -eps)/chi  # limit zone 0-1
            v12 = z0+ (ecy -eps)/chi  # limit zone 1-2
            v23 = z0+ (0   -eps)/chi  # limit zone 2-3
            pp1 = self.bandcut(v01, v12) # zone 1
            pp2 = self.bandcut(v12, v23) # zone 2
        # calculate area moments 
        A10 = pp1.calc_moment(0, 0, origin=(self.ccx, z0))
        A11 = pp1.calc_moment(0, 1, origin=(self.ccx, z0))
        A20 = pp2.calc_moment(0, 0, origin=(self.ccx, z0))
        A21 = pp2.calc_moment(0, 1, origin=(self.ccx, z0))
        A22 = pp2.calc_moment(0, 2, origin=(self.ccx, z0))
        A23 = pp2.calc_moment(0, 3, origin=(self.ccx, z0))
        # calculate forces
        Nc1 = fcd *A10
        Mc1 = fcd *A11
        Nc2 = fcd/ecy**2 * ( -chi**2 *A22 + 2*chi*(ecy-eps) *A21 + (2*ecy*eps-eps**2) *A20)
        Mc2 = fcd/ecy**2 * ( -chi**2 *A23 + 2*chi*(ecy-eps) *A22 + (2*ecy*eps-eps**2) *A21)
        # total forces
        Nc = Nc1 + Nc2
        Mc = Mc1 + Mc2

        # plt.figure()
        # for p in self:
        #     x = p.exterior.coords.xy[0]
        #     y = p.exterior.coords.xy[1]
        #     plt.fill(x, y, color='grey', alpha=0.5)        
        # if not pp1.is_empty:
        #     for p in pp1:
        #         x = p.exterior.coords.xy[0]
        #         y = p.exterior.coords.xy[1]
        #         plt.fill(x, y, color='blue', alpha=0.5)
        # if not pp2.is_empty:
        #     for p in pp2:
        #         x = p.exterior.coords.xy[0]
        #         y = p.exterior.coords.xy[1]
        #         plt.fill(x, y, color='red', alpha=0.5)
        # plt.axis("equal")
        # plt.gca().invert_yaxis()
        # plt.savefig("tmp-1.png", dpi=200)

        return (Nc, Mc)

    def get_steel_forces(self, eps:float, chi:float, z0=None, fyd=315, Es=210000.0, esu=0.0675):
        '''
        calculate forces on area, as material of steel-type, under deformation: 
            eps = strain at centroid, compression negative;
            chi = rotation about centroid;
        with material characteristics: [ref. stress-strain model EN1992-1-1]
            fyd     = [MPa] yielding strength
            Es      = [MPa] elastic modulus
            esu     = [-] ultimate strain
        return (Ns, Ms)
        '''
        # strain distribution: xy -> yz 
        #     [eps] = eps+chi*[z]   # z postive => tension side
        # stress distribution in 5 zones: 
        #   zone 0 ----------------------------      [eps]<-esu     - crashed
        #     [sig] = 0
        #   zone 1 ---------------------------- -esu<[eps]<-esy     - yield, flat
        #     [sig] = -fyd
        #         Ns2 = -fyd*INT(dy*dz)     = -fyd*[A]
        #         Ms2 = -fyd*INT([z]*dy*dz) = -fyd*[Az]
        #   zone 2 ---------------------------- -esy<[eps]<+esy     - elastic, linear
        #     [sig] = Es*[eps] = Es*(eps+chi*[z]) 
        #         Ns3 = INT([sig]*dy*dz)    = Es * ( chi*[Az]  + eps*[A] )
        #         Ms3 = INT([sig]*[z]*dy*dz)= Es * ( chi*[Azz] + eps*[Az])
        #   zone 3 ----------------------------  esy<[eps]<esu      - yield, flat
        #     [sig] = fyd
        #         Ns4 = fyd*INT(dy*dz)     = fyd*[A]
        #         Ms4 = fyd*INT([z]*dy*dz) = fyd*[Az]
        #   zone 4 ---------------------------- esu<[eps]           - fracture
        #     [sig] = 0
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # get polygons in zones 1 and 2
        z0 = z0 or self.ccy
        esy = fyd/Es
        if chi ==0:
            if eps>=-esu and eps<=-esy:      # all zone 1
                pp1 = self
                pp2 = Polygons([])
                pp3 = Polygons([])
            elif eps>-esy and eps<esy:       # all zone 2
                pp1 = Polygons([])
                pp2 = self
                pp3 = Polygons([])
            elif eps>=esy and eps<=esu:      # all zone 3
                pp1 = Polygons([])
                pp2 = Polygons([])
                pp3 = self
            else:
                return (0, 0)
        else:
            # zones limits [z] = ([eps] - eps) / chi
            v01 = z0+ (-esu -eps)/chi  # limit zone 0-1
            v12 = z0+ (-esy -eps)/chi  # limit zone 1-2
            v23 = z0+ (+esy -eps)/chi  # limit zone 2-3
            v34 = z0+ (+esu -eps)/chi  # limit zone 3-4
            pp1 = self.bandcut(v01, v12) # zone 1
            pp2 = self.bandcut(v12, v23) # zone 2
            pp3 = self.bandcut(v23, v34) # zone 3
        # calculate area moments 
        A10 = pp1.calc_moment(0, 0, origin=(self.ccx, z0))
        A11 = pp1.calc_moment(0, 1, origin=(self.ccx, z0))
        A20 = pp2.calc_moment(0, 0, origin=(self.ccx, z0))
        A21 = pp2.calc_moment(0, 1, origin=(self.ccx, z0))
        A22 = pp2.calc_moment(0, 2, origin=(self.ccx, z0))
        A30 = pp3.calc_moment(0, 0, origin=(self.ccx, z0))
        A31 = pp3.calc_moment(0, 1, origin=(self.ccx, z0))
        # calculate forces
        Ns1 = -fyd *A10
        Ms1 = -fyd *A11
        Ns2 =  Es * ( chi *A21 + eps *A20)
        Ms2 =  Es * ( chi *A22 + eps *A21)
        Ns3 =  fyd *A30
        Ms3 =  fyd *A31
        # total forces
        Ns = Ns1 + Ns2 + Ns3
        Ms = Ms1 + Ms2 + Ms3
        return (Ns, Ms) 


    def get_elastic_modulus(self, phi=0):
        '''
        calculate elastic modulus about axis in angle phi
        return (Wel+, Wel-)
        '''
        poly1 = self.rotate(angle=-phi)
        Ixx = poly1.moment_xx
        y1  = poly1.bounds[1]
        y2  = poly1.bounds[3]
        Wel1 = Ixx/(y1-poly1.ccx)
        Wel2 = Ixx/(y2-poly1.ccx)
        return (Wel2, Wel1) 

    def get_plastic_modulus(self, phi=0):
        '''
        calculate plastic modulus about axis in angle phi
        return (Wpl, y0)
        '''
        poly1 = self.rotate(angle=-phi)
        A1 = self.area /2    # area in tension
        # A2 = self.A - A1     # area in compression
        wb = poly1.bounds[2]-poly1.bounds[0]
        # loop to find z0
        y0 = poly1.ccy
        At = poly1.bandcut(ymin=y0)
        n = 0
        while abs(At.area-A1)>1e-5 and n<1e5:
            y0 += (At.area - A1)/wb
            At = self.bandcut(ymin=y0)
            n += 1
        Ac = self.bandcut(ymax=y0)
        Wpl1 = At.area * (At.ccy - y0)
        Wpl2 = Ac.area * (y0 - Ac.ccy)
        return (Wpl1+Wpl2, y0)


    def get_plastic_moment(self, fyd=315, Nx=0):
        # A1*fy - A2*fy = Nx
        #  M = A1*fy*z1 + A2*fy*z2
        dA = Nx*1000 / fyd
        A1 = (self.area + dA)/2    # area in tension
        # A2 = self.A - A1     # area in compression
        wb = self.bounds[2]-self.bounds[0]
        # loop to find z0
        z0 = 0
        At = self.bandcut(ymin=z0)
        n = 0
        while abs(At.area-A1)>1e-5 and n<1e5:
            z0 += (At.area - A1)/wb
            At = self.bandcut(ymin=z0)
            n += 1
        Ac = self.bandcut(ymax=z0)
        z1 = At.ccy - z0
        z2 = z0 - Ac.ccy
        S1 = At.area * z1
        S2 = Ac.area * z2
        Wpl = S1 + S2
        Mpl = Wpl * fyd / 1e6
        # find shear width
        t = 0
        line = LineString([(self.bounds[0], z0), (self.bounds[2], z0)])
        ls = line.intersection(self)
        if not ls.is_empty:
            if ls.geom_type=="LineString":
                t = ls.length
            if ls.geom_type=="GeometryCollection":
                for l in ls:
                    if l.geom_type=="LineString":
                        t += l.length
        return (Mpl, z0, S1, S2, t)

# ----------------------------------------
class Rebars:
    '''
    longitudinal reinforcement via list of rebar dict(y,z,d),...]
            y = position in section,
            z = position in section,
            d = diameter,
        .As_tot = total area
    '''
    def __init__(self, rebar={"d":[]}):
        self.y  = []
        self.z  = []
        self.d  = []
        self.As = []
        self.As_tot = 0
        self.bounds = [0,0,0,0]
        if len(rebar["d"])<1:
            self.is_empty = True
        else:
            self.is_empty = False
            self.y = rebar["y"]
            self.z = rebar["z"]
            self.d = rebar["d"]
            self.As = [d**2/4*pi for d in rebar["d"]]
            self.As_tot = np.array(self.As).sum()
            self.bounds = [min(self.y),min(self.z),max(self.y),max(self.z)]

    def rotate(self, angle=0, origin=(0,0)):
        '''
        angle to rotate coordinates (positive in counter-clockwise)  
        origin = [default] (0,0) 
        '''
        if abs(angle)<1e-3:
            return Rebars(self.__dict__)
        if self.is_empty:
            return Rebars()
        else:
            y = np.array(self.y) - origin[0]
            z = np.array(self.z) - origin[1]
            yy = origin[0] + y * np.cos(angle/180*pi) - z * np.sin(angle/180*pi)
            zz = origin[1] + y * np.sin(angle/180*pi) + z * np.cos(angle/180*pi)
        return Rebars(dict(self.__dict__, y=yy.tolist(), z=zz.tolist()))
   
    def get_forces(self, eps:float, chi:float, z0=0, fyd=420.0, ftd=540, Es=210000.0, esu=0.0675):
        '''
        calculate forces as material of steel-type, under deformation: 
            eps = strain at 'origin', compression negative;
            chi = rotation about 'phi';
        with material characteristics: [ref. stress-strain model EN1992-1-1]
            fyd     = [MPa] yielding strength
            Es      = [MPa] elastic modulus
            esu     = [-] ultimate strain
        return (Ns, Ms)
        '''
        if self.is_empty:
            return (0, 0)
        # strain distribution: xy -> yz 
        z = np.array(self.z) - z0
        # v  = -sin(phi/180*pi) * (pp[:,0] - origin[0]) + cos(phi/180*pi) * (pp[:,1] - origin[1])
        epss = eps + chi* z
        sigs = epss*Es
        eyd = fyd/Es
        for i in range(len(epss)):
            if np.abs(epss[i])> eyd:
                sigs[i] = fyd + (ftd-fyd)/(esu-eyd)*(np.abs(epss[i]) - eyd)
                sigs[i] = sigs[i]*np.sign(epss[i])
        sigs[np.abs(epss)>esu/0.9] = 0
        Ns = sigs * np.array(self.As)   # [N]
        Ms = Ns * z                     # [Nmm]
        N = np.sum(Ns)
        M = np.sum(Ms)
        return (N, M)

class Stirrups:
    '''
    stirrup / shear reinforcement via list [dict(y, z, d, n, s, beta, bw, dh, alpha, theta),...]
            y     = reference position in section,
            z     = reference position in section,
            d     = stirrup diameter,
            n     = number of legs,
            s     = spacing of stirrup (in longitudinal direction of member),
            beta  = direction of stirrup in section,
            bw    = reference width,
            dh    = effective height,
            alpha = inclination angle of stirrup, default=90,
            theta = angle of struct-model, default=45,
        .Vrds = steel shear resistance in direction .beta
        .Vrdc = concrete shear resistance in direction .beta
    '''
    def __init__(self, stirr={"d":[]}):
        self.y   = []
        self.z   = []
        self.d   = []
        self.As  = []
        self.n   = []
        self.s   = []
        self.beta  = []
        self.bw    = []
        self.dh    = []
        self.alpha = []
        self.theta = []
        self.sum_dir   = [] 
        self.sum_tie    = []
        self.sum_strut  = []
        if len(stirr["d"])<1:
            self.is_empty = True
        else:
            self.is_empty = False
            # defaults
            stirr = dict(dict(y=[], z=[], d=[], n=[], s=[], beta=[], bw=[], dh=[], alpha=[], theta=[]), **stirr)
            ns = max(len(stirr["y"]),len(stirr["z"]),len(stirr["d"]))
            self.y      = stirr["y"    ] or [0]*ns
            self.z      = stirr["z"    ] or [0]*ns
            self.d      = stirr["d"    ] or [0]*ns
            self.n      = stirr["n"    ] or [0]*ns
            self.s      = stirr["s"    ] or [100]*ns
            self.beta   = stirr["beta" ] or [0]*ns
            self.bw     = stirr["bw"   ] or [1000]*ns
            self.dh     = stirr["dh"   ] or [1000]*ns
            self.alpha  = stirr["alpha"] or [90]*ns
            self.theta  = stirr["theta"] or [45]*ns
            self.As     = [self.d[i]**2 /4 *pi * self.n[i] / self.s[i]  for i in range(ns)]
            self.get_organized()

    def get_organized(self, beta0=0): 
        # count only with beta=0:y and beta=90:z
        self.sum_dir   = ['-']*len(self.beta) 
        self.sum_tie   = [0]*len(self.beta)
        self.sum_strut = [0]*len(self.beta)
        self.sum_z     = [0]*len(self.beta)
        for i,b in enumerate(self.beta):
            # z  = lever-arm of truss model (see EN1992-1-1, Figure 6.5) =0.9d (default None)
            self.sum_z[i]     = 0.9 * self.dh[i]  # lever arm
            cot_theta = 1/tan(self.theta[i]/180*pi)
            cot_alpha = 1/tan(self.alpha[i]/180*pi)
            sin_alpha = sin(self.alpha[i]/180*pi)
            self.sum_tie[i]   = self.As[i]*self.sum_z[i]*( cot_theta + cot_alpha ) * sin_alpha              # [mm2]
            self.sum_strut[i] = self.bw[i]*self.sum_z[i]*( cot_theta + cot_alpha ) / ( 1 + cot_theta**2)    # [mm2]
            if abs(cos((b-beta0)/180*pi))<1e-3:
                self.sum_dir[i] = 'Z'
            if abs(sin((b-beta0)/180*pi))<1e-3:
                self.sum_dir[i] = 'Y'

    def deff(self):
        bhz = 0
        bhy = 0
        bwz = 0
        bwy = 0
        for i,r in enumerate(self.sum_dir):
            if r in ['Z']:
                bhz += self.dh[i]*self.bw[i] 
                bwz += self.bw[i]
            if r in ['Y']:
                bhy += self.dh[i]*self.bw[i]
                bwy += self.bw[i]
        dhz = bhz/bwz if bwz!=0 else 0
        dhy = bhy/bwy if bwy!=0 else 0
        return (dhy, bwy, dhz, bwz)

    def Vrd_tie(self, fyd=450):
        # Vrd,s = Asw*z*fyd*(cot(theta)+cot(alfa))*sin(alfa) = vs*fyd
        Vz = 0
        Vy = 0
        for i,r in enumerate(self.sum_dir):
            if r in ['Z']:
                Vz += self.sum_tie[i]*fyd 
            if r in ['Y']:
                Vy += self.sum_tie[i]*fyd 
        return (Vy, Vz)

    def Vrd_strut(self, fcvd=25, v1=0.5, acw=1):
        # Vrd,c = acw*bw*z*v1*fcvd*(cot(theta)+cot(alfa))/(1+cot(theta)^2) = vc*acw*v1*fcvd
        Vz = 0
        Vy = 0
        for i,r in enumerate(self.sum_dir):
            if r in ['Z']:
                Vz += self.sum_strut[i]*acw*v1*fcvd  # [N]
            if r in ['Y']:
                Vy += self.sum_strut[i]*acw*v1*fcvd  # [N]
        return (Vy, Vz)


#########################################################################################
# ----------------------------------------
# shapes
# ----------------------------------------

def Rectangle(d=500, b=300, r=0, n_r=4, xc=0, yc=0):
    '''
    Constructs a rectangular section with: 
        geometric center (xc, yc)
        depth d and width b. 
        if r>0, using n_r points to construct the chamfers.
    '''
    points = []
    if r>0:
        points = []
        for i in range(n_r):
            theta = np.pi/2 * (0 + i * 1.0 / max(1, n_r - 1))
            x = +b/2 - r + r * np.cos(theta)
            y = +d/2 - r + r * np.sin(theta)
            points.append((x, y))
        for i in range(n_r):
            theta = np.pi/2 * (1 + i * 1.0 / max(1, n_r - 1))
            x = -b/2 + r + r * np.cos(theta)
            y = +d/2 - r + r * np.sin(theta)
            points.append((x, y))
        for i in range(n_r):
            theta = np.pi/2 * (2 + i * 1.0 / max(1, n_r - 1))
            x = -b/2 + r + r * np.cos(theta)
            y = -d/2 + r + r * np.sin(theta)
            points.append((x, y))
        for i in range(n_r):
            theta = np.pi/2 * (3 + i * 1.0 / max(1, n_r - 1))
            x = +b/2 - r + r * np.cos(theta)
            y = -d/2 + r + r * np.sin(theta)
            points.append((x, y))
    else: 
        points = [
            ( b/2, d/2),
            (-b/2, d/2),
            (-b/2,-d/2),
            ( b/2,-d/2),
        ]
    return points

def Round(d=500, n=32, xc=0, yc=0):
    '''
    Constructs a solid cicular bar with: 
        center (xc, yc)
        diameter d, and using 
        n points to construct the circle.
    '''
    p0 = Point(xc,yc).buffer(d/2, resolution=int(n/4))
    return list(p0.exterior.coords)

def Angle(d, b, t, r_root=0, r_toe=0, t1=None, n_r=4, xc=0, yc=0):
    '''
    Constructs an angle section with: 
        outer corner at (xc, yc), width towards x+, depth towards y+
        depth d, width b, thickness t (t1), root radius r_root, toe radius r_toe, and using 
        n_r points to construct the root radius.
    '''
    points = []
    points.append((0, 0))
    points.append((b, 0))
    t1 = t1 or t
    # bottom toe radius
    if r_toe>0:
        for i in range(n_r):
            theta = i * 1.0 / max(1, n_r - 1) * np.pi * 0.5
            x = b - r_toe + r_toe * np.cos(theta)
            y = t - r_toe + r_toe * np.sin(theta)
            points.append((x, y))
    else:
        points.append((b, t))
    # root radius
    if r_root>0:
        for i in range(n_r):
            theta = 3.0 / 2 * np.pi * (1 - i * 1.0 / max(1, n_r - 1) * 1.0 / 3)
            x = t1 + r_root + r_root * np.cos(theta)
            y = t + r_root + r_root * np.sin(theta)
            points.append((x, y))
    else:
        points.append((t1, t))
    # top toe radius
    if r_toe>0:
        for i in range(n_r):
            theta = i * 1.0 / max(1, n_r - 1) * np.pi * 0.5
            x = t1 - r_toe + r_toe * np.cos(theta)
            y = d - r_toe + r_toe * np.sin(theta)
            points.append((x, y))
    else:
        points.append((t1, d))
    points.append((0, d))
    return [(xc+p[0], yc+p[0]) for p in points]


def Tee(d, b, tf, tw, r=0, n_r=4, xc=0, yc=0):
    '''
    Constructs a Tee section (flange on bottom side) with: 
        flange outer center at (xc, yc), depth towards y+
        depth d, width b, flange thickness tf, web thickness tw, root radius r, and using 
        n_r points to construct the root radius.
    '''
    points = []
    points.append(( b * 0.5, 0))
    points.append(( b * 0.5, tf))
    # bottom right radius
    if r>0:
        for i in range(n_r):
            theta = 3.0 / 2 * np.pi * (1 - i * 1.0 / max(1, n_r - 1) * 1.0 / 3)
            x = tw * 0.5 + r + r * np.cos(theta)
            y = tf       + r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((tw/2, tf))
    points.append((+tw/2, d))
    points.append((-tw/2, d))
    # bottom left radius
    if r>0:
        for i in range(n_r):
            theta = -np.pi * i * 1.0 / max(1, n_r - 1) * 0.5
            x = - tw * 0.5 - r + r * np.cos(theta)
            y =   tf       + r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((-tw/2, tf))
    points.append((-b/2, tf))
    points.append((-b/2, 0))
    return [(xc+p[0], yc+p[0]) for p in points]


def DoubleT(d, b, tf, tw, r=0, n_r=4):
    '''
    Constructs a double-T (i.e. H- or I-) section with: 
        depth d, width b, flange thickness tf, web thickness tw, root radius r, and using 
        n_r points to construct the root radius.
    '''
    points = []
    points.append((-b/2, -d/2))
    points.append((+b/2, -d/2))
    points.append((+b/2, -d/2+tf))
    # bottom right radius
    if r>0:
        for i in range(n_r):
            theta = 3.0 / 2 * np.pi * (1 - i * 1.0 / max(1, n_r - 1) * 1.0 / 3)
            x = tw * 0.5 + r + r * np.cos(theta)
            y = -d/2+ tf + r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((tw/2, -d/2+tf))
    # top right radius
    if r>0:
        for i in range(n_r):
            theta = np.pi * (1 - i * 1.0 / max(1, n_r - 1) * 0.5)
            x = tw * 0.5 + r + r * np.cos(theta)
            y = +d/2- tf - r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((tw/2, +d/2-tf))
    points.append((+b/2, +d/2 - tf))
    points.append((+b/2, +d/2))
    points.append((-b/2, +d/2))
    points.append((-b/2, +d/2 - tf))
    # top left radius
    if r>0:
        for i in range(n_r):
            theta = np.pi * 0.5 * (1 - i * 1.0 / max(1, n_r - 1))
            x = -tw * 0.5 - r + r * np.cos(theta)
            y = +d/2 - tf - r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((-tw/2, +d/2-tf))
    # bottom left radius
    if r>0:
        for i in range(n_r):
            theta = -np.pi * i * 1.0 / max(1, n_r - 1) * 0.5
            x = -tw * 0.5 - r + r * np.cos(theta)
            y = -d/2 + tf + r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((-tw/2, -d/2+tf))
    points.append((-b/2, -d/2+tf))
    return points


def PFC(d, b, tf, tw, r=0, n_r=4):
    '''
    Constructs a PFC (Parallel Flange Channel, like 'UPE') section with: 
        depth d, width b, flange thickness tf, web thickness tw, root radius r, and using 
        n_r points to construct the root radius.
    '''
    points = []
    points.append((0, -d/2))
    points.append((b, -d/2))
    points.append((b, -d/2+tf))
    if r>0:
        # bottom right radius
        for i in range(n_r):
            theta = 3.0 / 2 * np.pi * (1 - i * 1.0 / max(1, n_r - 1) * 1.0 / 3)
            x = tw + r + r * np.cos(theta)
            y = -d/2+tf + r + r * np.sin(theta)
            points.append((x, y))
        # top right radius
        for i in range(n_r):
            theta = np.pi * (1 - i * 1.0 / max(1, n_r - 1) * 0.5)
            x = tw + r + r * np.cos(theta)
            y = +d/2 - tf - r + r * np.sin(theta)
            points.append((x, y))
    else:
        points.append((tw, -d/2+tf))
        points.append((tw, +d/2-tf))
    points.append((b, d/2 - tf))
    points.append((b, d/2))
    points.append((0, d/2))
    return points


def IPN(d, b, tf, tw, r_root, r_toe, n_r=4):
    '''
    Constructs a IPN (taper flange I-section) with: 
        depth d, width b, flange thickness tf, web thickness tw, root radius r_root, toe radius r_toe, and using 
        n_r points to construct the root radius.
    '''
    points = []
    u  = b/4
    fs = 0.14
    a = np.arctan(fs)
    points.append((0, 0))
    points.append((b, 0))
    # bottom right toe radius
    tcx = b - r_toe
    tcy = tf - u*np.tan(a) - r_toe*np.tan(np.pi/4-a/2)
    for i in range(n_r):
        theta = i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = tcx + r_toe * np.cos(theta)
        y = tcy + r_toe * np.sin(theta)
        points.append((x, y))
    # bottom right root radius
    bcx = b/2 + tw/2 + r_root
    bcy = tf + (b - u - bcx + r_root*np.sin(a))*np.tan(a) + r_root*np.cos(a)
    for i in range(n_r):
        theta = 3/2*np.pi - a -  i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = bcx + r_root * np.cos(theta)
        y = bcy + r_root * np.sin(theta)
        points.append((x, y))
    # top right root radius
    bcy = d - bcy
    for i in range(n_r):
        theta = np.pi -  i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = bcx + r_root * np.cos(theta)
        y = bcy + r_root * np.sin(theta)
        points.append((x, y))
    # top right toe radius
    tcy = d - tcy
    for i in range(n_r):
        theta = 3/2*np.pi + a + i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = tcx + r_toe * np.cos(theta)
        y = tcy + r_toe * np.sin(theta)
        points.append((x, y))
    points.append((b, d))
    points.append((0, d))
    # top left toe radius
    tcx = b - tcx
    for i in range(n_r):
        theta = np.pi + i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = tcx + r_toe * np.cos(theta)
        y = tcy + r_toe * np.sin(theta)
        points.append((x, y))
    # top left root radius
    bcx = b - bcx
    for i in range(n_r):
        theta = np.pi/2 - a -  i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = bcx + r_root * np.cos(theta)
        y = bcy + r_root * np.sin(theta)
        points.append((x, y))
    # bottom left root radius
    bcy = d - bcy
    for i in range(n_r):
        theta = 0 -  i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = bcx + r_root * np.cos(theta)
        y = bcy + r_root * np.sin(theta)
        points.append((x, y))
    # bottom left toe radius
    tcy = d - tcy
    for i in range(n_r):
        theta = np.pi/2 + a + i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = tcx + r_toe * np.cos(theta)
        y = tcy + r_toe * np.sin(theta)
        points.append((x, y))
    p0 = Polygon(points)
    p1 = affinity.translate(p0, xoff=-b/2, yoff=-d/2)
    return list(p1.exterior.coords)


def UPN(d, b, tf, tw, r_root, r_toe, n_r=4):
    '''
    Constructs a UPN (taper flange channel) section with: 
        depth d, width b, flange thickness tf, web thickness tw, root radius r_root, toe radius r_toe, and using 
        n_r points to construct the root radius.
    '''
    points = []
    if d<=300:
        u  = b/2
        fs = 0.08
    else:
        u  = (b-tw)/2
        fs = 0.05
    a = np.arctan(fs)
    points.append((0, 0))
    points.append((b, 0))
    # bottom toe radius
    tcx = b - r_toe
    tcy = tf - u*np.tan(a) - r_toe*np.tan(np.pi/4-a/2)
    for i in range(n_r):
        theta = i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = tcx + r_toe * np.cos(theta)
        y = tcy + r_toe * np.sin(theta)
        points.append((x, y))
    # bottom root radius
    bcx = tw + r_root
    bcy = tf + (b - u - bcx + r_root*np.sin(a))*np.tan(a) + r_root*np.cos(a)
    for i in range(n_r):
        theta = 3/2*np.pi - a -  i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = bcx + r_root * np.cos(theta)
        y = bcy + r_root * np.sin(theta)
        points.append((x, y))
    # top root radius
    bcy = d - bcy
    for i in range(n_r):
        theta = np.pi -  i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = bcx + r_root * np.cos(theta)
        y = bcy + r_root * np.sin(theta)
        points.append((x, y))
    # top toe radius
    tcy = d - tcy
    for i in range(n_r):
        theta = 3/2*np.pi + a + i * 1.0 / max(1, n_r - 1) * (np.pi/2-a)
        x = tcx + r_toe * np.cos(theta)
        y = tcy + r_toe * np.sin(theta)
        points.append((x, y))
    points.append((b, d))
    points.append((0, d))
    p0 = Polygon(points)
    p1 = affinity.translate(p0, xoff=0, yoff=-d/2)
    return list(p1.exterior.coords)


def CHS(d, t, n=32):
    '''
    Constructs a circular hollow section with: 
        diameter d, 
        thickness t, and using
        n points to construct the inner and outer circles.
    '''
    p_out = Round(d=d, n=n)
    p_in  = Round(d=d-2*t, n=n)
    p_in  = list(reversed(p_in))   # inner circle (hole) in reversed sequence
    return (p_out, p_in)


def RHS(d, b, t, r_out, r_in=None, n_r=4):
    '''
    Constructs a Rectangular/Square Hollow Section with:
        depth d, width b, thickness t, outer radius r_out, and using 
        n_r points to construct the inner and outer radii.
    '''
    if r_in is None:
        r_in = r_out - t
    p_out = Rectangle(d=d, b=b, r=r_out, n_r=n_r)
    p_in  = Rectangle(d=d-t*2, b=b-t*2, r=r_in, n_r=n_r)
    p_in  = list(reversed(p_in))   # inner circle (hole) in reversed sequence
    return (p_out, p_in)


def simple_shape(shape='rect', d=500, b=300, t=0, r=0, b1=0, t1=0, r1=0):
    '''
    common shape definition

    torsion constant reference: 
        - W.C.Young and R.G.Budynas, 2002, "Roark’s Formulas for Stress and Strain"
    '''
    if shape is None:
        return None
    if shape.lower() in ['rect','rectangle']:
        polygons = Polygons([Rectangle(d=d, b=b)])
        Avy = polygons.area * 5/6
        Avz = polygons.area * 5/6
        a1 = min(d,b)
        a2 = max(d,b)
        It  = a1 * a2**3 * (16/3 - 3.36*a2/a1 * ( 1 - a2**4 / a1**4 / 12))
            # ref. <Roark's formulas for stress and strain>
    elif shape.lower() in ['circ','circle','round']:
        polygons = Polygons([Round(d=d)])
        Avy = polygons.area * 9/10
        Avz = polygons.area * 9/10
        It  = pi * d**4 / 32
    elif shape.lower() in ['angle','l']:
        polygons = Polygons([Angle(d=d, b=b, t=t, t1=t1)])
        Avy = polygons.area * 5/6  # TODO verification?
        Avz = polygons.area * 5/6  # TODO verification?
        if t>=t1:
            K1 = b * t**3 * (1/3 - 0.21 * t/b * (1 - t**4 /b**4 /12)) 
            K2 = (d-t) * t1**3 * (1/3 - 0.105 * t1/(d-t) * (1 - t1**4 /(d-t)**4 /192)) 
            K3 = t1/t * 0.07 * (2*t+2*t1-sqrt(2*t*t1))**4
        else:
            K1 = d * t1**3 * (1/3 - 0.21 * t1/d * (1 - t1**4 /d**4 /12)) 
            K2 = (b-t1) * t**3 * (1/3 - 0.105 * t/(b-t1) * (1 - t**4 /(b-t1)**4 /192)) 
            K3 = t/t1 * 0.07 * (2*t+2*t1-sqrt(2*t*t1))**4
        It  = K1+K2+K3
    elif shape.lower() in ['tee','t']:
        polygons = Polygons([Tee(d=d, b=b, tf=t, tw=t1)])
        Avy = polygons.area * 5/6  # TODO verification?
        Avz = polygons.area * 5/6  # TODO verification?
        K1 = b * t**3 * (1/3 - 0.21 * t/b * (1 - t**4 /b**4 /12)) 
        K2 = (d-t) * t1**3 * (1/3 - 0.105 * t1/(d-t) * (1 - t1**4 /(d-t)**4 /192)) 
        K3 = min(t,t1)/max(t,t1) * 0.15 * (t + t1**2 / t / 4)**4
        It  = K1+K2+K3
    else:
        print("shape not valid!")
        return None
    A   = polygons.area
    yc  = polygons.ccx
    zc  = polygons.ccy
    Iyy = polygons.moment_xx
    Izz = polygons.moment_yy
    Iyz = polygons.moment_xy
    I11 = polygons.moment_11
    I22 = polygons.moment_22
    theta = polygons.principal_angle
    Avym  = Izz/(Iyy+Izz) * A
    Avzm  = Iyy/(Iyy+Izz) * A
    Wely = Iyy/max(abs(polygons.bounds[1]-zc),abs(polygons.bounds[3]-zc))
    Welz = Izz/max(abs(polygons.bounds[0]-yc),abs(polygons.bounds[2]-yc))
    points = [list(p.exterior.coords) for p in polygons]
    inner_points = []
    return {
        "A":A, "Avy":Avy, "Avz":Avz, "yc":yc, "zc":zc, "Iyy":Iyy, "Izz":Izz, "Iyz":Iyz, "Wely":Wely, "Welz":Welz, 
        "It":It, "I11":I11, "I22":I22, "theta":theta, "Avym":Avym, "Avzm":Avzm,
        "points":points, "inner_points":inner_points, "bounds":polygons.bounds, 
    }




# ----------------------------------------
# rebars
# ----------------------------------------

def rebarLong(distribution='Single', d=16, position=None, n=None, line=None, circle=None, phi1=0, phi2=360, concr=None, cc=None, smax=None):
    '''
    longitudinal Rebar, d = diameter

    distribution = 'Single': Rebar single at 
        position = (y0,z0)

    distribution = 'Line': Rebar distributed on
        line = [(y1,z1), (y2,z2)]
        n = total number (n>1)
    
    distribution = 'Circle':  Rebar distributed on
        circle = (y0, z0, r) 
        phi1 = 0    [°] starting angle
        phi2 = 360  [°] end angle
        n = total number (n>1)

    distribution = 'Perimeter':  Rebar distributed on
        concr = instance of Polygons
        cc    = 40    clear cover (inner polygon)
        smax  = 100   maximum spacing allowed for auto-placing.
    '''
    if distribution.lower() in ['single','sing']:
        position = position or (0, 0)
        y0 = position[0]
        z0 = position[1]
        rebar = [(y0, z0, d)]
    elif distribution.lower() in ['linear','line']:
        line = line or [(-100, 0), (100, 0)]
        n = n or 5
        rebar = []
        y1 = line[0][0]
        z1 = line[0][1]
        y2 = line[1][0]
        z2 = line[1][1]
        if n>1:
            for i in range(n):
                rebar.append((y1+(y2-y1)/(n-1)*i, z1+(z2-z1)/(n-1)*i, d))
    elif distribution.lower() in ['circular','circle','circ']:
        circle= circle or (0, 0, 100)
        n = n or 4
        rebar = []
        y0 = circle[0]
        z0 = circle[1]
        r  = circle[2]
        if n>1:
            dp = phi2 - phi1
            if dp ==360:
                dp = dp - dp/n
            dp = dp/180*np.pi
            for i in range(n):
                rebar.append((y0+r*np.cos(dp/(n-1)*i), z0+r*np.sin(dp/(n-1)*i), d))
    elif distribution.lower() in ['perimetric','perimeter','peri']:
        concr = concr or Polygons([Rectangle(b=300,d=500)])
        cc   = cc or 40
        smax = smax or 100
        rebar = []
        pp = concr.get_envelope(offset=-cc-d/2)
        xy = np.array(pp[0].exterior.coords)
        for i in range(len(xy)-1):
            v1 = xy[i,:]
            v2 = xy[i+1,:]
            ds = np.linalg.norm(v2-v1)
            ns = int(np.ceil(ds/smax))+1   # >1
            rb = rebarLong('Line', d=d, n=ns, line=[v1, v2])
            rebar += [(rb["y"][i],rb["z"][i],rb["d"][i]) for i in range(len(rb["d"])-1)]
    else:
        rebar = []
    return dict(y=[r[0] for r in rebar],z=[r[1] for r in rebar],d=[r[2] for r in rebar]) 


def rebarShear(d=8, n=[2,2], s=150, bw=None, dh=None, concr=None, cc=40, beta=[0,90], y0=None, z0=None, beta0=0, alpha=90, theta=45):
    '''
    Shear reinforcement for shear in direction beta(°, positive deform right face downward, corresponding a positive moment)
        d  = diameter
        n  = number of legs (n>=1)
        s  = spacing
        bw = width of concrete in considered
        dh = depth for shear resistance (effective height)
        concr = section shape, instance of Polygons
        beta = shear direction  ====>  phi = bending axis direction = beta-90°
            beta =  90, phi =   0 : positive bending My (tension in positive z)
            beta = 270, phi = 180 : negative bending My (tension in negative z)
            beta =   0, phi = 270 : positive bending Mz (tension in positive y)
            beta = 180, phi =  90 : negative bending Mz (tension in negative y)
        beta0  = 'concr' x-axis 
        y0     = cut through point (default at centroid of polygon) 
        z0     = cut through point (default at centroid of polygon) 
        cc     = clear cover (for defining lever-arm)
        alpha  = shear reinforcement inclination [°] (see EN1992-1-1, Figure 6.5)
        theta  = compression strut inclination [°] (see EN1992-1-1, Figure 6.5)
        torque = True/False : if to reisit torque effect
    '''
    ns = len(beta)
    concr = concr or Polygons([Rectangle(d=300,b=300)])
    pp = concr.get_envelope(offset=-cc-max(d)/2)
    if not isinstance(y0,list):
        y0 = [concr.centroid.coords.xy[0][0] ]*ns
    if not isinstance(z0,list):
        z0 = [concr.centroid.coords.xy[1][0] ]*ns
    if not isinstance(d,list):
        d = [d]*ns
    if not isinstance(n,list):
        n = [n]*ns
    if not isinstance(s,list):
        s = [s]*ns     
    if not isinstance(bw,list):
        bw = [1000]*ns
    if not isinstance(dh,list):
        dh = [0]*ns
    if not isinstance(alpha,list):
        alpha = [alpha]*ns
    if not isinstance(theta,list):
        theta = [theta]*ns
    for i in range(ns):
        phi = beta[i] + beta0 - 90
        tb, _ = pp.linecut(origin=(y0[i],z0[i]), angle=phi)
        td, _ = pp.linecut(origin=(y0[i],z0[i]), angle=phi+90)
        if tb>0:
            bw[i] = tb + 2*cc + d[i]
        if td>0 and dh[i]<=0:
            dh[i] = 0.9 * td
    return dict(y=y0, z=z0, d=d, n=n, s=s, beta=beta, bw=bw, dh=dh, alpha=alpha, theta=theta)


def simple_reinf(rebar=None, stirr=None, concr=None, cc=40, dc=None, beta0=0):
    '''
    generate reinforcements from simple inputs

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
    
    beta0 = theta - theta_origin
    * rebar * defined according to actual shape with theta (rotated back -beta0 and re-rotated beta0)
    * stirr * defined according to original shape with theta_origin (rotated back -beta0)
    '''
    concr0 = concr or Polygons([Rectangle(b=300,d=500)])
    concr = concr0.rotate(-beta0)
    if rebar is not None:
        rebar1 = rebar
        if "type" in rebar:
            rebar = dict(dict(type='peri',d=20,cc=cc,smax=100,r=150,n=4), **rebar)
            if rebar["type"].lower() in ["peri","perimetric"]:
                cc = rebar["cc"]
                rebar1 = rebarLong('peri', d=rebar["d"], cc=rebar["cc"], smax=rebar["smax"], concr=concr)
            elif rebar["type"].lower() in ["circ","circular"]:
                if dc is not None:
                    cc = dc/2 - rebar["r"] - rebar["d"]/2
                rebar1 = rebarLong('circ', d=rebar["d"], circle=(concr.ccx, concr.ccy, rebar["r"]), n=rebar["n"])
            elif rebar["type"].lower() in ["symx"]:
                c = rebar["cc"]+rebar["d"]/2
                cc = rebar["cc"]
                line1 = [(concr.bounds[0]+c, concr.bounds[1]+c), (concr.bounds[2]-c, concr.bounds[1]+c)]
                line2 = [(concr.bounds[0]+c, concr.bounds[3]-c), (concr.bounds[2]-c, concr.bounds[3]-c)]
                r1 = rebarLong('line', d=rebar["d"], line=line1, n=rebar["n"])
                r2 = rebarLong('line', d=rebar["d"], line=line2, n=rebar["n"])
                rebar1 = {"y":r1["y"]+r2["y"], "z":r1["z"]+r2["z"], "d":r1["d"]+r2["d"]}
            elif rebar["type"].lower() in ["symy"]:
                c = rebar["cc"]+rebar["d"]/2
                cc = rebar["cc"]
                line1 = [(concr.bounds[0]+c, concr.bounds[1]+c),(concr.bounds[0]+c, concr.bounds[3]-c)]
                line2 = [(concr.bounds[2]-c, concr.bounds[1]+c),(concr.bounds[2]-c, concr.bounds[3]-c)]
                r1 = rebarLong('line', d=rebar["d"], line=line1, n=rebar["n"])
                r2 = rebarLong('line', d=rebar["d"], line=line2, n=rebar["n"])
                rebar1 = {"y":r1["y"]+r2["y"], "z":r1["z"]+r2["z"], "d":r1["d"]+r2["d"]}
        # rebar1.update({"As": [d**2/4*pi for d in rebar1["d"]]}) # self.rebar.As_tot
        rebar1 = Rebars(rebar1)
        dy = concr.bounds[2] - rebar1.bounds[0]  # effective depth in y for shear resistance
        dz = concr.bounds[3] - rebar1.bounds[1]  # effective depth in z for shear resistance
        rebar1 = rebar1.rotate(beta0)
        rebar1 = rebar1.__dict__
    else:
        # rebar = [sg.rebarLong('peri', d=16, cc=cc, smax=10000, concr=polygons)]
        rebar1 = {"d":[],"As":[]}
        dy = 0.9* (concr.bounds[2] - concr.bounds[0])
        dz = 0.9* (concr.bounds[3] - concr.bounds[1])

    # shear stirrups
    if stirr is not None:
        if "nx" in stirr:
            stirr = dict(dict(d=8,nx=0,ny=0,s=150), **stirr)
            stirr1 = rebarShear(d=[stirr["d"]]*2, n=[stirr["nx"],stirr["ny"]], s=[stirr["s"]]*2, beta=[0,90], dh=[dy, dz],
                beta0=0, concr=concr, cc=cc)
        stirr1 = Stirrups(stirr1).__dict__
    else:
        stirr1 = {"d":[]}
    
    return (rebar1, stirr1, cc)
    
