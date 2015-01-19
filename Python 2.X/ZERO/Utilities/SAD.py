import os

def main():
    try:
        while True:
            while True:
                mode = raw_input('Mode: ')
                if mode == 'search':
                    mode = False
                    break
                elif mode == 'destroy':
                    mode = True
                    break
                print '"search" or "destroy"'
            path = raw_input('Path: ')
            extention = raw_input('Extention: ')
            for path_name in search(path, extention, mode):
                print '\t', path_name
    except:
        pass

def search(path, extention, destroy):
    assert os.path.isdir(path)
    path_list = list()
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        try:
            if os.path.isdir(path_name):
                path_list += search(path_name, extention, destroy)
            elif os.path.isfile(path_name):
                if len(extention) == 0 or path_name[-len(extention):] == extention:
                    if destroy:
                        os.remove(path_name)
                    else:
                        path_list.append(path_name)
        except:
            print '\t', 'ERROR:', path_name
    return path_list

if __name__ == '__main__':
    main()
