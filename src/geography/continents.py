import awoc as awoc

class OurWorld():
    our_world = awoc.AWOC()
    
    CONTINENTS   = our_world.get_continents_list()
    Africa       = our_world.get_countries_list_of(CONTINENTS[0])
    Anarctica    = our_world.get_countries_list_of(CONTINENTS[1])
    Asia         = our_world.get_countries_list_of(CONTINENTS[2])
    Europe       = our_world.get_countries_list_of(CONTINENTS[3])
    NorthAmerica = our_world.get_countries_list_of(CONTINENTS[4])
    Oceania      = our_world.get_countries_list_of(CONTINENTS[5])
    SouthAmerica = our_world.get_countries_list_of(CONTINENTS[6])

    ContinentLatLong = {'Africa': [11.5024338, 17.7578122],
                         'Antarctica': [-79.4063075, 0.3149312], 
                         'Asia': [51.2086975, 89.2343748], 
                         'Europe': [51.0, 10.0], 
                         'North America': [51.0000002, -109.0], 
                         'Oceania': [-18.3128, 138.5156], 
                         'South America': [-21.0002179, -61.0006565]
                         }
    
    CZ      = "Czechia"
    CZ_FULL = "Czech Republic" 
    
    CountryLatLong = {'Algeria': [28.0000272, 2.9999825],
                      'Angola': [-11.8775768, 17.5691241], 
                      'Benin': [9.5293472, 2.2584408], 
                      'Botswana': [-23.1681782, 24.5928742], 
                      'Burkina Faso': [12.0753083, -1.6880314], 
                      'Burundi': [-3.426449, 29.9324519], 
                      'Cameroon': [4.6125522, 13.1535811], 
                      'Cape Verde': [16.0000552, -24.0083947], 
                      'Central African Republic': [7.0323598, 19.9981227], 
                      'Chad': [15.6134137, 19.0156172], 
                      'Comoros': [-12.2045176, 44.2832964], 
                      'Democratic Republic of the Congo': [-2.9814344, 23.8222636], 
                      'Djibouti': [11.8145966, 42.8453061], 
                      'Egypt': [26.2540493, 29.2675469], 
                      'Equatorial Guinea': [1.613172, 10.5170357], 
                      'Eritrea': [15.9500319, 37.9999668], 
                      'Ethiopia': [10.2116702, 38.6521203], 
                      'Gabon': [-0.8999695, 11.6899699], 
                      'Gambia': [13.470062, -15.4900464],
                      'Ghana': [8.0300284, -1.0800271], 
                      'Guinea': [10.7226226, -10.7083587], 
                      'Guinea-Bissau': [12.100035, -14.9000214], 
                      'Ivory Coast': [7.9897371, -5.5679458], 
                      'Kenya': [1.4419683, 38.4313975], 
                      'Lesotho': [-29.6039267, 28.3350193], 
                      'Liberia': [5.7499721, -9.3658524], 
                      'Libya': [26.8234472, 18.1236723], 
                      'Madagascar': [-18.9249604, 46.4416422], 
                      'Malawi': [-13.2687204, 33.9301963], 
                      'Mali': [16.3700359, -2.2900239], 
                      'Mauritania': [20.2540382, -9.2399263], 
                      'Mauritius': [-20.2759451, 57.5703566], 
                      'Mayotte': [-12.825543, 45.148490830203045], 
                      'Morocco': [31.1728205, -7.3362482], 
                      'Mozambique': [-19.302233, 34.9144977], 
                      'Namibia': [-23.2335499, 17.3231107], 
                      'Niger': [17.7356214, 9.3238432], 
                      'Nigeria': [9.6000359, 7.9999721], 
                      'Republic of the Congo': [-0.7264327, 15.6419155], 
                      'Reunion': [-21.130737949999997, 55.536480112992315], 
                      'Rwanda': [-1.9646631, 30.0644358], 
                      'Saint Helena': [-15.9694573, -5.7129442], 
                      'Sao Tome and Principe': [0.9713095, 7.02255], 
                      'Senegal': [14.4750607, -14.4529612], 
                      'Seychelles': [-4.6574977, 55.4540146], 
                      'Sierra Leone': [8.6400349, -11.8400269], 
                      'Somalia': [8.3676771, 49.083416], 
                      'South Africa': [-28.8166236, 24.991639], 
                      'South Sudan': [7.8699431, 29.6667897], 
                      'Sudan': [14.5844444, 29.4917691], 
                      'Swaziland': [-26.5624806, 31.3991317], 
                      'Tanzania': [-6.5247123, 35.7878438], 
                      'Togo': [8.7800265, 1.0199765], 
                      'Tunisia': [33.8439408, 9.400138], 
                      'Uganda': [1.5333554, 32.2166578], 
                      'Western Sahara': [24.16819605, -13.892143025000001], 
                      'Zambia': [-14.5189121, 27.5589884], 
                      'Zimbabwe': [-18.4554963, 29.7468414], 
                      'Antarctica': [-79.4063075, 0.3149312], 
                      'Afghanistan': [33.7680065, 66.2385139], 
                      'Armenia': [40.7696272, 44.6736646], 
                      'Azerbaijan': [40.3936294, 47.7872508], 
                      'Bahrain': [26.1551249, 50.5344606], 
                      'Bangladesh': [24.4769288, 90.2934413], 
                      'Bhutan': [27.549511, 90.5119273], 
                      'British Indian Ocean Territory': [-5.3497093499999995, 71.86064227010121], 
                      'Brunei': [4.4137155, 114.5653908], 
                      'Cambodia': [12.5433216, 104.8144914], 
                      'China': [35.000074, 104.999927], 
                      'Christmas Island': [-10.49124145, 105.6173514897963], 
                      'Cocos Islands': [-12.0728315, 96.8409375], 
                      'Georgia': [32.3293809, -83.1137366], 
                      'Hong Kong': [22.2793278, 114.1628131], 
                      'India': [22.3511148, 78.6677428], 
                      'Indonesia': [-2.4833826, 117.8902853], 
                      'Iran': [32.6475314, 54.5643516], 
                      'Iraq': [33.0955793, 44.1749775], 
                      'Israel': [30.8124247, 34.8594762], 
                      'Japan': [36.5748441, 139.2394179], 
                      'Jordan': [31.1667049, 36.941628], 
                      'Kazakhstan': [48.1012954, 66.7780818], 
                      'Kuwait': [29.2733964, 47.4979476], 
                      'Kyrgyzstan': [41.5089324, 74.724091], 
                      'Laos': [20.0171109, 103.378253], 
                      'Lebanon': [33.8750629, 35.843409], 
                      'Macau': [22.1899448, 113.5380454], 
                      'Malaysia': [4.5693754, 102.2656823], 
                      'Maldives': [3.7203503, 73.2244152], 
                      'Mongolia': [46.8250388, 103.8499736], 
                      'Myanmar': [17.1750495, 95.9999652], 
                      'Nepal': [28.1083929, 84.0917139], 
                      'North Korea': [40.3736611, 127.0870417], 
                      'Oman': [21.0000287, 57.0036901], 
                      'Pakistan': [30.3308401, 71.247499], 
                      'Palestine': [31.462420950000002, 34.262716572130714], 
                      'Philippines': [12.7503486, 122.7312101], 
                      'Qatar': [25.3336984, 51.2295295], 
                      'Saudi Arabia': [25.6242618, 42.3528328], 
                      'Singapore': [1.357107, 103.8194992], 
                      'South Korea': [36.638392, 127.6961188], 
                      'Sri Lanka': [7.5554942, 80.7137847], 
                      'Syria': [34.6401861, 39.0494106], 
                      'Taiwan': [23.9739374, 120.9820179], 
                      'Tajikistan': [38.6281733, 70.8156541], 
                      'Thailand': [14.8971921, 100.83273], 
                      'Turkey': [38.9597594, 34.9249653], 
                      'United Arab Emirates': [24.0002488, 53.9994829], 
                      'Uzbekistan': [41.32373, 63.9528098], 
                      'Vietnam': [15.9266657, 107.9650855], 
                      'Yemen': [16.3471243, 47.8915271], 
                      'Albania': [41.000028, 19.9999619], 
                      'Andorra': [42.5407167, 1.5732033], 
                      'Austria': [47.59397, 14.12456], 
                      'Belarus': [53.4250605, 27.6971358], 
                      'Belgium': [50.6402809, 4.6667145], 
                      'Bosnia and Herzegovina': [44.3053476, 17.5961467], 
                      'Bulgaria': [42.6073975, 25.4856617], 
                      'Croatia': [45.5643442, 17.0118954], 
                      'Cyprus': [34.9823018, 33.1451285], 
                      'Czech Republic': [49.7439047, 15.3381061], 
                      'Denmark': [55.670249, 10.3333283], 
                      'Estonia': [58.7523778, 25.3319078], 
                      'Faroe Islands': [62.0448724, -7.0322972], 
                      'Finland': [63.2467777, 25.9209164], 
                      'France': [46.603354, 1.8883335], 
                      'Germany': [51.1638175, 10.4478313], 
                      'Gibraltar': [36.1285933, -5.3474761], 
                      'Greece': [38.9953683, 21.9877132], 
                      'Guernsey': [49.4566233, -2.5822348], 
                      'Hungary': [47.1817585, 19.5060937], 
                      'Iceland': [64.9841821, -18.1059013], 
                      'Ireland': [52.865196, -7.9794599], 
                      'Isle of Man': [54.1936805, -4.5591148], 
                      'Italy': [42.6384261, 12.674297], 
                      'Jersey': [49.2214561, -2.1358386], 
                      'Kosovo': [42.5869578, 20.9021231], 
                      'Latvia': [56.8406494, 24.7537645], 
                      'Liechtenstein': [47.1416307, 9.5531527], 
                      'Lithuania': [55.3500003, 23.7499997], 
                      'Luxembourg': [49.8158683, 6.1296751], 
                      'Macedonia': [41.6171214, 21.7168387], 
                      'Malta': [35.8885993, 14.4476911], 
                      'Moldova': [47.2879608, 28.5670941], 
                      'Monaco': [43.7323492, 7.4276832], 
                      'Montenegro': [42.9868853, 19.5180992], 
                      'Netherlands': [52.2434979, 5.6343227], 
                      'Norway': [60.5000209, 9.0999715], 
                      'Poland': [52.215933, 19.134422], 
                      'Portugal': [39.6621648, -8.1353519], 
                      'Romania': [45.9852129, 24.6859225], 
                      'San Marino': [43.9458623, 12.458306], 
                      'Serbia': [44.1534121, 20.55144], 
                      'Slovakia': [48.7411522, 19.4528646], 
                      'Slovenia': [45.8133113, 14.4808369], 
                      'Spain': [39.3260685, -4.8379791], 
                      'Svalbard and Jan Mayen': [78.51240265, 16.605574070831505], 
                      'Sweden': [59.6749712, 14.5208584], 
                      'Switzerland': [46.7985624, 8.2319736], 
                      'Ukraine': [49.4871968, 31.2718321], 
                      'United Kingdom': [54.7023545, -3.2765753], 
                      'Vatican': [41.903411, 12.4528527], 
                      'Anguilla': [18.1954947, -63.0750234], 
                      'Antigua and Barbuda': [17.2234721, -61.9554608], 
                      'Aruba': [12.51756625, -69.98186415210564], 
                      'Bahamas': [24.7736546, -78.0000547], 
                      'Barbados': [13.1500331, -59.5250305], 
                      'Bermuda': [32.30382, -64.7561647], 
                      'British Virgin Islands': [18.4024395, -64.5661642], 
                      'Canada': [61.0666922, -107.991707], 
                      'Cayman Islands': [19.703182249999998, -79.9174627243246], 
                      'Costa Rica': [10.2735633, -84.0739102], 
                      'Cuba': [23.0131338, -80.8328748], 
                      'Curacao': [12.21339425, -69.0408499890865], 
                      'Dominica': [19.0974031, -70.3028026], 
                      'Dominican Republic': [19.0974031, -70.3028026], 
                      'El Salvador': [13.8000382, -88.9140683], 
                      'Greenland': [77.6192349, -42.8125967], 
                      'Grenada': [12.1360374, -61.6904045], 
                      'Guatemala': [15.5855545, -90.345759], 
                      'Haiti': [19.1399952, -72.3570972], 
                      'Honduras': [15.2572432, -86.0755145], 
                      'Jamaica': [18.1850507, -77.3947693], 
                      'Mexico': [23.6585116, -102.0077097], 
                      'Montserrat': [16.7417041, -62.1916844], 
                      'Netherlands Antilles': [12.1845, -68.6607922625], 
                      'Nicaragua': [12.6090157, -85.2936911], 
                      'Panama': [8.559559, -81.1308434], 
                      'Puerto Rico': [18.2247706, -66.4858295], 
                      'Saint Barthelemy': [17.9036287, -62.811568843006896], 
                      'Saint Kitts and Nevis': [17.250512, -62.6725973], 
                      'Saint Lucia': [13.8250489, -60.975036], 
                      'Saint Martin': [18.0814066, -63.0467131], 
                      'Saint Pierre and Miquelon': [46.783246899999995, -56.195158907484085], 
                      'Saint Vincent and the Grenadines': [12.90447, -61.2765569], 
                      'Sint Maarten': [18.0423736, -63.0549948], 
                      'Trinidad and Tobago': [10.7466905, -61.0840075], 
                      'Turks and Caicos Islands': [21.721746, -71.5527809], 
                      'U.S. Virgin Islands': [17.789187, -64.7080574], 
                      'United States': [39.7837304, -100.445882], 
                      'American Samoa': [-14.297124, -170.7131481], 
                      'Australia': [-24.7761086, 134.755], 
                      'Cook Islands': [-19.919672900000002, -157.9753368892878], 
                      'East Timor': [-8.5151979, 125.8375756], 
                      'Fiji': [-18.1239696, 179.0122737], 
                      'French Polynesia': [-17.0243749, -144.6434898], 
                      'Guam': [13.450125700000001, 144.75755102972062], 
                      'Kiribati': [0.3448612, 173.6641773], 
                      'Marshall Islands': [8.9995549, 168.0002575], 
                      'Micronesia': [8.6062347, 151.832744331612], 
                      'Nauru': [-0.5252306, 166.9324426], 
                      'New Caledonia': [-21.3019905, 165.4880773], 
                      'New Zealand': [-41.5000831, 172.8344077], 
                      'Niue': [-19.0536414, -169.861341], 
                      'Northern Mariana Islands': [15.1753648, 145.7379338], 
                      'Palau': [5.3783537, 132.9102573], 
                      'Papua New Guinea': [-5.6816069, 144.2489081], 
                      'Pitcairn': [-25.0657719, -130.101782], 
                      'Samoa': [-13.7693895, -172.12005], 
                      'Solomon Islands': [-8.7053941, 159.1070693851845], 
                      'Tokelau': [-9.1676396, -171.819687], 
                      'Tonga': [-19.9160819, -175.202642], 
                      'Tuvalu': [-8.6405212, 179.1582918181797], 
                      'Vanuatu': [-16.5255069, 168.1069154], 
                      'Wallis and Futuna': [-13.289402, -176.204224], 
                      'Argentina': [-34.9964963, -64.9672817], 
                      'Bolivia': [-17.0568696, -64.9912286], 
                      'Brazil': [-10.3333333, -53.2], 
                      'Chile': [-31.7613365, -71.3187697], 
                      'Colombia': [4.099917, -72.9088133], 
                      'Ecuador': [-1.3397668, -79.3666965], 
                      'Falkland Islands': [-51.9492937, -59.5383657], 
                      'Guyana': [4.8417097, -58.6416891], 
                      'Paraguay': [-23.3165935, -58.1693445], 
                      'Peru': [-6.8699697, -75.0458515], 
                      'Suriname': [4.1413025, -56.0771187], 
                      'Uruguay': [-32.8755548, -56.0201525], 
                      'Venezuela': [8.0018709, -66.1109318],
                      'Turkmenistan': [39.3763807, 59.3924609], 
                      'Russia': [64.6863136, 97.7453061], 
                      'Belize': [16.8259793, -88.7600927]
                      }