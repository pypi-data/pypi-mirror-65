
import math
import time
import glob
import numpy as np
import shapely
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import PySimpleGUI as sg
from shapely.wkb import loads
from shapely.geometry import Polygon
from shapely.ops import cascaded_union, unary_union, nearest_points
pd.options.mode.chained_assignment = None

class check_topology:
    
    def __init__(self, data):
        
        self.data = data
        if isinstance(data, str):
            gdf = gpd.read_file(self.data)
        elif isinstance(data, gpd.GeoDataFrame):
            gdf = self.data
        else:
            raise TypeError(f"{self.data} is not supported type of data location,\neither use shapefile location or geodataframe")
        val_data = gpd.GeoDataFrame()
        for index, row in tqdm(gdf.iterrows(), total = gdf.shape[0]):
            if row['geometry'].is_valid == False | row['geometry'].is_simple == False:
                deci = sg.PopupYesNo("Do you want to fix the geometry?")
                if deci == 'Yes':
                    pol = row['geometry'].buffer(0)
                    time.sleep(1)
                    mid = gpd.GeoDataFrame(geometry=gpd.GeoSeries(pol))
                    val_data = val_data.append(mid)
                else:
                    break
            else:
                val = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                val_data = val_data.append(val)
        if val_data.crs == None:
            val_data.crs = {'init': 'epsg:4326'}
        self.geosolution = val_data

class dissolve_polygon:
    
    def __init__(self,
                 data: gpd.GeoDataFrame, threshold: float
                 )-> gpd.GeoDataFrame:
        self.threshold = threshold
        if not isinstance(data, gpd.GeoDataFrame):
            return gpd.GeoDataFrame()
        data = data.copy()
        while True:
            src = src_idx = None
            for i in range(len(data.index)):
                row = data.iloc[i]
                row_geom = row["geometry"]
                if row_geom.area <= threshold/1.0e10:
                    src_idx = i
                    src = row
                    break
            if src is None:
                break
            src_geom = src["geometry"]
            # if not isinstance(src_geom, (shapely.geometry.polygon.Polygon)):
            #     print(f"src {src.name} is not a polygon")
            # Find adjacent poly with largest shared border to merge
            dst = dst_len = None
            intersection = data.intersection(src_geom)
            for i in tqdm(range(len(data.index))):
                if src_idx == i:
                    continue
                shape = intersection.iloc[i]
                intersection_length = 0
                if isinstance(shape, shapely.geometry.LineString):
                    intersection_length = shape.length
                elif isinstance(shape, shapely.geometry.MultiLineString):
                    intersection_length = max([line.length for line in shape.geoms])
                else:
                    continue
                if dst is None or intersection_length > dst_len:
                    dst = data.iloc[i]
                    dst_len = intersection_length
                    continue
            if dst is None:
                # print(f"Couldn't find candidate for merge with {src_idx}")
                break
            dst_geom = dst["geometry"]
            #print(f"Merging {src.name} into {dst.name}")
            try:
                data.loc[dst.name, "geometry"] = cascaded_union([src_geom, dst_geom])
            except ValueError:
                pass
            if src_geom.area > dst_geom.area:
                #print(f"Copying attributes from src {src.name} to dst {dst.name}")
                for column in data.columns:
                    if column == "geometry":
                        continue
                    data.loc[dst.name, column] = src[column]
            data.drop([src.name], inplace=True)
        self.geosolution = data

class hexagon_grid:
    
    def __init__(self,
                 data, 
                 spacing,
                 hexagon_dis:bool,
                 area_threshold:float = None
                 ):
        self.data = data
        self.spacing = spacing
        self.hexagon_dis = hexagon_dis
        self.area_threshold = area_threshold
        if isinstance(data, str):
            gdf = gpd.read_file(self.data)
        elif isinstance(data, gpd.GeoDataFrame):
            gdf = self.data
        else:
            raise TypeError(f"{self.data} is not supported type of data location,\neither use shapefile location or geodataframe")
        
        hSpacing = spacing/100000
        vSpacing = spacing/100000
        hOverlay = 0.0
        vOverlay = 0.0
    
        # To preserve symmetry, hspacing is fixed relative to vspacing
        xVertexLo = 0.288675134594813 * vSpacing
        xVertexHi = 0.577350269189626 * vSpacing
        hSpacing = xVertexLo + xVertexHi
    
        hOverlay = hSpacing
        
        halfVSpacing = vSpacing / 2.0
    
        xmin, ymin = [i.min() for i in gdf.bounds.T.values[:2]]
        xmax, ymax = [i.max() for i in gdf.bounds.T.values[2:]]
        cols = int(math.ceil((xmax - xmin) / hOverlay))
        rows = int(math.ceil((ymax - ymin) / (vSpacing - vOverlay)))
        
        geoms = []
        for col in tqdm(range(cols)):
            # (column + 1) and (row + 1) calculation is used to maintain
            # topology between adjacent shapes and avoid overlaps/holes
            # due to rounding errors
            x1 = xmin + (col * hOverlay)    # far left
            x2 = x1 + (xVertexHi - xVertexLo)  # left
            x3 = xmin + (col * hOverlay) + hSpacing  # right
            x4 = x3 + (xVertexHi - xVertexLo)  # far right
    
            for row in range(rows):
                if (col % 2) == 0:
                    y1 = ymax + (row * vOverlay) - (((row * 2) + 0) * halfVSpacing)  # hi
                    y2 = ymax + (row * vOverlay) - (((row * 2) + 1) * halfVSpacing)  # mid
                    y3 = ymax + (row * vOverlay) - (((row * 2) + 2) * halfVSpacing)  # lo
                else:
                    y1 = ymax + (row * vOverlay) - (((row * 2) + 1) * halfVSpacing)  # hi
                    y2 = ymax + (row * vOverlay) - (((row * 2) + 2) * halfVSpacing)  # mid
                    y3 = ymax + (row * vOverlay) - (((row * 2) + 3) * halfVSpacing)  # lo
    
                geoms.append((
                    (x1, y2),
                    (x2, y1), (x3, y1), (x4, y2), (x3, y3), (x2, y3),
                    (x1, y2)
                ))
                
        hexa_data =  gpd.GeoDataFrame(
            index=[i for i in range(len(geoms))],
            geometry=pd.Series(geoms).apply(lambda x: Polygon(x)),
            crs=gdf.crs
            )
        
        datax = gpd.GeoDataFrame(crs = {'init': 'epsg:4326'})
        for index, row in tqdm(hexa_data.iterrows(), total = hexa_data.shape[0]):
            if row['geometry'] != None and row['geometry'].geom_type == 'Polygon':
                df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                datax = datax.append(df, sort = False)
            else:
                pass
        if datax.crs ==None:
            datax.crs ={'init': 'epsg:4326'}
        final_hexa =gpd.overlay(gdf.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                gpd.overlay(gdf.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                            datax, how='intersection'),
                                how = 'union')[['geometry']].copy()
        if final_hexa.crs ==None:
            final_hexa.crs ={'init': 'epsg:4326'}
        if hexagon_dis == True:
            self.geosolution = final_hexa
        else:
            if self.area_threshold == None:
                area_thres = (spacing*spacing)*0.33
                hexagon = dissolve_polygon(final_hexa, area_thres).geosolution
                df = hexagon.explode().reset_index().drop(['level_0', 'level_1'], axis = 1)
                df["geometry"] = df["geometry"].apply(lambda geom: geom.wkb)
                df = df.drop_duplicates(["geometry"])
                df["geometry"] = df["geometry"].apply(lambda geom: loads(geom))
                pdf = gpd.overlay(gdf, df, how = 'union')
                check_topology(pdf)
                self.geosolution = pdf
            elif 0.0 < self.area_threshold <= 0.8:
                area_thres = (spacing*spacing)*self.area_threshold
                hexagon = dissolve_polygon(final_hexa, area_thres).geosolution
                df = hexagon.explode().reset_index().drop(['level_0', 'level_1'], axis = 1)
                df["geometry"] = df["geometry"].apply(lambda geom: geom.wkb)
                df = df.drop_duplicates(["geometry"])
                df["geometry"] = df["geometry"].apply(lambda geom: loads(geom))
                pdf = gpd.overlay(gdf, df, how = 'union')
                check_topology(pdf)
                self.geosolution = pdf
            else:
                raise ValueError("You shouldn't cross the upper/lower limit of area threshold.\nThreshold should be 0.0> area_threshold>=0.8")


class merge_shapefile:
    
    def __init__(self, shape_path):
        
        self.shape_path = shape_path
        if not isinstance(self.shape_path, gpd.GeoDataFrame):
            try:
                gdf = pd.concat([gpd.read_file(shp)for shp in [i for i in glob.glob(f"{shape_path}/*.shp")]]).pipe(gpd.GeoDataFrame)
                self.geosolution = gdf
            except ValueError:
                self.geosolution = gpd.read_file(self.shape_path)
        elif isinstance(self.shape_path, gpd.GeoDataFrame):
            self.geosolution = self.shape_path
        else:
            raise TypeError(f"{self.shape_path} is not supported type of data location,\neither use shapefile location or geodataframe")

class check_crs:
    
    def __init__(self,
                 gdf
                 ):
        
        self.gdf = gdf
        if isinstance(gdf, gpd.GeoDataFrame):
            if gdf.crs == None:
                gdf.crs = {'init': 'epsg: 4326'}
            self.geosolution = gdf
        elif isinstance(gdf, str):
            data = gpd.read_file(gdf)
            if data.crs == None:
                data.crs = {'init': 'epsg: 4326'}
            self.geosolution = data
        else:
            raise TypeError(f"{self.gdf} is not supported type of data location,\neither use shapefile location or geodataframe")

class transfer_val:
    
    def __init__(self,
                     datas,
                     area_threshld:float,
                     attribute:str,
                     naval = None):
        
        self.datas = datas
        self.area_threshld = area_threshld
        self.attribute = attribute
        self.naval = naval
        if isinstance(self.datas, str):
            data = gpd.read_file(self.datas)
        elif isinstance(self.datas, gpd.GeoDataFrame):
            data = self.datas
        else:
            raise TypeError(f"{self.datas} is not supported type of data location,\neither use shapefile location or geodataframe")
        if 'UID' not in data.columns.unique():
            data['UID']=range(0, len(data))
        
        if self.naval is not None:
            print(f"Considered values {self.naval} in the {self.attribute} for replacing the NAN value")
            if len(data[data[f"{self.attribute}"].isnull()]) != 0:
                data[f"{self.attribute}"].fillna(self.naval, inplace = True)
            else:
                pass
        else:
            print(f"Considered values 3 in the {self.attribute} for replacing the NAN value")
            if len(data[data[f"{self.attribute}"].isnull()]) != 0:
                data[f"{self.attribute}"].fillna(3, inplace = True)
            else:
                pass
        data['area_ac'] = data.geometry.area*(100000**2)/4046.86
        df_null = data[data[f"{self.attribute}"].isnull()]
        area_silv = data[data['area_ac']<=self.area_threshld]
        silv = pd.concat([area_silv , df_null], sort = False)
        del silv[f"{self.attribute}"]
        ohex = data[data['area_ac']>=self.area_threshld]
        
        def conv_point(gdf):
            centx = gpd.GeoDataFrame(geometry=gpd.GeoSeries(gdf.representative_point()))
            if centx.crs == None:
                centx.crs = {'init': 'epsg:4326'}
            faul = gpd.sjoin(centx, gdf, op="intersects")
            del faul['index_right']
            return faul
        
        def calculate_nearest(row, destination, val, col="geometry"):
            # 1 - create unary union    
            dest_unary = destination["geometry"].unary_union
            # 2 - find closest point
            nearest_geom = nearest_points(row[col], dest_unary)
            # 3 - Find the corresponding geom
            match_geom = destination.loc[destination.geometry 
                        == nearest_geom[1]]
            # 4 - get the corresponding value
            match_value = match_geom[val].to_numpy()[0]
            return match_value
        
        silv_p = conv_point(silv)
        ohex_p =conv_point(ohex)
        silv_p["near_geom"] = silv_p.apply(calculate_nearest, destination=ohex_p, val="geometry", axis=1)
        silv_p["near_GZ"] = silv_p.apply(calculate_nearest, destination=ohex_p, val=f"{self.attribute}", axis=1)
        del silv_p["geometry"]
        silv_p.rename(columns={"near_geom": "geometry", "near_GZ": f"{self.attribute}"}, inplace = True)
        silve = gpd.GeoDataFrame(silv_p, geometry='geometry', crs={"init":"epsg:4326"})
        
        fg = silve[[f"{self.attribute}", "UID"]].copy()
        data_dvm=silv.merge(fg, on=["UID"])
        point_df = pd.concat([ohex, data_dvm], sort = False)
        point_df.drop(['UID', 'area_ac'], inplace = True, axis= 1)
        self.geosolution = point_df

class square_grid:
    
    def __init__(self,
                  gdf,
                  spacing:int,
                  cut=True
                  ):
        
        self.gdf = gdf
        self.spacing = spacing
        self.cut = cut
        
        if isinstance(self.gdf, str):
            datas = gpd.read_file(self.gdf)
            data = gpd.GeoDataFrame(
                geometry=gpd.GeoSeries(unary_union(datas.geometry).intersection(
                    unary_union(datas.geometry).buffer(0.1)))).explode().reset_index().drop(['level_0', 'level_1'],
                                                                                              axis = 1)
        elif isinstance(self.gdf, gpd.GeoDataFrame):
            datas = self.gdf
            data = gpd.GeoDataFrame(
                geometry=gpd.GeoSeries(unary_union(datas.geometry).intersection(
                    unary_union(datas.geometry).buffer(0.1)))).explode().reset_index().drop(['level_0', 'level_1'],
                                                                                              axis = 1)
        else:
            raise TypeError(f"{self.gdf} is not supported type of data location,\neither use shapefile location or geodataframe")
        
        if data.crs == None:
            data.crs = {'init': 'epsg:4326'}
            length = (self.spacing/1.0e5)
        else:
            length = self.spacing
        
        xmin,ymin,xmax,ymax =  data.total_bounds
        rows = int(np.ceil((ymax-ymin) /  length))
        cols = int(np.ceil((xmax-xmin) / length))
        x_left_origin = xmin
        x_right_origin = xmin + length
        y_top_origin = ymax
        y_bottom_origin = ymax -  length
        res_geoms = []
        for countcols in range(cols):
            y_top = y_top_origin
            y_bottom = y_bottom_origin
            for countrows in range(rows):
                res_geoms.append((
                (x_left_origin, y_top), (x_right_origin, y_top),
                (x_right_origin, y_bottom), (x_left_origin, y_bottom)))
                y_top = y_top -  length
                y_bottom = y_bottom -  length
            x_left_origin = x_left_origin + length
            x_right_origin = x_right_origin + length
        if cut:
            if all(data.eval(
                "geometry.type =='Polygon' or geometry.type =='MultiPolygon'")):
                res = gpd.GeoDataFrame(geometry=gpd.GeoSeries(res_geoms).apply(lambda x: Polygon(x)),crs=data.crs).intersection(unary_union(data.geometry).convex_hull)
            else:
                res = gpd.GeoDataFrame(geometry=gpd.GeoSeries(res_geoms).apply(lambda x: Polygon(x)),crs=data.crs).intersection(unary_union(data.geometry).convex_hull)
            res = res[res.geometry.type == 'Polygon']
            res.index = [i for i in range(len(res))]
            dfds =  gpd.GeoDataFrame(geometry=res)
            datax = gpd.GeoDataFrame(crs = {'init': 'epsg:4326'})
            for index, row in tqdm(dfds.iterrows(), total = dfds.shape[0]):
                if row['geometry'] != None and row['geometry'].geom_type == 'Polygon':
                    df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                    datax = datax.append(df, sort = False)
                else:
                    pass
            if datax.crs ==None:
                datax.crs ={'init': 'epsg:4326'}
            final_hexa =gpd.overlay(datas.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                    gpd.overlay(datas.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                                datax, how='intersection'),
                                    how = 'union')[['geometry']].copy()
            area_thresholda = (length*length)*0.10
            disolve_square = dissolve_polygon(final_hexa, area_thresholda).geosolution
            check_topology(disolve_square)
            self.geosolution = disolve_square
        else:
            dfds = gpd.GeoDataFrame(index=[i for i in range(len(res_geoms))],geometry=gpd.GeoSeries(res_geoms).apply(lambda x: Polygon(x)),crs=data.crs)
            datax = gpd.GeoDataFrame(crs = {'init': 'epsg:4326'})
            for index, row in tqdm(dfds.iterrows(), total = dfds.shape[0]):
                if row['geometry'] != None and row['geometry'].geom_type == 'Polygon':
                    df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                    datax = datax.append(df, sort = False)
                else:
                    pass
            if datax.crs ==None:
                datax.crs ={'init': 'epsg:4326'}
            final_hexa =gpd.overlay(datas.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                    gpd.overlay(datas.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                                datax, how='intersection'),
                                    how = 'union')[['geometry']].copy()
            area_thresholda = (length*length)*0.10
            disolve_square = dissolve_polygon(final_hexa, area_thresholda).geosolution
            check_topology(disolve_square)
            self.geosolution = disolve_square

class calc_area:
    
    def __init__(self,
                 df,
                 delarea:float = None,
                 ):
        
        self.df = df
        self.delarea = delarea
        
        if isinstance(self.df, str):
            data = gpd.read_file(self.df)
            if data.crs == None:
                data.crs = {'init':'epsg:4326'}
        elif isinstance(self.df, gpd.GeoDataFrame):
            data = self.df
            if data.crs == None:
                data.crs = {'init':'epsg:4326'}
        else:
            raise KeyError(f"{self.df} is errorneous data location, please fix the data location problem")
        
        if self.delarea == None:
            data['area_ac'] = data.geometry.area*(100000**2)/4046.86
            ohex = data[data['area_ac']>=0.0000001]
            self.geosolution = ohex
        else:
            data['area_ac'] = data.geometry.area*(100000**2)/4046.86
            ohex = data[data['area_ac']>=self.delarea]
            self.geosolution = ohex

class assign_uid:
    
    def __init__(self,
                 df,
                 attribute:str = None
                 ):
        
        self.df = df
        self.attribute = attribute
        
        if isinstance(self.df, str):
            data = gpd.read_file(self.df)
            if data.crs == None:
                data.crs = {'init': 'epsg:4326'}
        elif isinstance(self.df, gpd.GeoDataFrame):
            data = self.df
            if data.crs == None:
                data.crs = {'init':'epsg:4326'}
        else:
            raise KeyError(f"{self.df} is errorneous data location, please fix the data location problem")
        
        if self.attribute == None:
            data['Soil_Sampl'] = range(0, 0+len(data))
            self.geosolution = data
        elif self.attribute != None:
            data[f"{self.attribute}"] = range(0, 0+len(data))
            self.geosolution = data
        else:
            print("You need to apecify the parameters")
        
        