def calculate_risk(income,credit,emi):
 score=(30 if income>100000 else 20)+(40 if credit>=750 else 20)+(30 if emi/max(income,1)<0.3 else 10)
 return min(score,100)
