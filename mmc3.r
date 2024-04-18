#Final Features
#Note:  You need to additionally define a "ClassKey", one entry per row in your data matrix, which has the class labels for the training data.  

FractTO<-1:nrow(Mat)
SPP<-1:nrow(Mat)
  for (i in 1:nrow(Mat))
      SPP[i]<-sum(grepl(pattern = ".", Mat[i, ], fixed = TRUE))
      
	for (i in 1:nrow(Mat))
	if (SPP[i]==0) (SPP[i]<-1)
V1<-SPP

ParLength<-1:nrow(Mat)
 for (i in 1:nrow(Mat))
ParLength[i]<-sum(!is.na(Mat[i, ]))
V2<-ParLength

 for (i in 1:nrow(Mat))
    FractTO[i]<-  sum(grepl(pattern = ")", Mat[i, ])) 
 VPar<-FractTO
 VPar<-as.numeric(VPar>0)
 V3<-VPar


for (i in 1:nrow(Mat))
 FractTO[i]<-  sum(grepl(pattern = "-", Mat[i, ])) 
 Vdash<-FractTO
 Vdash1<-as.numeric(Vdash>0)
V4<-Vdash1


 for (i in 1:nrow(Mat))
 FractTO[i]<-  sum(grepl(pattern = ";", Mat[i, ]))
 VSem<-as.numeric(FractTO>0)

 for (i in 1:nrow(Mat))
 FractTO[i]<-   sum(grepl(pattern = ":", Mat[i, ]))
 VCol<-as.numeric(FractTO>0)

VSemCol<-as.numeric((VCol+VSem)>0)
V5<-VSemCol


for (i in 1:nrow(Mat))
     FractTO[i]<-  sum(grepl(pattern = "\\?", Mat[i, ])) 
 VQuest<-FractTO
 VQuest<-as.numeric(VQuest>0)
 V6<-VQuest


 for (i in 1:nrow(Mat))
     FractTO[i]<-  sum(grepl(pattern = "\\'", Mat[i, ])) 
 Vapos<-as.numeric(FractTO>0)
V7<-Vapos


SPP2<-1:nrow(Mat)
  for (i in 1:nrow(Mat))
      SPP2[i]<-sum(grepl(pattern = ".", Mat[i, ], fixed = TRUE))      
 Sentence<-which(as.numeric(apply(t(Mat), c(1,2), grepl, pattern = ".", fixed = TRUE))==1)
 for (i in (nrow(Mat)-1):1)  #Note 48 is the number of rows minus 1
     for (j in 1:sum(SPP2)) #Note: 121 is the total number of sentneces -- found by sum(SPP)
         if (Sentence[j]>300*i) (Sentence[j]<-Sentence[j]-300*i) 
  Sentence2<-Sentence
 for (i in sum(SPP2):2)
     (ifelse (Sentence[i]>Sentence[i-1], Sentence2[i]<-Sentence[i]-Sentence[i-1], Sentence2[i]<-Sentence[i]))

V8<-1:length(V5)   ##V8 is the standard deviation of the sentence length for the paragraph.
start_idx <- 1 # Index of first unused value.

for (i in seq_along(SPP2)) {
  end_idx <- start_idx + SPP2[i] - 1 # Index of last value to use.
  vals <- Sentence2[start_idx:end_idx] # Subset of values from Sentence2 to use
  std_dev <- sd(vals) # Calculate standard deviation of subset
  V8[i] <- std_dev # Store standard deviation in V8
  start_idx <- end_idx + 1 # Update index of first unused value in Sentence2
}
V8[is.na(V8)]<-0

 Sentence3<-Sentence2
 for (i in 1:sum(SPP2))
     Sentence3[i]<-Sentence2[i+1]-Sentence2[i]
	Sentence3[sum(SPP2)]<-Sentence2[sum(SPP2)]-Sentence2[(sum(SPP2)-1)]

V9<-1:length(V5) 
start_idx <- 1 # Index of first unused value
 
 for (i in seq_along(SPP2)) {
     end_idx <- start_idx + SPP2[i] - 1 # Index of last value to use 
     vals <- Sentence3[start_idx:end_idx] # Subset of values from Sentence3 to use
     std_dev <- mean(abs(vals)) # Calculate abs value of median of subset
     V9[i] <- std_dev # Store standard deviation in V9
     start_idx <- end_idx + 1 # Update index of first unused value in Sentence3
 }

V10<-V7     #V10 is a yes/no answer to whether there is a sentence with <11 words in the parag.
 
start_idx <- 1 # Index of first unused value
 for (i in seq_along(SPP2)) {
     end_idx <- start_idx + SPP2[i] - 1 # Index of last value to use in Sentence2
     vals <- Sentence2[start_idx:end_idx] # Subset of values from Sentence2 to use
     result <- ifelse(any(vals < 11), 0, 1)  #a true/false test if there is a sentence w <11 words
     V10[i] <- result # Store answer in V10
     start_idx <- end_idx + 1 # Update index of first unused value in Sentence2
 }


V11<-V7     #V11 is a yes/no answer to whether there is a sentence with >34 words in the parag.
 start_idx <- 1 # Index of first unused value
 
 for (i in seq_along(SPP2)) {
     end_idx <- start_idx + SPP2[i] - 1 # Index of last value to use in Sentence2
     vals <- Sentence2[start_idx:end_idx] # Subset of values from Sentence2 to use
      result <- ifelse(any(vals > 34), 0, 1)  #a true/false test if there is a sentence w >34 words
     V11[i] <- result # Store answer in V11
     start_idx <- end_idx + 1 # Update index of first unused value in Sentence2
 }


 for (i in 1:nrow(Mat))
     FractTO[i]<-   length(which(tolower(iconv(Mat[i, ], to="ASCII//TRANSLIT")) == "although"))

 VAlth<-as.numeric(FractTO>0)
V12<-VAlth

 for (i in 1:nrow(Mat))
 FractTO[i]<-  sum(grepl(pattern = "However", Mat[i, ])) 
 VHow<-FractTO
V13<-VHow

 for (i in 1:nrow(Mat))
FractTO[i]<-   length(which(tolower(iconv(Mat[i, ], to="ASCII//TRANSLIT")) == "but"))
 VBut<-as.numeric(FractTO>0)
V14<-VBut

 for (i in 1:nrow(Mat))
 FractTO[i]<-   length(which(tolower(iconv(Mat[i, ], to="ASCII//TRANSLIT")) == "because"))
VBec<-as.numeric(FractTO>0)
V15<-VBec


 for (i in 1:nrow(Mat))
FractTO[i]<-   length(which(tolower(iconv(Mat[i, ], to="ASCII//TRANSLIT")) == "this"))
 Vthis<-as.numeric(FractTO>0)
 V16<-Vthis

###Note: these capture more than "hers" Ex: others, researchers.  
for (i in 1:nrow(Mat))
     FractTO[i]<-  as.numeric(sum(grepl(pattern = "hers", Mat[i, ])) >0)
 Vhers<-FractTO
 V17<-Vhers

for (i in 1:nrow(Mat))
     FractTO[i]<-  as.numeric((sum(grepl(pattern = "[0-9]", Mat[i, ])))>0)
 VNums<-as.numeric(FractTO)
 V18<-VNums

library(stringr) 
for (i in 1:nrow(Mat))
(
     FractTO[i]<- length(which(str_count(Mat[i, ], "[A-Z]")>0))/SPP[i]
 )
 V19<-as.numeric(FractTO>2)

 for (i in 1:nrow(Mat))
     FractTO[i]<-   length(which(Mat[i, ] == "et"))
 Vet<-as.numeric(FractTO>0)
V20<-Vet


TestMat<-matrix(0, nrow(Mat), 21)
TestMat[,1 ]<-ClassKey  #The class assignments need to be provided as "ClassKey"
TestMat[,2 ]<-V1
TestMat[,3 ]<-V2
TestMat[,4 ]<-V3
TestMat[,5 ]<-V4
TestMat[,6 ]<-V5
TestMat[,7 ]<-V6
TestMat[,8 ]<-V7
TestMat[,9 ]<-V8
TestMat[,10 ]<-V9
TestMat[,11 ]<-V10
TestMat[,12 ]<-V11
TestMat[,13 ]<-V12
TestMat[,14 ]<-V13
TestMat[,15 ]<-V14
TestMat[,16 ]<-V15
TestMat[,17 ]<-V16
TestMat[,18 ]<-V17
TestMat[,19 ]<-V18
TestMat[,20 ]<-V19
TestMat[,21 ]<-V20