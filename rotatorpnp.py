'''
    2019-Oct-10
    Jinwoo Park (pmnxis@gmail.com)
    https://github.com/pmnxis/RotatorPnp
    This was made for JLCPCB Assembly service for
    cheap prototyping own project.
    Enjoy it!

    This is my own Pick and Place's CSV header
    "Designator","Footprint","Center-X(mil)","Center-Y(mil)","Layer","Rotation","Supplier Part Number 1","Comment","Description"
    if your csv file is different with this stuff. you need to to change regex line
    Find comment "# Fix here if your csv file's rotation value is not in 6th col."

    !!! IMPORTANT THINGS !!!
    And Currently I didn't implemented about argument parsing.
    Need to fix "main()" yourself.
'''

import csv
import sys
import codecs
import re
import icu

def inteli_open(__path, opt='rb'):
    with open(__path, 'rb') as stuff:
        data = stuff.read()
    stuff.close()
    coding = icu.CharsetDetector(data).detect().getName()
    print(__path , ' - Encoding : ' , coding)
    stuff = codecs.open(__path, opt, encoding=coding)
    return stuff, coding
    
def runner(__in, __rule, __out):
    fin, i_code = inteli_open(__in, 'rb')
    ruf, r_code = inteli_open(__rule, 'r')
    fou = codecs.open(__out, 'w', 'utf-8')
    line_cnt = int(0)
    cnt = int(0)
    data = fin.read()
    data = data.encode().decode('utf-8')
    data = data.split("\n")
    rule_book = list(csv.reader(ruf))
    # Fix here if your csv file's rotation value is not in 6th col.
    # I will fix this later. But not now. I don't need auto detector for now.
    dog = re.compile('^([^,]*,[^,]*,[^,]*,[^,]*,[^,]*,)(\d+)(.*$)')
    for line in data:
        line_cnt += 1
        new_line = line
        for part_name in rule_book:
            if(line.find(part_name[0]) != -1):
                cnt += 1
                pig = dog.search(line)
                print('Rule book Detected !! - ', cnt,' Counted :: ', end='')
                print('old : ', line, end='\n')
                new_rot = int(pig.group(2)) + int(part_name[1])
                new_rot = new_rot % 360
                print(pig.group(2),' + ', part_name[1], ' = ', new_rot)
                new_line = pig.group(1)+str(new_rot)+pig.group(3)+str('\n')
                print('new : ', new_line, end='')
                print('-------------------')
                break
        fou.write(new_line)
    print(line_cnt, "of Lines in input file were parsed.")
    print(cnt, "of component are re-roated for assembly factory")
    fin.close()
    ruf.close()
    fou.close()

def main():
    runner('Sample_PnP.csv','rule_example.csv', 'test.csv')

if __name__ == "__main__":
    main()
