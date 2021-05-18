library(dplyr)
library(RColorBrewer)
source("style.r")

args = commandArgs(trailingOnly = TRUE)
data = read.csv(args[1])

data$time = data$time/60
data = subset(data, app_id == 5 & alpha == 100)
data$discount = factor(data$discount, labels = c("Discount", "No Discount"))

colors = brewer.pal(n = 5, name = 'Dark2')

p = ggplot() +
	geom_line(data, mapping = aes(x = time, y = tasks_fulfilled, linetype = discount), size = 1, color = colors[5]) +
	xlab("Time (min)") +
	ylab("Tasks") +
	labs(linetype = "") +
	theme(legend.position = "top", legend.margin=margin(0,0,0,0))
ggsave(args[2], p, width = 3, height = 1.5, units = 'in')

