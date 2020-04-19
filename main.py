import threading
import logging
import sys
import time
from course import Course

WAIT_TIME = 30
threads = []

def search(link, init, killSwitch):
    # print out completion when done
    logging.info(' Search: search with link ' + link)
    course = Course(link, init)
    try: 
        while not course.hasAvailableSeats():
            if killSwitch.isSet():
                break
            logging.info(' Search: course does not have available seats')
            time.sleep(WAIT_TIME)
    except Exception as e:
        logging.error(e)
        
    for thread in threads:
        if threading.get_ident() == thread[0].ident :
            threads.remove(thread)
    return

def remove(name):
    for thread in threads:
        if thread[1] == name:
            thread[2].set()
            thread[0].join()
            logging.info(' Remove: remove thread ' + thread[1])
            return
    logging.info(' Remove: thread ' + name + " doesn't exist" )
    return
    
def lists():
    for item in threads:
        print(item[1])

def isDuplicate(name):
    for item in threads:
        if item[1] == name:
            return True
    return False

def add(link, name, init):
    if isDuplicate(name):
        logging.error('Name already exists. Please pick a new name')
        return 
    killSwitch = threading.Event()
    thread = threading.Thread(target=search, args=(link, init, killSwitch), daemon=True)
    tup = (thread, name, killSwitch)
    threads.append(tup)
    thread.start()

def isValidCommand(command):
    if command == 'exit':
        return True
    elif command == 'help':
        return True
    elif command == 'add':
        return True
    elif command == 'list':
        return True
    elif command == 'rm':
        return True
    else:
        return False

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info(' Main: starting program')
    while(True):
        try: 
            stdin = input()
            
            array = stdin.split()
            command = array[0]

            if (not isValidCommand(command)):
                print('Invalid Command')
                continue

            if command == 'exit':
                logging.info(' Main: closing program')
                sys.exit()
            elif command == 'help':
                print("commands implemented: help, exit, add <link> <name> [intial number of seats], list, rm <name>, set <interval in seconds>")
                continue
            elif command == 'add':
                if (len(array) != 3 and len(array) != 4): 
                    logging.error('Usage: add <link> <name> [intial number of seats]')
                    continue
                logging.info(' Main: adding link to list')
                num_seats = None if len(array) == 3 else array[3]
                add(array[1], array[2], num_seats)
            elif command == 'list':
                logging.info(' Main: listing followed link')
                lists()
                continue
            elif command == 'rm':
                logging.info(' Main: removing link from list')
                if (len(array) != 2):
                    logging.error('Usage: rm <name>. use list to view existing searches')
                remove(array[1])
        except KeyboardInterrupt:
            logging.info(' Main: closing program')
            sys.exit()
    
if __name__ == '__main__' :
    main()
    pass