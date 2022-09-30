import numpy as np
import urllib.request
from zipfile import ZipFile
import os

class StudySite:
    def __init__(self, left, right, bottom, top):
        self.left = int(str(left)[:4])
        self.right = int(str(right)[:4])
        self.bottom = int(str(bottom)[:4])
        self.top = int(str(top)[:4])
        
        self.bounds = [left, right, bottom, top]
        self.crs = epsg_code
        
        links = np.genfromtxt('download_links.csv',dtype='<U500')
        filename = np.empty((links.shape[0]),dtype='<U100')
        tiles = np.empty((links.shape[0]),dtype='<U9')
        
        for i in range(links.shape[0]):
            fn = links[i].split('swisssurface3d_')[2]
            filename[i] = fn
    
            x = fn.split('_')[1].split('-')[0]
            y = fn.split('_')[1].split('-')[1]
            tiles[i] = x + '_' + y
        
        x_area = np.arange(self.left,self.right+1,1)
        y_area = np.arange(self.bottom,self.top+1,1)
        grid = np.meshgrid(x_area,y_area,indexing='ij')
        length = grid[0].shape[0] * grid[0].shape[1]
        
        comb = np.empty((length),dtype='<U9')
        for j in range(length):
            comb[j] = str(grid[0].reshape(length)[j]) + '_' + str(grid[1].reshape(length)[j])
        
        mask = np.in1d(tiles, comb)
        self.index = np.nonzero(mask)
        self.links = links[self.index]
        self.tiles = tiles[self.index]
        self.filename = filename[self.index]
    
    def download(self,path_to_download:str):
        for link, file in zip(self.links,self.filename):
            filepath = path_to_download + file
            urllib.request.urlretrieve (link, filepath)
            
    def unzip(self,path_of_zipfiles:str, path_to_unzip:str):
        zip_files = os.listdir(path_of_zipfiles)
        for file in zip_files:
            path = path_of_zipfiles + file
            with ZipFile(path, 'r') as zipObj:
                zipObj.extractall(path=path_to_unzip)