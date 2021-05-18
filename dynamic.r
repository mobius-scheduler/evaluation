library(dplyr)
source("style.r")

args = commandArgs(trailingOnly = TRUE)
data = read.csv(args[1])

data$time = data$time / 60
data = data %>%
	group_by(alpha, app_id) %>%
	mutate(thp = cumsum(tasks_fulfilled)/time)
data = data.frame(data)

data$app_id = factor(
					 data$app_id,
					 levels = c(1, 2, -1),
					 labels = c("Customer 1", "Customer 2", "Total"))
data$alpha = factor(
					data$alpha,
					levels = c(0, -2, -1, 1, 3, 100),
					labels = c("Max Throughput", "Round Robin", 
							   "Dedicated Vehicles", "Mobius (Prop. Fair)",
							   "Mobius (alpha=3)", "Mobius (Max-Min)"))

p = ggplot(data, aes(x = time, y = thp, color = app_id, linetype = app_id)) +
	geom_line(size = 1.0) +
	scale_color_manual(values = c('#fc8d62', '#8da0cb', '#000000')) +
	scale_linetype_manual(values = c('solid', 'solid', 'dashed')) +
	facet_wrap(alpha ~ ., nrow = 2) +

	# formatting
	theme(
		  legend.position = "top", 
		  legend.text = element_text(size = 10),
		  legend.margin=margin(0,0,0,0), legend.box.margin=margin(-7,-7,-7,-7)
	) +
	xlim(c(0, 60)) +
	xlab("Time (mins)") +
	ylab("Long-term Throughput\n(tasks/min)") +
	guides(linetype = FALSE) +
	labs(color = "")
ggsave(args[2], p, width = 5, height = 2.5, units = 'in')

