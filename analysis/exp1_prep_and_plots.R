# Feature binding is slow: temporal integration explains apparent ultrafast binding
# JASP Data Preparation and Plotting Script for Experiment 3

# ------------------------------------------------------------------------------
# Section 1: Library and data loading 
# ------------------------------------------------------------------------------

# Load necessary libraries
library(plyr)
library(tidyverse)
library(ggplot2)

# Set working directory and read files
setwd("C:/Users/Lucija/Desktop/binding_paper/data/raw_data_anonimized")
mydir <- "experiment 1"
myfiles <- list.files(path = mydir, pattern = "*.csv", full.names = TRUE)

# ------------------------------------------------------------------------------
# Section 2: Load and prepare data
# ------------------------------------------------------------------------------

# Masked-only data
data_masked <- ldply(myfiles, read_csv) %>%
  filter(mask_present == TRUE, stimulus_frame_duration != 60) %>%
  mutate(spatial_frequency = factor(spatial_frequency, levels = c("high", "low"), labels = c("High", "Low"))) %>%
  group_by(participant, spatial_frequency, cycle_number) %>%
  mutate(avg_accuracy = mean(accuracy))

# Masked and unmasked data in 1-cycle condition
data_one_cycle <- ldply(myfiles, read_csv) %>%
  filter(stimulus_frame_duration != 60, cycle_number == 1) %>%
  mutate(spatial_frequency = factor(spatial_frequency, levels = c("high", "low"), labels = c("High", "Low"))) %>%
  group_by(participant, mask_present, spatial_frequency) %>% 
  mutate(avg_accuracy = mean(accuracy))

# Remove 'plyr' package
detach(package:plyr)

# ------------------------------------------------------------------------------
# Section 3: d' calculation for masked-only data
# ------------------------------------------------------------------------------

# Create new variables for hits, misses, correct rejections, and false alarms
# Compute the hit rate, false alarm rate and d prime for each participant, for each condition
data_masked_dprime <- data_masked %>%
  group_by(participant, cycle_number, spatial_frequency) %>%
  summarise(
    n_signal = sum(correct_response == 'left'),
    n_noise = sum(correct_response == 'right'),
    hit = sum(correct_response == 'left' & answer == 'left'),
    miss = sum(correct_response == 'left' & answer == 'right'),
    cr = sum(correct_response == 'right' & answer == 'right'),
    fa = sum(correct_response == 'right' & answer == 'left'),
    .groups = 'keep'
  ) %>%
  rowwise() %>%
  mutate(
    hit_rate = if_else(hit / n_signal == 1, 1 - 1 / (2 * n_signal), if_else(hit / n_signal == 0, 1 / (2 * n_signal), hit / n_signal)),
    fa_rate = if_else(fa / n_noise == 1, 1 - 1 / (2 * n_noise), if_else(fa / n_noise == 0, 1 / (2 * n_noise), fa / n_noise)),
    d_prime = qnorm(hit_rate) - qnorm(fa_rate)
  )

# ------------------------------------------------------------------------------
# Section 4: Export of masked-only data
# ------------------------------------------------------------------------------

# Pivot and save the data frame
data_masked_dprime_long <- data_masked_dprime %>% 
  mutate(Cycle_SF = paste(spatial_frequency, cycle_number, sep = "_"))

data_masked_dprime_wide <- data_masked_dprime_long %>% 
  pivot_wider(names_from = Cycle_SF, 
              values_from = d_prime, 
              id_cols = participant)

write.csv(data_masked_dprime_wide[,-1], file = "exp1.csv", row.names = FALSE)

# ------------------------------------------------------------------------------
# Section 5: d' calculation for masked and unmasked one-cycle data
# ------------------------------------------------------------------------------
data_one_cycle_dprime <- data_one_cycle %>%
  group_by(participant, mask_present, spatial_frequency) %>% 
  summarise(
    n_signal = sum(correct_response == 'left'),
    n_noise = sum(correct_response == 'right'),
    hit = sum(correct_response == 'left' & answer == 'left'),
    miss = sum(correct_response == 'left' & answer == 'right'),
    cr = sum(correct_response == 'right' & answer == 'right'),
    fa = sum(correct_response == 'right' & answer == 'left'),
    .groups = 'keep'
  ) %>%
  rowwise() %>%
  mutate(
    hit_rate = if_else(hit / n_signal == 1, 1 - 1 / (2 * n_signal), 
                       if_else(hit / n_signal == 0, 1 / (2 * n_signal), hit / n_signal)),
    fa_rate = if_else(fa / n_noise == 1, 1 - 1 / (2 * n_noise), 
                      if_else(fa / n_noise == 0, 1 / (2 * n_noise), fa / n_noise)),
    d_prime = qnorm(hit_rate) - qnorm(fa_rate)
  )

# ------------------------------------------------------------------------------
# Section 6: Export of masked and unmasked one-cycle data
# ------------------------------------------------------------------------------

data_one_cycle_dprime_long <- data_one_cycle_dprime %>% 
  mutate(mask_SF = paste(spatial_frequency, mask_present, sep = "_"))

data_one_cycle_dprime_wide <- data_one_cycle_dprime_long %>% 
  pivot_wider(names_from = mask_SF, 
              values_from = d_prime, 
              id_cols = participant)

write.csv(data_one_cycle_dprime_wide[,-1], file = 'exp1_mask.csv', row.names = FALSE)

# ------------------------------------------------------------------------------
# Section 7: Plotting
# ------------------------------------------------------------------------------
# Renaming Columns and preparing data for plotting
data_one_cycle_dprime$cycle_number <- 1
names(data_one_cycle_dprime) <- c('participant', 'mask', 'spatial_frequency', 
                             'n_signal', 'n_noise', 'hit', 'miss', 'cr', 'fa', 
                             'hit_rate', 'fa_rate', 'd_prime', 'cycle_number')

data_one_cycle_dprime <- data_one_cycle_dprime%>%
  mutate(
    mask = if_else(mask, "Present", "Absent")
  )

data_masked_dprime$mask <- 'Present'
names(data_masked_dprime) <- c('participant', 'cycle_number', 'spatial_frequency', 
                        'n_signal', 'n_noise', 'hit', 'miss', 'cr', 'fa', 
                        'hit_rate', 'fa_rate', 'd_prime', 'mask')

# Combining data frames
combined_data <- rbind(data_masked_dprime, data_one_cycle_dprime)

# Summarize the data
plot_data <- combined_data %>%
  group_by(cycle_number, mask, spatial_frequency) %>%
  summarise(
    mean_dprime = mean(d_prime),
    error = sd(d_prime) / sqrt(n()),
    .groups = 'drop'
  )

# Creating the plot
ggplot(plot_data, aes(x = factor(cycle_number), y = mean_dprime, shape = mask)) +
  geom_errorbar(aes(ymin = mean_dprime - error, ymax = mean_dprime + error, linetype = mask, color = spatial_frequency), width = 0.3, linewidth = 0.5) +
  geom_line(aes(color = spatial_frequency, group = interaction(spatial_frequency, mask)), size = 1) +
  geom_point(aes(color = spatial_frequency, group = interaction(spatial_frequency, mask)), size = 3.1) +
  scale_color_manual(values = c("Low" = "darkgreen", "High" = "tan3")) +
  scale_shape_manual(values = c(17, 16)) +
  scale_linetype_manual(values = c("Present" = "solid", "Absent" = "dashed")) +
  labs(color = "Spatial Frequency", x = "Cycle number", y = "Sensitivity (d')", shape = "Mask", linetype = "Mask") +
  theme(
    panel.background = element_rect(fill = "white"),
    axis.line.x = element_line(colour = "gray", size = 0.5, lineend = "butt"),
    axis.line.y = element_line(colour = "gray", size = 0.5),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    legend.title = element_text(size = 20), 
    legend.text = element_text(size = 20),
    legend.key.size = unit(2, "lines"),
    axis.text = element_text(size = 16, color = 'black')
  ) +
  guides(color = guide_legend(override.aes = list(shape = NA)))

# Save the plot
ggsave('exp1.png', width = 9, height = 7, dpi = 300)
ggsave('figure_2.tiff', width = 9, height = 7, dpi = 300)
