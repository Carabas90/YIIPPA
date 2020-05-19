def insulin_adaptation(bloodglucose, bg_change, insulin_rate):
    """
    This function uses the Yale Insulin Infusion Protocol to calculate the new insulin rate,
    from the current insulin rate(in I.E/h), the current bloodglucose levels(in mg/dl), 
    and the hourly change in blood glucose (in mg/dl/h) levels since the last measurement. 
    """
    if insulin_rate >19 or insulin_rate < 0:
        raise Exception('insulin_rate out of reach of Protocol.insulin_rate has to be between 0-19 IE/h')
    elif insulin_rate < 3:
        d = 0.5 
        # The change of the insulin rate is dependant on the current insulin_rate to reflect the insulin sensitivity of the Patient.
    elif insulin_rate <= 6:
        d = 1
    elif insulin_rate <= 9:
        d = 1.5
    elif insulin_rate <= 14:
        d = 2
    elif insulin_rate <= 19:
        d = 3
    
    if bloodglucose < 75:
     insulin_rate = 0
    elif (((75 <= bloodglucose <= 99) and (-25 <= bg_change <= -1)) or 
         ((100 <= bloodglucose <= 139) and (bg_change <= -25)) or
         ((140 <= bloodglucose <= 180) and (bg_change <= -50)) or
         ((bloodglucose >= 180) and (bg_change <= -75))):
            insulin_rate -= 2*d
    elif (((75 <= bloodglucose <= 99) and ( bg_change >= 0)) or 
         ((100 <= bloodglucose <= 139) and (-24 <= bg_change <= -1)) or
         ((140 <= bloodglucose <= 180) and (-49 <= bg_change <= -26)) or
         ((bloodglucose >= 180) and (-74 <= bg_change <= -51))):
            insulin_rate -= d
    elif (((100 <= bloodglucose <= 139) and (bg_change >= 0 )) or
         ((140 <= bloodglucose <= 180) and (-25 <= bg_change <= 25)) or
         ((bloodglucose >= 180) and (-50 <= bg_change <= 0))):
            insulin_rate += 0 
    elif (((140 <= bloodglucose <= 180) and (bg_change >= 26)) or
         ((bloodglucose >= 180) and (1 <= bg_change <= 50))):
            insulin_rate += d
    elif (((bloodglucose >= 180) and (bg_change >= 50))):
            insulin_rate += 2*d
    
    return round(insulin_rate, 2)


def mmol_to_mg(mmol):
    return round(mmol*18.02 , 0)

def mg_to_mmol(mg):
    return round(mg*0.0555, 2)

if __name__ == "__main__":
   print(mmol_to_mg(mg_to_mmol(135)))
