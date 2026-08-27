def predict_default(income,credit,emi):
 risk=max(0,min(95,100-((credit-300)/6)-(income/5000)+(emi/1000)))
 return round(risk,1)
