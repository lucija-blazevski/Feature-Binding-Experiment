# Feature binding is slow: temporal integration explains apparent ultrafast binding
# JASP Data Preparation and Plotting Script for Experiment 2

# ------------------------------------------------------------------------------
# Section 1: Library and data loading 
# ------------------------------------------------------------------------------

# Load necessary libraries
library(plyr)
library(tidyverse)
library(ggplot2)
library(stringr)
library(rempsyc)

# Set working directory and select a folder from which files would be read
setwd("C:/Users/Lucija/Desktop/binding_paper/data/raw_data_anonimized/")
mydir = "experiment 2"
myfiles = list.files(path=mydir, pattern="*.csv", full.names=TRUE)

# Load data
st_data = ldply(myfiles, read_csv)

detach(package:plyr)

# ------------------------------------------------------------------------------
# Section 2: Data manipulation
# ------------------------------------------------------------------------------

# Move staircase reversal number one up as it lags in the experiment script
st_data <- st_data %>%
  group_by(participant, staircase_name) %>%
  arrange(participant, staircase_name, staircase_trial_num) %>%
  mutate(staircase_reversal = lead(staircase_reversal, 1),
         staircase_reversal_num = lead(staircase_reversal_num, 1))

# ------------------------------------------------------------------------------
# Section 3: Staircase convergence analysis
# ------------------------------------------------------------------------------

reversal_counts <- st_data %>%
  filter(staircase_phase == 1) %>%
  group_by(participant, staircase_name) %>%
  summarize(reversal_count = sum(staircase_reversal, na.rm = T))
reversal_counts

min_across_participants <- reversal_counts %>%
  group_by(staircase_name) %>%
  summarise(min_last_reversal = min(reversal_count))%>%
  mutate(staircase_name = case_when(
    grepl("high", staircase_name) & grepl("_1", staircase_name) ~ "High SF - 1 Cycle",
    grepl("high", staircase_name) & grepl("_2", staircase_name) ~ "High SF - 2 Cycles",
    grepl("high", staircase_name) & grepl("_3", staircase_name) ~ "High SF - 3 Cycles",
    grepl("high", staircase_name) & grepl("_4", staircase_name) ~ "High SF - 4 Cycles",
    grepl("high", staircase_name) & grepl("_6", staircase_name) ~ "High SF - 6 Cycles",
    grepl("low", staircase_name) & grepl("_1", staircase_name) ~ "Low SF - 1 Cycle",
    grepl("low", staircase_name) & grepl("_2", staircase_name) ~ "Low SF - 2 Cycles",
    grepl("low", staircase_name) & grepl("_3", staircase_name) ~ "Low SF - 3 Cycles",
    grepl("low", staircase_name) & grepl("_4", staircase_name) ~ "Low SF - 4 Cycles",
    grepl("low", staircase_name) & grepl("_6", staircase_name) ~ "Low SF - 6 Cycles",
    TRUE ~ staircase_name
  ))
colnames(min_across_participants) <- c('Condition', 'Number of Reversals')
nice_table(min_across_participants, title = 'Minimum Last Reversal Number per Staircase')
# Very low reversal number in some low SF staircases

low_reversal_counts <- reversal_counts[reversal_counts$reversal_count<15,] # Participant 7 problematic
low_reversal_counts

# Plot all staircases for all participants
# Loop through each participant in myfiles
for (i in 1:length(myfiles)) {
  
  # Read in data and preprocess
  participant <- plyr::ldply(myfiles[i], read_csv)
  participant <- participant[-nrow(participant), ]
  participant <- participant %>%
    group_by(participant, staircase_name) %>%
    arrange(participant, staircase_name, staircase_trial_num) %>%
    mutate(staircase_reversal = lead(staircase_reversal, 1),
           staircase_reversal_num = lead(staircase_reversal_num, 1))
  
  # For clear title
  participant <- participant %>%
    mutate(staircase_name = gsub("high_", "High SF - ", staircase_name)) %>%
    mutate(staircase_name = gsub("low_", "Low SF - ", staircase_name)) %>%
    mutate(staircase_name = gsub("_", "-", staircase_name)) %>%
    mutate(staircase_name = gsub("- 1", "- 1-Cycle", staircase_name)) %>%
    mutate(staircase_name = gsub("- 2", "- 2-Cycles", staircase_name)) %>%
    mutate(staircase_name = gsub("- 3", "- 3-Cycles", staircase_name)) %>%
    mutate(staircase_name = gsub("- 4", "- 4-Cycles", staircase_name)) %>%
    mutate(staircase_name = gsub("- 5", "- 5-Cycles", staircase_name)) %>%
    mutate(staircase_name = gsub("- 6", "- 6-Cycles", staircase_name))
  
  # Generate plot - uncomment if you want to save plots:
  # png(paste0('st_participant_', i, '.png'), width = 1000, height = 800)
  print(ggplot(data = participant, aes(x = staircase_trial_num, y = staircase_dv*(1/165*1000)))+
          geom_point(aes(color = staircase_reversal))+
          geom_line()+
          facet_wrap(~staircase_name, ncol = 2)+
          labs(x = 'Staircase trial number', y = 'Stimulus duration (ms)',title = paste0('Participant ', i))+
          theme(panel.grid = element_blank(), 
                legend.position = 'none',
                panel.background = element_rect(fill = "white"),
                plot.title = element_text(size = 20, 
                                          face = "italic", 
                                          color = "black",
                                          hjust = 0,
                                          vjust = 1),
                axis.line.x = element_line(colour = "gray", 
                                           size = 0.5, 
                                           lineend = "butt"),
                axis.line.y = element_line(colour = "gray", 
                                           size = 0.5),
                axis.title.x = element_text(size = 20),
                axis.title.y = element_text(size = 20),
                axis.text = element_text(size = 14, color = 'black'),
                strip.text = element_text(size = 20)) +
          scale_color_manual(values = c('lightgray', 'red')))
 # Uncomment if you want to save plots:
 # dev.off() 
}

# Comment on exclusion:
# 1. Participant 7 problematic:
#     - 0 reversals in 6-cycle-low-SF condition
#     - 5 reversals in 4-cycle-low-SF condition
#     - 7 reversals in 3-cycle-low-SF condition
# 2. 6-cycle-low-SF condition is to easy and does not converge
# Therefore, exclusion of high and low SF 6-cycle conditions (for balanced design) and participant 7

# ------------------------------------------------------------------------------
# Section 4: Exclusion and threshold extraction
# ------------------------------------------------------------------------------

# Extract median thresholds
thresholds <-
  st_data %>%
  ungroup() %>%
  # Removing low and high SF 6-cycle-condition
  select(threshold_low1, threshold_low2, threshold_low3, threshold_low4,
         threshold_high1, threshold_high2, threshold_high3, threshold_high4) %>%
  na.omit() %>% 
  t() %>% 
  as.data.frame()

# Add the factors
thresholds$Cycles <- rep(c(1,2,3,4), times = 2)
thresholds$SF <- rep(c('Low', 'High'), each = 4)

# Make nice columns names
colnames(thresholds)<- c(paste('P',sep = '_', seq(1,length(myfiles))), 'Cycle', 'SF')

# Change the mode of cycle
thresholds$Cycle<- as.integer(thresholds$Cycle)

# Exclude participant for which staircase didn't converge
thresholds <- thresholds [,-7]

# Make into a long format
data_long <- gather(thresholds, Participant, Threshold, P_1:P_11, factor_key=TRUE)
data_long$Threshold<- as.numeric(data_long$Threshold)

# Calculate mean in milliseconds
data_long <- data_long%>%
  group_by(SF, Cycle)%>%
  mutate(Mean = mean(Threshold), 
         Mean_ms = mean(Threshold)*6.0606, 
         SE_ms = sd(Threshold) / sqrt(n()))

# ------------------------------------------------------------------------------
# Section 5: Data export
# ------------------------------------------------------------------------------

# First, create a new column that combines the levels of Cycle and SF
data_long <- data_long %>% 
  mutate(Cycle_SF = paste(SF, Cycle, sep = "_"))

# Then pivot the data
data_wide <- data_long %>% 
  pivot_wider(names_from = Cycle_SF, 
              values_from = Threshold, 
              id_cols = Participant)

# Write the data frame to a CSV file
write.csv(data_wide[,-1], file = "exp2.csv", row.names = FALSE)

# ------------------------------------------------------------------------------
# Section 6: Plotting
# ------------------------------------------------------------------------------

data_to_plot <- data_long %>%
  group_by(Cycle, SF) %>%
  summarize(Mean_ms = mean(Threshold * 6.0606),
            SE_ms = sd(Threshold * 6.0606) / sqrt(n()))

ggplot(data_to_plot, aes(x = factor(Cycle), y = Mean_ms, color = factor(SF))) +
  geom_line(aes(group = SF), linewidth = 0.8) +
  geom_point(size = 2) +
  geom_errorbar(aes(ymin = Mean_ms - SE_ms, 
                    ymax = Mean_ms + SE_ms), 
                width = 0.2) +
  scale_color_manual(values = c("High" = "tan3", "Low" = "#067D06")) +
  labs(x = 'Number of cycles', color = 'Spatial frequency', 
       y = 'Stimulus duration for 75% accuracy (ms)') +
  theme (
    text = element_text(size=16, color = 'black'),
    panel.background = element_rect(fill = "white"),
    axis.line.x = element_line(colour = "black", 
                               linewidth = 0.4, 
                               lineend = "butt"),
    axis.line.y = element_line(colour = "black", 
                               linewidth = 0.4),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    legend.title = element_text(size=16), 
    legend.text = element_text(size=16),
    axis.text = element_text(size = 16, color = 'black'),
    strip.text = element_text(size = 16),
    legend.key.size = unit(2, "lines"))

ggsave('exp2.png', width = 8, height = 6, dpi = 300)
ggsave('figure_3.tiff', width = 9, height = 7, dpi = 300)
