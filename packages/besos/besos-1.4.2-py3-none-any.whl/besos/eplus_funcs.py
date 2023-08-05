import json
import os
import re
import platform
import shutil
import subprocess
import warnings

import config
from objectives import read_eso
from utils import create_temp_directory, resolve_path


def get_idf_version(building):
    """ get energyplus version from idf or json file """
    if isinstance(building, dict):
        try:
            idf_version = building["Version"]["Version 1"]["version_identifier"]
        except:
            warnings.warn(f"Cannot find IDF version.")
            idf_version = config.energy_plus_version
    else:
        idf_version = building.idfobjects["VERSION"][0].Version_Identifier
    return idf_version


def check_idf_version(building, version):
    """ check if the version of energyplus matchs the version in idf/json. """
    idf_version = get_idf_version(building).replace("-", ".")
    version = version.replace("-", ".")
    if idf_version != version[:3]:
        msg = f"IDF v{idf_version} does not match energyplus v{version[:3]}."
        warnings.warn(msg)


def run_building(building, out_dir=config.out_dir, **eplus_args):
    """ Run energy plus on a building object and return results

        If out_dir is not defined, the results will not be saved 
        in the file system"""
    with create_temp_directory() as temp_dir:
        if out_dir is None:
            out_dir = temp_dir
        try:
            building_path = resolve_path(temp_dir, "in.idf")
            building.saveas(building_path)
        except AttributeError:
            building_path = resolve_path(temp_dir, "in.epJSON")
            with open(building_path, "w") as f:
                json.dump(building, f)
        run_energyplus(building_path, out_dir=out_dir, **eplus_args)
        results = read_eso(out_dir, version=eplus_args.get("version"))
        return results


def run_energyplus(
    building_path,
    out_dir=config.out_dir,
    epw_file=config.files["epw"],
    err_dir=config.err_dir,
    schema_file=None,
    error_mode="Silent",
    version=config.energy_plus_version,
    ep_path=None,
):
    """ Run energy plus. 
        This method is intended to work as similar to the cli tool as possible"""
    building_path, schema_file, epw_file, out_dir, err_dir = (
        resolve_path(p)
        for p in (building_path, schema_file, epw_file, out_dir, err_dir)
    )

    ep_exe_path, ep_directory = get_ep_path(version, ep_path)
    if schema_file is None:
        schema_file = resolve_path(ep_directory, "Energy+.idd")

    try:
        cmd = [
            ep_exe_path,
            "--idd",
            schema_file,
            "--weather",
            epw_file,
        ]
        if out_dir:
            cmd += ["--output-directory", out_dir]
        cmd.append(building_path)
        if platform.system() == "Windows":
            subprocess.run(cmd, check=True, shell=True)
        else:
            subprocess.run(cmd, check=True, shell=False)
    except subprocess.CalledProcessError as e:
        if error_mode != "Silent":
            # print eplus error
            filename = resolve_path(out_dir, "eplusout.err")
            if os.path.exists(filename):
                err_file = open(filename, "r")
                for line in err_file:
                    print(line)
                print()
                err_file.close()
        if err_dir is not None and out_dir != err_dir:
            # copy eplus error files to err_dir
            if os.path.exists(err_dir):
                shutil.rmtree(err_dir)
            shutil.copytree(out_dir, err_dir)
        raise e


def get_ep_path(version, ep_path):
    """ get energyplus installation path by version"""
    if ep_path != None:
        ep_directory = ep_path
        if platform.system() == "Windows":
            ep_exe = os.path.join(ep_directory, "energyplus.exe")
        elif platform.system() == "Linux":
            ep_exe = os.path.join(ep_directory, "energyplus")
        else:
            ep_exe = os.path.join(ep_directory, "energyplus")
    else:
        if len(version) == 3:
            if version == "9.0":
                version = "9-0-1"
            else:
                version = version.replace(".", "-") + "-0"
        else:
            version = version.replace(".", "-")
        if platform.system() == "Windows":
            ep_directory = "C:/EnergyPlusV{version}".format(version=version)
            ep_exe = os.path.join(ep_directory, "energyplus.exe")
        elif platform.system() == "Linux":
            ep_directory = "/usr/local/EnergyPlus-{version}".format(version=version)
            ep_exe = os.path.join(ep_directory, "energyplus")
        else:
            ep_directory = "/Applications/EnergyPlus-{version}".format(version=version)
            ep_exe = os.path.join(ep_directory, "energyplus")
    return ep_exe, ep_directory


def print_available_outputs(
    building, version=config.energy_plus_version, name=None, frequency=None,
):
    if name is not None:
        name = name.lower()
    if frequency is not None:
        frequency = frequency.lower()
    results = run_building(building, version=version)
    for key in results.keys():
        if name is not None:
            if not re.match(f".*{name}.*", key[0].lower()):
                continue
            if frequency is not None:
                if key[1].lower() != frequency:
                    continue
        elif frequency is not None:
            if key[1].lower() != frequency:
                continue
        print(list(key))
