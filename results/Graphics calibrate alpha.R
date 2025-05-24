library(readxl)
library(ggplot2)

files <- list.files("results/analyzed")[grep(".xlsx", list.files("results/analyzed"))]
all_data <- data.frame()
for (f in files){
  read <- readxl::read_excel(paste0("results/analyzed/",f), skip = 1)
  time <- as.integer(strsplit(strsplit(f, "[-]")[[1]][3], "[.]")[[1]][1])
  data_time <- t(rbind(colnames(read), c("Time",rep(time, 12)), read))
  row.names(data_time) <- NULL
  data_time <- data_time[2:nrow(data_time),]
  
  all_data <- rbind(all_data, data_time)
}
colnames(all_data) <- c("alpha", "time", "n_best", "desv_best")
all_data$alpha <- gsub("^α = ", "", all_data$alpha)
all_data$time[all_data$time == 0] <- 0.1
all_data$time <- as.numeric(all_data$time)
all_data$n_best <- as.numeric(all_data$n_best)
all_data$desv_best <- as.numeric(all_data$desv_best)


ggplot2::ggplot(all_data, aes(alpha, n_best)) +
  geom_col(fill = "blue") +
  facet_wrap(~time, scales = "free_y")+
  theme_light()+
  xlab("α") + ylab("Number of times the maximum is reached")+
  labs(title = "Number of times the best solution is reached for each α and different times")

ggplot2::ggplot(all_data, aes(alpha, round(desv_best,5))) +
  geom_col(fill = "red") +
  facet_wrap(~time, scales = "free_y") +
  theme_light()+
  xlab("α") + ylab("Average deviation from the maximum")+
  labs(title = "Mean deviation to the best solution for all instances for each α and different times")
