#!python
#
"""
This file is generated by "aflow --protos > prototype.all" and delete some lines, only the anrl prototype is kept
Ref: [1] M. J. Mehl, D. Hicks, C. Toher, O. Levy, R. M. Hanson, G. L. W. Hart, and S. Curtarolo, 
         The AFLOW Library of Crystallographic Prototypes: Part 1, Comp. Mat. Sci. 136, S1-S828 (2017). 
         (doi=10.1016/j.commatsci.2017.01.017)
     [2] D. Hicks, M. J. Mehl, E. Gossett, C. Toher, O. Levy, R. M. Hanson, G. L. W. Hart, and S. Curtarolo, 
         The AFLOW Library of Crystallographic Prototypes: Part 2, Comp. Mat. Sci. 161, S1-S1011 (2019). 
         (doi=10.1016/j.commatsci.2018.10.043)
"""
import os
import re
import time
import json
from pymatgen import Structure
from urllib.request import urlopen

def gen_proto_dict(struct_dict, proto_info):
    """
    Generate the dict for a single prototype.
        The formate referanced the format of pymatgen's prototype

    Parameters
    ----------
        struct_dict: dict
            The structure dict generated by pymatgen
        aflow_proto: str
            The aflow symbol of the prototype
        pearson: str
            The pearson symbol of the prototype
        strukturbericht: str
            The strukturbericht symbol of the prototype
        mineral: str
            The mineral name of the prototype
    Returns
    -------
        proto_dict: dict
            The dict for a single prototype
    """
    [aflow_proto, sg, pearson, strukturbericht, mineral, param_list, param_value, ref] = proto_info
    #[aflow_proto, pearson, strukturbericht, mineral, param, param_value, ref] = proto_info
    proto_dict = {}
    timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    about = {"authors": [{"name": "AFLOW Library of Crystallographic Prototypes","email": ""}],
             "projects": [], "references": ref,"remarks": [
                    "Parsed from AFLOW Library of Crystallographic Prototypes. Please cite appropriate AFLOW publication."],
             "history": [],"created_at": {"@module": "datetime","@class": "datetime","string": timestr}}
    struct_dict["about"] = about
    tags = {"spacegroup": sg, "pearson": pearson,"aflow": aflow_proto,"strukturbericht": strukturbericht,"mineral": mineral}
    proto_dict["snl"] = struct_dict
    proto_dict["tags"] = tags
    param = {"param_list":param_list, "param_value": param_value}
    proto_dict["proto_param"] = param
    return proto_dict

def parse_poscar(poscar_folder="."):
    """
    Parse poscar using pymatgen
        if the scale factor is nan, then replace it with scale_struct

    Parameter
    ---------
        poscar_folder: str
            The folder contain the poscar (named as "POSCAR-tmp")
    Return
    ------
        struct: pymatgen structure
            The structure
    """
    pos_template = open(poscar_folder + "/POSCAR-tmp", "r")
    pos_file = open(poscar_folder + "/POSCAR-test", "w+")
    pos_count = 0
    for eachline in pos_template:
        if pos_count == 1:
            scale_factor = eachline.strip("\n").strip()
            if scale_factor == "nan":
                pos_file.write("1.0\n")
            else:
                pos_file.write(eachline)
        else:
            pos_file.write(eachline)
        pos_count = pos_count + 1
    pos_template.close()
    pos_file.close()
    struct = Structure.from_file('POSCAR-test')
    os.remove(poscar_folder + "/POSCAR-test")
    os.remove(poscar_folder + "/POSCAR-tmp")
    return struct

def poscar_map(num):
    """
    Create poscar map for parsing error in pymatgen
    """
    poscarmap = {
    67 : """AB2_aP12_1_4a_8a & a,b/a,c/a,alpha,beta,gamma,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4,x5,y5,z5,x6,y6,z6,x7,y7,z7,x8,y8,z8,x9,y9,z9,x10,y10,z10,x11,y11,z11,x12,y12,z12 --params=5.417,1.0,1.0,90.0,90.0,90.0,0.001,0.002,0.003,0.4966,0.0001,0.5036,0.5001,0.502,0.0011,-0.0006,0.5013,0.5038,0.3857,0.3832,0.384,0.1149,0.6114,0.8846,0.8854,0.1157,0.6143,0.6153,0.8865,0.1141,0.6151,0.6132,0.6137,0.8854,0.3818,0.1149,0.1147,0.8856,0.3841,0.3857,0.1161,0.8842 & P1       C_1^1 #1 (a^12) & aP12 & & FeS2 & anisotropic Pyrite & Bayliss, Am. Mineral. 62, 1168-72 (1977)
   1.0000000000000000
   5.41700000000000   0.00000000000000   0.00000000000000
   0.00000000000000   5.41700000000000   0.00000000000000
   0.00000000000000   0.00000000000000   5.41700000000000
   Fe S
   4  8
  Direct
  -0.00060000000000   0.50130000000000   0.50380000000000   Fe    (1a)
   0.00100000000000   0.00200000000000   0.00300000000000   Fe    (1a)
   0.49660000000000   0.00010000000000   0.50360000000000   Fe    (1a)
   0.50010000000000   0.50200000000000   0.00110000000000   Fe    (1a)
   0.11470000000000   0.88560000000000   0.38410000000000    S    (1a)
   0.11490000000000   0.61140000000000   0.88460000000000    S    (1a)
   0.38570000000000   0.11610000000000   0.88420000000000    S    (1a)
   0.38570000000000   0.38320000000000   0.38400000000000    S    (1a)
   0.61510000000000   0.61320000000000   0.61370000000000    S    (1a)
   0.61530000000000   0.88650000000000   0.11410000000000    S    (1a)
   0.88540000000000   0.11570000000000   0.61430000000000    S    (1a)
   0.88540000000000   0.38180000000000   0.11490000000000    S    (1a)""",
   252: """A3B4_tI28_141_ad_h & a,c/a,y3,z3 --params=5.765,1.63781439722,0.0278,0.2589 & I4_1/amd         D_{4h}^{19} #141 (adh) & tI28 & & Mn3O4 & Hausmannite & D. Jorosch, Mineral. Petrol. 37, 15-23 (1987)
   1.0000000000000000
  -2.88250000000000   2.88250000000000   4.72100000000000
   2.88250000000000  -2.88250000000000   4.72100000000000
   2.88250000000000   2.88250000000000  -4.72100000000000
  Mn    O
  6    8
  Direct
   0.12500000000000  -0.12500000000000   0.25000000000000   Mn    (4a)
  -0.12500000000000   0.12500000000000  -0.25000000000000   Mn    (4a)
   0.00000000000000   0.50000000000000   0.50000000000000   Mn    (8d)
   0.50000000000000   0.00000000000000  -0.00000000000000   Mn    (8d)
   0.50000000000000   0.50000000000000  -0.00000000000000   Mn    (8d)
   0.50000000000000   0.50000000000000   0.50000000000000   Mn    (8d)
   0.25890000000000  -0.26890000000000  -0.02780000000000    O   (16h)
  -0.25890000000000   0.26890000000000   0.02780000000000    O   (16h)
   0.25890000000000   0.28670000000000  -0.47220000000000    O   (16h)
  -0.25890000000000  -0.28670000000000   0.47220000000000    O   (16h)
   0.26890000000000  -0.25890000000000  -0.47220000000000    O   (16h)
  -0.26890000000000   0.25890000000000   0.47220000000000    O   (16h)
   0.28670000000000   0.25890000000000   0.02780000000000    O   (16h)
  -0.28670000000000  -0.25890000000000  -0.02780000000000    O   (16h)"""
    }
    return poscarmap[num]

def formula_map(num):
    """
    Creat formula map for parsing error in url
    """
    formulamap = {18: "-I",
                  30: ".alpha-Pa", 
                  39: ".beta-Po",
                  40: ".alpha-Hg",
                  41: ".alpha-As",
                  43: ".beta-O",
                  350: ".alpha-CO"}
    return formulamap[num]

def multi_replace(s, rep_dict):
    """
    Replace multi strings

    Parameter
    ---------
        s: string
            The string need to be replaced
        rep_dict: dict
            The replace patterns, {old: new}
    Return
    ------
        s: string
            The replaced string
    """
    for pattern in rep_dict:
        s = s.replace(pattern, rep_dict[pattern])
    return s

def parse_proto_param(poscar):
    """
    Parse the parameters and reference of the prototype

    Parameter
    ---------
        poscar: str
            The poscar str in AFLOW website, obtaind by ulropen
    Return
    ------
        param: str
            The parameter list of the prototype, e.g. a,b,c,alpha,beta,gama,x1,y1,z1,...
        value: str
            The value of corresponding parameters of the prototype, e.g. 5.4,5.4,5.4,90,90,90,...
        ref: str
            The reference of the prototype
    """
    line1 = poscar.split("\n")[0].split("&")
    aflow_proto = line1[0].strip()
    paramstr = line1[1]
    paramstr = multi_replace(paramstr, {"\\a": "a", "\\b": "b", "\\g": "g", "\a": "a", "\b": "b", r"\g": "g"})
    param_list = paramstr.split()
    param = param_list[0]
    value = param_list[1].split("=")[-1]
    sg = int(line1[2].split()[2][1:])
    pearson = line1[3].strip()
    strukturbericht = line1[4].strip()
    mineral = line1[-2].strip()
    ref = line1[-1].strip()
    proto_info = [aflow_proto, sg, pearson, strukturbericht, mineral, param, value, ref]
    return proto_info
    #return param, value, ref

def parse_aflow_proto_single(url, fmt="url"):
    """
    Parsing single aflow prototype

    Parameter
    ---------
      url: str
        The POSCAR url of the prototype, e.g. http://www.aflowlib.org/CrystalDatabase/POSCAR/A_cF4_225_a.poscar
          Or the poscar str
      fmt: str
        the format of url
          url: the url is a url
          poscar: the url is a poscar
    Return
    ------
    """
    if fmt == "url":
        try:
            poscar = urlopen(url).read().decode('utf-8')
        except:
            print("Warning: Can't parse the provided url: " + url)
            poscar = ""
    elif fmt == "poscar":
        poscar = url
    else:
        print("Warning: Current format: " + fmt + " not supported.")
        poscar = ""
    try:
        struct = Structure.from_str(poscar, fmt="POSCAR")
        struct_dict = struct.as_dict()
        proto_info = parse_proto_param(poscar)
        proto_dict = gen_proto_dict(struct_dict, proto_info)
        print("Successful")
    except:
        print("Warning: pymatgen can't parse the following poscar.")
        print(poscar)
        proto_dict = None
    return proto_dict

def parse_aflow_proto_url(write_json=True, write_path="."):
    """
    Parse the aflow prototype lib by parsing the url

    Parameter
    ---------
        write_json: bool
            Write out the result as json(True, defalut) or not(False)
        write_path: str
            The path to save the result, default(".")
    Return
    ------
        proto_list: list[dict]
            The list of the prototype database, each element in the list is a prototype(dict)
            If write_json is True, it will generate the aflow_prototype_db.json file
    """
    SERVER = "http://aflow.org/CrystalDatabase/"
    proto_list = []
    filename = os.path.join(os.path.dirname(__file__), "prototype_anrl.all")
    n_count = 0
    special_num = [18, 30, 39, 40, 41, 43, 350]
    with open(filename) as fid:
        for linei in fid:
            n_count += 1
            print("Beign the ith prototype:" + str(n_count))
            linei = linei.strip()
            # aflow, pearson, sg, strukturbericht, formula, sg_num, mineral
            linei_list = re.split(r"\s+", linei)
            #Remove the content after .
            aflow_proto = linei_list[0].split(".")[0]
            formula = linei_list[4]
            mineral = "(".join(" ".join(linei_list[6:]).split("(")[0:-1]).strip()
            aflow_proto_list = aflow_proto.split("-")
            pre_url = aflow_proto_list[0]
            mid_url = [pre_url, pre_url+"."+formula, pre_url+"."+formula.split("-")[-1]]
            if n_count in [67, 252]:
                poscar = poscar_map(n_count)
                proto_dict = parse_aflow_proto_single(poscar, fmt="poscar")
            else:
                for url_i in mid_url:
                    if n_count in special_num:
                        url = SERVER + "POSCAR/" + pre_url + formula_map(n_count) + ".poscar"
                    else:
                        url = SERVER + "POSCAR/" + url_i + ".poscar"
                    proto_dict = parse_aflow_proto_single(url)
                    if proto_dict is None:
                        continue
                    else:
                        break
            proto_dict["tags"]["mineral"] = mineral
            proto_list.append(proto_dict)
    if write_json:
        with open(write_path + '/aflow_prototype_db.json', 'w') as f:
            json.dump(proto_list, f)        
    return proto_list
