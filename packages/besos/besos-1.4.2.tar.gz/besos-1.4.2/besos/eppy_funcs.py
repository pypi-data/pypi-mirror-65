"""
This file is a collection of functions to interact with eppy and geomeppy.
They could do with some sorting and refactoring.
"""

import contextlib
import json
import os
import warnings
from functools import partial

import numpy as np
from geomeppy import IDF
from shapely.geometry import LineString, Point, Polygon

import config
import eplus_funcs as eplus
from errors import ModeError

import sqlite3
import pandas as pd
import csv
import re
from pathlib import Path


def merge_building(building_from, building_to):
    """Copy objects in building_from to building_to.
    """
    mode_from = get_mode(building_from)
    mode_to = get_mode(building_to)
    if mode_to == "idf" and mode_from == "idf":
        for attr in building_from.idfobjects:
            for idfobject in building_from.idfobjects[attr]:
                building_to.copyidfobject(idfobject)
    elif mode_to == "json" and mode_from == "json":
        for attr in building_from:
            if attr in building_to:
                building_to[attr].update(building_from[attr])
            else:
                building_to[attr] = building_from[attr]
    else:
        raise NotImplementedError


def convert_format(s: str, place, mode):
    """Converts energyPlus names to their Eppy equivalents

    :param s: name to convert
    :param place: the type of place that is being used 'field' or 'class'
    :param mode: whether to convert to idf or json formating
    :return: the converted name
    """
    # TODO: Find an authoritative source for the naming conventions
    if mode == "idf":
        if place == "field":
            return s.replace(" ", "_").replace("-", "")
        if place == "class":
            return s.upper()
    if mode == "json":
        if place == "field":
            return s.replace(" ", "_").replace("-", "_").lower()
        if place == "class":
            # uses camel case, s.title() removes some of the capitals and does not work
            return s
    raise ModeError(message=f"no format defined for place:{place} and mode:{mode}")


def get_mode(building):
    if isinstance(building, IDF):
        return "idf"
    if isinstance(building, dict):
        return "json"
    raise ModeError(message=f"Cannot find a valid mode for {building}")


def get_idf(
    idf_file: str = config.files.get("idf"),
    idd_file: str = None,
    version=config.energy_plus_version,
    output_directory=config.out_dir,
    ep_path=None,
) -> IDF:
    """Uses eppy to read an idf file and generate the corresponding idf object"""
    if idd_file is None:
        ep_exe, ep_directory = eplus.get_ep_path(version, ep_path)
        idd_file = os.path.join(ep_directory, "Energy+.idd")
    # Trying to change the idd file inside a program will cause an error
    IDF.setiddname(idd_file)
    # TODO: Fix this rather than hiding it.
    # calling IDF causes a warning to appear, currently redirect_stdout hides this.
    with contextlib.redirect_stdout(None):
        idf = IDF(idf_file)
        # override the output location so I stop messing up
        idf.run = partial(idf.run, output_directory=output_directory)
        return idf


def get_building(
    building=None,
    data_dict=None,
    output_directory=config.out_dir,
    mode=None,
    version=config.energy_plus_version,
    ep_path=None,
):
    """Get building from directory
    """
    if mode is None and building is None:
        building = config.files.get("building")
        mode = config.energy_plus_mode
    if mode is None:
        ending = building.split(".")[-1]
        if ending == "idf":
            mode = "idf"
        elif ending == "epJSON":
            mode = "json"
        else:
            warnings.warn(
                f'expected "idf" or "epJSON" file. building has extension {ending}'
            )
    if building is None:
        building = config.files[mode]
    if mode == "idf":
        if data_dict is None:
            _, ep_directory = eplus.get_ep_path(version, ep_path)
            data_dict = os.path.join(ep_directory, "Energy+.idd")
        idf = get_idf(
            idf_file=building, idd_file=data_dict, output_directory=output_directory
        )
        return idf
    elif mode == "json":
        with open(building) as f:
            return json.load(f)
    ModeError(mode)


def get_windows(building):
    mode = get_mode(building)
    if mode == "idf":
        return (
            (window.Name, window)
            for window in building.idfobjects["FENESTRATIONSURFACE:DETAILED"]
        )
    elif mode == "json":
        return building["FenestrationSurface:Detailed"].items()
    else:
        raise ModeError(mode)


def wwr_all(building, wwr: float) -> None:
    """Sets the wwr for all walls that have a window.
    Will malfunction if there are multiple windows on one wall
    """
    mode = get_mode(building)
    windows = get_windows(building)
    for window_name, window in windows:
        wwr_single(window, wwr, building, mode)


def set_vertex(idfObj, vertexNum: int, x: float = 0, y: float = 0, z: float = 0):
    """Sets a single vertex of the passed idfObject (idfObj)
     to the specified x,y and z coordinates."""
    for val, name in zip((x, y, z), "XYZ"):
        idfObj["Vertex_{}_{}coordinate".format(vertexNum, name)] = round(val, 2)


def one_window(building):
    """Removes some windows so that each wall has no more than one"""
    mode = get_mode(building)
    walls = set()
    toRemove = []
    windows = get_windows(building)
    for window_name, window in windows:
        if mode == "idf":
            wall_name = window.Building_Surface_Name
        elif mode == "json":
            wall_name = window["building_surface_name"]
        else:
            raise ModeError(mode)
        if wall_name in walls:
            toRemove.append((window_name, window))
        else:
            walls.add(wall_name)
    if mode == "idf":
        for window_name, window in toRemove:
            building.idfobjects["FENESTRATIONSURFACE:DETAILED"].remove(window)
    elif mode == "json":
        for window_name, window in toRemove:
            building["FenestrationSurface:Detailed"].pop(window_name)


def wwr_single(window, wwr: float, building, mode):
    """Sets `window` to have the window to wall ratio specified by `wwr`"""

    # will not work for some orientations
    # multiple windows on a single wall will break this
    if mode == "idf":

        def coordinates(ax):
            return [window[f"Vertex_{n}_{ax.upper()}coordinate"] for n in range(1, 5)]

        wall = building.getobject(
            "BUILDINGSURFACE:DETAILED", window.Building_Surface_Name
        )
    elif mode == "json":

        def coordinates(ax):
            return [window[f"vertex_{n}_{ax.lower()}_coordinate"] for n in range(1, 5)]

        wall = building["BuildingSurface:Detailed"][window["building_surface_name"]]
    else:
        raise ModeError(mode)

    xs = coordinates("X")
    ys = coordinates("Y")
    zs = coordinates("Z")

    if max(ys) == min(ys):
        axis = "x"
        axs = xs
    elif max(xs) == min(xs):
        axis = "y"
        axs = ys
    else:
        raise ValueError("The window is not aligned with the x or y axes")
    width = max(axs) - min(axs)
    scale_factor = np.sqrt(wwr)
    new_width = width * scale_factor
    height = max(zs) - min(zs)
    new_height = height * scale_factor

    startW = (width - new_width) / 2
    endW = startW + new_width
    startH = (height - new_height) / 2
    endH = startH + new_height

    # Maintains vertex order by mimicking the current order
    s = [0] * 4
    for vertex in range(0, 4):
        if zs[vertex] == max(zs):
            # vertex on the top
            if axs[vertex] == max(axs):
                # TOP RIGHT
                s[0] += 1
                set_vertex(window, vertex + 1, z=endH, **{axis: endW})
            else:
                # TOP LEFT
                s[1] += 1
                set_vertex(window, vertex + 1, z=endH, **{axis: startW})
        else:
            if axs[vertex] == max(axs):
                # BOTTOM RIGHT
                s[2] += 1
                set_vertex(window, vertex + 1, z=startH, **{axis: endW})
            else:
                # BOTTOM LEFT
                s[3] += 1
                set_vertex(window, vertex + 1, z=startH, **{axis: startW})
    assert s == [1] * 4, ("verticesS are wrong:", s)


def set_daylight_control(building, zone_name, distance, illuminance=500):
    """ Set daylighting control to the biggest window of the zone.

    :param building: an idf object
    :param zone_name: name of the zone
    :param distance: the distance from the reference point to the window
    :param illuminance: illuminance setpoint at reference point
    """
    surfs = [
        s.Name
        for s in building.idfobjects["BUILDINGSURFACE:DETAILED"]
        if s.Surface_Type.upper() == "WALL" and s.Zone_Name == zone_name
    ]
    windows = [
        w
        for w in building.idfobjects["FENESTRATIONSURFACE:DETAILED"]
        if w.Surface_Type.upper() == "WINDOW" and w.Building_Surface_Name in surfs
    ]
    if not windows:
        raise ValueError(f"No window found in {zone_name}.")
    window = windows[0]
    max_area = window.area
    for w in windows[1:]:
        area = w.area
        if area > max_area:
            max_area = area
            window = w
    vertex = get_vertices(building, zone_name, window, distance)
    if vertex is None:
        raise ValueError(f"Unable to find a daylighting reference point.")
    building.newidfobject(
        "Daylighting:Controls".upper(),
        Name=f"{zone_name} Daylighting Control",
        Zone_Name=zone_name,
        Minimum_Input_Power_Fraction_for_Continuous_or_ContinuousOff_Dimming_Control=0.01,
        Minimum_Light_Output_Fraction_for_Continuous_or_ContinuousOff_Dimming_Control=0.01,
        Glare_Calculation_Daylighting_Reference_Point_Name=f"{zone_name} Daylighting Reference Point",
        Daylighting_Reference_Point_1_Name=f"{zone_name} Daylighting Reference Point",
        Illuminance_Setpoint_at_Reference_Point_1=illuminance,
    )
    building.newidfobject(
        "Daylighting:ReferencePoint".upper(),
        Name=f"{zone_name} Daylighting Reference Point",
        Zone_Name=zone_name,
        XCoordinate_of_Reference_Point=vertex[0],
        YCoordinate_of_Reference_Point=vertex[1],
        ZCoordinate_of_Reference_Point=vertex[2],
    )


def get_vertices(building, zone_name, window, distance):
    v1 = (
        window.Vertex_1_Xcoordinate,
        window.Vertex_1_Ycoordinate,
        window.Vertex_1_Zcoordinate,
    )
    v2 = (
        window.Vertex_2_Xcoordinate,
        window.Vertex_2_Ycoordinate,
        window.Vertex_2_Zcoordinate,
    )
    v3 = (
        window.Vertex_3_Xcoordinate,
        window.Vertex_3_Ycoordinate,
        window.Vertex_3_Zcoordinate,
    )
    vertices = [v1, v2, v3]

    def subtract(v1, v2):
        return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

    for i in range(3):
        for j in range(i + 1, 3):
            line = subtract(vertices[i], vertices[j])
            if line[2] == 0:
                point1, midpoint = (
                    vertices[j],
                    (
                        (vertices[j][0] + vertices[i][0]) / 2,
                        (vertices[j][1] + vertices[i][1]) / 2,
                    ),
                )
            elif line[1] == 0 or line[0] == 0:
                height = abs(line[2]) / 2
    r_point1, r_point2 = get_reference_point(point1[:2], midpoint, distance)
    r_point = point_in_zone(building, zone_name, [r_point1, r_point2])
    if r_point is not None:
        return r_point + (height,)
    return None


def point_in_zone(building, zone_name, points):
    surfs = building.idfobjects["BUILDINGSURFACE:DETAILED"]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone_name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == "FLOORS"]
    for floor in floors:
        for p in points:
            if point_in_surface(floor, p):
                return p
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() in ["ROOF", "CEILING"]]
    for roof in roofs:
        for p in points:
            if point_in_surface(roof, p):
                return p
    return None


def point_in_surface(surface, p):
    v1 = (surface.Vertex_1_Xcoordinate, surface.Vertex_1_Ycoordinate)
    v2 = (surface.Vertex_2_Xcoordinate, surface.Vertex_2_Ycoordinate)
    v3 = (surface.Vertex_3_Xcoordinate, surface.Vertex_3_Ycoordinate)
    v4 = (surface.Vertex_4_Xcoordinate, surface.Vertex_4_Ycoordinate)
    poly = Polygon((v1, v2, v3, v4))
    point = Point(p)
    return poly.contains(point)


def get_reference_point(p1, p2, distance):
    line1 = LineString([p1, p2])
    left = line1.parallel_offset(distance, "left")
    right = line1.parallel_offset(distance, "right")
    p3 = left.boundary[1]
    p4 = right.boundary[0]
    return (p3.x, p3.y), (p4.x, p4.y)


def read_sql(path: str, cmds: list, direction=None):
    """ Open sql file wiht connect

        :param path: absolute directory to the sql file.
        :param cmds: list of commands need to be processed, 'all' will process all cmds. All cmds available : 'all', 'wall area', 'ceiling height', 'floor area', 'volume'
        :param direction: a list of directions of walls when process wall area cmd, None means taking both area and gross area of walls in all directions and the total areas of all walls.
        :return: a dictionary of all data desired.

    """
    try:
        sql_path = path
        conn = sqlite3.connect(sql_path)
        cur = conn.cursor()
    except IOError:
        print("Either no such file or file path is not correct.")

    def wallArea(dire: str):
        """Find total area with window substracted of either all walls or only walls in current direction
        """
        table_name = "Surfaces"
        azim_range = [0, 0]
        query = ""
        if dire == "total":
            azim_range = [0, 360]
        elif dire == "north":
            query = "SELECT SUM(Area), SUM(GrossArea) FROM {} WHERE (ClassName = 'Wall' AND ((Azimuth >= 0 AND Azimuth <= 44.99) or (Azimuth >= 315 AND Azimuth <= 360)))".format(
                table_name
            )
            cur.execute(query)
            data = cur.fetchall()
            return data
        elif dire == "east":
            azim_range = [45, 135]
        elif dire == "south":
            azim_range = [135, 269.99]
        elif dire == "west":
            azim_range = [270, 515]
        else:
            raise NameError(
                "Wrong direction! attention on the str, 'north', 'south', 'west', 'east'"
            )

        query = "SELECT SUM(Area), SUM(GrossArea) FROM {} WHERE (ClassName = 'Wall' AND Azimuth >= {} AND Azimuth <= {})".format(
            table_name, azim_range[0], azim_range[1]
        )
        cur.execute(query)
        data = cur.fetchall()
        return data

    def ceiling_height():
        """Find height of the ceiling
        """
        floor = floor_area()
        volume = zoneVolume()
        height = volume / floor
        return height

    def floor_area():
        """Find total floor area
        """
        table_name = "Zones"
        query = f"SELECT SUM(FloorArea) FROM {table_name}"
        cur.execute(query)
        data = cur.fetchall()
        return data[0][0]

    def zoneVolume():
        """Find total voulme of Zones
        """
        table_name = "Zones"
        query = f"SELECT SUM(Volume) FROM {table_name}"
        cur.execute(query)
        data = cur.fetchall()
        return data[0][0]

    if isinstance(cmds, list) != True:
        raise TypeError("cmds has be a list")

    # Taking commands, there is a small problem is that the code is not checking if the direction is correc.
    # And there is no protection when using cmd all and others
    result = {}
    direct = []
    # decide which direction we want
    if direction == None:
        direct = ["total", "south", "north", "west", "east"]
    else:
        direct = direction
    if len(cmds) == 1 and cmds[0] == "all":
        result.update(
            {
                "ceiling height": ceiling_height(),
                "floor area": floor_area(),
                "volume": zoneVolume(),
            }
        )
        for dire in direct:
            area = wallArea(dire)
            result.update(
                {f"{dire} wall area": area[0][0], f"{dire} wall gross area": area[0][1]}
            )
    else:
        for cmd in cmds:
            if cmd == "all":
                raise NameError(
                    "There should not be an 'all' command with other commands"
                )
            elif cmd == "wall area":
                for dire in direct:
                    area = wallArea(dire)
                    result.update(
                        {
                            f"{dire} wall area": area[0][0],
                            f"{dire} wall gross area": area[0][1],
                        }
                    )
            elif cmd == "ceiling height":
                result.update({"ceiling height": ceiling_height()})
            elif cmd == "floor area":
                result.update({"floor area": floor_area()})
            elif cmd == "volume":
                result.update({"volume": zoneVolume()})
            else:
                raise NameError(
                    "No such command, available cmds are 'all', 'wall area', 'buiding height', 'floor area'"
                )
    conn.close()
    return result


# TODO make this function customizable for more cmds, not just a handler for one task.
# Add direction
# Add cmds
def write_csv(path: str, dest: str):
    """ A handler to call read_sql() function and get data, then put the data into exl file

        :param path: path to read sql file
        :param dest: destination to put data
        :param cmds: commands passing to read_sql()
        :param direction: direction of the desired walls passing to read_sql()
    """
    # Get data from sql file get all datas for now
    data = read_sql(path, ["all"],)

    # Get number of floors and shape from file name
    filename = Path(dest).name
    match = re.search(r"M.idf", filename)
    numOfFloor = 0
    if match == None:
        numOfFloor = 1
    else:
        numOfFloor = 3
    shape = filename[0].upper()

    # Read csv file
    df = pd.read_csv(dest)
    wall_area = []
    south_wall_area = []
    total_rows = len(df["Window to Wall Ratio"])
    for i in range(total_rows):
        totalArea = data["total wall gross area"] * (1 - df["Window to Wall Ratio"][i])
        southArea = data["south wall gross area"] * (1 - df["Window to Wall Ratio"][i])
        wall_area.append(totalArea)
        south_wall_area.append(southArea)

    # put data back to csv
    df["wall area net"] = wall_area
    df["wall area gross"] = data["total wall gross area"]
    df["south wall area net"] = south_wall_area
    df["south wall area gross"] = data["south wall gross area"]
    df["number of floors"] = numOfFloor
    df["ceiling height"] = data["ceiling height"]
    df["total floor area"] = data["floor area"]
    df["total volume"] = data["volume"]
    df["shape"] = shape
    df.to_csv(dest)


def get_files(directory: str, filetype: str):
    """ Get all file names in the directory

        :param directory: directory to the folder contains all files
        :param filetype: the desired file's types
        :return: a list of file names 
    """
    fileNames = []
    entries = Path(directory)
    for entry in entries.iterdir():
        match = re.search(f".{filetype}$", entry.name)
        if match:
            fileNames.append(entry.name)
    if len(fileNames) == 0:
        raise NameError(
            "No desired file type matched, please check with the file type again."
        )
    return fileNames
