#!/usr/bin/env python
# coding: utf-8

# This is a notebook for reading the xml file of the InSight Event Catalog

# In[10]:


import csv
import requests
import xml.etree.ElementTree as ET


# In[11]:


ns = {"q":"http://quakeml.org/xmlns/quakeml/1.2",
       "d":"http://quakeml.org/xmlns/bed/1.2",
        "catalog":"http://anss.org/xmlns/catalog/0.1",
        "tensor":"http://anss.org/xmlns/tensor/0.1",
        "mars":"http://quakeml.org/xmlns/bed/1.2/mars"}

tree = ET.parse('events_extended_multiorigin_v6_2021-01-01.xml')
root = tree.getroot()
eventlist = root.findall('d:eventParameters',ns)


# In[12]:


for ep in eventlist:
        xevents = ep.findall('d:event',ns)
        print ("Found %d events." % (len(xevents)))


# In[13]:


import os
if os.path.exists("SeismicCatalog"):
  os.remove("SeismicCatalog")

file1 = open("SeismicCatalog","a")

print ('Name','Time','Distance','Quality','Type', sep='          ')

for e in range (0, len(xevents)):

    eventpar = xevents[e].findall('d:origin',ns)
    eventarr = eventpar[0].findall('d:arrival',ns)
    eventpha = eventarr[0].findall('d:phase',ns)
    eventmars = eventpar[0].findall('mars:distance',ns)
    if len(eventmars)>0:
        eventdist = eventmars[0].findall('mars:value', ns)
        eventdescr = xevents[e].findall('d:description',ns)
        check= eventdescr[0].findall('d:type',ns)
        checktxt=check[0].text
        if checktxt == 'earthquake name':
            eventname = eventdescr[0].findall('d:text',ns)
        else:
            eventname = eventdescr[1].findall('d:text',ns)
        eventqual = eventpar[0].findall('mars:locationQuality',ns)
        eventtype = xevents[e].findall('mars:type',ns)

        eventcre = eventpar[0].findall('d:time', ns)
        eventtime = eventcre[0].findall('d:value', ns)

        name = eventname[0].text
        etime = eventtime[0].text
        epdist = eventdist[0].text
        mtype = eventtype[0].text[53:72]
        mqual = eventqual[0].text[63:68]
        print (name, etime, epdist, mtype, mqual, sep=' ')

        line = [name,' ', etime,' ', epdist,' ', mqual,' ', mtype + '\n']

        file1.writelines(line)

file1.close()


# In[ ]:





# In[ ]:
