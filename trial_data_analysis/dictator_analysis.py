import pandas as pd
import matplotlib.pyplot as plt
# import spreadsheet
data = pd.read_excel("large_sample.xlsx")

for col_name in list(data.columns.values):
	print col_name
# filter by most meaningful column names
col_names = ["participant.id_in_session",
"participant.code",
"participant.payoff",
"player.id_in_group",
"player.predicted",
"player.rating",
"player.rating",
# "bot_id",
"player.payoff",
"group.id_in_subsession",
"subsession.round_number",
"session.code"]

data = data.filter(col_names)

## show first 5 rows of dataset so we know filtering and import worked:
# print data.head(n=5)

print "yo"
# plot predictions vs. received allotment, e.g.for 1st player:
p1_data = data[data["player.id_in_group"]==1]
t = p1_data["subsession.round_number"].head(n=8)
predicted = p1_data["player.payoff"].head(n=8)
received = p1_data["player.predicted"].head(n=8)
rating = p1_data["player.rating"].head(n=8)

#plt.plot(t, predicted, t, received)
#plt.step(t, rating)

# plot creation:
fig, ax = plt.subplots()
# show 2 axes & 2 legends:
def two_scales(ax1, time, data):
    ax2 = ax1.twinx()
    ax1.plot(time, data[0], time, data[1])
    ax1.set_xlabel('round number')
    ax1.set_ylabel('Points offered')
    ax1.legend(["predicted", "received"], loc="lower left")

    ax2.step(time, data[2], color="blue")
    ax2.set_ylabel('Rating: fair/unfair')
    ax2.legend(["rating"], loc="lower right")
    return ax1, ax2

ax1, ax2 = two_scales(ax, t, [predicted, received, rating])
# show rounds as integer only on x-axis
x_axis = range(t.min(),t.max()+1)
plt.xticks(x_axis)

def color_y_axis(ax, color):
    """Color selected axes."""
    for yt in ax.get_yticklabels():
        yt.set_color(color)
    return None
color_y_axis(ax1, 'r')
color_y_axis(ax2, 'b')

plt.show()
# TODO: label lines (legend), separate axis for true/false

# plt.show()
