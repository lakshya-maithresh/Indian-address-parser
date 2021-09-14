
import re
import pandas as pd



#===================================================================== We define few functions here ================================================================================================   
# Removing unnecessary space and next line from data
def strip(data):
    data = data.strip('\n')
    data = "\n".join(data.split('\n'))
    data = " ".join(data.split())
    return data


###############################################################################################################################################################################################################################################################################3
# Identifying pincode and mobile number positions in the data

def pincode(data):   
       
    posi = []
    count = 0
    count_space = 0
    count_dash = 0
    for pos,char in enumerate(data):


        if char.isdigit() is True:                      
            count = count+1                               # count of digits
   
        elif ((char == ' ') )and count>0: 
            count_space = count_space +1                  # count of spaces between the digits
    
        elif char == '-' and count>=0:
            count_dash +=1                                # count for dashes between digits
        else:
    

            if count ==6 and count_dash ==0:              # general pincode pattern, also removes date format 
                count = 0
                posi.append(pos)
                count_space = 0
        

            elif count >6 and count<=12:                  # general structure for mobile number, telephone number and fax-number
        
                count = 0 
                posi.append(pos)
                count_space = 0
                count_dash = 0
            else:                                         # reset condition (does not get reset when file ends with digit or dash characters )
                count = 0
                count_space = 0
                count_dash = 0
    if count >= 6 and count <=12:                         
        count =0                                          # taking care of above reset condition
        posi.append(pos)
        count_space =0
        count_dash = 0
    return posi
#####################################################################################################################################################################################################################
# loading key words files 
def keywords_load():
    import pickle
    global keywords_head,keywords_add,keywords_last,states,cities,states
    cities         = pd.read_csv('cities.csv')                  
    kw_head_file   = open('keywords_head', "rb")
    kw_add_file    = open('keywords_add','rb')
    kw_last_file   = open('keywords_last','rb')
    #kw_states_file = open('states','rb')
    keywords_head  = pickle.load(kw_head_file)
    keywords_add   = pickle.load(kw_add_file)
    keywords_last  = pickle.load(kw_last_file)
    #states         = pickle.load(kw_states_file)
    kw_head_file.close()
    kw_add_file.close()
    kw_last_file.close()
    return
#################################################################################################################################################################################################
# Finding the position of keywords
def keywords_find(data,keywords,l='start'):

    df = pd.DataFrame(columns = ['key','pos'])  #create a dataframe that to save keyword and its position
    data = data.lower()

    for key in keywords: 
        posi=[getattr(m,l)() for m in re.finditer(key, data)]
        
        if posi != []:

            for positions in posi:
                
                df = df.append({'key':key,'pos':positions},ignore_index = True)
    return df
########################################################################################################################################################################################33
# function to determine whether a position existis whithin
def check_pos (range, ls):
# range is two tuple variable and ls is the list to determine whether it contains something within range
    is_present = False
    pos = -5000
    for posi,value in enumerate(ls):

        if value>= range[0] and value<= range[1]:
            pos = posi
            is_present = True
            break
            
    return (is_present,pos)
########################################################################################################################################################################################
# case when there is no pincode but identified other keywords
def no_pincode(data,left,right,ll):

    length = right -left 
    ranges = {}
    r_l = 200
    kw_add_pos  = ll[1]

    for i in range(left,right):
        count = 0
        right2  = min(i+r_l,right)
        
        for val in ll:
            a = check_pos((i,right2),val['pos'])
            if a[0] is True:
                count += 1  

        add_count = 0
        for pos in kw_add_pos['pos']: 
            if i<= pos and pos<= right2: 
                add_count = add_count +1
                
        
        if add_count >=2:
            count = count+add_count -1
                              
        if count>=3:
            ranges[i] = [i,i+r_l]

    return ranges
#################################################################################################################################################################################################
# finding the range of the string 
def range_find(data,pos,left,right):
    
    output = {}
    dt =  data[max(0,pos-left):min(pos+right,len(data))]     # making sure we don't overshoot or go negative in data index

    dt_kw_last =  keywords_find(dt,keywords_last, l='end')['pos']     # finding keywords_last position in selected data 

    if len(dt_kw_last) != 0 and (max(dt_kw_last)+max(0,pos-left))>= pos:
        right_max = max(0,pos-left) +max(dt_kw_last)           # finding rightmax position to take
        
    else:
        right_max = pos

    dt_kw_add = keywords_find(dt,keywords_add)['pos']        # finding additional keywords positions

    if  len(dt_kw_add) != 0:
        left_max =  max( max(0,pos -left) + min(dt_kw_add) -100,0)          
        left_pos = left_max 
        
    else:
        left_max = pos - 50
        left_pos = left_max
        
    dt_kw_head =  keywords_find(data[max(0,pos -left):right_max],keywords_head,l ='end')['pos']  # finding header keywords

    if  len(dt_kw_head) != 0:
        min_head = max(0,pos -left)  + max(dt_kw_head)
    
        if min_head <= pos:
            left_max = min_head 
    
    else:
        kw_comma = [m.start() for m in re.finditer(',', data[left_max:right_max])]
        if len(kw_comma) >= 2:
            comma_pos =  min(kw_comma)
            left_max =  max(max(0,pos -left)+ comma_pos -60,0)
    

    return [left_max,right_max]
#############################################################################################################################################################################################################################
# trim function
def trim(data,dic):
    parsed = ''
    right_max = 0 
    
    keys = list(dic.keys())
    keys.sort()
    for key in keys:
        r = dic[key]

        if r[1]> right_max:
            parsed = parsed + data[max(right_max,r[0]):r[1]]  # making sure no rewriting occurs
            right_max = r[1]

    return parsed
#########################################################################################################################################################################################################################################3
# function to select address from the file 
def parse(data):
    # First we identify the position of a potential address by pincode, state and city. If  two or more are present,
    # then we consider that a potential address
    left = 200
    right = 150 
    pin_pos = pincode(data)
    global ll 

    states_pos = keywords_find(data,cities['state'].unique())
    cities_pos = keywords_find(data,cities['city'])    
    kw_head_pos = keywords_find(data,keywords_head)
    kw_add_pos = keywords_find(data,keywords_add)
    kw_last_pos = keywords_find(data,keywords_last)
    ll = [kw_head_pos,kw_add_pos,kw_last_pos,cities_pos,states_pos]

    ranges = {}
    
    
    for pos in pin_pos:
    	count = 0
    	for posis in ll[:-1]:
    		if check_pos((max(0,pos-left),pos),posis['pos'])[0]:
    			count += 1
    	for posis in kw_add_pos['pos']:
    
    		if max(0,pos-left) <=posis <= pos:
    			count +=1
        #pass
    	for posis in kw_last_pos['pos']:
    
    		if pos <= posis <= pos+100:
        		count +=1
    
    	if count>=3:
    		ranges[pos] =  range_find(data,pos,left,right)
    	
    
    
                                                                
########################################## We are done with pincode at this point #############################################################################################################


################################################ Now we foucs on identifying addresses without pincode #####################################################################################



    if len(ranges) == 0:
        ranges =  no_pincode(data,0,len(data),ll)

    else:
        ranges2 = {}
        keys = list(ranges.keys())
        keys.sort()

        left_m = 0

        for idx,key in enumerate(keys):
    
            r = ranges[key]
    
            if r[0] > left_m:
        
                ranges2.update(no_pincode(data,left_m,r[0],ll))
        
            left_m = r[1]

        ranges2.update(no_pincode(data,left_m,ranges[keys[-1]][1],ll))

    return ranges

#========================================================================================== Defining functions is done ================================================================================


