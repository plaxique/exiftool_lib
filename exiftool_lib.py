#! /cygdrive/c/anaconda3/python
import subprocess
import os
import pathlib
import IPython; debug_here=IPython.embed
import datetime

p = pathlib.Path(r"\\nas\photo\Sortiert\NiCa Anfang")
DATE_FORMAT = '%Y:%m:%d %H:%M:%S'
TIME_ATTRIBUTE = 'Date/Time Original'
TIME_ATTRIBUTE2 = 'File Modification Date/Time'
ERROR_EXIF_READ = 101
ERROR_TIME_READ = 102


def get_win_path(cyg_path):
    return subprocess.check_output(["cygpath", "-w", cyg_path]).strip(b"\n").decode()

p_exiftool2 = get_win_path('/cygdrive/c/Users/Asus ROG/bin/exiftool')
#p_exiftool2 = get_win_path(p_exiftool.absolute())

def get_exif_info(filename):
    '''
    returns exif info as dictionary
    '''

    try:
        exif_info_orig = subprocess.check_output([p_exiftool2, filename]).decode("utf-8").split('\r\n')
    except:
        print('FAIL')
        return ERROR_EXIF_READ

    # remove empty list elements
    exif_info = list(filter(None,exif_info_orig))

    exif_tags = [ele.split(": ")[0].strip() for ele in exif_info]
    exif_values = [ele.split(": ")[1].strip() for ele in exif_info]

    return dict(zip(exif_tags, exif_values))

def get_original_date_time(filename, time_attribute=TIME_ATTRIBUTE):
    '''
    returns a particular exif attribute. default is 'Date/Time Original'
    '''

    exif_info = get_exif_info(filename)

    if exif_info == ERROR_EXIF_READ:
        return ERROR_EXIF_READ

    if time_attribute not in exif_info.keys():
        return ERROR_TIME_READ

    return exif_info[time_attribute]

def string_to_datetime(date, given_format=DATE_FORMAT):
    return datetime.datetime.strptime(date, given_format)

exif_info = get_exif_info('P1110750.JPG')
orig_date = get_original_date_time('P1110750.JPG')
the_date = string_to_datetime(orig_date, DATE_FORMAT)

def get_files_in_dir(path):
    files_in_dir = [element for element in path.iterdir() if os.path.isfile(element)]
    dirs_in_dir = [element for element in path.iterdir() if os.path.isdir(element)]
    rest_in_dir = [element for element in path.iterdir() if element not in files_in_dir and element not in dirs_in_dir]

    return files_in_dir, dirs_in_dir, rest_in_dir

def beautify_filename(aFile, date):
    part_date = date.strftime('%Y_%m_%d_%H%M%S')
    filename = aFile.name[:-len(aFile.suffix)]

    file_description = [ele for ele in filename.split('__') if str(date.year) not in ele]
    print('... {} : {}'.format(aFile.name, file_description))


def get_nice_original_date_time(files):
    files_to_be_renamed = {}
    files_sorted_out = []

    for aFile in files:
        file_date_time = get_original_date_time(str(aFile))
        
        if file_date_time == ERROR_EXIF_READ:
            print('OHOH {}'.format(aFile))
            files_sorted_out.append(aFile)
        elif file_date_time == ERROR_TIME_READ:
            print('OHNOO {}'.format(aFile))            
            file_date_time = get_original_date_time(str(aFile), time_attribute=TIME_ATTRIBUTE2)
            if file_date_time == ERROR_TIME_READ:
                print('OHNOO2 {}'.format(aFile))                        
                files_sorted_out.append(aFile)
            else:
                beautify_filename(aFile, string_to_datetime(file_date_time[:file_date_time.find('+')]))
                files_to_be_renamed[aFile] = 'xxx'
        else:
            print("{}: {}".format(aFile.suffix, file_date_time))
            beautify_filename(aFile, string_to_datetime(file_date_time))
            files_to_be_renamed[aFile] = 'yyy'

    return files_to_be_renamed, files_sorted_out

files, dirs, rest = get_files_in_dir(p)
get_nice_original_date_time(files)
debug_here()


