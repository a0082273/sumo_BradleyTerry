library("BradleyTerry2")

data <- read.csv("torikumi_btmodel_data/201805_bt_all.csv")
#data <- read.csv("torikumi_btmodel_data/201805_bt_rm_ketsujo.csv")
data[, 1] <- NULL

bt_model <- BTm(
  outcome = cbind(e_win, w_win), 
  player1 = e_rikishi, player2 = w_rikishi, 
  data = data)
BTabilities(bt_model)

write.csv(BTabilities(bt_model), "torikumi_btmodel_data/201805_bt_ability_all.csv", quote=FALSE, row.names=TRUE)
#write.csv(BTabilities(bt_model), "torikumi_btmodel_data/201805_bt_ability_rm_ketsujo.csv", quote=FALSE, row.names=TRUE)
