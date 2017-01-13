data_complete<-data.frame()
districts<-dir(path = 'districts/')
for (district in districts) {
        data_district<-data.frame()
        print(district)
        
        files <-
                dir(path = paste0('districts/',district),
                    pattern = '\\.csv$',
                    full.names = TRUE)
        for (file in files) {
                toppic=sub(".*/.*/", "", file, perl=TRUE)
                toppic=sub("\\.csv", "_", toppic, perl=TRUE)
                data_to_add <- read.csv(file)
                
                data_to_add <-
                        setNames (data_to_add, c(
                                names(data_to_add)[1],
                                paste0(toppic, names(data_to_add)[-1])
                        ))
                
                if (nrow(data_district) > 0) {
                        data_district <-
                                merge(data_district, data_to_add, by = "VDC.MUNICIPALITY")
                } else {
                        data_district <- data_to_add
                }
        }
        data_district <- cbind(DISTRICT = toupper(district), data_district)
        data_complete<-rbind(data_complete,data_district)
}
write.csv(data_complete,quote = FALSE,row.names = FALSE, file="districts_complete.csv")