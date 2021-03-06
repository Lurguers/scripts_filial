def base(bases):
    bases = bases.split('(')
    bases[0] = 'Bases.compor'
    bases[1] = bases[1].replace(')', '').replace(';', '').split(',')

    if bases[1][0] == 'vlrcalc':
        bases[1][0] = 'valorCalculado'
    elif bases[1][0] == 'vlrref':
        bases[1][0] = 'valorReferencia'
    elif bases[1][0] == 'salcontr':
        bases[1][0] = 'Funcionario.salario'

    basesDict = {242: '13DEFEAJPR',
241: '13DEFEPR',
40: 'TERFERVENRES',
28: 'ABATINSS',
21: 'ABATIRRF',
22: 'ABATIRRF13',
41: 'BASEAUXI1',
42: 'BASEAUXI2',
48: 'BAPEAF',
46: 'CESTABASICA',
47: 'CESBAS47',
39: 'COMPHORAMES',
36: 'CONTSIND',
38: 'DESC13REINT',
29: 'DESCTERFER',
23: 'DESCIRRF',
24: 'DESCIRRF13',
25: 'DESCIRRFERES',
248: 'DEVINSS',
247: 'DEVIRRF',
26: 'EXCEINSS',
27: 'EXCEINSS13',
6: 'FGTS',
7: 'FGTS13',
218: 'FG13SAAJPR',
219: 'FG13SAESPR',
217: 'FG13SAPR',
20: 'FGTSAVISO',
238: 'FGFEAJPR',
239: 'FGFEESPR',
237: 'FGFEPR',
15: 'FUNDASS',
16: 'FUNDASS13',
214: 'FUAS13SAAJPR',
216: 'FUAS13SADI',
215: 'FUAS13SAESPR',
213: 'FUAS13SAPR',
234: 'FUASFEAJPR',
236: 'FUASFEDI',
235: 'FUASFEESPR',
233: 'FUASFEPR',
201: 'FUNDFIN',
202: 'FUNDFIN13',
17: 'FUNDOPREV',
18: 'FUNDPREV13',
206: 'FUPR13SAAJPR',
208: 'FUPR13SADI',
207: 'FUPR13SAESPR',
205: 'FUPR13SAPR',
51: 'FUPRAF48EDES',
226: 'FUPRFEAJPR',
228: 'FUPRFEDI',
227: 'FUPRFEESPR',
225: 'FUPRFEPR',
50: 'GR46SAEES',
3: 'HORAEXTRA',
11: 'INSS',
12: 'INSS13',
204: 'IN13SADI',
222: 'INFEAJPR',
224: 'INFEDI',
223: 'INFEESPR',
221: 'INFEPR',
32: 'INSSOUTRA13',
31: 'INSSOUTRA',
8: 'IRRF',
9: 'IRRF13',
35: 'IRRFFER',
10: 'IRRFFERRESC',
34: 'IRRFOUTRA13',
33: 'IRRFOUTRA',
37: 'MEDIAUXMAT',
203: 'MEDAUXMATPR',
19: 'OUTRASBASES',
1: 'PAGAPROP',
249: 'PARCISENIRRF',
250: 'PAISIR13SA',
4: 'PERIC',
13: 'PREVEST',
14: 'PREVEST13',
210: 'PRES13SAAJPR',
212: 'PRES13SADI',
211: 'PRES13SAESPR',
209: 'PRES13SAPR',
230: 'PRESFEAJPR',
232: 'PRESFEDI',
231: 'PRESFEESPR',
229: 'PRESFEPR',
245: 'PRBAAUDI13SA',
246: 'PRBAAUDIFE',
244: 'PRBAAUMEHO13',
243: 'PRBAAUMEHOFE',
52: 'RESA20ED49ES',
49: 'RESADE20',
2: 'SALBASE',
43: 'SALFAMEST',
30: 'SALAFAM',
44: 'SALFAMNOR',
5: 'SIND',
45: 'TRIENIO'}

    for i in range(1, len(bases[1])):
        bases[1][i] = 'Bases.' + basesDict[int(bases[1][i])]

    bases[1] = ',\n'.join(bases[1])
    bases = '('.join(bases) + ')'
    return bases

print(base('montabase(vlrcalc, 6,8,11,15,36,43,47);'))
