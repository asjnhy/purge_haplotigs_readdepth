import pandas as pd


def find_cut(filename, cut_min):
	grp = pd.DataFrame(columns=['idx', 'y'])
	with open(filename, 'r', newline='\n') as fh:
		all_lines = fh.readlines()
		for idx, i in enumerate(all_lines):
			li = i[:-1].split('\t')
			if li[0] == 'genome':
				line = {'idx': li[1], 'y': li[2]}
				grp = grp.append(line, ignore_index=True)

	grp['y'] = grp['y'].map(lambda x: int(x))
	grp['idx'] = grp['idx'].map(lambda x: int(x))
	grp['diff'] = grp['y'].diff(1)

	def derivatives_2(df):
		idx = df['idx']
		if idx <= 5 or idx >= len(grp) - 5:
			return 1
		min = grp.loc[idx - 1, 'diff']
		max = grp.loc[idx + 1, 'diff']
		return (max - min) / 2

	grp['drv_2'] = grp.apply(lambda x: derivatives_2(x), axis=1)

	drv_list = list()
	for i in range(cut_min, len(grp)):
		x = grp.loc[i, 'idx']
		y = grp.loc[i, 'drv_2']
		drv_list.append((y, x))

	drv_list.sort()

	while (True):

		peak1 = drv_list[0]
		peak2 = drv_list[1]
		i = 1
		while (abs(peak2[0] - peak1[0]) <= 10):
			peak2 = drv_list[i + 1]
			i = i + 1

		valley = drv_list[-1]

		check_btwness = (peak2[1] < valley[1] and valley[1] < peak1[1])
		check_btwness_2 = (peak1[1] < valley[1] and valley[1] < peak2[1])

		if ((check_btwness) or (check_btwness_2)):
			mid = valley[1]
			break

		drv_list.pop(0)

	high = mid * 3
	low = cut_min

	return low, mid, high


if __name__ == '__main__':
	print(find_cut('C:/Users/user/Desktop/aligned.bam.gencov', cut_min=5))

