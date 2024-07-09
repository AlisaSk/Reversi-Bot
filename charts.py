import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import game 

# set seaborn style 
sns.set_theme() 

results = game.main()

periods = list(range(1, len(results) + 1))
greedy = [result[0] for result in results]
minimax = [result[1] for result in results]

# Statistics
greedy_wins = 0
minimax_wins = 0
avg_greedy_score = 0
avg_minimax_score = 0
for i in range(100):
	if greedy[i] < minimax[i]:
		minimax_wins += 1
	elif greedy[i] > minimax[i]:
		greedy_wins += 1
	avg_greedy_score += greedy[i]
	avg_minimax_score += minimax[i]

avg_greedy_score //= 100
avg_minimax_score //= 100

print("STATISTICS:")
print("G_wins: ", greedy_wins, "M_wins: ", minimax_wins)
print("G_avg: ", avg_greedy_score, "M_avg: ", avg_minimax_score)


# define DataFrame 
df = pd.DataFrame({'period': periods, 'greedy': greedy, 'minimax': minimax}) 

# define colors to use in chart 
color_map = ['orange', 'purple'] 

# create line chart
plt.plot(df.period, df.greedy, label='greedy', color='orange')
plt.plot(df.period, df.minimax, label='minimax', color='purple')

plt.legend(loc='upper left')

# Add titles and labels
plt.title('Greedy VS Minimax Results of 100 Othello Games (weights)')
plt.xlabel('Game #')
plt.ylabel('Score')

plt.xticks(ticks=range(0, 101, 10))

# Show plot
plt.show()
