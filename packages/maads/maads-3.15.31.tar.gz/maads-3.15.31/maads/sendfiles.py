#############################################################
#
#  Author: Sebastian Maurice, PhD
#  Copyright by Sebastian Maurice 2018
#  All rights reserved.
#  Email: Sebastian.maurice@otics.ca
#
#############################################################

import json, urllib
import requests
import csv
import os
import imp
import re
import urllib.request
import asyncio
import validators
from urllib.parse import urljoin
from urllib.parse import urlsplit



def formaturl(maindata,host,microserviceid,prehost,port):

    if len(microserviceid)>0:    
      mainurl=prehost + "://" + host +  ":" + str(port) +"/" + microserviceid + "/?hyperpredict=" + maindata
    else:
      mainurl=prehost + "://" + host + ":" + str(port) +"/?hyperpredict=" + maindata
        
    return mainurl
    
async def tcp_echo_client(message, loop,host,port,usereverseproxy,microserviceid):

    hostarr=host.split(":")
    hbuf=hostarr[0]
   # print(hbuf)
    hbuf=hbuf.lower()
    domain=''
    if hbuf=='https':
       domain=host[8:]
    else:
       domain=host[7:]
    host=domain  

    if usereverseproxy:
        geturl=formaturl(message,host,microserviceid,hbuf,port) #host contains http:// or https://
        message="GET %s\n\n" % geturl 

    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    try:
      mystr=str.encode(message)
      writer.write(mystr)
      datam=''
      while True:
        data = await reader.read(1024)
      #  print(data)
        datam=datam+data.decode("utf-8")
       # print(datam)
        if not data:
           break
        
        await writer.drain()
   #   print(datam)  
      prediction=("%s" % (datam))
      writer.close()
    except Exception as e:
      print(e)
      return e
    
    return prediction

def hyperpredictions(maadstoken,pkey,theinputdata,host,port,usereverseproxy=0,microserviceid='',username='',password='',company='',email=''):
    if '_nlpclassify' not in pkey:
      theinputdata=theinputdata.replace(",",":")
    else:  
      buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', theinputdata)
      buf2=buf2.replace("\n", "").strip()
      buf2=buf2.replace("\r", "").strip()
      theinputdata=buf2

    if usereverseproxy:
       theinputdata=urllib.parse.quote(theinputdata)
  
    value="%s,[%s],%s" % (pkey,theinputdata,maadstoken)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_client(value, loop,host,port,usereverseproxy,microserviceid))
    return val

def returndata(buffer,label):
      #print("LABEL: %s" % (label))
    try:
      if label=='PKEY:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='ALGO0:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY0:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON0:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         

      elif label=='ALGO1:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY1:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON1:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         
      elif label=='ALGO2:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY2:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON2:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         
      elif label=='ALGO3:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY3:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON3:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         
         
      elif label=='DATA:':
         val=""
         pattern = re.compile('\s*[:,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         fdate=listvalues[1]
         inp=listvalues[2]
         pred=float(listvalues[3])
         acc=float(listvalues[4])
         rval=[fdate,inp,pred,acc]
      else:
         return "%s not found" % (label)
    except Exception as e:
        return "ERROR retrieving label data: %s" % e
    return rval

def retraining(maadstoken,pkey,thefile,autofeature,removeoutliers,hasseasonality,dependentvariable,url,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy,username='',passw='',company='',email=''):

   rn=0
   tstr=''
   
   with open(thefile, 'r') as f:
     reader = csv.reader(f)
     for row in reader:
       row = ",".join(row)
       tstr = tstr + str(row) + '\n'
       rn=rn+1
       
   head, fname = os.path.split(thefile)
   print("Please wait...training can take several minutes.")
   
   files = {'file': tstr,
    'mode':-1,        
    'type':'CSV',
    'filename':fname,
    'username': username,
    'password': passw,
    'rowcount': rn,
    'autofeature': autofeature,
    'removeoutliers': removeoutliers,
    'hasseasonality': hasseasonality,
    'company': company,
    'email': email,            
    'dependentvariable': dependentvariable,
    'title':'File Upload for Training',
    'summer':summer,
    'winter':winter,
    'shoulder':shoulder,
    'trainingpercentage':trainingpercentage,
    'retrainingdays':retrainingdays,
    'retraindeploy':retraindeploy,
    'maadstoken':maadstoken,        
    'pkey':pkey
            
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def uploadcsvfortraining(maadstoken,thefile,autofeature,removeoutliers,hasseasonality,dependentvariable,url,throttle,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy,shuffle,theserverlocalname,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   if len(thefile)>0:
       with open(thefile, 'r',encoding='utf-8') as f:
         reader = csv.reader(f)
         for row in reader:
           row = ",".join(row)
           tstr = tstr + str(row) + '\n'
           rn=rn+1
       head, fname = os.path.split(thefile)    
   elif len(theserverlocalname)>0:
       tstr=''
       fname=theserverlocalname
   else:
       return "ERROR: Must specify a local file, or a file in the server."
       
   
   print("Please wait...training can take several minutes.")
   
   files = {'file': tstr,
    'mode':0,        
    'type':'CSV',
    'filename':fname,
    'username': username,
    'password': passw,
    'rowcount': rn,
    'autofeature': autofeature,
    'removeoutliers': removeoutliers,
    'hasseasonality': hasseasonality,
    'company': company,
    'email': email,            
    'dependentvariable': dependentvariable,
    'title':'File Upload for Training',
    'summer':summer,
    'winter':winter,
    'shoulder':shoulder,
    'trainingpercentage':trainingpercentage,
    'retrainingdays':retrainingdays,
    'retraindeploy':retraindeploy,
    'shuffle':shuffle,
    'throttle':throttle,
    'maadstoken':maadstoken        
            
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def getpredictions(maadstoken,attr,pkey,thefile,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   if attr==0:
      tstr=thefile
         
      files = {'file': tstr,
        'mode':1,        
        'type':'CSV',
        'pkey':pkey,            
        'username': username,
        'password': passw,
    #'rowcount': rn,
    #'autofeature': autofeature,
    #'removeoutliers': removeoutliers,
    #'hasseasonality': hasseasonality,
       'company': company,
       'email': email,
       'maadstoken':maadstoken,        
    #'dependentvariable': dependentvariable,
       'title':'Do Predictions'
      }

   #print(files)
      r = requests.post(url, files)
      msg = r.text
   #print ("Message %s" % (msg))
   
      return msg


def dolistkeys(maadstoken,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   files = {
      'mode':2,        
      'type':'CSV',        
      'username': username,
      'password': passw,
      'company': company,
      'email': email,
      'maadstoken':maadstoken,
     'title':'Do List keys'
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def dolistkeyswithkey(maadstoken,pkey,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   files = {
      'mode':3,
      'pkey':pkey,        
      'type':'CSV',        
      'username': username,
      'password': passw,
      'company': company,
      'email': email,
      'maadstoken':maadstoken,
     'title':'Do List keys with Key'
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def dodeletewithkey(maadstoken,pkey,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   files = {
      'mode':4,
      'pkey':pkey,        
      'type':'CSV',        
      'username': username,
      'password': passw,
      'company': company,
      'email': email,
      'maadstoken':maadstoken,
     'title':'Do Delete with Key'
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg



def getpicklezip(maadstoken,pkey,url,localfolder,username='',passw='',company='',email=''):

    url = "%s/prodfiles/%s_DEPLOYTOPROD.zip" % (url,pkey)
    localname="%s/%s_DEPLOYTOPROD.zip" % (localfolder,pkey)
    try:
      urllib.request.urlretrieve(url, localname)
    except Exception as e:
      return "ERROR: %s" % e  
    #print(url)
    return "File retrieved: %s FROM %s" % (localname,url)


def sendpicklezip(maadstoken,pkey,url,localname,username='',passw='',company='',email=''):
    bn=os.path.basename(localname)
    data = {'mode':'uploads', 'username':username, 'password':passw,'company':company,'email':email,'pkey':pkey,'maadstoken':maadstoken}
    
    files = {'file': open(localname, 'rb')}
    try:
      r = requests.post(url, data=data, files=files)
    except Exception as e:
      return "ERROR: %s" % e  
    return "File Sent: %s TO %s" % (localname,url)
    
def deploytoprod(maadstoken,pkey,url,localname='',ftpserver='',ftpuser='',ftppass='',username='',passw='',company='',email=''):

    data = {'mode':'deploy', 'username':username, 'password':passw,'company':company,'email':email,'localname':localname,'pkey':pkey,'maadstoken':maadstoken,'ftpserver':ftpserver,'ftpuser':ftpuser,'ftppass':ftppass}

    #print(prodserverurl)
    bn=''

    try: 
        if len(localname)>0:
            bn=os.path.basename(localname)
            data = {'mode':'deploy', 'username':username, 'password':passw,'company':company,'email':email,'localname':bn,'maadstoken':maadstoken,'pkey':pkey,'ftpserver':ftpserver,'ftpuser':ftpuser,'ftppass':ftppass}        
            files = {'file': open(localname, 'rb')}
            r = requests.post(url, data=data, files=files)
        else:
            bn="%s_DEPLOYTOPROD.zip" % (pkey)
            data = {'mode':'deploy', 'username':username, 'password':passw,'company':company,'email':email,'localname':localname,'maadstoken':maadstoken,'pkey':pkey,'ftpserver':ftpserver,'ftpuser':ftpuser,'ftppass':ftppass}                
            r = requests.post(url, data=data)
    except Exception as e:
      return "ERROR: %s" % e  
    return "File Deployed: %s TO %s" % (bn,url)
#    return r.text

def nlp(maadstoken,url,buffer,theserverfolder='',detail=20,maxkeywords=10,username='',passw='',company='',email=''):
    isurl=0
    print("Please wait..this could take several minutes")
    if len(buffer)>0:
        if validators.url(buffer):
            isurl=1
        else:
            isurl=0
        try:    
            if os.path.isfile(buffer):  #pdf
                filename, file_extension = os.path.splitext(buffer)
                flower=file_extension.lower()
                bn=os.path.basename(buffer)
                if flower=='.pdf':         
                   files = {'file': open(buffer, 'rb')}
                elif flower=='.txt':
                   files = {'file': open(buffer, 'r')}               
                data = {'mode':'nlp1', 'username':username, 'password':passw,'company':company,'email':email,'localname':bn,'maadstoken':maadstoken,'theserverfolder':theserverfolder,'fvalue': detail,'maxkeywords': maxkeywords}
                r = requests.post(url, data=data, files=files)
            elif isurl==1:  #url
                data = {'mode':'nlp2', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'fvalue': detail,'maxkeywords': maxkeywords}
                r = requests.post(url, data=data)
            else: #paste text
                data = {'mode':'nlp3', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'fvalue': detail,'maxkeywords': maxkeywords}
                r = requests.post(url, data=data)
        except Exception as e:
            try:
              data = {'mode':'nlp3', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'fvalue': detail,'maxkeywords': maxkeywords}
              r = requests.post(url, data=data)
            except Exception as e:
              return r.text
    elif len(theserverfolder)>0:
           data = {'mode':'nlp1', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'theserverfolder':theserverfolder,'fvalue': detail,'maxkeywords': maxkeywords}
           r = requests.post(url, data=data)
        
    return r.text

def nlpaudiovideo(maadstoken,maads_rest_url,thefile='',theserverfolder='',duration=-1,offset=0,username='',passw='',company='',email=''):   
    print("Please wait..this could take several minutes")
    if len(thefile)>0:
      files = {'file': open(thefile, 'rb')}
      data = {'mode':'nlpaudiovideo', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder,'duration':duration,'offset':offset}
      r = requests.post(maads_rest_url, data=data, files=files)
    elif len(theserverfolder)>0:
      data = {'mode':'nlpaudiovideo', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder,'duration':duration,'offset':offset}
      r = requests.post(maads_rest_url, data=data)
    else:
        return "ERROR: Please choose a file or server folder"
    return r.text

def nlpocr(maadstoken,maads_rest_url,thefile='',theserverfolder='',username='',passw='',company='',email=''):
    print("Please wait..this could take several minutes")
    if len(thefile)>0:
      files = {'file': open(thefile, 'rb')}
      data = {'mode':'nlpocr', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder}
      r = requests.post(maads_rest_url, data=data, files=files)
    elif len(theserverfolder)>0:
      data = {'mode':'nlpocr', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder}
      r = requests.post(maads_rest_url, data=data)
    else:
        return "ERROR: Please choose a file or server folder"
    return r.text
    
#csvfile,iscategory,maads_rest_url,trainingpercentage,retrainingdays,retraindeploy
def nlpclassify(maadstoken,iscategory,maads_rest_url,thefile='',theserverlocalname='',throttle=-1,csvonly=0,username='',trainingpercentage=75,retrainingdays=0,retraindeploy=0,passw='',company='',email=''):
    print("Please wait..this could take several minutes")
    tstr=''
    rn=0
    if len(thefile)>0:
        with open(thefile, 'r', encoding='utf8') as f:
         reader = csv.reader(f)
         for row in reader:
           #print(row)  
           rowstr = ",".join(row)
          # print(len(row))
           if len(row)>2:
               print("Ignored ROW %d: Improperly formatted CSV.  You have too many commas separating your data." % (rn+1))
           elif len(row)==2 and len(row[0])>1 and len(row[1])>1:
               buf=row[1]
               buf=buf.replace(","," ")
               buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', buf)
               buf2=buf2.replace("\n", "").strip()
               buf2=buf2.replace("\r", "").strip()
               row[1]=buf2

               buf=row[0]
               buf=buf.replace(","," ")
               buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', buf)
               buf2=buf2.replace("\n", "").strip()
               buf2=buf2.replace("\r", "").strip()

               row[0]=buf2
               rowstr = ",".join(row)
               tstr = tstr + str(rowstr) + '\n'
           else:
               print("Ignored ROW %d: Improperly formatted CSV." % (rn+1))
           rn=rn+1
        base=os.path.basename(thefile)
        filename=os.path.splitext(base)[0]
    elif len(theserverlocalname)>0:
        tstr=''
        filename=theserverlocalname
    else:
        return "ERROR: Must specify a local file, or a file in the server"
        
    files = {'file': tstr,
        'mode':'nlpclassify',        
        'type':'CSV',
        'iscategory':iscategory,            
        'username': username,
        'password': passw,
        'trainingpercentage': trainingpercentage,
        'retrainingdays': retrainingdays,
        'retraindeploy': retraindeploy,
        'company': company,
        'email': email,
        'filename':filename,
        'csvonly':csvonly,
        'throttle':throttle,
        'maadstoken':maadstoken,     
    #'dependentvariable': dependentvariable,
        'title':'Do NLP Classify'
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text

    if csvonly==1:
      localname=username + '_' + filename + '_nlpclassify_' + str(iscategory) + '_.csv'
      baseurl=urljoin(maads_rest_url,'/')
      url = "%smaadsweb/csvtemps/%s" % (baseurl,localname)
      #localname="%s" % (localname)
      try:
        urllib.request.urlretrieve(url, localname)
        return msg
      except Exception as e:
        return "ERROR retrieving NLP CSV: %s" % e

    return msg

def genpdf(maadstoken,maads_rest_url,pkey,urltomaadsserver,savetofolder,username='',passw='',company='',email=''):
    files = {'mode':'genpdf',        
        'username': username,
        'password': passw,
        'company': company,
        'email': email,
        'maadstoken':maadstoken,     
        'pkey':pkey     
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text
# retrieve file
    try:
      url = "%s/maadsweb/pdfreports/%s.pdf" % (urltomaadsserver,pkey)
      localname="%s/%s.pdf" % (savetofolder,pkey)
      urllib.request.urlretrieve(url, localname)
      return "PDF retrieved: %s" % localname
    except Exception as e:  
      return "ERROR: Retrieving PDF: %s" % e 

def algoinfo(maadstoken,maads_rest_url,pkey,isrest=0,username='',passw='',company='',email=''):
    files = {'mode':'algoinfo',        
        'username': username,
        'password': passw,
        'company': company,
        'email': email,
        'maadstoken':maadstoken,     
        'pkey':pkey,
        'isrest':isrest     
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text
   
    return msg

def nlpgeosentiment(maadstoken,maads_rest_url,lat,long,radius,searchterms,numtweets=50,wordcount=300,username='',passw='',company='',email=''):

    if len(searchterms)>0:
        searchterms=searchterms.replace(","," ")
        files = {'mode':'nlpgeosentiment',        
            'lat': lat,
            'long': long,
            'radius': radius,
            'searchterms': searchterms,
            'numtweets': numtweets,
            'wordcount': wordcount,             
            'maadstoken':maadstoken
          }

        r = requests.post(maads_rest_url, files)
        msg = r.text
    else:
       return "ERROR: Enter search terms" 
   
    return msg

def featureselectionjson(maadstoken,maads_rest_url,pkey,username='',passw='',company='',email=''):
    files = {'mode':'featureselection',        
        'username': username,
        'password': passw,
        'company': company,
        'email': email,
        'maadstoken':maadstoken,     
        'pkey':pkey     
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text
   
    return msg
    
#getpicklezip('demouser','demouser0828','OTICS','sebastian.maurice@otics.ml','demouser_acnstocksdatatest_csv','http://www.otics.ca/maadsweb','c:/maads')
