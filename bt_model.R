library("BradleyTerry2")

#data <- read.csv("input/torikumi_btmodel_data/201801_bt_all.csv")
data <- read.csv("input/torikumi_btmodel_data/201801_bt_rm_kyujo.csv")
data[, 1] <- NULL

bt_model <- BTm(
  outcome = cbind(e_win, w_win),
  player1 = e_rikishi, player2 = w_rikishi,
  data = data)
BTabilities(bt_model)

#write.csv(BTabilities(bt_model), "input/bt_ability/201801_bt_ability_all.csv", quote=FALSE, row.names=TRUE)
write.csv(BTabilities(bt_model), "input/bt_ability/201801_bt_ability_rm_kyujo.csv", quote=FALSE, row.names=TRUE)
