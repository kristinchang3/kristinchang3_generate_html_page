
def domain(region, **kwargs):

    swap = False

    if region == 'California':

        lats = 34
        latn = 42
        lonw = -126 +360
        lone = -119 + 360

    elif region in ['SAmerica','S.America','S America']:

        lats = -56
        latn = -30
        lonw = -76 + 360
        lone = -68 + 360

    elif region in ['WAfrica','W.Africa','W Africa']:

        lats = 10
        latn = 35
        lonw = -19 + 360
        lone = -5 + 360

    elif region in ['WEurope','W.Europe','W Europe']:

        swap = True

        lats = 35
        latn = 49.8
        lonw = -10 + 360
        lone = 3.5

    elif region in ['NEurope','N.Europe','N Europe']:

        lats = 53
        latn = 70
        lonw = 3.5
        lone = 20

    elif region == 'UK':

        swap = True
        
        lats = 49.8
        latn = 60
        lonw = -10 + 360
        lone = 2

    elif region == 'Baja':

        lats = 20
        latn = 36
        lonw = -119 + 360
        lone = -105 + 360

    elif region in ['PAC NW','PAC_NW','PAC. NW','PAC.NW','Pacific Northwest','Pacific NW']:

        lats = 42
        latn = 51
        lonw = -126 + 360
        lone = -119 + 360

    elif region == 'Australia':

        lats = -35.5
        latn = -23
        lonw = 112.8
        lone = 120

    elif region in ['SAfrica','S.Africa','S Africa']:

        lats = -35.5
        latn = -21
        lonw = 11
        lone = 20

    elif region in ['New Zealand','New_Zealand']:

        lats = -46.5
        latn = -34
        lonw = 166
        lone = 179

    elif region == 'Alaska':

        lats = 53
        latn = 63
        lonw = -170 + 360
        lone = -130 + 360

    elif region == 'Greenland':

        lats = 59.5
        latn = 71
        lonw = -55 + 360
        lone = -35 + 360

    elif region == 'Antarctica':

        lats = -77
        latn = -62
        lonw = -94 + 360
        lone = -57 + 360

    elif region in ['EAsia','E.Asia','E Asia']:

        lats = 30
        latn = 41
        lonw = 125
        lone = 141

    elif region in ['New England', 'New_England']:

        lats = 38
        latn = 47
        lonw = -77 + 360
        lone = -64 + 360

    elif region == 'Iceland':

        lats = 63
        latn = 67.5
        lonw = -25 + 360
        lone = -13 + 360


### global

    elif region in ['global','Global']:
        lats = -70
        latn = 75
        lonw = 0
        lone = 360

###  ocean basin

    elif region in ['NPacific','N.Pacific','N Pacific','N. Pacific', 'North Pacific']:

        lats = 0
        latn = 67
        lonw = 99
        lone = 262

    elif region in ['SPacific','S.Pacific','S Pacific', 'S. Pacific', 'South Pacific']:

        lats = -70
        latn = 0
        lonw = 142
        lone = -70 + 360

    elif region in ['NAtlantic','N.Atlantic','N Atlantic', 'N. Atlantic', 'North Atlantic']:

        lats = 0
        latn = 75
        lonw = -80 + 360
        lone = 10

    elif region in ['SAtlantic','S.Atlantic','S Atlantic', 'S. Atlantic', 'South Atlantic']:

        lats = -70
        latn = 0
        lonw = -70 + 360 
        lone = 20

    elif region in ['Indian', 'Indian Ocean']:

        lats = -70 
        latn = 0 
        lonw = 30
        lone = 120

    else:
        lats = kwargs[lats]
        latn = kwargs[latn]
        lonw = kwargs[lonw]
        lone = kwargs[lone]


    return lats, latn, lonw, lone
