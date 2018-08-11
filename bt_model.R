library("BradleyTerry2")

#bashoId = "201801" #input from main.py

infile <- paste("input/torikumi_btmodel_data/", bashoId, "_bt.csv", sep="")
data <- read.csv(infile)
data[, 1] <- NULL

bt_model <- BTm(
  outcome = cbind(e_win, w_win),
  player1 = e_rikishi, player2 = w_rikishi,
  data = data)
BTabilities(bt_model)

outfile <- paste("input/bt_ability/", bashoId, "_bt_ability.csv", sep="")
write.csv(BTabilities(bt_model), outfile, quote=FALSE, row.names=TRUE)
