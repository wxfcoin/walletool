import argparse
from walletool.wallet_files import read_wallet_dat
from walletool.wallet_items import parse_wallet_dict, KeyWalletItem, CKeyWalletItem
from walletool.consts import addrtypes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dat', help='wallet.dat path', required=True, dest='filename')
    ap.add_argument('-v', '--version', help='address version, as integer, 0xHEX, or any of the following known coins:\n[%s]' % ', '.join(sorted(addrtypes)), required=True)
    args = ap.parse_args()
    if args.version.startswith('0x'):
        version = int(args.version[2:], 16)
    elif args.version.isdigit():
        version = int(args.version)
    else:
        if args.version not in addrtypes:
            raise ValueError('invalid version (see --help)')
        version = addrtypes[args.version]
    w_data = read_wallet_dat(args.filename)
    #for a in w_data:
    #	print(a,',  ',w_data[a])
    addr_tuples = []
    for item in parse_wallet_dict(w_data):
        #print(item)
        if isinstance(item, KeyWalletItem):
            print(item)
            address = item.get_address(version=version)
            privkey = item.get_private_key(version=version)
            addr_tuples.append((address, privkey))
        elif isinstance(item, CKeyWalletItem):
            print(item)
            
    for address, privkey in addr_tuples:
        print(address, privkey)


if __name__ == '__main__':
    main()
