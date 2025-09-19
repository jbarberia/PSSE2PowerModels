import sys
import psse34
import psspy

_i=psspy.getdefaultint()
_f=psspy.getdefaultreal()
_s=psspy.getdefaultchar()

def remover_hvdc():
    "se elimina el hvdc y se netea el mismatch con una demanda"
    psspy.dscn(87)
    psspy.dscn(86)
    psspy.gexmbus(85)
    psspy.bsys(1,0,[0.0,0.0],0,[],1,[85],0,[],0,[])
    psspy.bgen(1,0,2)
    psspy.fnsl([1,0,0,1,1,0,0,0])


def remover_villalbin():
    "vinculo radial del paraguay"
    psspy.dscn(43412)
    psspy.dscn(43212)
    psspy.dscn(43202)
    psspy.dscn(43402)
    psspy.dscn(40558)
    psspy.dscn(43800)
    psspy.bsys(1,0,[0.0,0.0],0,[],1,[43002],0,[],0,[])
    psspy.bgen(1,0,2)
    psspy.fnsl([1,0,0,1,1,0,0,0])


def ajustar_angulos_trafos():
    "hay transformadores con angulo de 30 grados que rompen el flujo"
    psspy.two_winding_chng_6(48034,48040,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48034,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48033,48039,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48033,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48032,48038,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48032,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48031,48037,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48031,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48030,48036,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48030,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48029,48035,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48029,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48022,48028,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48022,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48021,48027,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48021,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48020,48026,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48020,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48019,48025,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48019,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48018,48024,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48018,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(48017,48023,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,48017,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(46202,46402,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,46202,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(46201,46401,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,46201,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45207,45407,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,45207,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45206,45406,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,45206,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45205,45405,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,45205,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45205,45405,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,45205,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45204,45404,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,45204,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45204,45404,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,45204,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(45200,45400,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,45200,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(44213,44413,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,44213,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(44210,44410,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,44210,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(44209,44409,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,44209,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(44208,44408,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,44208,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43217,43417,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43217,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43215,43415,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43215,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43214,43514,r"""4""",[_i,_i,_i,_i,_i,_i,_i,_i,43214,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43214,43514,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,43214,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43214,43414,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,43214,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43214,43414,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43214,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43213,43413,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43213,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43212,43412,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,43212,_i,_i,_i,-1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43212,43412,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43212,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43205,43405,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43205,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(43202,43402,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,43402,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42317,42517,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,42317,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42226,42426,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,42226,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42226,42426,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42226,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42219,42419,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42219,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42218,42418,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,42218,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42218,42418,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42218,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42217,42417,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42217,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42216,42516,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42216,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42216,42416,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,42216,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42216,42416,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42216,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42214,42414,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,42214,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42214,42414,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42214,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42213,42513,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42213,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42212,42512,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42212,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42212,42412,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42212,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42209,42409,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,42209,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42209,42409,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42209,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42207,42507,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42207,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42201,42601,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42201,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(42201,42501,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,42201,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41345,41445,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41345,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41345,41445,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41345,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41331,41531,r"""4""",[_i,_i,_i,_i,_i,_i,_i,_i,41331,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41257,41457,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41257,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41257,41457,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41257,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41257,41457,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41257,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41255,41455,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41255,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41255,41455,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41255,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41255,41455,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41255,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41254,41454,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41254,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41254,41454,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41254,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41254,41454,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41254,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41249,41449,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41249,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41249,41449,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41249,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41248,41448,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41248,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41245,41545,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41245,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41244,41444,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41244,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41244,41444,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41244,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41243,41443,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41243,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41243,41443,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41243,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41242,41442,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41242,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41242,41442,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41242,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41241,41441,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41241,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41240,41440,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41240,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41240,41440,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41240,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41239,41439,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41239,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41239,41439,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41239,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41238,41438,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41238,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41237,41537,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41237,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41237,41437,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41237,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41235,41535,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41235,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41235,41435,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41235,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41234,41434,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41234,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41234,41434,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41234,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41233,41433,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41233,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41233,41433,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41233,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41232,41432,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41232,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41232,41432,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41232,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41232,41432,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41232,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41231,41431,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41231,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41231,41431,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41231,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41231,41431,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41231,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41230,41430,r"""3""",[_i,_i,_i,_i,_i,_i,_i,_i,41230,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41230,41430,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41230,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41230,41430,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41230,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41219,41419,r"""4""",[_i,_i,_i,_i,_i,_i,_i,_i,41219,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41219,41419,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41219,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41209,41409,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41209,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41207,41407,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,41207,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(41207,41407,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41207,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(40229,41251,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41251,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""DYN11""")
    psspy.two_winding_chng_6(92870,97872,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,92870,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""561TA02""",r"""YND1""")
    psspy.two_winding_chng_6(92870,97871,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,92870,_i,_i,_i,1,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""561TA01""",r"""YND1""")
    psspy.two_winding_chng_6(46400,46403,r"""2""",[_i,_i,_i,_i,_i,_i,_i,_i,46400,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41317,41416,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41416,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41315,45801,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,45801,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41313,41462,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41462,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41312,41460,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41460,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41311,41461,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41461,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41310,41459,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41459,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41309,41414,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41414,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41306,41403,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41403,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41305,41403,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41403,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41304,41405,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41405,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41303,41405,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41405,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41302,41416,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41416,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41301,41415,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41415,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    psspy.two_winding_chng_6(41300,41415,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,41415,_i,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"",r"""ZND1""")
    
    psspy.three_wnd_winding_data_5(92872,95872,98872,r"""1""",3,[_i,_i,_i,_i,_i,_i],[_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
    psspy.three_wnd_winding_data_5(92871,95871,98871,r"""1""",3,[_i,_i,_i,_i,_i,_i],[_f,_f,0.0,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])

    psspy.rsol([1,0,0,0,0,0,0,0,0,1],[0.0, 0.96114E-13])
    psspy.fnsl([1,0,0,1,1,0,0,0])


# def apagar_capacitores_inexistentes():
#     "capacitores mal modelados o que no van en escalada"
#     psspy.shunt_chng(3294,r"""1""",0,[_f,_f])
#     psspy.shunt_chng(3294,r"""3""",0,[_f,_f])
#     psspy.fnsl([1,0,0,1,1,0,0,0])


def corregir_tipo_de_barra():
    "barras que son tipo 1 pero hay generadores conectados por lineas ZI"
    psspy.bus_chng_4(8584,0,[2,_i,_i,_i],[_f,_f,_f,_f,_f,_f,_f],_s)
    psspy.bus_chng_4(8205,0,[2,_i,_i,_i],[_f,_f,_f,_f,_f,_f,_f],_s)
    psspy.fnsl([1,0,0,1,1,0,0,0])


# def apagar_maquinas_pequenas():
#     "S3GCDI01 - aunque no estoy seguro que moleste"
#     psspy.dscn(3631)
#     psspy.dscn(3591)
#     psspy.dscn(3590)
#     psspy.fnsl([1,0,0,1,1,0,0,0])


def ubicar_controles_locales_de_tension(it=5):
    psspy.machine_chng_2(675,r"""1""",[_i,_i,_i,_i,_i,2],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f, 0.96])
    psspy.machine_chng_2(676,r"""3""",[_i,_i,_i,_i,_i,2],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f, 0.96])
    psspy.machine_chng_2(98781,r"""G1""",[_i,_i,_i,_i,_i,2],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f, 0.96])

    ierr, (number_arr, ireg_arr,) = psspy.agenbusint(sid=-1, flag=1, string=["NUMBER", "IREG"])
    ierr, (pu_arr, vspu_arr,) = psspy.agenbusreal(sid=-1, flag=1, string=["PU", "VSPU"])

    changes = False
    for number, ireg, pu, vspu in zip(number_arr, ireg_arr, pu_arr, vspu_arr):
        if pu - vspu > 0.0:
            psspy.plant_data_4(number, 0, [0, 0], [pu + 0.00001, 100.0])
            changes = True
        elif pu - vspu < 0.0:
            psspy.plant_data_4(number, 0, [0, 0], [pu - 0.00001, 100.0])
            changes = True

    psspy.fnsl([1,0,0,1,1,0,0,0])
    
    if changes and it > 0:    
        ubicar_controles_locales_de_tension(it-1)
    


if __name__ == "__main__":
    ifile = sys.argv[1]
    ofile = sys.argv[2]    
    psspy.psseinit()
    psspy.case(ifile)

    # correcciones
    remover_hvdc()
    remover_villalbin()
    ajustar_angulos_trafos()    
    corregir_tipo_de_barra()    
    ubicar_controles_locales_de_tension()

    psspy.save(ofile)

