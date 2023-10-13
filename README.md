
Authors: 
Palemkota Maithresh(m.palemkota@gmail.com)
and 
Lakshya Gupta (lakshcool100@gmail.com)


# This code finds all the Indian addresses in any HTML file

1) pdf file 'Algorithm description' describes all the steps followed to find the address and how much space was reduced in the process.

2) 'keywords_new' is a python notebook file that is used to create 'keywords_head', 'keywords_last' and 'keywords_add' files
   for header keywords, last keywords and additional keywords present in the address respectively.

3) 'cities' is a csv file that contains two columns, city and corresponding state.

NOTE: Identifying an address depends a lot on these keywords. For current code these keywords can identify indian addresses. By adding 
      keywords(in 'keywords_new.ipynb' and generating new 'keywords_add', 'k) and cities(in 'cities.csv') that are in your addresses, this code can be generalized to any
      region.

4) By executing 'process.py', all the HTML files in 'input' folder will be processed and hew HTML files containing addesses will be created in 'output' folder.
