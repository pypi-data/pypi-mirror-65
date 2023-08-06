from musurgia.fractaltree.fractalmusic import FractalMusic

# fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
#                   quarter_duration=30, tempo=80)
fm = FractalMusic(quarter_duration=10, tempo=60)
fm.midi_generator.midi_range = (60, 72)
fm.add_layer()
#
# expected = [child.children_generated_midis for child in fm.get_children()]
# actual = [child.children_generated_midis for child in fm.get_children()]
children_midis_1 = [child.children_generated_midis for child in fm.get_children()]
choral_midis_1 = [child.get_choral_midis() for child in fm.get_children()]
choral_midis_2 = [child.get_choral_midis() for child in fm.get_children()]
children_midis_2 = [child.children_generated_midis for child in fm.get_children()]


print(choral_midis_1)
print(children_midis_1)
print(children_midis_2)
# print(choral_midis_2)
