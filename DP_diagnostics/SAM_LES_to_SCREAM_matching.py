#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thurs Feb 01 13:24:40 2023

@author: bogenschutz1
"""
# Define a function so that we can equate specific SAM LES variables
# with specific SCREAM variables

def makevarlist(varstoplot,lesvarstoplot):

    print("Getting matching SAM LES variables")

    numvars=len(varstoplot)

    for v in range(0,numvars):
        #################################################
        # BELOW VARIABLES ARE FOR PROFILES
        # Temperature
        if (varstoplot[v] == "T"):
            lesvarstoplot.append("TABS")

        # Cloud fraction
        elif (varstoplot[v] == "CLOUD"):
            lesvarstoplot.append("CLD")

        # Cloud fraction
        elif (varstoplot[v] == "TOT_CLOUD_FRAC"):
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

        # Water Vapor
        elif (varstoplot[v] == "Q"):
            lesvarstoplot.append("QV")

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

        #################################################
        # BELOW VARIABLES ARE FOR TIME SERIES

        # Total liquid water path
        elif (varstoplot[v] == "TGCLDLWP"):
            lesvarstoplot.append("CWP")

        # Total ice water path
        elif (varstoplot[v] == "TGCLDIWP"):
            lesvarstoplot.append("IWP")

        # Precipitable water
        elif (varstoplot[v] == "TMQ"):
            lesvarstoplot.append("PW")

        # Convective available potential energy
        elif (varstoplot[v] == "CAPE"):
            lesvarstoplot.append("CAPE")

        # Convective inhibition
        elif (varstoplot[v] == "CIN"):
            lesvarstoplot.append("CIN")

        # Integrated low cloud amount
        elif (varstoplot[v] == "CLDLOW"):
            lesvarstoplot.append("CLDLOW")

        # Integrated mid-level cloud amount
        elif (varstoplot[v] == "CLDMED"):
            lesvarstoplot.append("CLDMID")

        # Integrated high-level cloud amount
        elif (varstoplot[v] == "CLDHGH"):
            lesvarstoplot.append("CLDHI")

        # Solar insolation
        elif (varstoplot[v] == "SOLIN"):
            lesvarstoplot.append("SOLIN")

        # Surface precipitation rate
        elif (varstoplot[v] == "PRECL" or varstoplot[v] == "PRECT"):
            lesvarstoplot.append("PREC")

        # Net longwave flux at top of model
        elif (varstoplot[v] == "FLNT"):
            lesvarstoplot.append("LWNT")

        # Downwelling longwave flux at surface
        elif (varstoplot[v] == "FLDS"):
            lesvarstoplot.append("LWDS")

        # Clear sky net longwave flux at surface
        elif (varstoplot[v] == "FLNSC"):
            lesvarstoplot.append("LWNSC")

        # Net longwave flux at surface
        elif (varstoplot[v] == "FLNS"):
            lesvarstoplot.append("LWNS")

        # Donwelling solar flux at surface
        elif(varstoplot[v] == "FSDS"):
            lesvarstoplot.append("SWDS")

        # Net shortwave flux at surface
        elif (varstoplot[v] == "FSNS"):
            lesvarstoplot.append("SWNS")

        # Net shortwave flux at top of model
        elif(varstoplot[v] == "FSNT"):
            lesvarstoplot.append("SWNT")

        # Net shortwave flux at top of atmosphere
        elif(varstoplot[v] == "FSNTOA"):
            lesvarstoplot.append("SWNTOA")

        # Net clear sky net surface flux at surface
        elif(varstoplot[v] == "FSNSC"):
            lesvarstoplot.append("SWNSC")

        # Sensible surface heat flux
        elif(varstoplot[v] == "SHFLX"):
            lesvarstoplot.append("SHF")

        # Latent surface heat flux
        elif(varstoplot[v] == "LHFLX"):
            lesvarstoplot.append("LHF")

        #################################################
        # Do this if there is no matching LES variable
        else:
            lesvarstoplot.append("NONE")

    return lesvarstoplot
