'''
    2019-Oct-10
    Jinwoo Park (pmnxis@gmail.com)
    https://github.com/pmnxis/RotatorPnp
    This was made for JLCPCB Assembly service for
    cheap prototyping own project.
    Enjoy it!

    This is my own PickAndPlace Modifier script.
    First . Rotate PnP from rulebook
    Second. Convert Kicad format to JLCPCB format.
'''

import csv
import sys
import os
import codecs
import re
    
def runner(__in, __rule, __out):
    fin = codecs.open(__in, 'rb', 'utf-8')
    ruf = codecs.open(__rule, 'r', 'utf-8')
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
    # '^( [^,]*, [^,]*, [^,]*, [^,]*, [^,]*,)(\d+)(.*$)'
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

        if('\n' not in new_line):
            new_line = new_line + '\n'
        fou.write(new_line)
    print(line_cnt, "of Lines in input file were parsed.")
    print(cnt, "of component are re-roated for assembly factory")
    fin.close()
    ruf.close()
    fou.close()

def argv_hello():
    print('Rotator-Kicad :: Please follow commands.\n')

def argv_error():
    print('Rotator-Kicad :: Wrong command!!\n')

def argv_instruction():
    print('Example - Quick (--default)')
    print('--default ./LambdaCoin-pos.csv')
    print('this will export result to ./LambdaCoin-pos-renew.csv that renew postfix.')
    print('')
    print('Example - Manual')
    print('./input.csv ./ruleBook.csv ./output.csv')
    print('')
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        argv_hello()
        argv_instruction()
        exit()
    elif len(sys.argv) <= 2 or len(sys.argv) >= 5:
        argv_error()
        argv_instruction()
        exit()
    elif (len(sys.argv) == 3 and not ('--default' in sys.argv[1])):
        argv_error()
        argv_instruction()
        exit()
    elif (len(sys.argv) == 4 and ('--default' in sys.argv[1])):
        argv_error()
        argv_instruction()
        exit()

    if(sys.argv[1] == '--default'):
        inpath = sys.argv[2]
        __tmp = os.path.splitext(inpath)
        tmpoutpath = __tmp[0] + '-tmp' + __tmp[-1]
        finaloutpath = __tmp[0] + '-renew' + __tmp[-1]
        print('Use Default rulebook - rule_example.csv')
        print('Store to ', finaloutpath)
        rulepath = './rule_example.csv'
    else:
        print('Use Custom rulebook')
        inpath = sys.argv[1]
        tmpoutpath = __tmp[0] + '-tmp' + __tmp[-1]
        __tmp = os.path.splitext(inpath)
        rulepath = sys.argv[2]
        finaloutpath = sys.argv[3]
    
    runner(inpath, rulepath, tmpoutpath)
    kuku = 'python3 ./kicad-jlcpcb-bom-plugin/kicad_pos_to_cpl.py' + ' ' + tmpoutpath + ' ' + finaloutpath
    os.system(kuku)
    os.remove(tmpoutpath)
