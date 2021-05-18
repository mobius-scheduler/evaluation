library(RColorBrewer)
source("style.r")

args = commandArgs(trailingOnly = TRUE)
data = read.csv(args[1])

mycolors <- colorRampPalette(brewer.pal(9, "Blues"))(60)
tgt = data.frame(x = c(23.919, 161/6), y = c(23.919, 140/6), type = c('Avg Target Tput', 'Mobius'))

p = ggplot() +
	geom_abline(slope = 1, color = "grey") +
	geom_line(data = data, mapping = aes(x = app1, y = app2, color = factor(round)), size = 0.7) +
	geom_point(data = data, mapping = aes(x = app1, y = app2, color = factor(round)), size = 3) +
	geom_point(data = tgt, mapping = aes(x = x, y = y, shape = type), fill = 'red', size = 3) +
	#geom_point(aes(x = 23.919, y = 23.919), shape = 'asterisk', color = 'red', size = 4) +
	#geom_point(aes(x = 161/6, y = 140/6), shape = 'diamond', color = 'red', size = 4) +
	scale_color_manual(values = mycolors) +
	scale_shape_manual(values = c(22, 25)) +
	guides(color = FALSE) +
	xlab("Cust 1 Tput (tasks/round)") +
	ylab("Cust 2 Tput (tasks/round)") +
	theme(legend.position = "top", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-7,-7,-7,-7)) +
	labs(color = "", shape = "")
ggsave(args[2], p, width = 3, height = 2.5, units = 'in')

