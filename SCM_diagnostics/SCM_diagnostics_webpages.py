#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:54:25 2017

@author: bogenschutz1
"""

import os
import SCM_diagnostics_functions
from shutil import copyfile, move
    
# Generate the main web page
def main_web(casename,casedir):
    
    replacements={'CASENAME_here':casename}
    SCM_diagnostics_functions.replace_string("SCM_diagnostics_template.html","SCM_diagnostics.html",\
                                             replacements)
                
    move("SCM_diagnostics.html",casedir+"/SCM_diagnostics.html")           

# Generate the webpage for the output files
def sets_web(casename,casedir,varstoplot,setnum,setname,width,height):
    
    # Replace relevant headers in the webpages
    replacements={'CASENAME_here':casename, 'SETNAME_here':setname}
    SCM_diagnostics_functions.replace_string("set_template.htm","set_working.htm",\
                                             replacements)

    with open("set_working.htm","r") as in_file:
        buf = in_file.readlines()
        
    with open("set_working.htm","w") as out_file:
        for line in buf:
            if line == "<TABLE>\n":
                for v in range(0,len(varstoplot)):
                    thevar=varstoplot[v]
                    line = line + '\n<img src="'+setnum+'/'+thevar+\
                    '.png" style="width:'+width+'px;height:'+height+'px;">'                
    
            out_file.write(line)
            
    move("set_working.htm",casedir+"/"+setnum+".htm")

