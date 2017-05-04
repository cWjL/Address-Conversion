#!/usr/bin/env python
'''
@author Jacob Loden

'''
import sys
import getopt

def main(argv):
	'''
        Entry main
		
        Get command line options and choose appropriate action
	
        @type argv, in , string
        @param address, partition start, cluster size, reserved sectors, fat tables, fat length 
        @rtype none
        @return none

	'''
        default_offset = 0
        sector_size = 512 #bytes
        logical_known = 0
        physical_known = 0
        cluster_known = 0
        cluster_size = 0
        reserved_sectors = 0
        fat_tables = 0
        fat_length = 0
        par_start = 0
        return_bytes = False
        logical_known = 0
        option = ''
        flags = []

        try:
                opts, args = getopt.getopt(argv, 'hLPCb:Bs:l:p:c:k:r:t:s:f:', ['help', 'logical', 'physical', 'cluster', 'partition-start=', 'sector-size=', 'logical-known=', 'physical-known=', 'cluster-known=', 'cluster-size=', 'reserved=', 'fat-tables=', 'fat-length='])
        except getopt.GetoptError, e:
                print e
                print_help()
                sys.exit(2)


        for opt, arg in opts:
                if opt in ("-h", "--help"):
                        print_help()
                        sys.exit(0)
                elif opt in ("-L", "--logical"):
                        option = "L"
                elif opt in ("-P", "--physical"):
                        option = "P"
                elif opt in ("-C", "--cluster"):
                        option = "C"
                elif opt in ("-b", "--partition-start"):
                        flags.append('b')
                        par_start = arg
                elif opt in ("-B", "--byte-address"):
                        return_bytes = True
                elif opt in ("-s", "--sector-size"):
                        flags.append("s")
                        sector_size = arg
                elif opt in ("-l", "--logical-known"):
                        flags.append("l")
                        logical_known = arg
                elif opt in ("-p", "--physical-known"):
                        flags.append("p")
                        physical_known = arg
                elif opt in ("-c", "--cluster-known"):
                        flags.append("c")
                        cluster_known = arg
                elif opt in ("-k", "--cluster-size"):
                        flags.append("k")
                        cluster_size = arg
                elif opt in ("-r", "--reserved"):
                        flags.append("r")
                        reserved_sectors = arg
                elif opt in ("-t", "--fat-tables"):
                        flags.append("t")
                        fat_tables = arg
                elif opt in ("-f", "--fat-length"):
                        flags.append("f")
                        fat_length = arg
                else:
                        print_help()
                        sys.exit(2)

        if option == "L":
                if "c" in flags:
                        if "k" in flags and "r" in flags and "t" in flags and "f" in flags:
                                calc_logical(return_bytes, sector_size, par_start, cluster_known, cluster_size, reserved_sectors, fat_tables, fat_length)
                        else:
                                print_help()
                                sys.exit(2)
                elif "p" in flags:
                        calc_logical(return_bytes, sector_size, physical_known, par_start, None, None, None, None)
                elif "l" in flags:
                        if return_bytes:
                                print int(logical_known)*int(sector_size)
                        else:
                                print logical_known
                        sys.exit(0)
                else:
                        print_help()
                        sys.exit(2)
        elif option == "P":
                if "c" in flags:
                        if "k" in flags and "r" in flags and "t" in flags and "f" in flags:
                                calc_physical(return_bytes, sector_size,  cluster_known, par_start, cluster_size, reserved_sectors, fat_tables, fat_length)
                        else:
                                print_help()
                                sys.exit(2)
                elif "l" in flags:
                        calc_physical(return_bytes, sector_size, logical_known, par_start, None, None, None, None)
                elif "p" in flags:
                        if return_bytes:
                                print int(physical_known)*int(sector_size)
                        else:
                                print physical_known
                        sys.exit(0)
                else:
                        print_help()
                        sys.exit(2)
        elif option == "C":
                if "c" in flags:
                        if return_bytes:
                                print int(cluster_known)*int(sector_size)
                        else:
                                print cluster_known
                        sys.exit(0)
                elif "l" in flags:
                        calc_cluster(return_bytes, sector_size, logical_known, cluster_known, cluster_size, reserved_sectors, fat_tables, fat_length)
                elif "p" in flags:
                        physical_known = int(physical_known)-int(par_start) # sub partition start (offset)
                        calc_cluster(return_bytes, sector_size, physical_known, cluster_known, cluster_size, reserved_sectors, fat_tables, fat_length)
                else:
                        print_help()
                        sys.exit(2)
        else:
                print_help()
                sys.exit(2)

def calc_logical(ret_bytes, sectors, addr, b_par_start, k_sector, r_sectors, t_tables, f_sectors):
    '''
    Convert to logical address using option and arguments passed from command line

    Only the address param is required, all others will be treated as None if not present
    
    @type logical address, int
    @param address, partition start (offset), cluster size, reserved sectors, fat tables, fat length 
    @rtype none
    @return none

    '''
    tmp = 0
    if k_sector is None and r_sectors is None and t_tables is None and f_sectors is None:
            tmp = int(addr) - int(b_par_start)
    else:
            tmp = ((int(b_par_start)+(int(addr)-2)*int(k_sector)+int(r_sectors)+(int(t_tables)*int(f_sectors))) - int(b_par_start))-int(b_par_start)

    if ret_bytes:
            tmp = int(tmp)*int(sectors)

    print tmp
    sys.exit(0)
                    

def calc_physical(ret_bytes, sectors, addr, b_par_start, k_sector, r_sectors, t_tables, f_sectors):
    '''
    Convert to physical address using option and arguments passed from command line

    Only the address and offset params are required, all others will be treated as None if not present
    
    @type logical address, int
    @param address, partition start (offset), cluster size, reserved sectors, fat tables, fat length 
    @rtype none
    @return none

    '''
    tmp = 0
    if k_sector is None and r_sector in None and t_tables is None and f_sectors is None:
            tmp = int(addr)+int(b_par_start)
    else:
            tmp = (int(b_par_start)+(int(addr)-2)*int(k_sector)+int(r_sectors)+(int(t_tables)*int(f_sectors)))

    if ret_bytes:
            tmp = int(tmp)*int(sectors)

    print tmp
    sys.exit(0)
    
def calc_cluster(ret_bytes, sectors, addr, k_sector, r_sectors, t_tables, f_sectors):
    '''
    Convert to cluster address using option and arguments passed from command line

    Address, cluster size, reserved sectors, fat tables, and fat length params are required.
    
    @type logical address, int
    @param address, cluster size, reserved sectors, fat tables, fat length 
    @rtype none
    @return none

    '''
    tmp = 0
    if int(k_sectors) != 0:
            tmp = ((int(addr)-int(r_sector)-(int(t_tables)*int(f_sectors)))/int(k_sectors))+2
    else:
            print_help()
            sys.exit(2)
		
    if ret_bytes:
            tmp = int(tmp)*int(sectors)

    print tmp
    sys.exit(0)

def print_help():
    f = open("help.txt", "r")
    print f.read()
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
