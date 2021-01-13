# -*- coding: utf-8 -*-

import pandas as pd
import glob
import numpy as np
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from matplotlib import cm
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator

def readData(filename):
    '''
    Read the input file that contains data of the form:
    NUTS2 Value
    DE21 0.347
    Parameters
    ----------
    filename : string
        The name of the file that we need to read.

    Returns
    -------
    data : pandas DataFrame
        A DataFrame with two columns.
        First column is the NUTS2 regions.
        Second column is their respective values.
    '''
    data = pd.read_csv('average-triangles-common.txt', sep=' ')
    data.rename(columns={'NormTriangles':'Value'}, inplace=True) # To remove
    return data


def plot(data, filename):
    '''
    Plot the map with the NUTS2 regions colored according to their values

    Parameters
    ----------
    data : pandas DataFrame
    filename : string
        input data filename.

    Returns
    -------
    None. It saves the plot in .png format.

    '''
    
    # Read the file that contain the Polygons that will be used for the drawing of the NUTS2 regions
    # They are provided at: 
    # https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts
    df2021 = gpd.read_file('NUTS_RG_01M_2021_3857_LEVL_2.geojson')
    df2016 = gpd.read_file('NUTS_RG_01M_2016_3857_LEVL_2.geojson')
    countries = gpd.read_file('NUTS_RG_01M_2021_3857_LEVL_0.geojson')
    
    # Define the color boundaries that will be used for the colorbar.
    bounds = np.array([0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.25, 0.3, 0.35, 0.4,                   0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors=len(bounds)+1)
    
    # Define the colormar
    cmap = cm.get_cmap('rainbow', len(bounds)+1)
    
    # Figure of the map
    fig, ax = plt.subplots(figsize=(8,8))
    
    # Plot the NUTS2 regions with white background color and black lines as a background layer 
    df2016.plot(facecolor="none", edgecolor='black', lw=0.05, ax=ax, zorder=2)
    df2021.plot(facecolor="none", edgecolor='black', lw=0.05, ax=ax, zorder=2)
    
    # Plot the input data
    for index, row in data.iterrows():
        node = row['Node']
        val = row['Value']
        if val==0.0:
            # If the value is zero, leave it white
            continue       
        # Draw the NUTS2 region according to its value
        if len(df2021[ df2021['id']==node ]) > 0:
            patch = PolygonPatch(df2021[ df2021['id']==node].iloc[0]['geometry'], facecolor=cmap(norm(val)), edgecolor='white', lw=0.25)
            ax.add_patch(patch)
            continue
        elif len(df2016[ df2016['id']==node ]) > 0:
            patch = PolygonPatch(df2016[ df2016['id']==node].iloc[0]['geometry'], facecolor=cmap(norm(val)), edgecolor='white', lw=0.25, zorder=2)
            ax.add_patch(patch)
        
    ax.set_xlim([-2750000, 5000000])
    ax.set_ylim([4000000, 11500000])
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    # Draw countries on top, so that the countries borders are more clear
    countries.plot(facecolor="none", edgecolor='black', lw=0.5, ax=ax, zorder=3)
    plt.savefig('{}-plot.png'.format(filename), dpi=300, bbox_inches='tight')
    plt.close()


def main(filename):
    # Read data
    data = readData(filename)
    # Plot
    plot(data, filename)


if __name__ == "__main__":
    main(filename)




















