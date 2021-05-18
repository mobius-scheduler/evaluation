library(dplyr)
library(RColorBrewer)
source("style.r")

args = commandArgs(trailingOnly = TRUE)
data = read.csv(args[1])

data$time = data$time/60
data = data %>%
	group_by(alpha, app_id) %>%
	mutate(
		   thp = cumsum(tasks_fulfilled)/time,
		   req = cumsum(tasks_requested)/time) %>%
	summarize(norm = last(thp/req))
data = data.frame(data)
data$app_id = factor(
					 data$app_id,
					 levels = c(3, 4, 5, 1, 2),
					 labels = c("iPerf", "Air Quality", "Roof", "Traffic", "Parking"))
data$alpha = factor(data$alpha, levels = c(100, 1, 0, -1), labels = c("Mobius\n(Max-Min)", "Mobius\n(Prop. Fair)", "Max\nThroughput", "Dedicated\nDrones"))
data = subset(data, app_id != -1)

colors = brewer.pal(n = 5, name = 'Dark2')
colors = c(colors[3], colors[4], colors[5], colors[1], colors[2])

p = ggplot(data, aes(x = alpha, y = 100 * norm, fill = app_id)) +
	geom_col(position = "dodge", color = "black") +
	scale_fill_manual(values = colors) +

	# formatting
	theme(
		  legend.position = "top", legend.box = "vertical", legend.margin = margin(),
		  legend.box.margin=margin(-4,-4,-7,-7),
		  legend.text = element_text(size = 10),
		  axis.title.x = element_blank()
	) +
	ylim(c(0, NA)) +
	ylab("Tasks\nCompleted (%)") +
	labs(fill = "", shape = "")
ggsave(args[2], p, width = 5, height = 1.5, units = 'in')

