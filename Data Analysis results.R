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

graphics <- list()
position <- 0
for (cat in c("Prop: 0.05", "Prop: 0.1", "Nsols: 10", "Nsols: 20")){
  position <- position + 1
  
  gr <- ggplot(analyzed %>%
           filter(startsWith(method_constr, cat)) %>% 
           mutate(pairs = str_sub(method_constr, -1)),
         aes(pairs, num_best)) +
    geom_col(fill = "blue") +
    facet_wrap(~max_time)+
    labs(
      y = "",
      x = "",
      title = cat
    )
  
  if (cat == "Prop: 0.1"){
    gr <- gr + scale_y_continuous(breaks = c(0,1,2),
                            labels = c(0,1,2))
  }
  graphics[[position]] <- gr
}

comb <- graphics[[1]] + graphics[[2]] + graphics[[3]] + graphics[[4]]
grid.newpage()
pushViewport(viewport(layout = grid.layout(
  2, 2,
  widths = unit(c(1, 21), "lines"),  # espacio para eje Y y plots
  heights = unit(c(21, 1), "lines")  # espacio para plots y eje X
)))

grid.text("Number the best solution is achieved", x = 0.1, rot = 90,
          vp = viewport(layout.pos.row = 1, layout.pos.col = 1),
          gp = gpar(fontsize = 14))

# Etiqueta del eje X (abajo)
grid.text("Elite set size (in pairs)", y = 0.1,
          vp = viewport(layout.pos.row = 2, layout.pos.col = 2),
          gp = gpar(fontsize = 14))

print(comb, vp = viewport(layout.pos.row = 1, layout.pos.col = 2))


graphics_desv <- list()
position <- 0
for (cat in c("Prop: 0.05", "Prop: 0.1", "Nsols: 10", "Nsols: 20")){
  position <- position + 1
  
  gr <- ggplot(analyzed %>%
                 filter(startsWith(method_constr, cat)) %>% 
                 mutate(pairs = str_sub(method_constr, -1)),
               aes(pairs, desv * 100)) +
    geom_col(fill = "red") +
    facet_wrap(~max_time)+
    labs(
      y = "",
      x = "",
      title = cat
    )
  
  # if (cat == "Prop: 0.1"){
  #   gr <- gr + scale_y_continuous(breaks = c(0,1,2),
  #                                 labels = c(0,1,2))
  # }
  graphics_desv[[position]] <- gr
}

comb_desv <- graphics_desv[[1]] + graphics_desv[[2]] + graphics_desv[[3]] + graphics_desv[[4]]
grid.newpage()
pushViewport(viewport(layout = grid.layout(
  2, 2,
  widths = unit(c(1, 21), "lines"),  # espacio para eje Y y plots
  heights = unit(c(21, 1), "lines")  # espacio para plots y eje X
)))

grid.text("Avg deviation to the best solution (%)", x = 0.1, rot = 90,
          vp = viewport(layout.pos.row = 1, layout.pos.col = 1),
          gp = gpar(fontsize = 14))

grid.text("Elite set size (in pairs)", y = 0.1,
          vp = viewport(layout.pos.row = 2, layout.pos.col = 2),
          gp = gpar(fontsize = 14))

print(comb_desv, vp = viewport(layout.pos.row = 1, layout.pos.col = 2))
# grid.newpage()