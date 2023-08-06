aachen_cathedral = 1622
amphitheatre = 251
aqueduct = 231
arch_of_constantine = 899
archery_range = 87
army_tent_a = 1196
army_tent_b = 1197
army_tent_c = 1198
army_tent_d = 1199
army_tent_e = 1200
barracks = 12
blacksmith = 103
bombard_tower = 236
bridge_a_bottom = 607
bridge_a_broken_bottom = 740
bridge_a_broken_top = 739
bridge_a_cracked = 738
bridge_a_middle = 606
bridge_a_top = 605
bridge_b_bottom = 610
bridge_b_broken_bottom = 743
bridge_b_broken_top = 742
bridge_b_cracked = 741
bridge_b_middle = 609
bridge_b_top = 608
bridge_c_bottom = 1206
bridge_c_broken_bottom = 1212
bridge_c_broken_top = 1211
bridge_c_cracked = 1210
bridge_c_middle = 1205
bridge_c_top = 1204
bridge_d_bottom = 1209
bridge_d_broken_bottom = 1215
bridge_d_broken_top = 1214
bridge_d_cracked = 1213
bridge_d_middle = 1208
bridge_d_top = 1207
bridge_e_bottom = 1552
bridge_e_broken_bottom = 1558
bridge_e_broken_top = 1557
bridge_e_cracked = 1556
bridge_e_middle = 1551
bridge_e_top = 1550
bridge_f_bottom = 1555
bridge_f_broken_bottom = 1561
bridge_f_broken_top = 1560
bridge_f_cracked = 1559
bridge_f_middle = 1554
bridge_f_top = 1553
castle = 82
cathedral = 599
chain = 1396
city_gate1 = 1579
"""Please note: The game does not handle this building properly at this point"""
city_gate2 = 1583
"""Please note: The game does not handle this building properly at this point"""
city_gate3 = 1587
"""Please note: The game does not handle this building properly at this point"""
city_gate4 = 1591
"""Please note: The game does not handle this building properly at this point"""
city_wall = 370
colosseum = 263
dock = 45
dormition_cathedral = 1369
farm = 50
feitoria = 1021
fence = 1062
fire_tower = 190
fish_trap = 199
fortified_palisade_wall = 119
fortified_tower = 1102
fortified_wall = 155
fortress = 33
gate_down = 88
gate_horizontal = 659
gate_up = 64
gate_vertical = 667
gol_gumbaz = 1217
guard_tower = 234
harbor = 1189
house = 70
hut_a = 1082
hut_b = 1083
hut_c = 1084
hut_d = 1085
hut_e = 1086
hut_f = 1087
hut_g = 1088
keep = 235
krepost = 1251
lumber_camp = 562
market = 84
mill = 68
mining_camp = 584
monastery = 104
monument = 826
outpost = 598
palisade_gate_down = 793
palisade_gate_horizontal = 797
palisade_gate_up = 789
palisade_gate_vertical = 801
palisade_wall = 72
pyramid = 689
quimper_cathedral = 872
rice_farm = 1187
rock_church = 1378
sanchi_stupa = 1216
sankore_madrasah = 1367
sea_gate1 = 1391
"""Please note: The game does not handle this building properly at this point"""
sea_gate2 = 1383
"""Please note: The game does not handle this building properly at this point"""
sea_gate3 = 1379
"""Please note: The game does not handle this building properly at this point"""
sea_gate4 = 1387
"""Please note: The game does not handle this building properly at this point"""
sea_tower = 785
sea_wall = 788
shrine = 1264
siege_workshop = 49
stable = 101
stone_wall = 117
storage = 1081
temple_of_heaven = 637
tent_a = 1097
tent_b = 1098
tent_c = 1099
tent_d = 1100
tent_e = 1101
tower_of_london = 1368
town_center = 109
khosrau = 444
trade_workshop = 110
university = 209
watch_tower = 79
wonder = 276
wooden_bridge_a_bottom = 1311
wooden_bridge_a_middle = 1310
wooden_bridge_a_top = 1309
wooden_bridge_b_bottom = 1314
wooden_bridge_b_middle = 1313
wooden_bridge_b_top = 1312
yurt_a = 712
yurt_b = 713
yurt_c = 714
yurt_d = 715
yurt_e = 716
yurt_f = 717
yurt_g = 718
yurt_h = 719


def get_building_id_by_string(building):
    """
    Returns the ID of the given building. None otherwise.
    """
    try:
        return eval(building)
    except NameError:
        return None
