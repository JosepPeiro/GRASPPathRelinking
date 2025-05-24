library(dplyr)
library(ggplot2)
library(patchwork)
library(stringr)
library(grid)

data <- data.frame()
path <- "results/PR/"

for (csv in list.files("results/PR/")){
  readed <- read.csv(paste0(path, csv))
  data <- rbind(data, readed)
}

data <- data %>% mutate(
  local_search_before = as.logical(local_search_before),
  local_search_after = as.logical(local_search_after),
  random_pairs = ifelse(random_pairs == "None", 0, as.integer(random_pairs))
) %>% select(-alpha, -iters)


comp_befF_aftF <- data%>% filter(local_search_after == FALSE,
                                 local_search_before == FALSE)

comp_befT_aftF <- data%>% filter(local_search_after == FALSE,
                                 local_search_before == TRUE)

comp_befF_aftT <- data%>% filter(local_search_after == TRUE,
                                 local_search_before == FALSE)

comp_befT_aftT <- data%>% filter(local_search_after == TRUE,
                                 local_search_before == TRUE)

befT_F <-inner_join(comp_befF_aftF, comp_befT_aftF,
                    by = c("path", "max_time", "nsols", "prop_time_grasp", "random_pairs"),
                    suffix = c("_F", "_T")) %>% 
  select(obj_value_F, obj_value_T) %>% 
  mutate(diff = obj_value_T - obj_value_F)

test_bef <- t.test(befT_F$diff,
                         mu = 0,
                         alternative = "greater")
test_bef$p.value
mean(befT_F$diff)
mean(befT_F$diff > 0)

aftT_F <-inner_join(comp_befF_aftF, comp_befF_aftT,
                    by = c("path", "max_time", "nsols", "prop_time_grasp", "random_pairs"),
                    suffix = c("_F", "_T")) %>% 
  select(obj_value_F, obj_value_T) %>% 
  mutate(diff = obj_value_T - obj_value_F)

test_aft <- t.test(aftT_F$diff,
                         mu = 0,
                         alternative = "greater")
test_aft$p.value
mean(aftT_F$diff)
mean(aftT_F$diff > 0)


bTfF_bfT <-inner_join(comp_befT_aftF, comp_befT_aftT,
                      by = c("path", "max_time", "nsols", "prop_time_grasp", "random_pairs"),
                      suffix = c("_TF", "_TT")) %>% 
  select(obj_value_TF, obj_value_TT) %>% 
  mutate(diff = obj_value_TT - obj_value_TF)


bFfT_bfT <-inner_join(comp_befF_aftT, comp_befT_aftT,
                      by = c("path", "max_time", "nsols", "prop_time_grasp", "random_pairs"),
                      suffix = c("_FT", "_TT")) %>% 
  select(obj_value_FT, obj_value_TT) %>%
  mutate(diff = obj_value_TT - obj_value_FT)

hist(bTfF_bfT$diff)
t.test(bTfF_bfT$diff,mu = 0,alternative = "greater")$p.value
mean(bTfF_bfT$diff)
mean(bTfF_bfT$diff > 0)

t.test(bFfT_bfT$diff,mu = 0,alternative = "greater")$p.value
mean(bFfT_bfT$diff)
mean(bFfT_bfT$diff > 0)


##############################################################
##############################################################

df <- data %>% filter(local_search_before == T,
                      local_search_after == T) %>% 
  select(-local_search_before,
         -local_search_after)

analyzed <- df %>%
  mutate(
    method_constr = ifelse(
      nsols == 999999,
      paste0("Prop: ", prop_time_grasp, " - pairs: ", random_pairs),
      paste0("Nsols: ", nsols, " - pairs: ", random_pairs)
    )
  ) %>% 
  group_by(path, max_time) %>% 
  mutate(best = max(obj_value),
         diff_best = (best - obj_value) / best) %>%
  ungroup() %>% 
  select(-prop_time_grasp, -nsols, -random_pairs, -time_taken) %>%
  group_by(max_time, method_constr) %>%
  reframe(num_best = sum(best == obj_value),
          desv = mean(diff_best))

max_best <- analyzed %>% 
  group_by(max_time) %>%
  slice_max(order_by = num_best, n = 5) %>%
  ungroup()

min_desv <- analyzed %>% 
  group_by(max_time) %>%
  slice_min(order_by = desv, n = 5) %>%
  ungroup()

both_best <- intersect(distinct(max_best), distinct(min_desv))
both_best

only_grasp_files_all <- list.files("results")
only_grasp_files <- only_grasp_files_all[grepl("csv$", only_grasp_files_all)]
grasp_only <- data.frame()
for (csv in only_grasp_files){
  readed_gr <- read.csv(paste0("results/", csv))
  readed_gr$time <- as.integer(strsplit(strsplit(csv, "-")[[1]][3], "[.]")[[1]][1])
  grasp_only <- rbind(grasp_only, readed_gr)
}

union_datas <- grasp_only %>%
  filter(alpha == 0.1) %>%
  select(instance, obj_value, time) %>%
  mutate(time = ifelse(time == 0, 0.1, time)) %>% 
  inner_join(data %>% 
               filter(local_search_before == TRUE,
                      local_search_after == TRUE,
                      nsols %in% c(10,20)) %>% 
               select(path, max_time, nsols, random_pairs, obj_value) %>% 
               mutate(path = gsub("\\.txt$", "", path)),
             by = c("instance" = "path",
                    "time" = "max_time"),
             suffix = c("_grasp", "_pr"))

small <- union_datas %>% 
  filter(time %in% c(0.1, 1, 5),
         nsols == 20,
         random_pairs == 3) %>% 
  mutate(diff = obj_value_pr - obj_value_grasp)
hist(small$diff)

test_small <- t.test(small$diff,
                   mu = 0,
                   alternative = "greater")
test_small$p.value
mean(small$diff)
mean(small$diff > 0)


biggo <- union_datas %>% 
  filter(time %in% c(10, 15, 60),
         nsols == 10,
         random_pairs == 4) %>% 
  mutate(diff = obj_value_pr - obj_value_grasp)
hist(biggo$diff)

test_biggo <- t.test(biggo$diff,
                   mu = 0,
                   alternative = "greater")
test_biggo$p.value
mean(biggo$diff)
mean(biggo$diff > 0)

ggplot(small, aes(diff)) + theme_minimal() +geom_histogram(fill = "lightblue", color = "black")+
  labs(title = "Difference for low executing time observations",
       x = "Differences", y = "Frequency")
ggplot(biggo, aes(diff)) + theme_minimal() +geom_histogram(fill = "lightgreen", color = "black")+
  labs(title = "Difference for high executing time observations",
       x = "Differences", y = "Frequency")
