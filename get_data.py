from urllib.request import urlopen
import re
import pandas as pd
import sys

def main():

	if sys.argv[1] == 'pro':
		try:
			file = urlopen('https://en.wikipedia.org/wiki/'+sys.argv[2]+'_Pro_Bowl').read().decode()

			if int(sys.argv[2]) >=2012:
				AFC_vals = file.split('<caption>American Football Conference</caption>')[1].split('<caption>National Football Conference</caption>')[0]
				NFC_vals = file.split('<caption>National Football Conference</caption>')[1].split('id="Broadcasting">')[0]

				teams = re.findall('title="(.*) season">', AFC_vals)
				teams += re.findall('title="(.*) season">', NFC_vals)

				n = list(map(int, re.findall('</a></td>\n<td>(.*)</td>', AFC_vals)))
				n += list(map(int, re.findall('</a></td>\n<td>(.*)</td>', NFC_vals)))

			else:
				vals = file.split('<th>NFC Team</th>\n<th>Selections</th>')[1].split('</table>')[0]

				lst = re.findall('<td>(.*)</td>', vals)
				teams = [lst[i] for i in range(len(lst)) if i%2==0]
				n = [int(lst[i]) for i in range(len(lst)) if i%2==1]

			pros_per_team = sorted(list(zip(teams, n)))

			df=pd.DataFrame(pros_per_team)
			df.to_excel(sys.argv[2]+ ' probowlers.xlsx', header=['Team Name', 'Probowlers'], index=False)
			print('Success!')

		except:
			print('Something went wrong. Remember to type [pro Year]')

	elif sys.argv[1] == 'pr':
		pass


if __name__ == '__main__':
	main()