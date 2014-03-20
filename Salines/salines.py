#!/usr/bin/python

#  salines.py
#  
#
#  Created by Theodore Lindsay on 10/2/09.
#  Copyright (c) 2009 University of Oregon. All rights reserved.
#
"""calculate recipe for a volume of saline given the desired concentrations"""

import quantities as pq #physical quatntites library
from struct import Struct #just import the Structure class into the module namespace
from sollib import * #import all names from sallib into the module namespace
pq.molar = pq.UnitQuantity('molar', pq.mol/pq.liter, symbol='M') #create a new physical quantity for concentration mol/liter


###external salines
class ext(Struct):
    class tets(Struct):
        mod2 = saline(name = 'ext.tets.mod2',volume = 0.200)
        mod2['NaCl'] = solute(concentration = 0.145,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        mod2['KCl'] = solute(concentration = 0.005,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        mod2['MgCl2'] = solute(concentration = 0.005,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        mod2['CaCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        mod2['HEPES'] = solute(concentration = 0.010,stock = 1.0, FW = 238.30,ions = ['HEPES'])
        
        highCa = saline(name = 'ext.tets.highCa',volume = 0.200)
        highCa['NaCl'] = solute(concentration = 0.143,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        highCa['KCl'] = solute(concentration = 0.005,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        highCa['CaCl2'] = solute(concentration = 0.008,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        highCa['HEPES'] = solute(concentration = 0.010,stock = 1.0, FW = 238.30,ions = ['HEPES'])
        highCa['Glucose'] = solute(concentration = 0.030,stock = 1.0, FW = 180.16,ions = ['Glucose'])
    
    class mk801(Struct):
        mod1 = saline(name = 'ext.mk801.mod1',volume = 0.010)
        mod1['NaCl'] = solute(concentration = 0.145,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        mod1['KCl'] = solute(concentration = 0.005,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        mod1['MgCl2'] = solute(concentration = 0.005,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        mod1['CaCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        mod1['HEPES'] = solute(concentration = 0.010,stock = 1.0, FW = 238.30,ions = ['HEPES'])
        mod1['MK801'] = solute(concentration = 0.000050,stock = 0.01, FW = 238.30,ions = ['MK801+','HM-'])
        
    class CNQX(Struct):
        mod1 = saline(name = 'ext.CNQX.mod1',volume = 0.01)
        mod1['NaCl'] = solute(concentration = 0.145,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        mod1['KCl'] = solute(concentration = 0.005,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        mod1['MgCl2'] = solute(concentration = 0.005,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        mod1['CaCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        mod1['HEPES'] = solute(concentration = 0.010,stock = 1.0, FW = 238.30,ions = ['HEPES'])
        mod1['CNQX'] = solute(concentration = 0.0002,stock = 0.01, FW = 276.12,ions = ['CNQX','Na+','Na+'],hydration = 0)

###internal salines
class internal(Struct):
    class buffCa(Struct):
        mod2 = saline(name = 'internal.bufCa.mod2',volume = 0.050)
        mod2['Kgluc'] = solute(concentration = 0.125,stock = 1.0, FW = 234.25, ions = ['K+','gluc-'])
        mod2['NaCl'] = solute(concentration = 0.004,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        mod2['KCl'] = solute(concentration = 0.018,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        mod2['MgCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        mod2['CaCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        mod2['HEPES'] = solute(concentration = 0.010,stock =  1.0, FW = 238.30,ions = ['HEPES'])
        mod2['EGTA'] = solute(concentration = 0.010,stock = 1.0, FW = 380.35,ions = ['EGTA'])

        cellsignals = saline(name = 'internal.buffCa.cellsignals',volume = 0.002)
        cellsignals['Kgluc'] = solute(concentration = 0.075,stock = 1.0, FW = 234.25, ions = ['K+','gluc-'])
        cellsignals['NaCl'] = solute(concentration = 0.001,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        cellsignals['KCl'] = solute(concentration = 0.018,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        cellsignals['MgCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        cellsignals['CaCl2'] = solute(concentration = 0.0006,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        
        cellsignals['KATP'] = solute(concentration = 0.005,stock = 0.01, FW = 619.39,ions = ['K+','K+','ATP--'])
        cellsignals['NaGTP'] = solute(concentration = 0.001,stock = 0.01, FW = 523.18,ions = ['Na+','Na+','GTP--'])
        cellsignals['cAMP'] = solute(concentration = 0.0005,stock = 0.01, FW = 369.20,ions = ['Na+','cAMP-'])
        cellsignals['cGMP'] = solute(concentration = 0.0005,stock = 0.01, FW = 367.19,ions = ['Na+','cGMP-'])
        
        cellsignals['HEPES'] = solute(concentration = 0.010,stock = 1.0, FW = 238.30,ions = ['HEPES',])
        cellsignals['BAPTA'] = solute(concentration = 0.005,stock = 1.0, FW = 628.8,ions = ['BAPTA','K+','K+','K+','K+'])
        cellsignals['EGTA'] = solute(concentration = 0.005,stock = 1.0, FW = 380.35,ions = ['EGTA--'])
        cellsignals['CrPO4'] = solute(concentration = 0.010,stock = 1.0, FW = 287.3,ions = ['Cre--','K+','K+'])
        cellsignals['Speram'] = solute(concentration = 0.010,stock = 1.0, FW = 202.34,ions = ['Spe'])
        
        lowCl = saline(name = 'internal.bufCa.lowCl',volume = 0.200)
        lowCl['Kgluc'] = solute(concentration = 0.143,stock = 1.0, FW = 234.25, ions = ['K+','gluc-'])
        lowCl['NaCl'] = solute(concentration = 0.004,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        lowCl['MgCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        lowCl['CaCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        lowCl['HEPES'] = solute(concentration = 0.010,stock =  1.0, FW = 238.30,ions = ['HEPES'])
        lowCl['EGTA'] = solute(concentration = 0.010,stock = 1.0, FW = 380.35,ions = ['EGTA'])

    class perfpatch(Struct):
        amp = saline(name = 'internal.perfpatch.amp',volume = 0.006)
        amp['Kgluc'] = solute(concentration = 0.125,stock = 1.0, FW = 234.25, ions = ['K+','gluc-'])
        amp['NaCl'] = solute(concentration = 0.004,stock = 2.0, FW = 58.44, ions = ['Na+','Cl-'])
        amp['KCl'] = solute(concentration = 0.018,stock = 1.0, FW = 74.55,ions = ['K+','Cl-'])
        amp['MgCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 95.21,ions = ['Mg++','Cl-','Cl-'])
        amp['CaCl2'] = solute(concentration = 0.001,stock = 1.0, FW = 110.98,ions = ['Ca++','Cl-','Cl-'])
        amp['HEPES'] = solute(concentration = 0.010,stock =  1.0, FW = 238.30,ions = ['HEPES'])
        amp['EGTA'] = solute(concentration = 0.010,stock = 1.0, FW = 380.35,ions = ['EGTA'])
        #Solubulized Amphotericin B, lot 118k4029. MW = 924.08 * 2.57 (lot potency correction factor)
        amp['AmpB'] = solute(concentration = 0.006,stock = 1.0, FW = 2374.88,ions = ['AmpB'])

    
def test():
    a = internal.buffCa.mod2
    print(str(a))
    b = internal.buffCa.cellsignals
    print(str(b))
    
if __name__ == '__main__':
    test()
        
