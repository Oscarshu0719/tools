# -*- coding: utf-8 -*-
# @Author: Zi Jun, Xu.

import os
import sys


def CreateBatchFiles(argv):
    not_create_file = []
    create_file = []
    arg_list = argv[1:]

    print('------------------------------------------------------------')

    if len(arg_list) == 4:
        print('Format (1)')
        if arg_list[3][0] != '.':
            print('------------------------------'
                  '------------------------------')
            print('Error: The filename extension'
                  'must be started with a dot (.).')
            print('------------------------------'
                  '------------------------------')
            sys.exit(1)
        elif not (arg_list[1].isdigit() or arg_list[2].isdigit()):
            print('------------------------------'
                  '------------------------------')
            print('Error: <StartNo> or <EndNo> is NOT a number.')
            print('------------------------------'
                  '------------------------------')
            sys.exit(1)
        elif int(arg_list[1]) > int(arg_list[2]):
            print('------------------------------'
                  '------------------------------')
            print('Error: <StartNo> is larger than <EndNo>.')
            print('------------------------------'
                  '------------------------------')
            sys.exit(1)

        print('------------------------------------------------------------')
        print('Prefix: {}.'.format(arg_list[0]))
        print('StartNo: {}.'.format(arg_list[1]))
        print('EndNo: {}.'.format(arg_list[2]))
        print('FilenameExt: {}.'.format(arg_list[3]))
        print('--------------------------------------------------\n')

        for i in range(int(arg_list[1]), int(arg_list[2]) + 1):
            filename = arg_list[0] + str(i) + arg_list[3]
            if os.path.isfile(filename):
                print('Warning: The file {} exists.'.format(filename))
                not_create_file.append(filename)
                continue
            else:
                # Create the file.
                with open(filename, 'w') as file:
                    create_file.append(filename)
                    file.close()
    elif len(arg_list) == 3:
        if arg_list[2][0] == '.':
            print('Format (2)')
            if not (arg_list[0].isdigit() or arg_list[1].isdigit()):
                print('------------------------------'
                      '------------------------------')
                print('Error: <StartNo> or <EndNo> is NOT a number.')
                print('------------------------------'
                      '------------------------------')
                sys.exit(1)
            elif int(arg_list[0]) > int(arg_list[1]):
                print('------------------------------'
                      '------------------------------')
                print('Error: <StartNo> is larger than <EndNo>.')
                print('------------------------------'
                      '------------------------------')
                sys.exit(1)

            print('------------------------------'
                  '------------------------------')
            print('StartNo: {}.'.format(arg_list[0]))
            print('EndNo: {}.'.format(arg_list[1]))
            print('FilenameExt: {}.'.format(arg_list[2]))
            print('--------------------------------------------------\n')

            for i in range(int(arg_list[0]), int(arg_list[1]) + 1):
                filename = str(i) + arg_list[2]
                if os.path.isfile(filename):
                    print('Warning: The file {} exists.'.format(filename))
                    not_create_file.append(filename)
                    continue
                else:
                    # Create the file.
                    with open(filename, 'w') as file:
                        create_file.append(filename)
                        file.close()
        else:
            print('Format (3)')
            if not (arg_list[1].isdigit() or arg_list[2].isdigit()):
                print('------------------------------'
                      '------------------------------')
                print('Error: <StartNo> or <EndNo> is NOT a number.')
                print('------------------------------'
                      '------------------------------')
                sys.exit(1)
            elif int(arg_list[1]) > int(arg_list[2]):
                print('------------------------------'
                      '------------------------------')
                print('Error: <StartNo> is larger than <EndNo>.')
                print('------------------------------'
                      '------------------------------')
                sys.exit(1)

            print('------------------------------'
                  '------------------------------')
            print('Prefix: {}.'.format(arg_list[0]))
            print('StartNo: {}.'.format(arg_list[1]))
            print('EndNo: {}.'.format(arg_list[2]))
            print('--------------------------------------------------\n')

            for i in range(int(arg_list[1]), int(arg_list[2]) + 1):
                filename = arg_list[0] + str(i)
                if os.path.isfile(filename):
                    print('Warning: The file {} exists.'.format(filename))
                    not_create_file.append(filename)
                    continue
                else:
                    # Create the file.
                    with open(filename, 'w') as file:
                        create_file.append(filename)
                        file.close()
    else:
        print('Format (4)')
        if not (arg_list[0].isdigit() or arg_list[1].isdigit()):
            print('------------------------------'
                  '------------------------------')
            print('Error: <StartNo> or <EndNo> is NOT a number.')
            print('------------------------------'
                  '------------------------------')
            sys.exit(1)
        elif int(arg_list[0]) > int(arg_list[1]):
            print('------------------------------'
                  '------------------------------')
            print('Error: <StartNo> is larger than <EndNo>.')
            print('------------------------------'
                  '------------------------------')
            sys.exit(1)

        print('------------------------------------------------------------')
        print('StartNo: {}.'.format(arg_list[0]))
        print('EndNo: {}.'.format(arg_list[1]))
        print('------------------------------------------------------------\n')

        for i in range(int(arg_list[0]), int(arg_list[1]) + 1):
            filename = str(i)
            if os.path.isfile(filename):
                print('Warning: The file {} exists.'.format(filename))
                not_create_file.append(filename)
                continue
            else:
                # Create the file.
                with open(filename, 'w') as file:
                    create_file.append(filename)
                    file.close()

    return create_file, not_create_file


if __name__ == '__main__':
    print('------------------------------------------------------------')
    print('Format can be: ')
    print('------------------------------------------------------------')
    print('1. <Prefix> <StartNo> <EndNo> <FilenameExt>')
    print('2. <StartNo> <EndNo> <FilenameExt>')
    print('3. <Prefix> <StartNo> <EndNo>')
    print('4. <StartNo> <EndNo>')
    print('------------------------------------------------------------\n')

    if len(sys.argv) > 5 or len(sys.argv) < 3:
        print('------------------------------'
              '------------------------------')
        print('Error: The number of parameters is {}, and it\' wrong.'.format(
            len(sys.argv)))
        print('------------------------------'
              '------------------------------')
        sys.exit(1)
    else:
        created, not_created = CreateBatchFiles(sys.argv)

        print('\n--------------------------------------------------')
        if len(created) == 0:
            if len(not_created) > 1:
                print('The files below were NOT created: ')
            else:
                print('The file below was NOT created: ')
            print('------------------------------'
                  '------------------------------')
            for n in not_created:
                print(n)
            print('------------------------------'
                  '------------------------------')
            print('* None of the files was created.')
        elif len(not_created) == 0:
            if len(created) > 1:
                print('The files below were created: ')
            else:
                print('The file below was created: ')
            print('------------------------------'
                  '------------------------------')
            for c in created:
                print(c)
            print('------------------------------'
                  '------------------------------')
            print('* All the files were created.')
        else:
            if len(created) > 1:
                print('The files below were created: ')
            else:
                print('The file below was created: ')
            print('------------------------------'
                  '------------------------------')
            for c in created:
                print(c)
            print('------------------------------'
                  '------------------------------')
            if len(created) > 1:
                print('The files below were NOT created: ')
            else:
                print('The file below was NOT created: ')
            print('------------------------------'
                  '------------------------------')
            for n in not_created:
                print(n)
            print('------------------------------'
                  '------------------------------')
            if len(created) > 1:
                print('* {} files were created,'.format(len(created)),
                      end='\0')
            else:
                print('* Only 1 file was created,', end='\0')
            if len(not_created) > 1:
                print('and {} files were NOT created.'.
                      format(len(not_created)))
            else:
                print('and only 1 file was NOT created.')
        print('------------------------------------------------------------')
