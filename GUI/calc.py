import math
def calcFlowRate(tau):
    '''
    Calculate the flow rate given shear stress value tau.    
    '''
    h = 0.0005
    w = 0.05
    nu = 0.0006922 

    # Calculate flow rate from given shear stress units: m^3 / s
    Q = (w * (h ** 2) * tau) / (6 * nu)

    Q = Q * 6 * 10 ** 7 # adjust to ml / min

    return Q

def main():
    values = [0.15, 0.23, 0.31, 0.49, 0.54, 0.70, 1.0, 1.5, 2.0]
    
    for v in values:
        flow = calcFlowRate(v)
        print("Shear Stress: {} mPa, Flow Rate: {:.2f} ml/min".format(v, flow))
   
if __name__ == '__main__':
    main()
