

df_01 <- read.delim(file.choose(),sep=",",header=T)

# total noise events
fit_noise_event <- lm(noise_event ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit1)

# Call:
#   lm(formula = noise_event ~ LC_DWPTEMP + LC_RAININ + Thursday + 
#        Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min      1Q  Median      3Q     Max 
# -19.072  -7.584  -2.246   4.612 105.608 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)    8.64599    0.52528  16.460  < 2e-16 ***
#   LC_DWPTEMP     0.17027    0.04711   3.614 0.000307 ***
#   LC_RAININ    567.25519  380.87827   1.489 0.136536    
# Thursday       3.79412    0.71335   5.319 1.15e-07 ***
#   Friday         4.06053    0.71414   5.686 1.47e-08 ***
#   Saturday      -1.20497    0.71523  -1.685 0.092175 .  
# X21.00.03.00  -0.61399    0.72873  -0.843 0.399572    
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 11.57 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.03452,	Adjusted R-squared:  0.032 
# F-statistic: 13.71 on 6 and 2301 DF,  p-value: 2.323e-15

#each kinds of noise events
fit_Human.voice...Shouting <- lm(Human.voice...Shouting ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Human.voice...Shouting)

# Call:
#   lm(formula = Human.voice...Shouting ~ LC_DWPTEMP + LC_RAININ + 
#        Thursday + Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min     1Q Median     3Q    Max 
# -5.124 -1.143 -0.391  0.153 32.538 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)    1.20483    0.13876   8.683  < 2e-16 ***
#   LC_DWPTEMP    -0.09141    0.01244  -7.345 2.83e-13 ***
#   LC_RAININ     73.69481  100.61829   0.732    0.464    
# Thursday       0.96039    0.18845   5.096 3.75e-07 ***
#   Friday         1.12325    0.18866   5.954 3.02e-09 ***
#   Saturday      -0.21246    0.18894  -1.124    0.261    
# X21.00.03.00   3.08273    0.19251  16.013  < 2e-16 ***
#   ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 3.056 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.1385,	Adjusted R-squared:  0.1362 
# F-statistic: 61.65 on 6 and 2301 DF,  p-value: < 2.2e-16

fit_Human.voice...Singing <- lm(Human.voice...Singing ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Human.voice...Singing)

# Call:
#   lm(formula = Human.voice...Singing ~ LC_DWPTEMP + LC_RAININ + 
#        Thursday + Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min      1Q  Median      3Q     Max 
# -0.2930 -0.1319 -0.0854 -0.0586 14.9162 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)    0.125098   0.030286   4.131 3.75e-05 ***
#   LC_DWPTEMP    -0.005611   0.002716  -2.066  0.03895 *  
#   LC_RAININ    -15.101352  21.960293  -0.688  0.49173    
# Thursday       0.066903   0.041130   1.627  0.10395    
# Friday         0.117958   0.041175   2.865  0.00421 ** 
#   Saturday      -0.003259   0.041238  -0.079  0.93701    
# X21.00.03.00   0.023663   0.042016   0.563  0.57337    
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 0.6669 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.006633,	Adjusted R-squared:  0.004043 
# F-statistic: 2.561 on 6 and 2301 DF,  p-value: 0.01786

fit_Transport.road...Passenger.car <- lm(Transport.road...Passenger.car ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Transport.road...Passenger.car)

# Call:
#   lm(formula = Transport.road...Passenger.car ~ LC_DWPTEMP + LC_RAININ + 
#        Thursday + Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min      1Q  Median      3Q     Max 
# -12.462  -4.805  -1.350   3.690  61.609 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)    4.58447    0.29849  15.359  < 2e-16 ***
#   LC_DWPTEMP     0.27371    0.02677  10.225  < 2e-16 ***
#   LC_RAININ    574.99540  216.43739   2.657  0.00795 ** 
#   Thursday       0.92932    0.40537   2.293  0.02196 *  
#   Friday         0.56459    0.40582   1.391  0.16428    
# Saturday      -0.51258    0.40643  -1.261  0.20738    
# X21.00.03.00  -3.94786    0.41411  -9.533  < 2e-16 ***
#   ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 6.573 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.08846,	Adjusted R-squared:  0.08608 
# F-statistic: 37.21 on 6 and 2301 DF,  p-value: < 2.2e-16

fit_Transport.road...Siren <- lm(Transport.road...Siren ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Transport.road...Siren)

# Call:
#   lm(formula = Transport.road...Siren ~ LC_DWPTEMP + LC_RAININ + 
#        Thursday + Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min       1Q   Median       3Q      Max 
# -0.26856 -0.06421 -0.05673 -0.03658  2.93431 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   0.050680   0.011655   4.348 1.43e-05 ***
#   LC_DWPTEMP    0.001298   0.001045   1.242   0.2143    
# LC_RAININ    14.849571   8.451034   1.757   0.0790 .  
# Thursday     -0.007899   0.015828  -0.499   0.6178    
# Friday       -0.004605   0.015846  -0.291   0.7714    
# Saturday     -0.031197   0.015870  -1.966   0.0494 *  
#   X21.00.03.00 -0.032350   0.016169  -2.001   0.0455 *  
#   ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 0.2566 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.005779,	Adjusted R-squared:  0.003186 
# F-statistic: 2.229 on 6 and 2301 DF,  p-value: 0.03784

fit_Music.non.amplified <- lm(Music.non.amplified ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Music.non.amplified)

# Call:
#   lm(formula = Music.non.amplified ~ LC_DWPTEMP + LC_RAININ + Thursday + 
#        Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min      1Q  Median      3Q     Max 
# -0.0251 -0.0079 -0.0032  0.0006  3.9843 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   0.0160101  0.0043248   3.702 0.000219 ***
#   LC_DWPTEMP   -0.0011663  0.0003879  -3.007 0.002667 ** 
#   LC_RAININ    -0.1445312  3.1358916  -0.046 0.963243    
# Thursday     -0.0019476  0.0058733  -0.332 0.740221    
# Friday       -0.0053510  0.0058797  -0.910 0.362879    
# Saturday     -0.0026398  0.0058887  -0.448 0.653995    
# X21.00.03.00 -0.0045963  0.0059999  -0.766 0.443712    
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 0.09523 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.004582,	Adjusted R-squared:  0.001986 
# F-statistic: 1.765 on 6 and 2301 DF,  p-value: 0.1024

fit_Nature.elements...Wind <- lm(Nature.elements...Wind ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Nature.elements...Wind)

# Call:
#   lm(formula = Nature.elements...Wind ~ LC_DWPTEMP + LC_RAININ + 
#        Thursday + Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min       1Q   Median       3Q      Max 
# -0.05486 -0.01132 -0.00684 -0.00440  0.99637 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)  
# (Intercept)   0.0069090  0.0041038   1.684   0.0924 .
# LC_DWPTEMP   -0.0002751  0.0003680  -0.747   0.4549  
# LC_RAININ     3.9641003  2.9756682   1.332   0.1829  
# Thursday      0.0039695  0.0055732   0.712   0.4764  
# Friday        0.0069229  0.0055793   1.241   0.2148  
# Saturday      0.0100183  0.0055878   1.793   0.0731 .
# X21.00.03.00  0.0026375  0.0056933   0.463   0.6432  
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 0.09037 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.002801,	Adjusted R-squared:  0.0002006 
# F-statistic: 1.077 on 6 and 2301 DF,  p-value: 0.3737

fit_Unsupported <- lm(Unsupported ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_Unsupported)

# Call:
#   lm(formula = Unsupported ~ LC_DWPTEMP + LC_RAININ + Thursday + 
#        Friday + Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min     1Q Median     3Q    Max 
# -4.946 -2.348 -1.374  0.620 69.110 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)    2.251256   0.271397   8.295  < 2e-16 ***
#   LC_DWPTEMP     0.009727   0.024340   0.400    0.689    
# LC_RAININ    -49.840146 196.790059  -0.253    0.800    
# Thursday       1.968784   0.368571   5.342 1.01e-07 ***
#   Friday         2.222062   0.368977   6.022 2.00e-09 ***
#   Saturday      -0.437875   0.369540  -1.185    0.236    
# X21.00.03.00   0.340124   0.376516   0.903    0.366    
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 5.976 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.0276,	Adjusted R-squared:  0.02506 
# F-statistic: 10.88 on 6 and 2301 DF,  p-value: 5.597e-12

fit_NaN. <- lm(NaN. ~ LC_DWPTEMP + LC_RAININ + Thursday +Friday+Saturday+X21.00.03.00, data =df_01)
summary(fit_NaN.)

# Call:
#   lm(formula = NaN. ~ LC_DWPTEMP + LC_RAININ + Thursday + Friday + 
#        Saturday + X21.00.03.00, data = df_01)
# 
# Residuals:
#   Min     1Q Median     3Q    Max 
# -0.532 -0.301 -0.233 -0.169 32.680 
# 
# Coefficients:
#   Estimate Std. Error t value Pr(>|t|)    
# (Intercept)    0.406737   0.087620   4.642 3.64e-06 ***
#   LC_DWPTEMP    -0.016001   0.007858  -2.036   0.0418 *  
#   LC_RAININ    -35.162663  63.533450  -0.553   0.5800    
# Thursday      -0.125401   0.118993  -1.054   0.2921    
# Friday         0.035702   0.119124   0.300   0.7644    
# Saturday      -0.014978   0.119305  -0.126   0.9001    
# X21.00.03.00  -0.078340   0.121558  -0.644   0.5193    
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Residual standard error: 1.929 on 2301 degrees of freedom
# (4 observations deleted due to missingness)
# Multiple R-squared:  0.002844,	Adjusted R-squared:  0.0002443 
# F-statistic: 1.094 on 6 and 2301 DF,  p-value: 0.3634