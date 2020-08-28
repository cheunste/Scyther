import unittest
import main
import re


class test_varexp_reader(unittest.TestCase):

	test_line = "ACM,12328913,DESER,AVC,ConsigTensFueraRango,,,,,Voltage set point out of range,Voltage set point out of range,DESER,AVC,,,,I,0,0,0,0,0,0,0,0,0,0,,,,,,,,,,,,,Generica,1,1,HI,0,4,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
	test_dict = {'DESER.T081.XSWI1.FuStBit2': 'CMD,12311166,DESER,T081,XSWI1,FuStBit2,,,,PLC Fuse State bit2,PLC Fuse State bit2,DESER,T081,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,0,0,HI,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,T22,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T081.XSWI1.Opn': 'CMD,12311167,DESER,T081,XSWI1,Opn,,,,1AS - Open circuit breaker,1AS - Open circuit breaker,DESER,T081,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,0,0,HI,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,T22,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T081.XSWI1.PosCls': 'CMD,12311168,DESER,T081,XSWI1,PosCls,,,,1AS - Circuit breaker closed,1AS - Circuit breaker closed,DESER,T081,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,0,0,HI,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,T22,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T081.XSWI1.PosOpn': 'CMD,12311169,DESER,T081,XSWI1,PosOpn,,,,1AS - Circuit breaker opened,1AS - Circuit breaker opened,DESER,T081,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,0,0,HI,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,T22,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T081.XSWI1.ProTr': 'CMD,12311170,DESER,T081,XSWI1,ProTr,,,,1AS - Protection 67/67N tripped,1AS - Protection 67/67N tripped,DESER,T081,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,0,0,HI,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,le set point 10 min Average,Pitch angle set point 10 min Average,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§,,-5,90,0,,,,,,-5,90,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WROT.PtAngSpBl1),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WROT.PtAngValBl1': 'CTV,12321655,DESER,T097,WROT,PtAngValBl1,,,,Pitch angle,Pitch angle,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,degrees,,-10,95,0,,,,,,-10,95,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WROT.PtAngValBl1Av': 'CTV,12321656,DESER,T097,WROT,PtAngValBl1Av,,,,Pitch angle 10 min Average,Pitch angle 10 min Average,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§,,-10,95,0,,,,,,-10,95,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WROT.PtAngValBl1),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WROT.RotNum': 'CTV,12321661,DESER,T097,WROT,RotNum,,,,Rotor diameter,Rotor diameter,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,m,,52,114,0,,,,,,52,114,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,52,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WROT.RotSpd': 'CTV,12321662,DESER,T097,WROT,RotSpd,,,,Rotor speed,Rotor speed,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,rpm,,-30,30,0,,,,,,-30,30,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-30,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WROT.RotSpdAv': 'CTV,12321663,DESER,T097,WROT,RotSpdAv,,,,Rotor speed 10 min Average,Rotor speed 10 min Average,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,rpm,,-30,30,0,,,,,,-30,30,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WROT.RotSpd),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-30,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WROT.RotSpdSp': 'CTV,12321664,DESER,T097,WROT,RotSpdSp,,,,Speed set point,Speed set point,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,rpm,,-50,2200,0,,,,,,-50,2200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRF.Col1Tmp': 'CTV,12321669,DESER,T097,WTRF,Col1Tmp,,,,Transformer 1st winding temperature,Transformer 1st winding temperature,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRF.Col2Tmp': 'CTV,12321670,DESER,T097,WTRF,Col2Tmp,,,,Transformer 2nd winding temperature,Transformer 2nd winding temperature,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRF.Col3Tmp': 'CTV,12321671,DESER,T097,WTRF,Col3Tmp,,,,Transformer 3rd winding temperature,Transformer 3rd winding temperature,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRF.TrfId': 'CTV,12321699,DESER,T097,WTRF,TrfId,,,,Transformer type,Transformer type,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.BrgHS1Tmp': 'CTV,12321702,DESER,T097,WTRM,BrgHS1Tmp,,,,Gearbox bearing temperature,Gearbox bearing temperature,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.BrgHS1TmpAv': 'CTV,12321703,DESER,T097,WTRM,BrgHS1TmpAv,,,,Gearbox bearing temperature 10m,Gearbox bearing temperature 10m,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WTRM.BrgHS1Tmp),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.CEClTmp': 'CTV,12321712,DESER,T097,WTRM,CEClTmp,,,,Cooling Circuit Input Coolant Temp,Cooling Circuit Input Coolant Temp,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-30,60,0,,,,,,-30,60,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-30,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.GbxId': 'CTV,12321724,DESER,T097,WTRM,GbxId,,,,Gearbox type,Gearbox type,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.GbxOilTmp': 'CTV,12321731,DESER,T097,WTRM,GbxOilTmp,,,,Gearbox oil temperature,Gearbox oil temperature,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.GbxOilTmpAv': 'CTV,12321732,DESER,T097,WTRM,GbxOilTmpAv,,,,Gearbox oil temperature 10 min Average,Gearbox oil temperature 10 min Average,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WTRM.GbxOilTmp),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.HyOilTmp': 'CTV,12321750,DESER,T097,WTRM,HyOilTmp,,,,Oil temperature - hydraulic group,Oil temperature - hydraulic group,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.HyOilTmpAv': 'CTV,12321751,DESER,T097,WTRM,HyOilTmpAv,,,,Oil temperature hydraulic group 10m,Oil temperature hydraulic group 10m,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WTRM.HyOilTmp),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.HyPres': 'CTV,12321758,DESER,T097,WTRM,HyPres,,,,Hydraulic group pressure,Hydraulic group pressure,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,bar,,0,400,0,,,,,,0,400,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.HyPresAv': 'CTV,12321759,DESER,T097,WTRM,HyPresAv,,,,Hydraulic group pressure 10 min Average,Hydraulic group pressure 10 min Average,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,bar,,0,400,0,,,,,,0,400,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WTRM.HyPres),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.HyVlvVol': 'CTV,12321764,DESER,T097,WTRM,HyVlvVol,,,,Servovalve output voltage,Servovalve output voltage,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,V,,-10,10,0,,,,,,-10,10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.LoRadtrTmp': 'CTV,12321765,DESER,T097,WTRM,LoRadtrTmp,,,,Radiator 1 temperature (lower),Radiator 1 temperature (lower),DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.MShfBrg1FtrTmp': 'CTV,12321768,DESER,T097,WTRM,MShfBrg1FtrTmp,,,,Filtered main shaft front bearing temp,Filtered main shaft front bearing temp,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.MShfBrg2FtrTmp': 'CTV,12321769,DESER,T097,WTRM,MShfBrg2FtrTmp,,,,Filtered main shaft rear bearing temp,Filtered main shaft rear bearing temp,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.SwGearId': 'CTV,12321778,DESER,T097,WTRM,SwGearId,,,,Switchgear Model,Switchgear Model,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,10,0,,,,,,0,10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTRM.UpRadtrTmp': 'CTV,12321780,DESER,T097,WTRM,UpRadtrTmp,,,,Radiator 2 temperature (upper),Radiator 2 temperature (upper),DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Â§C,,-50,200,0,,,,,,-50,200,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTm': 'CTV,12321787,DESER,T097,WTUR,AvlTm,,,,Total turbine availability - OK hours,Total turbine availability - OK hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,429497000000000,0,,,,,,0,429497000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmEx': 'CTV,12321788,DESER,T097,WTUR,AvlTmEx,,,,Ambient availability - OK hours,Ambient availability - OK hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,429497000000000,0,,,,,,0,429497000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmExMonth': 'CTV,12321789,DESER,T097,WTUR,AvlTmExMonth,,,,Ambient availability - OK hours month,Ambient availability - OK hours month,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,1500,0,,,,,,0,1500,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmExPrevMonth': 'CTV,12321790,DESER,T097,WTUR,AvlTmExPrevMonth,,,,Prev Month Ambient availability-OK hours,Prev Month Ambient availability-OK hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,1500,0,,,,,,0,1500,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmMonth': 'CTV,12321791,DESER,T097,WTUR,AvlTmMonth,,,,Monthly turbine availability - OK hours,Monthly turbine availability - OK hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,1500,0,,,,,,0,1500,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmPct': 'CTV,12321792,DESER,T097,WTUR,AvlTmPct,,,,% Total availability,% Total availability,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmPctMonth': 'CTV,12321793,DESER,T097,WTUR,AvlTmPctMonth,,,,% Monthly availability,% Monthly availability,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmPctPrevMonth': 'CTV,12321794,DESER,T097,WTUR,AvlTmPctPrevMonth,,,,% Availability previous month,% Availability previous month,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.AvlTmPrevMonth': 'CTV,12321795,DESER,T097,WTUR,AvlTmPrevMonth,,,,Prev Month Turbine availability-Ok hours,Prev Month Turbine availability-Ok hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,1500,0,,,,,,0,1500,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.DCtlSp': 'CTV,12321800,DESER,T097,WTUR,DCtlSp,,,,Delta Control Setpoint Applied,Delta Control Setpoint Applied,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%,,0,90,0,,,,,,0,90,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.DmdPF.actVal': 'CTV,12321968,DESER,T097,WTUR,DmdPF,actVal,,,Turbine Power Factor Setpoint,Turbine Power Factor Setpoint,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-1000,1000,0,,,,,,-1000,1000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-1000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.DmdW.actVal': 'CTV,12322005,DESER,T097,WTUR,DmdW,actVal,,,Set Point for the Turbine,Set Point for the Turbine,DESER,T097,,,P,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kW,,700,2000,0,,,,,,700,2000,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,700,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.DmdWWTM.actVal': 'CTV,12321969,DESER,T097,WTUR,DmdWWTM,actVal,,,Set Point for the Turbine,Set Point for the Turbine,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kW,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.GriAvlTm': 'CTV,12321808,DESER,T097,WTUR,GriAvlTm,,,,Total grid availability - hours,Total grid availability - hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,429497000000000,0,,,,,,0,429497000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.GriAvlTmMonth': 'CTV,12321809,DESER,T097,WTUR,GriAvlTmMonth,,,,Monthly grid availability - hours,Monthly grid availability - hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,1500,0,,,,,,0,1500,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.GriAvlTmPrevMonth': 'CTV,12321810,DESER,T097,WTUR,GriAvlTmPrevMonth,,,,Previous Month Grid availability - hours,Previous Month Grid availability - hours,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,1500,0,,,,,,0,1500,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.NoiseLev': 'CTV,12321825,DESER,T097,WTUR,NoiseLev,,,,Turbine Noise Level,Turbine Noise Level,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,10,0,,,,,,0,10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.NoiseLev.actVal': 'CTV,12321970,DESER,T097,WTUR,NoiseLev,actVal,,,Turbine Noise Level Setpoint,Turbine Noise Level Setpoint,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,10,0,,,,,,0,10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.NoiseLevDef': 'CTV,12321826,DESER,T097,WTUR,NoiseLevDef,,,,Noise level when remote control is lost,Noise level when remote control is lost,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,5,0,,,,,,0,5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.NoiseLevLoWd': 'CTV,12321827,DESER,T097,WTUR,NoiseLevLoWd,,,,Low wind noise level (Normal. A. B. C),Low wind noise level (Normal. A. B. C),DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,5,0,,,,,,0,5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.OpModSentSCADA': 'CTV,12321828,DESER,T097,WTUR,OpModSentSCADA,,,,Required operating mode sent to SCADA,Required operating mode sent to SCADA,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,100,0,,,,,,0,100,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.OpTmRs.actTmVal': 'CTV,12321972,DESER,T097,WTUR,OpTmRs,actTmVal,,,Number of hours in service menu,Number of hours in service menu,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,429497000000000,0,,,,,,0,429497000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.StraTurSt.actVal': 'CTV,12321973,DESER,T097,WTUR,StraTurSt,actVal,,,Strategy operations status,Strategy operations status,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,429497000000000,0,,,,,,0,429497000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWHour': 'CTV,12321837,DESER,T097,WTUR,SupWHour,,,,Hours producing active power,Hours producing active power,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,h,,0,2147000000000,0,,,,,,0,2147000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWPrevDay': 'CTV,12321838,DESER,T097,WTUR,SupWPrevDay,,,,Previous day production,Previous day production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,63000,0,,,,,,0,63000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWh': 'CTV,12321839,DESER,T097,WTUR,SupWh,,,,Total Production,Total Production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,4290000000,0,,,,,,0,4290000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWh10m': 'CTV,12321840,DESER,T097,WTUR,SupWh10m,,,,Turbine Actual Production 10 min,Turbine Actual Production 10 min,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kW,,0,2700,0,,,,,,0,2700,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhAv': 'CTV,12321841,DESER,T097,WTUR,SupWhAv,,,,Total Production Average,Total Production Average,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,4290000000,0,,,,,,0,4290000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,AVG(@DESER.T097.WTUR.SupWh),,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhCap': 'CTV,12321842,DESER,T097,WTUR,SupWhCap,,,,Wind turbine energy produced,Wind turbine energy produced,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,4294967000000000,0,,,,,,0,4294967000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhDay': 'CTV,12321843,DESER,T097,WTUR,SupWhDay,,,,Current Day Production,Current Day Production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,63000,0,,,,,,0,63000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhDayScd': 'CTV,12321985,DESER,T097,WTUR,SupWhDayScd,,,,Total Production Daily from SCADA,Total Production Daily from SCADA,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,4294967000,0,,,,,,0,4294967000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhHour': 'CTV,12321844,DESER,T097,WTUR,SupWhHour,,,,Current Hour Production,Current Hour Production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,2700,0,,,,,,0,2700,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhMonth': 'CTV,12321845,DESER,T097,WTUR,SupWhMonth,,,,Current Month Production,Current Month Production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,1953000,0,,,,,,0,1953000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhPrevDay': 'CTV,12321986,DESER,T097,WTUR,SupWhPrevDay,,,,Total Production Previous Day from SCADA,Total Production Previous Day from SCADA,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,4294967000,0,,,,,,0,4294967000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhPrevMonth': 'CTV,12321846,DESER,T097,WTUR,SupWhPrevMonth,,,,Previous Month Production,Previous Month Production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,1953000,0,,,,,,0,1953000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SupWhYear': 'CTV,12321847,DESER,T097,WTUR,SupWhYear,,,,Current Year Production,Current Year Production,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kWh,,0,4294967000000000,0,,,,,,0,4294967000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.SyncTMPLC.actVal': 'CTV,12321971,DESER,T097,WTUR,SyncTMPLC,actVal,,,Time Synchronization,Time Synchronization,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-99999,999999,0,,,,,,-99999,999999,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-99999,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.TotWCap': 'CTV,12321854,DESER,T097,WTUR,TotWCap,,,,Instantaneous producible power,Instantaneous producible power,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kW,,0,2900,0,,,,,,0,2900,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.TotWCap10m': 'CTV,12321855,DESER,T097,WTUR,TotWCap10m,,,,10 Min Producible Power Counter,10 Min Producible Power Counter,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,kW,,-50,2700,0,,,,,,-50,2700,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.TurSt.actSt': 'CTV,12322003,DESER,T097,WTUR,TurSt,actSt,,,Machine status,Machine status,DESER,T097,,,,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,250,0,,,,,,0,250,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,WEB,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n', 'DESER.T097.WTUR.TurStNoteNum': 'CTV,12321991,DESER,T097,WTUR,TurStNoteNum,,,,Turbine CORE Control Center Characterization,Turbine CORE Control Center Characterization,DESER,T097,,,P,I,0,0,0,0,0,1,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-5,100,0,,,,,,-5,100,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W19,,,,,,,,,,,,,,,,,,,,,,,,,,0,,,0,,,,,,,,,,,,,,0,0,0,0,1,-5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n'}
	test_keys = ['DESER.T081.XSWI1.FuStBit2', 'DESER.T081.XSWI1.Opn', 'DESER.T081.XSWI1.PosCls', 'DESER.T081.XSWI1.PosOpn', 'DESER.T081.XSWI1.ProTr']
	site_name_regex = "(?<=\,)\w{5}(?=\,)"

	def test_compile_variable_name(self):
		variable_name = main.get_variable_name(self.test_line)
		expected_name = "DESER.AVC.ConsigTensFueraRango"
		self.assertTrue(variable_name == expected_name, "The variable names are different")


	def test_create_varexp_dictionary(self):
		result = main.create_varexp_dictionary("./Desert Wind Varexp.txt")
		self.assertTrue(isinstance(result,dict),f"{result} is not a dict type")


	def test_find_keys_based_on_regex(self):
		user_tag_regex = r"\bT081\b"
		result_list = main.get_extraction_tags(user_tag_regex,self.test_dict)
		self.assertTrue(len(result_list) == 5, f"The list contains {len(result_list)} keys and not 5 as expected")


	def test_create_extracted_varexp(self):
		main.separate_tags_from_varexp(self.test_keys,self.test_dict)


if __name__ == '__main__':
	unittest.main()
