# Address-Conversion
Unix-like command line utility that will convert between three different address types when an address of a different type is given
address4forensics -L|-P|-C [–b offset] [-B [-s bytes]] [-l address] [-p address]
			[-c address -k sectors -r sectors -t tables -f sectors]

	-h, --help				Show this help file

	-L, --logical				Calculate the logical address from either the cluster address or
						the physical address. Either –c or –p must be given.
	-P, --physical				Calculate the physical address from either the cluster address
						or the logical address. Either –c or –l must be given.
	-C, --cluster				Calculate the cluster address from either the logical address or
						the physical address. Either –l or –p must be given.
	-b offset, --partition-start=offset	This specifies the physical address (sector number) of the start
						of the partition, and defaults to 0 for ease in working with
						images of a single partition. The offset value will always
						translate into logical address 0.
	-B, --byte-address			Instead of returning sector values for the conversion, this
						returns the byte address of the calculated value, which is the
						number of sectors multiplied by the number of bytes per sector.
	-s bytes, --sector-size=bytes		When the –B option is used, this allows for a specification of
						bytes per sector other than the default 512. Has no affect on
						output without –B.
	-l address, --logical-known=address	This specifies the known logical address for calculating either
						a cluster address or a physical address. When used with the –L
						option, this simply returns the value given for address.
	-p address, --physical-known=address	This specifies the known physical address for calculating either
						a cluster address or a logical address. When used with the –P
						option, this simply returns the value given for address.
	-c address, --cluster-known=address	This specifies the known cluster address for calculating either
						a logical address or a physical address. When used with the –C
						option, this simply returns the value given for address. Note
						that options –k, -r, -t, and –f must be provided with this
						option.
	-k sectors, --cluster-size=sectors	This specifies the number of sectors per cluster.
	-r sectors, --reserved=sectors		This specifies the number of reserved sectors in the partition.
	-t tables, --fat-tables=tables		This specifies the number of FAT tables, which is usually 2.
	-f sectors, --fat-length=sectors	This specifies the length of each FAT table in sectors.
