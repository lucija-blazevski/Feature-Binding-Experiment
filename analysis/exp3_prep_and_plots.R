# Feature binding is slow: temporal integration explains apparent ultrafast binding
# JASP Data Preparation and Plotting Script for Experiment 3

# ------------------------------------------------------------------------------
# Section 1: Library and data loading 
# ------------------------------------------------------------------------------

# Load necessary libraries
library(plyr)
library(tidyverse)
library(stringr)

# Set working directory and select a folder from which files would be read
setwd("C:/Users/Lucija/Desktop/binding_paper/data/raw_data_anonimized/")
mydir = "experiment 3"
myfiles = list.files(path=mydir, pattern="*.csv", full.names=TRUE)

# Load data
st_data_exp3 = ldply(myfiles, read_csv)

detach(package:plyr)

# ------------------------------------------------------------------------------
# Section 2: Data manipulation
# ------------------------------------------------------------------------------

# Extract median thresholds
thresholds <-
  st_data_exp3 %>%
  ungroup() %>%
  select(threshold_low1_mask_low, threshold_low2_mask_low, threshold_low3_mask_low, 
         threshold_low1_mask_high, threshold_low2_mask_high, threshold_low3_mask_high,
         threshold_med1_mask_low, threshold_med2_mask_low, threshold_med3_mask_low,
         threshold_med1_mask_high, threshold_med2_mask_high, threshold_med3_mask_high,
         threshold_high1_mask_low, threshold_high2_mask_low, threshold_high3_mask_low,
         threshold_high1_mask_high, threshold_high2_mask_high, threshold_high3_mask_high) %>%
  na.omit() %>% 
  t() %>% 
  as.data.frame() %>% 
  mutate(Cycles = as.integer(rep(c(1,2,3), times = 6)),
         SF = rep(c('Low','Medium', 'High'), each = 6),
         Mask = rep(c(rep('Low', 3), rep('High', 3)), 3))

# Make nice columns names
colnames(thresholds)<- c(paste('P',sep = '_', seq(1,length(myfiles))), 'Cycle', 'SF', 'Mask')

# ------------------------------------------------------------------------------
# Section 3: Data export
# ------------------------------------------------------------------------------

data_long <- thresholds %>%
  pivot_longer(cols = P_1:P_12, names_to = "Participant", values_to = "Threshold") %>%
  mutate(Threshold = as.numeric(Threshold)) %>%
  group_by(SF, Cycle, Mask) %>%
  mutate(Mean = mean(Threshold, na.rm = TRUE),
         Mean_ms = Mean * 6.0606,
         SE_ms = sd(Threshold, na.rm = TRUE) / sqrt(n()),
         Cycle_SF = paste(SF, Cycle, Mask, sep = "_"))

# Pivot the data
data_wide <- data_long %>% 
  pivot_wider(names_from = Cycle_SF, values_from = Threshold, id_cols = Participant)

# Write the data frame to a CSV file
write.csv(data_wide[,-1], file = "exp3_jasp.csv", row.names = FALSE)

# ------------------------------------------------------------------------------
# Section 4: Plotting
# ------------------------------------------------------------------------------
data_to_plot <- data_long %>%
  group_by(Cycle, SF, Mask) %>%
  summarize(Mean_ms = mean(Threshold * 6.0606),
            SE_ms = sd(Threshold * 6.0606) / sqrt(n())) %>%
  mutate(Mask = if_else(Mask == 'High', 'High SF mask', 'Low SF mask'))

ggplot(data_to_plot, aes(x = factor(Cycle), y = Mean_ms, color = factor(SF))) +
  geom_line(aes(group = SF), size = 0.8) +
  facet_wrap(~factor(Mask), labeller = labeller(Mask = c('High SF mask', 'Low SF mask'))) +
  geom_point(size = 2) +
  geom_errorbar(aes(ymin = Mean_ms - SE_ms, ymax = Mean_ms + SE_ms), width = 0.2) +
  scale_color_manual(values = c('High' = 'tan3', 'Low' = 'darkgreen', 'Medium' = 'lightslateblue'),
                     breaks = c('High', 'Medium', 'Low'))+
  labs(x = 'Number of cycles', color = 'Spatial frequency', y = 'Stimulus duration for 75% accuracy (ms)') +
  theme (
    text = element_text(size=16, color = 'black'),
    panel.background = element_rect(fill = "white"),
    axis.line.x = element_line(colour = "black", 
                               size = 0.4, 
                               lineend = "butt"),
    axis.line.y = element_line(colour = "black", 
                               size = 0.4),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text.x = element_text(color = 'black', size = 16),
    axis.text.y = element_text(color = 'black', size = 16),
    legend.title = element_text(size = 16), 
    legend.text = element_text(size = 16),
    legend.key.size = unit(2, "lines"),
    strip.text = element_text(size = 16))

ggsave('exp3.png', width = 9, height = 7, dpi= 300)
ggsave('figure_4.tiff', width = 9, height = 7, dpi = 300)
