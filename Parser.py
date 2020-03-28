__author__ = "Dima Cherepovskyi"
__copyright__ = "Copyright 2020"
__credits__ = ["Dima Cherepovskyi"]
__license__ = "BY-SA"
__version__ = "1.0"
__maintainer__ = "Dima Cherepovskyi"
__email__ = "dcher013@uottawa.ca"
__status__ = "Production"

import re

def get_sorted_data(input_filename, num_samples=1):

    if num_samples<1:
        raise ValueError('num_samples cannot be less than 1')
    if num_samples>100:
        while(True):
            ans=input('Your num_samples looks too large. Continue?(Y/N):')
            if ans.lower()=="y":
                break
            elif ans.lower()=="n":
                return Null
            else:
                print("Please repeat")
    f=open(input_filename, 'r')
    lines = f.readlines()
    dic = {}#initialize the root dictionary
    dicbuffer = {}#initialize the buffer dictionary
    i=0
    for line in lines:
        #print("->",i," ",line)#debug
        i+=1
        
        if line.strip()=="":#skip empty lines
            continue
        
        time = "^[0-9]+\.[0-9]+\s"#pattern matching
        header = "(\s(TS>)?[A-Z0-9]{2}\s)"
        value = "\s[0-9]+\s"
        
        time_matches = re.finditer(time, line, re.MULTILINE)
        header_matches = re.finditer(header, line, re.MULTILINE)
        value_matches = re.finditer(value, line, re.MULTILINE)

        for matchNum, match in enumerate(time_matches):
            if (matchNum != 0):
                raise ValueError('Time duplicate matched!')
            else:
                the_time=match.group().strip()
                
        for matchNum, match in enumerate(header_matches):
            if (matchNum != 0):
                raise ValueError('Header duplicate matched!')
            else:
                the_header=match.group().strip().replace("TS>","")
                
        for matchNum, match in enumerate(value_matches):
            if (matchNum != 0):
                raise ValueError('Value duplicate matched!')
            else:
                the_value=match.group().strip()
        
        #print(the_time)#debug
        #print(the_header)
        #print(the_value)
        
        if the_header not in dicbuffer:
            dicbuffer[the_header]=[]
        dicbuffer[the_header].append(int(the_value))#put value into buffer

        if len(dicbuffer[the_header]) >= num_samples:#so length is always>=1
            if the_header not in dic:
                dic[the_header]=[]
            avg = round(sum(dicbuffer[the_header])/(len(dicbuffer[the_header])))#rounded mean value
            dic[the_header].append({"osTimeStamp":the_time, "value":avg})#pu value into dictionary
            dicbuffer[the_header]=[]
        #some points are omitted since sampling is incomple
    f.close()
    return dic
