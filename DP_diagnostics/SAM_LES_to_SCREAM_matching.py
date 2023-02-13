#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thurs Feb 01 13:24:40 2023

@author: bogenschutz1
"""
# Define a function so that we can equate specific SAM LES variables
# with specific SCREAM variables

def makevarlist_profiles(varstoplot,lesvarstoplot):

    print("Getting matching SAM LES variables")

    numvars=len(varstoplot)

    for v in range(0,numvars):
        # Cloud fraction
        if (varstoplot[v] == "CLOUD"):
            lesvarstoplot.append("CLD")

        # Cloud liquid mixing ratio
        elif (varstoplot[v] == "CLDLIQ"):
            lesvarstoplot.append("QCL")

        # Cloud ice mixing ratio
        elif (varstoplot[v] == "CLDICE"):
            lesvarstoplot.append("QCI")

        # Liquid water potential temperature
        elif (varstoplot[v] == "THETAL"):
            lesvarstoplot.append("THETAL")

        # Total water mixing ratio
        elif (varstoplot[v] == "QT"):
            lesvarstoplot.append("QT")

        # Total water flux (total)
        elif (varstoplot[v] == "TOT_WQW"):
            lesvarstoplot.append("QTFLUX")

        # Total water flux (SGS)
        elif (varstoplot[v] == "WQW_SEC"):
            lesvarstoplot.append("QTOFLXS")

        # Thetal flux (total)
        elif (varstoplot[v] == "TOT_WTHL"):
            lesvarstoplot.append("TLFLUX")

        # Thetal flux (SGS)
        elif (varstoplot[v] == "WTHL_SEC"):
            lesvarstoplot.append("TLFLUXS")

        # Vertical velocity variance (total)
        elif (varstoplot[v] == "TOT_W2"):
            lesvarstoplot.append("W2")

        # Third moment vertical velocity (total)
        elif (varstoplot[v] == "TOT_W3"):
            lesvarstoplot.append("W3")

        # Eddy diffusivity (heat)
        elif (varstoplot[v] == "TKH"):
            lesvarstoplot.append("TKH")

        # Eddy diffusivity (momentum)
        elif (varstoplot[v] == "TK"):
            lesvarstoplot.append("TK")

        # Relative humidity
        elif (varstoplot[v] == "RELHUM"):
            lesvarstoplot.append("RELH")

        # Rain mixing ratio
        elif (varstoplot[v] == "RAINQM"):
            lesvarstoplot.append("QR")

        # Snow mixing ratio
        elif (varstoplot[v] == "SNOWQM"):
            lesvarstoplot.append("QPI")

        # Zonal wind
        elif (varstoplot[v] == "U"):
            lesvarstoplot.append("U")

        # Meridional wind
        elif (varstoplot[v] == "V"):
            lesvarstoplot.append("V")

        # Total cloud condensate
        elif (varstoplot[v] == "CLDLIQICE"):
            lesvarstoplot.append("QN")

        # Temperature variance
        elif (varstoplot[v] == "TOT_THL2"):
            lesvarstoplot.append("TL2")

        # Total water variance
        elif (varstoplot[v] == "TOT_QW2"):
            lesvarstoplot.append("QT2")

        # Do this if there is no matching LES variable
        else:
            lesvarstoplot.append("NONE")

    return lesvarstoplot
