library(dplyr)
library(RColorBrewer)
source("style.r")

args = commandArgs(trailingOnly = TRUE)
data = read.csv(args[1])

data$time = data$time/60
data = data %>%
	group_by(alpha, app_id) %>%
	mutate(
		   thp = ifelse(app_id == 5, cumsum(tasks_fulfilled)/(time-25), cumsum(tasks_fulfilled)/time),
		   req = cumsum(tasks_requested)/time)
data = data.frame(data)

data$app_id = factor(
					 data$app_id,
					 levels = c(5, 3, 4, 1, 2),
					 labels = c("Roof", "iPerf", "Air Quality", "Traffic", "Parking"))
data$alpha = factor(data$alpha, levels = c(100, 1, 0, -1), labels = c("Mobius\n(Max-Min)", "Mobius\n(Prop. Fair)", "Max\nThroughput", "Dedicated\nDrones"))
data = subset(data, app_id != -1)

colors = brewer.pal(n = 5, name = 'Dark2')
colors = c(colors[5], colors[3], colors[4], colors[1], colors[2])

p = ggplot(data, aes(x = time, y = thp, fill = app_id)) +
	geom_area(color = "black") +
	scale_fill_manual(values = colors) +
	facet_wrap(. ~ alpha, nrow=1) +

	# formatting
	theme(
		  legend.position = "top", legend.box = "vertical", 
		  legend.margin=margin(0,0,0,0), legend.box.margin=margin(-4,-4,-7,-7),
		  legend.text = element_text(size = 10)
	) +
	ylim(c(0, NA)) +
	xlim(c(0, NA)) +
	xlab("Time (min)") +
	ylab("Long-term Tput\n(tasks/min)") +
	labs(fill = "", shape = "")
ggsave(args[2], p, width = 5, height = 2, units = 'in')

