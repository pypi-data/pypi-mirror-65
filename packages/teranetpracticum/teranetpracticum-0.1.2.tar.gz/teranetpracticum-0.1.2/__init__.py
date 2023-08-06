from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.statespace.varmax import VARMAXResults

def national():
    print('nationalll2')
    return VARMAXResults.load('Nationa_log_Stationary_Order_1_1.pkl')
    
 

def bc():
    print('bc_provincialll')