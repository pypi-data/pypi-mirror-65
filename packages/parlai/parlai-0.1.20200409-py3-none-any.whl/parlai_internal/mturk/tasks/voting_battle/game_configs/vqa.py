#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from .base import BaseGameConfig

class VqaGC(BaseGameConfig):
    '''
    This config is currently hardcoded to use the train set, so please use that
    I also suspect the train dataset causes the HIT to glitch out sometimes,
    so maybe we should stop doing that.
    '''

    TASK_NAME = 'vqa_v1'
    TASK_IDENTIFIER = 'vqa_vanilla'
    EXAMPLE_MODE = 'image_and_dialog'

    START_LABEL_MSG = '\nRound {}! Please look at the image and answer \
    the question. Please make your answer as short as possible.'

    START_VOTE_MSG = '\nChoose which response is the most correct and click submit.'

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to come up with the best responses for examples by answering a question based on an image and voting on the best one.
    <br>
    This task is done in groups of 4, so it may take some time for 4 Turkers to be matched together. Once the game begins, the HIT will take an additional 5~10 seconds to load.
    <br>
    <h4><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats 10 times. Each round has a response stage and a voting stage.
    <br>
    Both stages have a time limit (60 seconds for responding, 30 seconds for voting). If you timeout, you will be kicked out and lose your bonuses.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see an image and a question. Please answer the question using the details of the image. Note that this answer must be exactly correct - you will be competing with other Turkers to see who gets it more correct.
    <br>
    Please make your answers <b>as short as possible</b> while still being complete (most answers will be 1 or 2 words long). Also, please write all numbers as digits, and avoid punctuation or other miscellaneous characters.
    <br>
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the different responses written by Turkers will appear under the example. Choose the response you believe is the <b>most correct</b>.
    <br>
    <h4><span style='color:blue'><b>Scoring and Bonuses</b></span></h4>
    After everyone has voted, the votes are tallied. The response with the most votes is the winner! If there is a tie for top response, then no bonuses are distributed - so be sure to vote for the right one.
    The players who wrote the winning response receive a bonus. All the players that voted for the winning response also receive a bonus.
    <br>
    Each player will receive <b>at most one</b> bonus per round, so there is no point in voting for your own response unless you truly think it is correct.
    <br>
    <h4><span style='color:blue'><b>Sample Question</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/210000/velka/grand-central-terminal-clock-14850183066ei.jpg" style="width: 20%"></img>
    <br>
    <span style='font-size: 18px'>Question: What time is it right now in the image?</span>
    <br>
    <span style='font-size: 18px'>Correct Answer: 1:34</span>
    {}
    '''

    HIT_TITLE = 'Answer Questions about an Image! (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'Based on the details of an image, you will be answering questions.'

    HIT_KEYWORDS = 'question,answer,image,'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for Visual Question Answering...</b></h1>
    <br>
    Your goal is to write an answer to the question using the image.
    <br>
    <br>
    {}
    '''

    # RANDOM SELECTION OF 2000 INDICES THAT HAVE ANSWER TYPE 'OTHER'
    OTHER_INDICES = [729, 2326, 3235, 2296, 2474, 2389, 4006, 1374, 199, 3450, 3192, 3700, 243, 31, 500, 1694, 3064, 4035, 2544, 2838, 234, 1035, 2678, 768, 2642, 166, 1319, 2470, 388, 3203, 3194, 2157, 3036, 2377, 775, 1487, 3932, 3613, 2895, 1923, 818, 2695, 2609, 564, 3646, 3760, 2512, 57, 1372, 1641, 2757, 3421, 3324, 4052, 986, 866, 1480, 3571, 3233, 1765, 2880, 3752, 116, 1258, 2282, 1388, 3352, 1198, 2513, 653, 3761, 528, 2614, 3213, 2648, 1902, 3030, 3643, 780, 3547, 1394, 961, 4054, 624, 2650, 2514, 1956, 3579, 2873, 2233, 2194, 2980, 2628, 3289, 890, 2419, 689, 2102, 3662, 2625, 705, 1570, 2710, 862, 1014, 1308, 1025, 4080, 1541, 3866, 3218, 2232, 1717, 2392, 2125, 1925, 1348, 2078, 2110, 1812, 760, 3339, 3942, 2598, 1567, 2231, 78, 2126, 2974, 1757, 721, 379, 431, 1145, 878, 3558, 668, 1673, 2159, 2753, 1275, 3388, 2523, 691, 2803, 3079, 2511, 107, 3739, 1516, 1139, 3669, 511, 2737, 1458, 2244, 872, 1102, 1838, 3070, 325, 3935, 3863, 2646, 2183, 327, 428, 1381, 3801, 2115, 1173, 2989, 4012, 38, 1247, 1830, 2150, 3510, 2024, 748, 60, 3227, 3283, 4, 1729, 3185, 3623, 942, 1979, 488, 1150, 299, 2010, 2466, 1590, 2931, 123, 3996, 3704, 3911, 3486, 1259, 1489, 972, 2536, 2149, 1684, 3891, 2044, 2899, 2612, 2910, 3435, 3261, 410, 3616, 522, 683, 3338, 1823, 1228, 4023, 3871, 630, 606, 945, 762, 2395, 3851, 3004, 2874, 2819, 1255, 3442, 1794, 3291, 3648, 4013, 1301, 3876, 1706, 21, 374, 2601, 3372, 3169, 3460, 3312, 3154, 3220, 802, 1020, 2801, 4050, 1848, 159, 136, 1552, 3001, 2353, 1360, 3378, 1525, 3975, 449, 2854, 3688, 427, 2491, 19, 1428, 3493, 1986, 2983, 1639, 498, 165, 2901, 3123, 358, 153, 2623, 390, 2248, 649, 1834, 2364, 692, 3117, 3341, 70, 1278, 3422, 824, 3111, 1961, 3481, 240, 1291, 3800, 881, 2096, 1844, 4008, 710, 3774, 3907, 3210, 1862, 1821, 1083, 3897, 3607, 2540, 1200, 3310, 844, 3879, 1138, 3397, 1971, 3668, 2280, 3931, 4089, 501, 1034, 1894, 1577, 1030, 1257, 905, 61, 3805, 150, 1845, 724, 3854, 3055, 162, 3342, 2403, 2888, 1987, 2001, 1703, 2375, 3140, 2134, 2685, 3792, 2023, 3491, 744, 2109, 1368, 1420, 930, 2251, 4031, 575, 2904, 1241, 2765, 1682, 2029, 2237, 578, 2573, 1328, 3831, 295, 3631, 2064, 3572, 969, 1810, 2671, 145, 448, 778, 3158, 2902, 2457, 696, 3640, 1101, 4051, 221, 1619, 2059, 2809, 2388, 1933, 2038, 2558, 3371, 356, 963, 2108, 614, 3808, 1230, 2568, 706, 3464, 363, 915, 3453, 3768, 141, 2162, 3534, 463, 3783, 2938, 2687, 880, 3824, 466, 2465, 1203, 2438, 1962, 1285, 2229, 285, 3349, 4086, 569, 2407, 1778, 2171, 777, 5, 557, 3126, 958, 3644, 2889, 2852, 2906, 2270, 3029, 1227, 2219, 422, 3346, 3747, 3559, 104, 2371, 1892, 2551, 1583, 2525, 1512, 936, 3373, 2937, 3244, 2118, 2222, 1165, 348, 2575, 1183, 521, 2777, 1515, 1415, 236, 1855, 994, 955, 2549, 3485, 1192, 1563, 1546, 1846, 1479, 1134, 3581, 40, 1238, 2173, 3762, 804, 1324, 2320, 3549, 743, 109, 1659, 1312, 2615, 2789, 283, 3682, 2624, 2489, 2785, 2571, 1320, 3980, 2833, 3482, 2354, 2121, 1964, 2778, 3252, 2263, 1032, 2312, 2797, 980, 2069, 3924, 2181, 3745, 3717, 4069, 2035, 1861, 2800, 1991, 1523, 2674, 2151, 897, 686, 3301, 2658, 467, 2480, 3105, 1753, 1926, 2284, 3200, 1215, 3101, 1171, 2688, 117, 815, 629, 2739, 3028, 3592, 2851, 1906, 337, 1265, 2206, 3193, 794, 596, 3180, 237, 333, 2531, 1885, 1026, 2768, 2239, 1503, 1315, 1840, 879, 1233, 2538, 2522, 943, 2866, 1708, 1585, 462, 99, 1898, 679, 2509, 2323, 1411, 2591, 3545, 3578, 2117, 4088, 3505, 1819, 3067, 277, 837, 55, 1690, 1001, 900, 1701, 1493, 3968, 532, 1052, 3596, 3601, 1195, 1332, 786, 131, 1597, 1159, 2128, 3350, 309, 2972, 1804, 454, 842, 1749, 992, 1797, 1076, 3330, 1273, 1650, 2172, 2032, 1178, 608, 2026, 808, 1647, 257, 3936, 2633, 2817, 1427, 2420, 254, 268, 577, 80, 71, 1196, 3499, 1329, 2629, 2396, 625, 3676, 2431, 1872, 2948, 1629, 2759, 378, 3652, 707, 2743, 2991, 3781, 3934, 75, 843, 405, 3741, 2553, 1599, 3068, 1995, 2103, 680, 2722, 1741, 336, 305, 1123, 2080, 1486, 3377, 2336, 616, 1044, 2267, 1683, 2647, 232, 1182, 1886, 3511, 3625, 1087, 3829, 833, 3830, 3221, 1974, 1377, 1725, 1235, 2711, 2188, 3960, 3013, 3256, 2329, 2279, 2213, 835, 270, 1675, 2824, 3058, 3403, 2186, 1799, 931, 2897, 2909, 3311, 3280, 1796, 132, 1445, 1172, 1135, 2823, 3540, 3115, 3857, 172, 3232, 1197, 2712, 140, 1208, 1686, 35, 1209, 1805, 2214, 3553, 2249, 2033, 3999, 991, 2028, 1776, 1364, 3211, 2034, 492, 1078, 1511, 3807, 2546, 3243, 1477, 1990, 3988, 3087, 1021, 2082, 1404, 2288, 2012, 574, 875, 3880, 798, 1040, 2369, 1722, 1989, 1636, 740, 1155, 1618, 2605, 503, 375, 1469, 1542, 2763, 652, 1780, 1423, 2487, 3612, 785, 2216, 1272, 2148, 424, 1820, 1559, 2560, 3089, 344, 208, 3555, 3714, 536, 937, 1402, 3418, 965, 1462, 1638, 2764, 1768, 2779, 3043, 556, 223, 540, 2257, 1595, 2680, 2144, 2905, 782, 3882, 3348, 2577, 298, 1852, 2286, 1452, 595, 982, 2775, 2672, 3629, 1517, 2883, 1045, 22, 3145, 906, 3672, 499, 3940, 3842, 3817, 1007, 2063, 2057, 2190, 3779, 2152, 2212, 1960, 2990, 3655, 1281, 1627, 391, 2716, 90, 3551, 812, 479, 2630, 248, 2040, 3858, 3925, 2587, 3899, 1408, 2515, 3777, 226, 284, 403, 149, 1391, 1019, 1920, 175, 3128, 2993, 715, 4053, 3416, 1419, 2242, 3444, 1331, 1985, 2387, 723, 3386, 537, 3137, 2009, 1164, 834, 138, 792, 1396, 3299, 3302, 1359, 559, 3225, 1107, 533, 2132, 1009, 599, 2619, 3131, 3718, 2107, 3917, 1808, 1713, 2462, 1179, 210, 1433, 3487, 3786, 4087, 849, 1522, 2668, 2104, 3720, 2820, 2784, 1829, 2141, 1210, 1510, 2807, 3591, 1468, 3798, 3415, 396, 977, 2428, 2036, 3583, 3266, 2005, 3731, 1387, 368, 1250, 1325, 2277, 2505, 207, 2951, 2221, 2460, 2588, 27, 3034, 648, 1346, 1129, 1786, 1663, 1530, 2604, 3431, 4059, 4044, 750, 1814, 4049, 2565, 2855, 3681, 2135, 2728, 3072, 1803, 1914, 139, 1000, 3895, 3706, 1413, 1626, 3580, 2943, 14, 1056, 3827, 2425, 2432, 885, 730, 561, 189, 1870, 2155, 2961, 3991, 3992, 1072, 3841, 2404, 3810, 919, 2056, 2313, 806, 3680, 4048, 2099, 1475, 2061, 2953, 2191, 2940, 1370, 3382, 339, 602, 29, 1383, 2138, 1661, 1375, 672, 1617, 354, 3263, 2595, 1877, 904, 2936, 1437, 2585, 468, 4021, 2166, 3162, 788, 829, 2156, 2004, 475, 97, 3919, 3670, 1609, 2962, 274, 260, 2886, 1950, 2593, 3186, 2098, 1657, 2755, 732, 2089, 871, 3823, 474, 920, 3223, 3666, 2786, 2139, 836, 2079, 3570, 1625, 3401, 3148, 3620, 1288, 1306, 2399, 2424, 2971, 17, 457, 1407, 2530, 510, 201, 3892, 2776, 3698, 3052, 3976, 1951, 3954, 1205, 2887, 2862, 2567, 2337, 2168, 821, 2413, 2339, 2039, 2346, 3412, 2331, 1163, 2113, 2177, 1472, 264, 831, 2720, 584, 1758, 3362, 1726, 1521, 2492, 3451, 2378, 24, 1352, 759, 398, 212, 173, 656, 54, 2020, 3007, 558, 1760, 567, 2751, 3750, 761, 2133, 3598, 2088, 1600, 2721, 2583, 3039, 1031, 3878, 2651, 4047, 903, 3839, 2608, 2011, 3713, 3812, 910, 1842, 853, 549, 1806, 1826, 581, 2617, 1919, 3095, 2762, 1578, 1680, 1449, 2596, 3734, 2203, 1006, 1798, 1693, 2074, 3405, 2963, 4036, 3828, 3187, 926, 3982, 3334, 2528, 4084, 631, 2919, 570, 3369, 701, 1889, 2299, 1921, 3253, 181, 1524, 3536, 2269, 3127, 2798, 2220, 1588, 2826, 2124, 2477, 3436, 2164, 3546, 956, 1878, 46, 2808, 1454, 245, 3190, 3236, 230, 1890, 1839, 1513, 3038, 3775, 2446, 1660, 2293, 2441, 1436, 432, 2504, 2526, 1459, 3000, 799, 1093, 2199, 128, 894, 2664, 2796, 2382, 838, 2774, 3360, 790, 326, 681, 3886, 2994, 105, 1152, 3287, 3709, 86, 2816, 3803, 695, 580, 3254, 3811, 1655, 995, 287, 3400, 3040, 387, 357, 2822, 3269, 2047, 1676, 2055, 2935, 551, 520, 288, 1873, 2274, 2357, 2255, 3251, 192, 3906, 650, 2174, 623, 1133, 1633, 3470, 4015, 1481, 1547, 95, 1955, 341, 2087, 3784, 848, 917, 1612, 251, 2348, 913, 3675, 902, 688, 1143, 3189, 3938, 426, 2669, 2576, 851, 3758, 4083, 2661, 2933, 3333, 1564, 1190, 791, 4079, 1297, 15, 1896, 1624, 3723, 349, 997, 1300, 3304, 3021, 3799, 1807, 1853, 3178, 3548, 3109, 2676, 3910, 976, 3097, 722, 3197, 3696, 2966, 2954, 16, 3950, 3434, 18, 1837, 598, 3027, 949, 784, 1441, 2198, 2639, 483, 1465, 3144, 563, 3163, 1739, 3199, 2376, 3132, 2867, 3275, 3979, 2607, 825, 1236, 989, 2502, 1669, 1702, 3285, 263, 3363, 1750, 3402, 2494, 3118, 3663, 328, 178, 33, 113, 3151, 3046, 1148, 315, 2675, 3344, 3267, 3313, 1211, 2707, 673, 3424, 3508, 1983, 3264, 1154, 3466, 797, 87, 772, 314, 659, 430, 663, 2524, 620, 1642, 3375, 3719, 3994, 2298, 1322, 546, 1393, 2459, 2638, 2927, 30, 3789, 10, 2285, 3888, 3100, 2896, 3044, 793, 1576, 3228, 978, 1287, 3177, 795, 877, 1747, 737, 1800, 2917, 1401, 1128, 2461, 3025, 4078, 2973, 1119, 3541, 3116, 840, 1666, 2566, 1284, 2632, 3409, 971, 1687, 2520, 3864, 712, 76, 3684, 2545, 2071, 3319, 126, 2761, 176, 1111, 907, 3651, 364, 1887, 922, 1982, 826, 2045, 1916, 4005, 1266, 89, 1932, 407, 839, 3016, 1934, 1054, 1560, 1147, 2606, 412, 3249, 3459, 944, 3667, 1720, 3873, 148, 3814, 3174, 147, 332, 3056, 471, 1978, 1743, 3214, 1785, 294, 1046, 2436, 82, 814, 2649, 3872, 1784, 376, 2, 2254, 2863, 2599, 2418, 342, 2970, 360, 2340, 530, 2670, 2949, 399, 1067, 1954, 2451, 2616, 898, 2704, 571, 4029, 738, 2373, 455, 3701, 1543, 2311, 641, 1756, 1478, 213, 2068, 3593, 2660, 592, 218, 2433, 460, 3006, 2876, 2497, 1063, 2782, 2105, 2682, 2204, 3889, 3703, 1856, 2429, 3856, 671, 1042, 1674, 3380, 177, 74, 3527, 1184, 3250, 612, 1957, 1366, 1425, 3573, 2065, 3394, 1880, 2013, 703, 3966, 2870, 497, 3847, 2945, 2932, 322, 909, 1344, 39, 2211, 3419, 627, 4065, 3303, 587, 3125, 886, 2828, 1646, 1114, 3584, 2247, 3423, 1015, 3815, 1456, 1170, 3586, 2844, 2165, 3603, 523, 3523, 3414, 3255, 2453, 2911, 4046, 734, 3641, 3647, 1992, 1817, 3691, 3531, 3998, 1323, 1495, 2769, 485, 487, 1591, 3832, 2861, 1871, 1326, 2142, 8, 2374, 2476, 3107, 3604, 3588, 423, 420, 3286, 160, 2760, 1356, 1945, 3384, 3633, 1610, 2554, 3820, 3619, 167, 3632, 225, 464, 1253, 867, 220, 1949, 2635, 88, 47, 2533, 870, 1060, 1589, 3724, 3420, 3554, 3690, 3569, 84, 366, 3083, 2253, 49, 2358, 2398, 3749, 404, 68, 1604, 3207, 4039, 3306, 1127, 2295, 1884, 736, 1536, 1774, 1483, 1005, 3053, 1226, 3142, 1216, 494, 2730, 1470, 1801, 3887, 1915, 1973, 63, 2521, 2637, 2352, 1131, 1270, 830, 2913, 3621, 1318, 266, 2400, 1185, 3946, 65, 807, 2252, 1282, 1527, 3160, 1802, 2182, 444, 2335, 114, 3921, 2884, 317, 1013, 3102, 3567, 3597, 2976, 2075, 774, 2924, 490, 3944, 733, 3257, 3449, 1157, 3124, 699, 2968, 1340, 1909, 3300, 2215, 1440, 2106, 3208, 2830, 1141, 1930, 3204, 2735, 0, 1047, 1204, 3467, 1022, 3524, 2485, 2611, 3538, 568, 2719, 3298, 1790, 3188, 3727, 4034, 585, 3153, 1857, 3047, 411, 687, 2273, 421, 3351, 1313, 901, 2702, 857, 642, 940, 37, 999, 3272, 572, 1494, 3206, 2600, 1214, 2448, 319, 20, 2840, 2537, 3787, 2987, 1429, 1606, 1003, 1904, 3962, 1643, 1240, 2845, 486, 3989, 129, 2481, 938, 3742, 3867, 1710, 947, 4071, 3048, 3514, 1482, 3480, 3594, 3602, 2347, 2613, 1735, 847, 2187, 1466, 103, 3661, 1598, 1544, 259, 3503, 674, 1082, 335, 2478, 1008, 626, 28, 3374, 973, 406, 3167, 3229, 1744, 925, 3561, 2344, 615, 2656, 2386, 841, 36, 1762, 2925, 1395, 889, 1053, 1373, 377, 272, 508, 1501, 1734, 2859, 1430, 1341, 1843, 2694, 13, 343, 44, 2185, 278, 3060, 1773, 3273, 1116, 1142, 265, 3710, 1140, 2094, 2223, 3176, 459, 3391, 269, 2390, 1424, 289, 1471, 1283, 2383, 2771, 3515, 1070, 2372, 2289, 3448, 2564, 665, 3963, 3074, 3245, 1206, 1518, 1122, 3452, 2130, 2017, 2579, 302, 2653, 544, 2547, 450, 1721, 3970, 2871, 2393, 2790, 53, 1697, 2327, 3173, 704, 3282, 2666, 2645, 1104, 1400, 1822, 555, 3457, 2746, 3398, 3658, 2548, 2986, 1207, 506, 1450, 1343, 1444, 1679, 1736, 3191, 203, 3439, 3964, 603, 2467, 361, 1781, 3529, 380, 1100, 2581, 2092, 751, 1905]

    def __init__(self):
        super().__init__()
        self.ex_idcs = None
        self.exs = []

    def get_img_path(self, id):
        return '/private/home/edwardpark/ParlAI/data/COCO-IMG-2014/train2014/COCO_train2014_{}{}.jpg'.format('0' * (12 - len(str(id))), id)

    def next_example(self, generator, total_rounds, offset):
        offset %= 2000
        if self.ex_idcs is None:
            self.ex_idcs = range(offset, offset+total_rounds)
            for idx in self.ex_idcs:
                ex = generator.get(self.OTHER_INDICES[idx])
                ex['offset'] = idx
                # load the next image in the background
                img_path = self.get_img_path(ex['image_id'])
                generator.data_loader.request_load(generator.receive_data,
                                                   generator.image_loader.load,
                                                   (img_path,))
                self.exs.append(ex)

        cur_ex = self.exs.pop(0)
        image = generator.data_queue.get()
        cur_ex['image'] = image
        return cur_ex


class VqaRespondingOnlyGC(VqaGC):
    """
    Variant of the Vqa game that only has the response stage.
    """

    TASK_IDENTIFIER = 'vqa_response_solo'

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to come up with the best responses for examples by answering a question based on an image.
    <br>
    Once the game begins, the HIT will take 5~10 seconds to load.
    <br>
    <h4><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats 10 times.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see an image and a question. Please answer the question using the details of the image.
    <br>
    Please make your answers <b>as short as possible</b> while still being complete (most answers will be 1 or 2 words long). Also, please write all numbers as digits, and avoid punctuation or other miscellaneous characters.
    <br>
    <h4><span style='color:blue'><b>Sample Question</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/210000/velka/grand-central-terminal-clock-14850183066ei.jpg" style="width: 20%"></img>
    <br>
    <span style='font-size: 18px'>Question: What time is it right now in the image?</span>
    <br>
    <span style='font-size: 18px'>Correct Answer: 1:34</span>
    {}
    '''

    END_INFO = \
    """
    <h3><span style="color:blue"><b>Reward/Bonus</b></span></h3>
    There are two bonuses that can be won that push the average pay to $15/hr.
    <br>
    <ol>
        <li>Round Completion: successfully progress through all rounds without disconnecting or being kicked (all-or-nothing $0.70)</li>
        <li>Participation: do not time out at any point (all-or-nothing $0.40)</li>
    </ol>
    There is a base pay rate of $0.05. So, for a given HIT, if you do not time out and finish all the rounds, you will earn $0.05 + $0.70 + $0.40 = $1.15.
    Please note that bonuses are typically paid 2~4 days after the HIT is completed.
    <br>
    <h3><span style="color:blue"><b>Close Window/Timeout/Return HIT</b></span></h3>
    Once the conversation has started, close window/timeout or return HIT during the chat will result in
    <b>HIT EXPIRED</b> to you. You will still earn the bonuses already won to that point.
    <br>
    Please remember that each question has a time limit. If you timeout even once, you will be kicked out of the HIT.
    <br>
    <br>
    <h3><span style='color:red'><b>IMPORTANT NOTICE</b></span></h4>
    1. <b>Be aware the conversations you have will be made public, so act as you would e.g. on a public social network like Twitter.</b>
    <br>
    2. Please do not send any message that could make others uncomfortable, including any level of discrimination, racism, sexism and offensive religious/politics comments, otherwise the submission will be rejected.
    <br>
    3. This particular HIT can only be completed by an individual worker up to 5 times.
    <br>
    4. Pressing ENTER on your keyboard currently does not work to submit answers, so please manually click the SEND button.
    <br>
    <br>
    """

    def __init__(self):
        super().__init__()
