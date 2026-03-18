import streamlit as st
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import io
import urllib.parse
import json
import os

# Configuration de la page Streamlit
st.set_page_config(page_title="Calculateur de Chargement", layout="wide")

# --- 🗄️ BASE DE DONNÉES INTÉGRÉE ---
CSV_DATA = """CTT Magasin;Longueur Ext (mm);Largeur Ext (mm);Hauteur Ext (mm)
'03VER';'1050';'800';'2800'
'04';'900';'555';'600'
'048G1';'3600';'1180';'1560'
'048G2';'3600';'1180';'2000'
'048G3';'3600';'1180';'2015'
'048GB';'3600';'1180';'1850'
'048GS';'3600';'1180';'1150'
'05';'1125';'900';'800'
'053';'1440';'1390';'1434'
'058';'1200';'1000';'1200'
'059';'1200';'1000';'600'
'081';'1150';'800';'730'
'083';'1370';'900';'920'
'084';'1600';'1150';'920'
'085';'1600';'1150';'1070'
'08747';'2260';'1460';'920'
'088';'2300';'1600';'1070'
'10';'1200';'1000';'150'
'103';'1370';'900';'920'
'106';'1200';'1000';'1150'
'12';'580';'370';'195'
'13002';'2000';'1200';'1200'
'13003';'3000';'1150';'1150'
'13010';'2110';'1900';'1697'
'13013';'1172';'817';'830'
'13024';'2090';'1250';'1200'
'13051';'2260';'2060';'1670'
'13250';'1010';'600';'684'
'13251';'1200';'1000';'840'
'13252';'1600';'1200';'840'
'13253';'1600';'1200';'1130'
'13600';'1172';'676';'830'
'13800';'800';'600';'614'
'13B48';'3600';'1180';'1850'
'13G13';'1172';'817';'830'
'13P13';'1172';'817';'830'
'13PNE';'2298';'1100';'850'
'14';'345';'275';'165'
'18';'260';'160';'160'
'200';'2180';'1000';'1000'
'201';'2180';'1080';'1000'
'203';'2180';'1210';'1000'
'204';'2180';'1300';'1000'
'205';'2180';'1000';'1000'
'206';'2180';'1000';'1000'
'210';'2180';'1100';'1000'
'21012';'3600';'1180';'2015'
'211';'2180';'1160';'1000'
'213';'2180';'1290';'1000'
'214';'2180';'1380';'1000'
'220';'2180';'1200';'1000'
'230';'2180';'1300';'1000'
'233';'2180';'1420';'1000'
'234';'2180';'1510';'1000'
'240';'2180';'1400';'1000'
'244';'2180';'1600';'1000'
'250';'2180';'1500';'1000'
'260';'2180';'1600';'1000'
'30';'2350';'1450';'1000'
'300';'2180';'1000';'1300'
'301';'2180';'1080';'1300'
'303';'2180';'1210';'1300'
'304';'2180';'1300';'1300'
'305';'2180';'1000';'1300'
'306';'2180';'1000';'1300'
'310';'2180';'1100';'1300'
'311';'2180';'1160';'1300'
'313';'2180';'1290';'1300'
'314';'2180';'1380';'1300'
'320';'2180';'1200';'1300'
'330';'2180';'1300';'1300'
'333';'2180';'1420';'1300'
'334';'2180';'1510';'1300'
'340';'2180';'1400';'1300'
'344';'2180';'1600';'1300'
'350';'2180';'1500';'1300'
'360';'2180';'1600';'1300'
'3924';'1100';'725';'780'
'401';'1000';'400';'200'
'402';'600';'330';'500'
'403';'600';'500';'500'
'40365';'2680';'1480';'1500'
'404';'1900';'400';'200'
'405';'1000';'600';'300'
'406';'1000';'600';'300'
'407';'1000';'200';'900'
'408';'900';'500';'500'
'409';'600';'1000';'500'
'410';'1000';'800';'400'
'411';'1000';'600';'600'
'412';'1000';'400';'900'
'413';'1200';'800';'400'
'414';'1600';'600';'400'
'415';'1200';'400';'900'
'416';'900';'1000';'500'
'417';'1000';'1130';'400'
'418';'1900';'600';'400'
'419';'1000';'800';'600'
'420';'1000';'600';'900'
'42066';'2400';'1480';'950'
'421';'1200';'1130';'400'
'422';'1200';'600';'900'
'423';'1000';'1200';'600'
'424';'1000';'800';'900'
'425';'1000';'300';'2500'
'426';'2100';'600';'600'
'427';'1200';'800';'900'
'428';'1600';'600';'900'
'429';'1900';'600';'900'
'430';'1000';'1200';'900'
'431';'1600';'600';'1300'
'432';'1200';'1200';'900'
'433';'1900';'1200';'600'
'434';'1000';'600';'2500'
'435';'1600';'600';'1600'
'436';'1600';'1200';'900'
'437';'1000';'600';'3000'
'438';'1900';'600';'1600'
'439';'2100';'600';'1600'
'44';'615';'400';'410'
'440';'1900';'1200';'1200'
'441';'1600';'1200';'1600'
'442';'1900';'1200';'1600'
'45';'2254';'1584';'1845'
'45C';'2234';'1592';'2070'
'45T';'2234';'1592';'2070'
'46';'2254';'1584';'920'
'48G1';'0';'0';'0'
'49';'2234';'1592';'1180'
'500';'2180';'1000';'1500'
'501';'2180';'1000';'1500'
'503';'2180';'1210';'1500'
'504';'2180';'1300';'1500'
'505';'2180';'1000';'1500'
'506';'2180';'1000';'1500'
'510';'2180';'1100';'1500'
'511';'2180';'1160';'1500'
'513';'2180';'1290';'1500'
'514';'2180';'1380';'1500'
'520';'2180';'1200';'1500'
'52GA';'0';'0';'0'
'52GB';'1550';'1150';'1510'
'52GE';'1550';'1150';'1110'
'52GJ';'1550';'1150';'1660'
'52GO';'1550';'1150';'1220'
'52GS';'1550';'1150';'1110'
'52GV';'1550';'1150';'1330'
'52PA';'0';'0';'0'
'52PB';'1550';'1150';'1510'
'52PJ';'1550';'1150';'1660'
'52PO';'1550';'1150';'1220'
'52PS';'1550';'1150';'1110'
'52PV';'1550';'1150';'1330'
'530';'2180';'1300';'1500'
'533';'2180';'1420';'1500'
'534';'2180';'1510';'1500'
'540';'2180';'1400';'1200'
'544';'2180';'1600';'1500'
'55';'2310';'1392';'1030'
'550';'2180';'1500';'1500'
'560';'2180';'1600';'1500'
'57';'1557';'1157';'990'
'570';'2300';'1300';'2220'
'57B';'1557';'1157';'990'
'57V';'1557';'1157';'1273'
'600';'2180';'1000';'1600'
'601';'2180';'1080';'1600'
'603';'2180';'1210';'1600'
'604';'2180';'1300';'1600'
'605';'2180';'1000';'1600'
'606';'2180';'1000';'1600'
'610';'2180';'1100';'1600'
'611';'2180';'1160';'1600'
'613';'2180';'1290';'1600'
'614';'2180';'1380';'1600'
'620';'2180';'1200';'1600'
'630';'2180';'1300';'1600'
'633';'2180';'1420';'1600'
'634';'2180';'1510';'1600'
'640';'2180';'1400';'1600'
'644';'2180';'1600';'1600'
'650';'2180';'1500';'1600'
'660';'2180';'1600';'1600'
'6B';'2180';'1000';'1000'
'6B0H';'2180';'1000';'1770'
'6B0M';'2180';'1000';'1470'
'6B2';'2180';'1210';'1000'
'6B213';'2180';'1290';'1000'
'6B2H';'2180';'1210';'1770'
'6B2M';'2180';'1210';'1470'
'6B6';'2180';'1610';'1000'
'6B6H';'2180';'1610';'1770'
'6B6M';'2180';'1610';'1470'
'72A3';'1870';'1180';'850'
'72A4';'1870';'1180';'1200'
'A1';'400';'520';'460'
'A2';'860';'520';'272'
'A3';'860';'520';'460'
'A4';'375';'560';'158'
'A5';'1160';'600';'158'
'A6';'1160';'600';'220'
'A7';'1160';'600';'282'
'A8';'1160';'600';'345'
'A9';'1600';'600';'335'
'AD1';'630';'850';'280'
'AD1B';'630';'850';'280'
'AD2';'630';'850';'580'
'AD2B';'630';'850';'580'
'AD3';'840';'1200';'420'
'AD3B';'840';'1200';'420'
'AD4';'1290';'850';'580'
'AD4B';'1290';'850';'580'
'AD5';'1690';'1200';'420'
'AD5B';'1690';'1200';'420'
'AD6';'840';'1200';'880'
'AD6B';'840';'1200';'880'
'AD7';'1690';'1200';'880'
'AD7B';'1690';'1200';'880'
'AH4L1';'500';'994';'436'
'AH4L2';'500';'497';'436'
'AH5L1';'500';'994';'490'
'AH5L2';'500';'497';'490'
'AH6L1';'500';'994';'596'
'AH9L1';'500';'994';'861'
'ANA20';'600';'400';'200'
'ANA25';'600';'400';'250'
'ANA30';'600';'400';'300'
'ANC15';'400';'300';'150'
'ANC20';'400';'300';'200'
'ANC30';'400';'300';'300'
'AND12';'300';'200';'125'
'AND20';'300';'200';'200'
'B1';'500';'94';'80'
'B2';'500';'188';'80'
'B3';'500';'235';'80'
'B4';'500';'182';'125'
'B5';'500';'230';'115'
'B6';'500';'310';'200'
'BACAS';'649';'449';'330'
'BC1';'515';'153';'114'
'BC2';'255';'153';'114'
'BC3';'165';'153';'114'
'BC4';'105';'153';'114'
'BG';'470';'300';'180'
'BI11';'597';'398';'220'
'BI12';'358';'279';'150'
'BI14';'279';'179';'150'
'BND09';'300';'200';'90'
'BR';'470';'145';'180'
'BS';'0';'0';'0'
'BV';'610';'470';'360'
'C0';'400';'295';'397'
'C1';'190';'150';'125'
'C2';'390';'150';'125'
'C3';'400';'148';'210'
'C4';'400';'195';'210'
'C5';'400';'295';'157'
'C6';'400';'295';'210'
'C7';'638';'400';'157'
'C8';'638';'400';'210'
'C9';'638';'400';'397'
'CB';'638';'400';'397'
'CB003';'3000';'1150';'1150'
'CBWG';'2100';'1440';'870'
'CH';'0';'0';'0'
'CH2L1';'590';'985';'220'
'CH2L2';'590';'490';'220'
'CH2L3';'590';'325';'220'
'CH2L4';'590';'246';'220'
'CH2L5';'600';'198';'278'
'CH2L6';'590';'160';'220'
'CH3L1';'590';'985';'330'
'CH3L2';'590';'490';'330'
'CH3L3';'590';'328';'330'
'CH3L6';'590';'164';'330'
'CH4L1';'590';'968';'410'
'CH4L2';'600';'500';'410'
'CH4L3';'600';'319';'410'
'CH4L4';'600';'250';'400'
'CH5L1';'590';'985';'480'
'CH5L2';'590';'492';'480'
'CH5L3';'590';'328';'480'
'CH5L6';'590';'164';'480'
'CH6L1';'600';'994';'596'
'CH6L2';'600';'497';'596'
'CH9L1';'600';'994';'861'
'CM';'0';'0';'0'
'CM1';'600';'610';'680'
'CM2';'770';'610';'680'
'CM3';'770';'610';'1020'
'CM4';'770';'1200';'1020'
'CM5';'770';'1200';'680'
'CM6';'900';'1200';'1150'
'CM712';'1125';'900';'800'
'CM713';'1870';'1180';'1150'
'CM714';'1550';'1180';'1150'
'CM715';'1550';'1180';'1450'
'CM717';'1870';'1180';'1450'
'CM718';'1870';'1180';'1660'
'CM719';'1170';'810';'830'
'CM720';'1170';'810';'560'
'CM721';'900';'555';'600'
'CM730';'2350';'1450';'950'
'CM731';'2000';'1180';'1150'
'CMJ';'0';'0';'0'
'CMPC';'1870';'1180';'1150'
'COQUE';'4000';'2000';'1200'
'CP';'1200';'1000';'750'
'CP002';'2000';'1200';'1200'
'CP52';'1520';'1105';'953'
'CPB';'1200';'1000';'600'
'CPC';'1840';'1160';'1150'
'CPF10';'1200';'1000';'1100'
'CPF8';'1200';'800';'1100'
'CPFH';'1150';'785';'783'
'CPFL';'1150';'785';'523'
'CPH';'1200';'1000';'1150'
'CPI08';'1200';'800';'1200'
'CPI10';'1200';'1000';'1200'
'CPICO';'1200';'810';'645'
'CPKE';'470';'350';'311'
'CPKJ';'1200';'1000';'600'
'CPND';'1200';'1000';'800'
'CTAE';'545';'340';'165'
'CTAE2';'210';'140';'170'
'CTAE3';'210';'140';'210'
'CTAE4';'280';'210';'210'
'CTDE';'2000';'2000';'2000'
'CTST';'395';'305';'255'
'CTTUC';'9999';'9999';'99'
'D0';'0';'0';'0'
'D1';'0';'0';'0'
'D3';'0';'0';'0'
'D4';'0';'0';'0'
'D6';'0';'0';'0'
'D7';'400';'638';'397'
'D8';'0';'0';'0'
'D9';'0';'0';'0'
'DC381';'355';'720';'245'
'DC383';'420';'820';'335'
'DC452';'1045';'350';'395'
'DC481';'255';'720';'245'
'DC483';'310';'820';'335'
'DC852';'1045';'170';'395'
'DC883';'150';'820';'335'
'DD252';'535';'710';'395'
'DD281';'520';'380';'245'
'DD283';'630';'430';'335'
'DD481';'255';'380';'245'
'DD483';'310';'430';'335'
'DD883';'150';'430';'335'
'DIVER';'0';'0';'0'
'DR252';'725';'520';'520'
'DR452';'360';'520';'520'
'DR852';'177';'520';'520'
'EC1';'1190';'850';'2850'
'EC2';'1790';'850';'665'
'EC3';'1190';'850';'665'
'ECIAM';'1200';'700';'450'
'F2';'0';'0';'0'
'F4416';'1600';'400';'380'
'F4419';'1900';'400';'380'
'F5';'1136';'881';'816'
'FH';'1172';'817';'830'
'FH2L1';'800';'1282';'278'
'FH2L5';'800';'256';'278'
'FH3L1';'800';'1282';'331'
'FH3L2';'800';'641';'384'
'FH3L5';'800';'256';'384'
'FH4L1';'800';'1282';'436'
'FH4L2';'800';'641';'436'
'FH5L1';'800';'1282';'490'
'FH5L2';'800';'641';'490'
'FH600';'1172';'677';'830'
'FH6L1';'800';'1282';'596'
'FH6L2';'800';'641';'596'
'FH9L1';'800';'1282';'861'
'FL';'1172';'817';'560'
'G1';'300';'200';'114'
'G2';'400';'300';'114'
'G3';'400';'300';'214'
'G4';'600';'400';'214'
'G5';'600';'400';'314'
'G6';'1196';'328';'150'
'GEFC3';'0';'0';'0'
'GEFC6';'0';'0';'0'
'GH4L1';'1000';'994';'436'
'GH6L1';'1000';'994';'596'
'GH6L2';'1000';'497';'596'
'GH9L1';'1000';'994';'861'
'HH2L1';'1000';'1282';'278'
'HH2L2';'1000';'641';'278'
'HH3L1';'1000';'1282';'384'
'HH4L1';'1000';'1282';'436'
'HH5L1';'1000';'1282';'490'
'HH5L2';'1000';'641';'490'
'HH6L1';'1000';'1282';'596'
'HH6L2';'1000';'641';'596'
'HH9L1';'1000';'1282';'861'
'IAM';'390';'225';'210'
'IAM52';'1550';'1150';'1110'
'IAMG3';'400';'300';'214'
'IAMG4';'600';'400';'214'
'IAMG5';'600';'400';'314'
'JH4L1';'1200';'1282';'436'
'JH4L2';'1200';'641';'436'
'JH6L1';'1200';'1282';'596'
'JH6L2';'1200';'641';'596'
'JH9L1';'1200';'1282';'861'
'KH4L1';'1500';'994';'436'
'KH6L1';'1500';'994';'596'
'KH6L2';'1500';'497';'596'
'KH9L1';'1500';'994';'861'
'KITA5';'1870';'1180';'956'
'M22L4';'575';'600';'2245'
'M22L6';'575';'400';'2245'
'M30L4';'575';'600';'3000'
'M30L6';'575';'400';'3000'
'MD200';'600';'400';'200'
'MD500';'600';'500';'400'
'Mirafiori opel';'1200';'1000';'620'
'NH6L2';'575';'1350';'645'
'NH6L3';'575';'900';'645'
'NH8L1';'575';'2700';'800'
'NH8L2';'575';'1350';'800'
'NH8L3';'575';'900';'800'
'P1';'1550';'1150';'215'
'P16L3';'800';'900';'1620'
'P2';'1550';'1150';'335'
'PB';'0';'0';'0'
'PCHG';'2400';'1950';'1520'
'PE';'1200';'800';'1150'
'PEB';'1200';'800';'450'
'PF';'3000';'2000';'1500'
'PF08';'1200';'800';'1150'
'PF10';'1200';'1000';'1150'
'PF12';'1200';'1200';'1150'
'PF20L';'1200';'1000';'520'
'PF52';'1550';'1150';'1150'
'PF800';'3600';'1400';'130'
'PFA';'1320';'780';'1250'
'PFB';'1160';'805';'600'
'PFC';'800';'800';'1400'
'PFGC';'2920';'1955';'1100'
'PFH';'1160';'805';'800'
'PFHB';'1160';'800';'1220'
'PFHV';'1160';'800';'900'
'PFI08';'1200';'800';'1200'
'PFI10';'1200';'1000';'1200'
'PFK';'1120';'1040';'1160'
'PFL';'1200';'1000';'800'
'PFP';'1200';'800';'760'
'PFPC';'2105';'1510';'1240'
'PFRS1';'1200';'1200';'1200'
'PH6L3';'800';'900';'655'
'PH8L2';'800';'1350';'805'
'PM';'900';'1200';'1020'
'PR';'0';'0';'0'
'PR252';'1460';'520';'510'
'PR452';'250';'1460';'520'
'PRT';'1360';'1200';'1270'
'Q22L2';'1050';'1200';'2245'
'Q22L4';'1050';'600';'2245'
'Q22L6';'1050';'400';'2245'
'Q30L4';'1050';'600';'3000'
'QH4L6';'1050';'400';'440'
'QH6L2';'1050';'1200';'665'
'QH6L3';'1050';'800';'665'
'QH6L4';'1050';'600';'665'
'QH6L6';'1050';'400';'665'
'QH8L1';'1050';'240';'815'
'QH8L2';'1050';'1200';'815'
'R12L2';'1200';'1260';'1210'
'R12L3';'1200';'840';'1210'
'R12L4';'1200';'630';'1210'
'R12L6';'1200';'420';'1210'
'Rack EB2L';'2250';'1500';'920'
'RG';'0';'0';'0'
'RH4L6';'1200';'420';'425'
'RH6L2';'1200';'1260';'645'
'RH6L3';'1200';'840';'645'
'RH6L4';'1200';'630';'645'
'RH6L6';'1200';'420';'645'
'RH8L2';'1200';'1260';'800'
'RI11';'597';'398';'220'
'RI12';'358';'279';'150'
'RI14';'279';'179';'150'
'RIM';'0';'0';'0'
'RLGA';'0';'0';'0'
'RLGB';'1870';'1150';'1510'
'RLGC';'1870';'1150';'1110'
'RLGJ';'1870';'1150';'1660'
'RLGS';'1870';'1150';'1110'
'RLGV';'1870';'1150';'1330'
'RLPA';'0';'0';'0'
'RLPB';'1870';'1150';'1510'
'RLPC';'1870';'1150';'1110'
'RLPJ';'1870';'1150';'1660'
'RLPO';'1870';'1150';'1220'
'RLPS';'1870';'1150';'1110'
'RLPV';'1870';'1150';'1330'
'RM';'0';'0';'0'
'RP';'0';'0';'0'
'S12L3';'1600';'900';'1255'
'S12L4';'1600';'675';'1255'
'S12L6';'1600';'450';'1255'
'S16L2';'1600';'1350';'1620'
'S16L3';'1600';'900';'1620'
'S16L4';'1600';'675';'1620'
'S16L6';'1600';'450';'1620'
'SH4L3';'1600';'900';'430'
'SH4L6';'1600';'450';'430'
'SH6L2';'1600';'1350';'655'
'SH6L3';'1600';'900';'655'
'SH6L4';'1600';'675';'655'
'SH6L6';'1600';'450';'655'
'SH8L2';'1600';'1350';'805'
'SH8L3';'1600';'900';'805'
'SP';'2000';'1500';'1200'
'ST';'1500';'1000';'1015'
'T0073';'1610';'1175';'1220'
'T0074';'1610';'1175';'1220'
'T1';'0';'0';'0'
'T12L4';'1900';'830';'1210'
'T12L5';'1900';'665';'1210'
'T12L8';'1900';'415';'1210'
'T15L2';'1900';'1250';'1585'
'T15L4';'1900';'830';'1585'
'T15L5';'1900';'665';'1585'
'T15L8';'1900';'415';'1585'
'TB2';'1250';'500';'400'
'TB4';'1250';'500';'200'
'TB8';'630';'500';'200'
'TH4L8';'1900';'415';'425'
'TH6L2';'1900';'1250';'645'
'TH6L4';'1900';'830';'645'
'TH6L5';'1900';'665';'645'
'TH6L8';'1900';'415';'645'
'TH8L1';'1900';'1660';'800'
'TH8L2';'1900';'1250';'800'
'TH8L4';'1900';'830';'800'
'TOUS';'1';'1';'1'
'TR084';'1240';'1040';'670'
'V26BM';'2180';'1000';'1470'
'VC003';'3000';'1150';'1150'
'VC252';'725';'1045';'810'
'VC257';'1557';'1157';'990'
'VC26B';'1090';'1000';'1000'
'VC281';'520';'720';'500'
'VC283';'630';'820';'680'
'VC285';'725';'1045';'810'
'VC2PE';'1200';'300';'300'
'VC2ST';'1500';'1000';'1015'
'VC30G';'2350';'1450';'1000'
'VC30P';'2350';'1450';'1000'
'VC352';'475';'1045';'810'
'VC36B';'680';'1000';'1000'
'VC381';'355';'720';'500'
'VC383';'400';'820';'680'
'VC385';'480';'1045';'810'
'VC3FH';'1172';'817';'830'
'VC3FL';'1172';'817';'560'
'VC3ST';'1500';'1000';'1015'
'VC452';'360';'1045';'810'
'VC459';'600';'500';'600'
'VC46B';'510';'1000';'1000'
'VC481';'255';'720';'500'
'VC483';'310';'820';'680'
'VC485';'360';'1045';'810'
'VC4ST';'1500';'1000';'1015'
'VC52';'1550';'1150';'1110'
'VC52B';'1550';'1150';'1510'
'VC52J';'1550';'1150';'1660'
'VC52V';'1550';'1150';'1330'
'VC59';'1200';'500';'600'
'VC852';'177';'1045';'810'
'VC883';'150';'820';'680'
'VC885';'180';'1045';'810'
'VCBS';'0';'0';'0'
'VCFH';'1172';'817';'830'
'VCFHG';'1172';'817';'830'
'VCFHP';'1172';'817';'830'
'VCFL';'1172';'817';'560'
'VCRL';'1870';'1150';'1110'
'VCZ6';'0';'0';'0'
'VD252';'725';'520';'810'
'VD281';'520';'380';'500'
'VD283';'630';'430';'680'
'VD452';'360';'520';'810'
'VD481';'255';'380';'500'
'VD483';'310';'430';'680'
'VD52';'1460';'520';'810'
'VD883';'150';'430';'680'
'VP081';'1150';'1600';'730'
'VP083';'1370';'1800';'920'
'VP252';'515';'1460';'810'
'VP283';'620';'1720';'680'
'VP383';'420';'1720';'680'
'VP452';'250';'1460';'810'
'VP483';'310';'1720';'680'
'VR252';'725';'1045';'520'
'VR352';'1045';'1460';'810'
'VR452';'360';'1045';'520'
'VR52';'1460';'1045';'550'
'VR852';'177';'1045';'520'
'XXX10';'2100';'1900';'1697'
'XXX24';'2090';'1250';'1200'
'XXX45';'0';'0';'0'
'XXX48';'0';'0';'0'
'XXX52';'1550';'1150';'1660'
'XXXBS';'0';'0';'0'
'XXXPF';'0';'0';'0'
'XXXRL';'1870';'1150';'1660'
'XXXSP';'0';'0';'0'
'XXXST';'1';'1';'1'
'XXXXX';'4000';'2000';'1200'
'Z0';'3508';'472';'296'
'Z1';'2958';'472';'296'
'Z10';'2300';'800';'750'
'Z10L';'3500';'800';'750'
'Z10M';'2950';'800';'570'
'Z1L';'2958';'944';'296'
'Z2';'2308';'472';'296'
'Z5';'2108';'472';'296'
'Z6';'918';'472';'296'
'Z7';'2958';'944';'296'
'Z8';'1218';'472';'296'
'Z9';'1611';'472';'296'
"""

@st.cache_data
def load_database():
    try:
        # FAIL-SAFE : on tente d'abord avec un point-virgule
        df = pd.read_csv(io.StringIO(CSV_DATA), sep=";", quotechar="'")
        df.columns = df.columns.str.strip()
        
        # Si on ne trouve pas la colonne cible, on essaye avec une virgule !
        if 'CTT Magasin' not in df.columns:
            df = pd.read_csv(io.StringIO(CSV_DATA), sep=",", quotechar="'")
            df.columns = df.columns.str.strip()
            
        return df
    except Exception as e:
        return None

df_db = load_database()

# CRÉATION SÉCURISÉE DE LA LISTE DES CONTENANTS
liste_contenants = []
if df_db is not None and 'CTT Magasin' in df_db.columns and not df_db.empty:
    liste_contenants = df_db['CTT Magasin'].dropna().astype(str).str.strip().tolist()
    liste_contenants = [c for c in liste_contenants if c and c.lower() != "nan"]

# --- GESTION DE LA SAUVEGARDE LOCALE ---
import json
import os

CONFIG_FILE = "config_app.json"

if 'config_loaded' not in st.session_state:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                st.session_state.saved_config = json.load(f)
        except:
            st.session_state.saved_config = {}
    else:
        st.session_state.saved_config = {}
    
    st.session_state.config_loaded = True
    st.session_state.nb_conteneurs = st.session_state.saved_config.get("nb_conteneurs", 1)

cfg = st.session_state.saved_config

# --- INJECTION CSS GLOBALE POUR UN DESIGN FUN ET LISIBLE ---
st.markdown("""
<style>
/* Cacher le padding supplémentaire des headers */
h4 {
    padding-bottom: 5px;
}

/* --- DESIGN DES BLOCS CLOISONNÉS (Gradients & Ombres) --- */
div[data-testid="stVerticalBlockBorderWrapper"]:has(#marker-camion) {
    background: linear-gradient(135deg, #e1f5fe 0%, #81d4fa 100%) !important;
    border: 3px solid #03a9f4 !important;
    border-radius: 15px !important;
    box-shadow: 0 6px 12px rgba(3, 169, 244, 0.2) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(#marker-charges) {
    background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%) !important;
    border: 3px solid #ff9800 !important;
    border-radius: 15px !important;
    box-shadow: 0 6px 12px rgba(255, 152, 0, 0.2) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(#marker-conteneurs) {
    background: linear-gradient(135deg, #e8f5e9 0%, #a5d6a7 100%) !important;
    border: 3px solid #4caf50 !important;
    border-radius: 15px !important;
    box-shadow: 0 6px 12px rgba(76, 175, 80, 0.2) !important;
}

/* --- LISIBILITÉ : Fond blanc pour les champs de saisie --- */
div[data-baseweb="input"] > div, 
div[data-baseweb="select"] > div, 
div[data-baseweb="number_input"] > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
}

/* --- TEXTE DES BOUTONS RADIO --- */
div[data-testid="stRadio"] label {
    color: #333 !important;
    font-weight: 500;
}

/* --- BOUTON D'AJOUT DE CONTENEURS & CASE A COCHER --- */
div[data-testid="stElementContainer"]:has(#conteneurs-header) + div div[data-testid="stCheckbox"] {
    background-color: rgba(255, 255, 255, 0.9) !important;
    padding: 8px 12px;
    border-radius: 8px;
    border: 2px dashed #4caf50;
}
div[data-testid="stElementContainer"]:has(#conteneurs-header) + div div[data-testid="stCheckbox"] p {
    color: #1b5e20 !important;
    font-weight: bold;
}

/* Boutons plus ronds et interactifs */
.stButton > button {
    background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%) !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 10px rgba(0,0,0,0.3) !important;
}

/* Bouton d'export */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%) !important;
    width: 100%;
    font-size: 1.1em !important;
    padding: 10px !important;
    border-radius: 10px !important;
}

/* =========================================================
   STYLE D'IMPRESSION (PDF)
   Cache la barre de menu, les boutons et les champs de saisie,
   ne garde QUE le schéma visuel et les textes pour le PDF.
========================================================= */
@media print {
    /* Cacher le menu latéral */
    [data-testid="stSidebar"] { display: none !important; }
    /* Cacher l'en-tête Streamlit (les trois petits points) */
    header { display: none !important; }
    /* Ajuster la largeur de la zone principale */
    .block-container { max-width: 100% !important; padding: 0 !important; }
    /* Cacher les boutons de l'application et iframes */
    .stButton, .btn-export, iframe { display: none !important; }
    /* Cacher les expanders fermés (Option 2) */
    [data-testid="stExpander"] { display: none !important; }
    /* Forcer l'affichage correct des couleurs de fond (schémas/alertes) */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- LOGO & TITRE PERSONNALISÉ (EN-TÊTE HERO) ---
LOGO_SVG = """<svg width="90" height="90" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="64" height="64" rx="14" fill="url(#grad_bg)"/>
<rect x="10" y="22" width="32" height="24" rx="2" fill="white" fill-opacity="0.25"/>
<path d="M44 28H52L56 34V46H44V28Z" fill="white"/>
<rect x="13" y="25" width="14" height="18" rx="2" fill="#ff9800"/>
<rect x="29" y="33" width="10" height="10" rx="2" fill="#4caf50"/>
<rect x="29" y="25" width="10" height="6" rx="2" fill="#ffcc80"/>
<circle cx="18" cy="46" r="4.5" fill="white"/>
<circle cx="18" cy="46" r="2" fill="#0288d1"/>
<circle cx="34" cy="46" r="4.5" fill="white"/>
<circle cx="34" cy="46" r="2" fill="#0288d1"/>
<circle cx="50" cy="46" r="4.5" fill="white"/>
<circle cx="50" cy="46" r="2" fill="#0288d1"/>
<defs>
<linearGradient id="grad_bg" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
<stop stop-color="#0288d1"/>
<stop offset="1" stop-color="#1565c0"/>
</linearGradient>
</defs>
</svg>"""

st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 2rem 0; margin-bottom: 2rem; background: linear-gradient(180deg, rgba(245,247,250,0) 0%, rgba(227,235,243,0.3) 100%); border-radius: 0 0 30px 30px;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
        {LOGO_SVG}
        <h1 style="margin: 0; padding: 0; background: -webkit-linear-gradient(135deg, #0288d1, #2e7d32); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.2em; font-weight: 900; letter-spacing: -1px; line-height: 1.2;">
            Calculateur de Chargement
        </h1>
    </div>
</div>
""", unsafe_allow_html=True)


# --- AIDE MÉMOIRE SVG ANIMÉ (BARRE LATÉRALE) ---
st.sidebar.markdown("""
<div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 1rem;">
    <svg viewBox="0 0 500 250" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#1b5e20" /></marker>
            <marker id="arrowhead-start" markerWidth="10" markerHeight="7" refX="1" refY="3.5" orient="auto"><polygon points="10 0, 0 3.5, 10 7" fill="#1b5e20" /></marker>
        </defs>
        <style>
            .cube-front { fill: rgba(129, 199, 132, 0.2); stroke: #388e3c; stroke-width: 2; stroke-linejoin: round; }
            .cube-top { fill: rgba(129, 199, 132, 0.4); stroke: #388e3c; stroke-width: 2; stroke-linejoin: round; }
            .cube-side { fill: rgba(129, 199, 132, 0.6); stroke: #388e3c; stroke-width: 2; stroke-linejoin: round; }
            .cube-back { stroke: rgba(56, 142, 60, 0.3); stroke-width: 1.5; stroke-dasharray: 4; fill: none; }
            .dim-line { stroke: #1b5e20; stroke-width: 2; marker-end: url(#arrowhead); marker-start: url(#arrowhead-start); }
            .dim-guide { stroke: rgba(27, 94, 32, 0.4); stroke-width: 1.5; stroke-dasharray: 3; }
            .dim-text { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; font-weight: 700; fill: #1b5e20; }
            @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-8px); } 100% { transform: translateY(0px); } }
            .floating { animation: float 4s ease-in-out infinite; }
        </style>
        <g class="floating">
            <polygon points="180,60 380,60 380,140 180,140" class="cube-back" />
            <line x1="120" y1="180" x2="180" y2="140" class="cube-back" />
            <line x1="120" y1="100" x2="180" y2="60" class="cube-back" />
            <polygon points="120,100 320,100 380,60 180,60" class="cube-top" />
            <polygon points="320,100 380,60 380,140 320,180" class="cube-side" />
            <polygon points="120,100 320,100 320,180 120,180" class="cube-front" />
            <line x1="120" y1="180" x2="120" y2="210" class="dim-guide" />
            <line x1="320" y1="180" x2="320" y2="210" class="dim-guide" />
            <line x1="120" y1="100" x2="90" y2="100" class="dim-guide" />
            <line x1="120" y1="180" x2="90" y2="180" class="dim-guide" />
            <line x1="320" y1="180" x2="345" y2="195" class="dim-guide" />
            <line x1="380" y1="140" x2="405" y2="155" class="dim-guide" />
            <line x1="120" y1="205" x2="320" y2="205" class="dim-line" />
            <text x="220" y="228" text-anchor="middle" class="dim-text">Longueur</text>
            <line x1="95" y1="100" x2="95" y2="180" class="dim-line" />
            <text x="80" y="140" text-anchor="middle" transform="rotate(-90 80 140)" class="dim-text">Hauteur</text>
            <line x1="340" y1="190" x2="400" y2="150" class="dim-line" />
            <text x="395" y="190" text-anchor="middle" class="dim-text">Largeur</text>
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# --- MENU MANUEL ---
afficher_manuel = st.sidebar.checkbox("📖 Afficher le manuel d'utilisation")
st.sidebar.markdown("---")

if afficher_manuel:
    st.title("📖 Manuel d'Utilisation")
    st.info("👉 Décochez la case '📖 Afficher le manuel d'utilisation' dans le menu à gauche pour revenir au calculateur.")
    st.markdown("""
    ## 1. Comprendre l'Interface
    L'application est divisée en deux parties principales :
    * **À gauche (Le panneau de configuration) :** C'est ici que vous renseignez les dimensions du camion et des colis. Il est divisé en blocs de couleurs.
    * **À droite (Les résultats) :** C'est ici qu'apparaissent les schémas calculés en temps réel.

    > 💡 **Astuce "Aide-mémoire" :** En haut du menu à gauche, une animation en 3D vous rappelle à quoi correspondent la Longueur, la Largeur et la Hauteur pour éviter toute erreur de saisie !

    ## 2. Étape par Étape : Comment configurer votre chargement ?
    
    ### 🗄️ ÉTAPE 1 : La Base de données intégrée
    Toutes les dimensions de vos contenants (VC52, 03VER, etc.) sont **directement intégrées et mémorisées**.

    ### 🟦 ÉTAPE 2 : Le Camion (Bloc Bleu)
    Renseignez les dimensions utiles intérieures de votre camion ou remorque (en mètres).

    ### 🟧 ÉTAPE 3 : Les Charges Principales (Bloc Orange)
    C'est la marchandise principale que vous souhaitez charger.
    1. **Choisissez le Mode de remplissage :**
       - **Automatique :** L'algorithme calculera le maximum de charges possibles.
       - **Manuel :** Si vous devez charger exactement 20 palettes, sélectionnez "Manuel" et tapez "20".
    2. **Saisie des dimensions :** Laissez sur **"Depuis la base"** et tapez le nom de votre contenant (ex: `VC...`). L'application trouvera automatiquement la suite !
    3. **Gerbage max :** Indiquez combien de charges peuvent être empilées.

    ### 🟩 ÉTAPE 4 : Les Conteneurs Secondaires (Bloc Vert) - *Optionnel*
    Si vous devez expédier des conteneurs spécifiques en plus, cochez la case *"J'ai des conteneurs spécifiques..."*.
    * Renseignez leurs quantités et dimensions.

    ---
    ## 3. Comprendre les Résultats (Panneau de Droite)
    L'application calcule automatiquement les deux orientations possibles et **vous affiche directement la plus performante**. Un bilan s'affiche pour vous indiquer le nombre de camions nécessaires si vous dépassez la capacité !
    """)
    st.stop() # Arrête l'exécution ici pour masquer le calculateur en dessous


# --- BARRE LATÉRALE : ENTRÉES UTILISATEUR CLOISONNÉES ---

# BLOC 1 : CAMION (Bleu)
with st.sidebar.container(border=True):
    st.markdown("""
    <div id='marker-camion' style='background: linear-gradient(135deg, #0288d1, #29b6f6); padding: 12px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h4 style='margin:0; color: white; text-align:center;'>📏 Dimensions du Camion</h4>
    </div>
    """, unsafe_allow_html=True)
    camion_L = st.number_input("Longueur du plancher (m)", min_value=1.0, value=float(cfg.get("camion_L", 13.5)), step=0.1)
    camion_l = st.number_input("Largeur du plancher (m)", min_value=1.0, value=float(cfg.get("camion_l", 2.4)), step=0.1)
    camion_h = st.number_input("Hauteur utile max (m)", min_value=1.0, value=float(cfg.get("camion_h", 2.7)), step=0.1)

# BLOC 2 : CHARGES PRINCIPALES (Orange)
with st.sidebar.container(border=True):
    st.markdown("""
    <div id='marker-charges' style='background: linear-gradient(135deg, #e65100, #ff9800); padding: 12px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h4 style='margin:0; color: white; text-align:center;'>📦 Charges Principales</h4>
    </div>
    """, unsafe_allow_html=True)
    def_mode_calcul = cfg.get("mode_calcul", "Automatique (Remplir l'espace)")
    idx_mode = 0 if def_mode_calcul == "Automatique (Remplir l'espace)" else 1
    mode_calcul = st.radio("Mode de remplissage :", ["Automatique (Remplir l'espace)", "Manuel (Quantité exacte)"], index=idx_mode)

    if mode_calcul == "Manuel (Quantité exacte)":
        saved_qte = int(cfg.get("qte_principale_demandee", 34))
        safe_qte = saved_qte if saved_qte >= 0 else 34
        qte_principale_demandee = st.number_input("Nombre exact de charges à placer", min_value=0, value=safe_qte, step=1)
    else:
        qte_principale_demandee = -1

    # Recherche sécurisée via Base de données
    if len(liste_contenants) > 0:
        def_source_princ = cfg.get("source_princ", "Depuis la base")
        idx_src_princ = 0 if def_source_princ == "Depuis la base" else 1
        source_princ = st.radio("Saisie des dimensions :", ["Depuis la base", "Manuelle"], key="src_princ", horizontal=True, index=idx_src_princ)
    else:
        source_princ = "Manuelle"
        st.warning("⚠️ Impossible de lire les contenants de la base de données. Format CSV invalide.")

    nom_charge = None
    if source_princ == "Depuis la base":
        def_nom_charge = cfg.get("nom_charge", "PF08")
        if def_nom_charge not in liste_contenants:
            def_nom_charge = 'PF08' if 'PF08' in liste_contenants else liste_contenants[0]
        idx_defaut_princ = liste_contenants.index(def_nom_charge)
        nom_charge = st.selectbox("Rechercher le contenant :", liste_contenants, index=idx_defaut_princ, key="sel_princ")
        
        row_princ = df_db[df_db['CTT Magasin'].astype(str).str.strip() == nom_charge]
        if not row_princ.empty:
            row_princ = row_princ.iloc[0]
            charge_L = float(row_princ['Longueur Ext (mm)']) / 1000.0
            charge_l = float(row_princ['Largeur Ext (mm)']) / 1000.0
            charge_h = float(row_princ['Hauteur Ext (mm)']) / 1000.0
            st.info(f"📏 **Dimensions trouvées :**\n\nLong: **{charge_L}m** | Larg: **{charge_l}m** | Haut: **{charge_h}m**")
        else:
            st.error("Erreur de récupération.")
            charge_L, charge_l, charge_h = 1.0, 1.2, 0.62
    else:
        charge_L = st.number_input("Longueur de la charge (m)", min_value=0.01, value=float(cfg.get("charge_L", 1.00)), step=0.01)
        charge_l = st.number_input("Largeur de la charge (m)", min_value=0.01, value=float(cfg.get("charge_l", 1.20)), step=0.01)
        charge_h = st.number_input("Hauteur de la charge (m)", min_value=0.01, value=float(cfg.get("charge_h", 0.62)), step=0.01)

    st.markdown('<div style="margin-top: 10px; margin-bottom: 5px;"><strong>⚙️ Contraintes</strong></div>', unsafe_allow_html=True)
    gerbage_autorise = st.number_input("Gerbage max (Combien de charges empilées max ?)", min_value=1, value=int(cfg.get("gerbage_autorise", 3)), step=1)

# BLOC 3 : CONTENEURS (Vert) DYNAMIQUE
with st.sidebar.container(border=True):
    st.markdown("""
    <div id='marker-conteneurs' style='background: linear-gradient(135deg, #2e7d32, #4caf50); padding: 12px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h4 style='margin:0; color: white; text-align:center;'>🧮 Conteneurs Secondaires</h4>
    </div>
    <div id='conteneurs-header'></div>
    """, unsafe_allow_html=True)
    inclure_conteneurs = st.checkbox("J'ai des conteneurs spécifiques à charger absolument", value=bool(cfg.get("inclure_conteneurs", False)))
    conteneurs_data = []
    raw_cont_data = []

    if inclure_conteneurs:
        couleurs_vert = ["#4caf50", "#43a047", "#388e3c", "#2e7d32", "#1b5e20"]
        dynamic_css = "<style>\n"
        
        saved_conts = cfg.get("conteneurs_list", [])

        for i in range(st.session_state.nb_conteneurs):
            saved_c = saved_conts[i] if i < len(saved_conts) else {}
            color = couleurs_vert[i % len(couleurs_vert)]
            
            # Création d'une "sous-carte" bien cloisonnée pour chaque type
            with st.container(border=True):
                st.markdown(f"<div id='marker-type-{i}'></div><b style='color: {color}; font-size: 1.1em;'>📦 Type {i+1}</b><hr style='margin: 5px 0; border: 1px dashed {color};'>", unsafe_allow_html=True)
                
                cont_qte = st.number_input(f"Nombre de conteneurs", min_value=0, value=int(saved_c.get("qte_exacte", 0)), step=1, key=f"qte_{i}")
                
                # Choix Manuel vs Base de données pour ce conteneur
                if len(liste_contenants) > 0:
                    def_src_sec = saved_c.get("source_sec", "Depuis la base")
                    idx_src_sec = 0 if def_src_sec == "Depuis la base" else 1
                    source_sec = st.radio("Saisie des dimensions :", ["Depuis la base", "Manuelle"], key=f"src_sec_{i}", horizontal=True, label_visibility="collapsed", index=idx_src_sec)
                else:
                    source_sec = "Manuelle"

                nom_cont = None
                if source_sec == "Depuis la base":
                    def_nom_cont = saved_c.get("nom_cont", "VC52")
                    if def_nom_cont not in liste_contenants:
                        def_nom_cont = 'VC52' if 'VC52' in liste_contenants else liste_contenants[0]
                    idx_defaut_sec = liste_contenants.index(def_nom_cont)
                    nom_cont = st.selectbox(f"Rechercher le contenant {i+1} :", liste_contenants, index=idx_defaut_sec, key=f"sel_sec_{i}")
                    
                    row_sec = df_db[df_db['CTT Magasin'].astype(str).str.strip() == nom_cont]
                    if not row_sec.empty:
                        row_sec = row_sec.iloc[0]
                        cont_L = float(row_sec['Longueur Ext (mm)']) / 1000.0
                        cont_l = float(row_sec['Largeur Ext (mm)']) / 1000.0
                        cont_h = float(row_sec['Hauteur Ext (mm)']) / 1000.0
                        st.info(f"📏 **Dimensions trouvées :**\n\nLong: **{cont_L}m** | Larg: **{cont_l}m** | Haut: **{cont_h}m**")
                    else:
                        cont_L, cont_l, cont_h = 2.25, 1.50, 0.92
                else:
                    col_L, col_l = st.columns(2)
                    with col_L: cont_L = st.number_input("Long. (m)", min_value=0.01, value=float(saved_c.get("L", 2.25)), step=0.01, key=f"L_{i}")
                    with col_l: cont_l = st.number_input("Larg. (m)", min_value=0.01, value=float(saved_c.get("l", 1.50)), step=0.01, key=f"l_{i}")
                    cont_h = st.number_input("Hauteur (m)", min_value=0.01, value=float(saved_c.get("h", 0.92)), step=0.01, key=f"h_{i}")

                cont_gerbage = st.number_input(f"Gerbage max de ce contenant", min_value=1, value=int(saved_c.get("gerbage", 2)), step=1, key=f"gerb_{i}")
                
                conteneurs_data.append({
                    "qte_exacte": cont_qte, "L": cont_L, "l": cont_l, "h": cont_h, "gerbage": cont_gerbage,
                    "color": color
                })

                raw_cont_data.append({
                    "qte_exacte": cont_qte,
                    "source_sec": source_sec,
                    "nom_cont": nom_cont if source_sec == "Depuis la base" else None,
                    "L": cont_L if source_sec == "Manuelle" else 2.25,
                    "l": cont_l if source_sec == "Manuelle" else 1.50,
                    "h": cont_h if source_sec == "Manuelle" else 0.92,
                    "gerbage": cont_gerbage
                })
                
            # Teinter légèrement les sous-blocs avec effet semi-transparent sur fond blanc
            dynamic_css += f"""
            div[data-testid="stVerticalBlockBorderWrapper"]:has(#marker-type-{i}) {{
                background-color: rgba(255, 255, 255, 0.6) !important; 
                border-left: 6px solid {color} !important;
                border-radius: 8px !important;
                margin-top: 15px;
            }}
            """
            
        dynamic_css += "</style>"
        st.markdown(dynamic_css, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        if col1.button("➕ Ajouter un type"):
            st.session_state.nb_conteneurs += 1
            st.rerun()
        if st.session_state.nb_conteneurs > 1:
            if col2.button("➖ Retirer type"):
                st.session_state.nb_conteneurs -= 1
                st.rerun()

# --- BOUTON DE SAUVEGARDE ---
st.sidebar.markdown("---")
if st.sidebar.button("💾 Sauvegarder ma configuration par défaut"):
    config_to_save = {
        "camion_L": camion_L,
        "camion_l": camion_l,
        "camion_h": camion_h,
        "mode_calcul": mode_calcul,
        "qte_principale_demandee": qte_principale_demandee,
        "source_princ": source_princ,
        "nom_charge": nom_charge if source_princ == "Depuis la base" else None,
        "charge_L": charge_L if source_princ == "Manuelle" else 1.0,
        "charge_l": charge_l if source_princ == "Manuelle" else 1.2,
        "charge_h": charge_h if source_princ == "Manuelle" else 0.62,
        "gerbage_autorise": gerbage_autorise,
        "inclure_conteneurs": inclure_conteneurs,
        "nb_conteneurs": st.session_state.nb_conteneurs,
        "conteneurs_list": raw_cont_data if inclure_conteneurs else []
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_to_save, f)
        st.session_state.saved_config = config_to_save
        st.sidebar.success("Configuration sauvegardée ! Elle sera rechargée au prochain lancement.")
    except Exception as e:
        st.sidebar.error("Erreur lors de la sauvegarde du fichier.")


# --- 1. CALCUL DE L'ESPACE PRIS PAR LES CONTENEURS FIXES ---
longueur_amputee_totale = 0
conteneurs_places = []
erreur_conteneurs = False

if inclure_conteneurs:
    for cont in conteneurs_data:
        if cont["qte_exacte"] > 0:
            c_couches = min(math.floor(camion_h / cont["h"]) if cont["h"] > 0 else 0, cont["gerbage"])
            if c_couches > 0:
                places_sol = math.ceil(cont["qte_exacte"] / c_couches)
                
                # Test Orientation A
                nb_l_A = math.floor(camion_l / cont["l"]) if cont["l"] > 0 else 0
                len_A = math.ceil(places_sol / nb_l_A) * cont["L"] if nb_l_A > 0 else float('inf')
                
                # Test Orientation B
                nb_l_B = math.floor(camion_l / cont["L"]) if cont["L"] > 0 else 0
                len_B = math.ceil(places_sol / nb_l_B) * cont["l"] if nb_l_B > 0 else float('inf')
                
                if len_A <= len_B and len_A != float('inf'):
                    l_amp = len_A
                    c_rangees = math.ceil(places_sol / nb_l_A)
                    c_largeur = nb_l_A
                    c_dim_x = cont["L"]
                    c_dim_y = cont["l"]
                elif len_B != float('inf'):
                    l_amp = len_B
                    c_rangees = math.ceil(places_sol / nb_l_B)
                    c_largeur = nb_l_B
                    c_dim_x = cont["l"]
                    c_dim_y = cont["L"]
                else:
                    l_amp = float('inf')
                    erreur_conteneurs = True
            else:
                l_amp = float('inf')
                erreur_conteneurs = True

            if not erreur_conteneurs:
                conteneurs_places.append({
                    "l_amp": l_amp, "rangees": c_rangees, "largeur": c_largeur,
                    "dim_x": c_dim_x, "dim_y": c_dim_y, "couches": c_couches,
                    "qte_sol": places_sol, "h": cont["h"], "color": cont["color"], "qte_exacte": cont["qte_exacte"]
                })
                longueur_amputee_totale += l_amp

L_dispo = round(max(0.0, camion_L - longueur_amputee_totale), 2)

# --- 2. CALCUL DES CHARGES PRINCIPALES DANS L'ESPACE RESTANT ---
couches_possibles_hauteur = math.floor(camion_h / charge_h) if charge_h > 0 else 0
couches_reelles = min(couches_possibles_hauteur, gerbage_autorise)

qte_opt1 = qte_opt2 = 0
rangees1 = largeur1 = rangees2 = largeur2 = 0
erreur_manuelle_opt1 = erreur_manuelle_opt2 = False

if L_dispo >= 0 and not erreur_conteneurs and longueur_amputee_totale <= camion_L and charge_L > 0 and charge_l > 0:
    # Scénario A (Orientation 1)
    max_L1 = math.floor(L_dispo / charge_L)
    max_l1 = math.floor(camion_l / charge_l)
    capa_max_1 = max_L1 * max_l1 * couches_reelles
    
    if mode_calcul == "Automatique (Remplir l'espace)":
        qte_opt1 = capa_max_1
    else:
        qte_opt1 = min(qte_principale_demandee, capa_max_1)
        if qte_principale_demandee > capa_max_1: erreur_manuelle_opt1 = True
        
    if qte_opt1 > 0:
        spots1 = math.ceil(qte_opt1 / couches_reelles)
        rangees1 = math.ceil(spots1 / max_l1) if max_l1 > 0 else 0
        largeur1 = max_l1

    # Scénario B (Orientation 2)
    max_L2 = math.floor(L_dispo / charge_l)
    max_l2 = math.floor(camion_l / charge_L)
    capa_max_2 = max_L2 * max_l2 * couches_reelles
    
    if mode_calcul == "Automatique (Remplir l'espace)":
        qte_opt2 = capa_max_2
    else:
        qte_opt2 = min(qte_principale_demandee, capa_max_2)
        if qte_principale_demandee > capa_max_2: erreur_manuelle_opt2 = True
        
    if qte_opt2 > 0:
        spots2 = math.ceil(qte_opt2 / couches_reelles)
        rangees2 = math.ceil(spots2 / max_l2) if max_l2 > 0 else 0
        largeur2 = max_l2

# --- FONCTION DE DESSIN UNIQUE (RÉSOLUTION BUG VISUEL) ---
def dessiner_chargement_complet(qte_totale, couches, rangees, largeur, dim_x, dim_y, dim_h):
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.15,
        subplot_titles=("<b>Plan au sol (Vue de dessus)</b>", "<b>Plan en hauteur (Vue latérale)</b>")
    )

    # --- LIGNE 1 : VUE DE DESSUS ---
    fig.add_shape(type="rect", x0=0, y0=0, x1=camion_L, y1=camion_l,
                  line=dict(color="red", width=3), fillcolor="rgba(0,0,0,0)", row=1, col=1)

    if qte_totale > 0:
        items_left = qte_totale
        for i in range(rangees):
            for j in range(largeur):
                if items_left > 0:
                    items_in_stack = min(items_left, couches)
                    x0 = i * dim_x
                    y0 = j * dim_y
                    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+dim_x, y1=y0+dim_y,
                                  line=dict(color="black", width=1), fillcolor="skyblue", row=1, col=1)
                    # Ajout du texte "x2", "x1" etc. au milieu du bloc pour une lecture exacte
                    fig.add_annotation(
                        x=x0 + dim_x/2, y=y0 + dim_y/2,
                        text=f"<b>x{items_in_stack}</b>",
                        showarrow=False, font=dict(color="black", size=14),
                        row=1, col=1
                    )
                    items_left -= items_in_stack

    if inclure_conteneurs and longueur_amputee_totale <= camion_L and not erreur_conteneurs:
        current_start_x = camion_L 
        for cp in conteneurs_places:
            start_x = current_start_x - cp["l_amp"]
            items_left = cp["qte_exacte"]
            for i in range(cp["rangees"]):
                for j in range(cp["largeur"]):
                    if items_left > 0:
                        items_in_stack = min(items_left, cp["couches"])
                        x0 = start_x + i * cp["dim_x"]
                        y0 = j * cp["dim_y"]
                        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+cp["dim_x"], y1=y0+cp["dim_y"],
                                      line=dict(color="black", width=1, dash="dot"), fillcolor=cp["color"], row=1, col=1)
                        fig.add_annotation(
                            x=x0 + cp["dim_x"]/2, y=y0 + cp["dim_y"]/2,
                            text=f"<b>x{items_in_stack}</b>",
                            showarrow=False, font=dict(color="black", size=14),
                            row=1, col=1
                        )
                        items_left -= items_in_stack
            current_start_x = start_x

    # --- LIGNE 2 : VUE LATÉRALE (CORRIGÉ POUR SIMULER UN VRAI CARISTE) ---
    fig.add_shape(type="rect", x0=0, y0=0, x1=camion_L, y1=camion_h,
                  line=dict(color="red", width=3), fillcolor="rgba(0,0,0,0)", row=2, col=1)

    if qte_totale > 0:
        items_left = qte_totale
        for i in range(rangees):
            if items_left <= 0: break
            items_in_this_row = min(items_left, largeur * couches)
            # La hauteur profil de la rangée est dictée par la pile la plus haute dans cette rangée
            max_layers_in_row = min(items_in_this_row, couches)
            
            for k in range(max_layers_in_row):
                x0 = i * dim_x
                y0 = k * dim_h
                fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+dim_x, y1=y0+dim_h,
                              line=dict(color="black", width=1), fillcolor="skyblue", row=2, col=1)
            items_left -= items_in_this_row

    if inclure_conteneurs and longueur_amputee_totale <= camion_L and not erreur_conteneurs:
        current_start_x = camion_L
        for cp in conteneurs_places:
            start_x = current_start_x - cp["l_amp"]
            items_left = cp["qte_exacte"]
            for i in range(cp["rangees"]):
                if items_left <= 0: break
                items_in_this_row = min(items_left, cp["largeur"] * cp["couches"])
                max_layers_in_row = min(items_in_this_row, cp["couches"])
                
                for k in range(max_layers_in_row):
                    x0 = start_x + i * cp["dim_x"]
                    y0 = k * cp["h"]
                    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+cp["dim_x"], y1=y0+cp["h"],
                                  line=dict(color="black", width=1, dash="dot"), fillcolor=cp["color"], row=2, col=1)
                items_left -= items_in_this_row
            current_start_x = start_x

    # --- VERROUILLAGE DES PROPORTIONS ---
    fig.update_xaxes(
        title_text="Longueur Camion (m)", 
        range=[-0.5, camion_L + 0.5], 
        constrain='domain', 
        autorange=False,
        fixedrange=True,
        row=2, col=1
    )
    fig.update_yaxes(
        title_text="Largeur (m)", 
        range=[-0.5, max(camion_l, 3.0) + 0.5], 
        scaleanchor="x", 
        scaleratio=1, 
        constrain='domain', 
        autorange=False,
        fixedrange=True,
        row=1, col=1
    )
    fig.update_yaxes(
        title_text="Hauteur (m)", 
        range=[-0.5, max(camion_h, 3.0) + 0.5], 
        scaleanchor="x", 
        scaleratio=1, 
        constrain='domain', 
        autorange=False,
        fixedrange=True,
        row=2, col=1
    )
    
    fig.update_layout(
        height=700,
        autosize=True,
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=20),
        showlegend=False
    )
    return fig

# --- AFFICHAGE DES RÉSULTATS ---
st.header("📊 Résultats de l'optimisation")

# Variable pour traquer la nécessité de déclencher l'alerte visuelle rouge globale
alerte_globale = False

# 1. Vérification du débordement des conteneurs
if erreur_conteneurs or longueur_amputee_totale > camion_L:
    alerte_globale = True
    st.error(f"⚠️ Impossible ! L'ensemble des conteneurs prend plus de place que le camion (ou ne rentre pas en hauteur).")
else:
    # --- 2. Vérification des alertes de Plafond (Charges Principales) ---
    if couches_possibles_hauteur < gerbage_autorise and charge_h > 0:
        alerte_globale = True
        st.warning(f"⚠️ **Plafond atteint (Charges Principales) :** Vous avez autorisé un gerbage de {gerbage_autorise}, mais la hauteur du camion ({camion_h}m) limite physiquement l'empilement à **{couches_reelles} couches**.")

    # --- 3. Vérification des alertes de Plafond (Conteneurs Secondaires) ---
    if inclure_conteneurs:
        for i, cont in enumerate(conteneurs_data):
            if cont["qte_exacte"] > 0 and cont["h"] > 0:
                c_pos = math.floor(camion_h / cont["h"])
                if c_pos < cont["gerbage"] and c_pos > 0:
                    alerte_globale = True
                    st.warning(f"⚠️ **Plafond atteint (Conteneurs Type {i+1}) :** Vous avez autorisé un gerbage de {cont['gerbage']}, mais la hauteur du camion limite l'empilement à **{c_pos} couches**.")

    if inclure_conteneurs:
        qte_totale_cont = sum(c["qte_exacte"] for c in conteneurs_data)
        if qte_totale_cont > 0:
            st.info(f"🚚 **Espace réservé au fond :** Les {qte_totale_cont} conteneurs prennent **{longueur_amputee_totale} m** de long au sol. Il reste **{L_dispo} m** pour les charges principales.")

    # Déterminer la meilleure option pour l'affichage principal
    if qte_opt1 >= qte_opt2:
        best_opt, alt_opt = 1, 2
        best_qte, best_rangees, best_largeur, best_dim_L, best_dim_l, best_err = qte_opt1, rangees1, largeur1, charge_L, charge_l, erreur_manuelle_opt1
        alt_qte, alt_rangees, alt_largeur, alt_dim_L, alt_dim_l, alt_err = qte_opt2, rangees2, largeur2, charge_l, charge_L, erreur_manuelle_opt2
    else:
        best_opt, alt_opt = 2, 1
        best_qte, best_rangees, best_largeur, best_dim_L, best_dim_l, best_err = qte_opt2, rangees2, largeur2, charge_l, charge_L, erreur_manuelle_opt2
        alt_qte, alt_rangees, alt_largeur, alt_dim_L, alt_dim_l, alt_err = qte_opt1, rangees1, largeur1, charge_L, charge_l, erreur_manuelle_opt1

    # --- 4. Vérification d'espace insuffisant pour le mode Manuel ---
    if best_err:
        alerte_globale = True
        st.warning(f"⚠️ **Espace insuffisant :** Le camion est trop petit pour placer vos {qte_principale_demandee} charges demandées. Le maximum possible a été affiché.")

    # --- AFFICHAGE DE LA MEILLEURE OPTION ---
    st.subheader(f"🌟 Orientation Recommandée (Option {best_opt})")
        
    st.metric(label="Total de charges principales", value=f"{best_qte} charges")
    if best_qte > 0:
        st.write(f"- Jusqu'à **{best_rangees}** rangées dans la longueur")
        st.write(f"- Jusqu'à **{best_largeur}** charges côte à côte")
        st.write(f"- Jusqu'à **{couches_reelles}** charges superposées en hauteur")
    
    fig_best = dessiner_chargement_complet(best_qte, couches_reelles, best_rangees, best_largeur, best_dim_L, best_dim_l, charge_h)
    st.plotly_chart(fig_best, use_container_width=True, key="chart_best")

    # --- AFFICHAGE CACHÉ DE L'OPTION ALTERNATIVE ---
    titre_expander = "👀 Voir l'orientation alternative (Résultat équivalent)" if qte_opt1 == qte_opt2 else "👀 Voir l'orientation alternative (Moins optimale)"
    
    with st.expander(titre_expander):
        st.markdown(f"**Option {alt_opt}**")
        if alt_err:
            st.warning(f"⚠️ L'espace restant est insuffisant pour placer vos {qte_principale_demandee} charges. Le maximum possible a été affiché.")
            
        st.metric(label="Total de charges principales", value=f"{alt_qte} charges")
        if alt_qte > 0:
            st.write(f"- Jusqu'à **{alt_rangees}** rangées dans la longueur")
            st.write(f"- Jusqu'à **{alt_largeur}** charges côte à côte")
            st.write(f"- Jusqu'à **{couches_reelles}** charges superposées en hauteur")
            
        fig_alt = dessiner_chargement_complet(alt_qte, couches_reelles, alt_rangees, alt_largeur, alt_dim_L, alt_dim_l, charge_h)
        st.plotly_chart(fig_alt, use_container_width=True, key="chart_alt")

# --- INJECTION DE L'ANIMATION GLOBALE (SI ALERTE DÉCLENCHÉE) ---
if alerte_globale:
    st.markdown("""
    <div id="overlay-rouge-clignotant"></div>
    <style>
    /* 1. L'overlay global rouge translucide */
    #overlay-rouge-clignotant {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none; /* Très important : permet de cliquer à travers l'alerte ! */
        z-index: 999999;
        animation: ecran-rouge 1.5s infinite;
    }
    @keyframes ecran-rouge {
        0%, 100% { background-color: rgba(255, 0, 0, 0); }
        50% { background-color: rgba(255, 0, 0, 0.15); } /* Rouge translucide */
    }
    
    /* 2. Effet de pulsation sur TOUS les messages d'alerte (jaunes et rouges) */
    div[data-testid="stAlert"] {
        animation: pulse-alert 1.5s infinite !important;
        border-left: 6px solid red !important;
    }
    @keyframes pulse-alert {
        0%, 100% { transform: scale(1); box-shadow: none; }
        50% { transform: scale(1.02); box-shadow: 0 0 20px rgba(255, 0, 0, 0.4); }
    }
    </style>
    """, unsafe_allow_html=True)
