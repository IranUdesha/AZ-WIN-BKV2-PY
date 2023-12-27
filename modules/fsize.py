

import os

#Check File Size
def file_size(file_path):
    file_size = []
    file_stat = os.path.getsize(file_path)
    
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if file_stat < 1024.0:
            #print("%0.4f %s" % (file_stat, unit))
            file_size.append(file_stat)
            file_size.append(unit)
            break
        file_stat /= 1024.0
    return file_size
    
#print("%0.4f %s" % (file_size(html_template)[0],file_size(html_template)[1]))

