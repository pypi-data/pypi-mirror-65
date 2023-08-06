import argparse
from avsim2D import avsim2D

def main():

    parser = argparse.ArgumentParser(description='Autonomous Vehicle Simulator 2D with CAN Drive-By-Wire\nAuthor : Raphaël LEBER')

    parser.add_argument('--no-CAN', dest='opt_no_CAN', default=False, help='no need to load a CAN bus')

    args = parser.parse_args()

    avs = avsim2D.AvSim2D( args.opt_no_CAN )
    avs.update()


if __name__ == "__main__":
    main()