from .generalUtils import *

PAX_S60 = 2
SPECTRA_T300 = 1
LANDI_A8 = 0

bilingualDict = {
	"SALE":"銷售",
    "VOID":"撤銷",
    "REFUND":"退款",
    "RETRIEVAL":"查詢",
    "MID":"商戶號",
    "TID":"終端號",
    "DATE":"日期",
    "TIME":"時間",
    "BATCH":"批次號",
    "TRACE":"交易號",
    "PAN":"卡號",
    "EXPDATE":"有效期",
    "APPCODE":"授權碼",
    "REFNUM":"參考號",
    "TOTAL":"總計",
    "NET":"淨額",
    "SIGNATURE":"簽名",
    "NOSIGNATURE":"不需簽名",
    "ACCEPTED":"接受",
    "REJECTED":"不接受"
}

haseLoyaltyDict = {
    "HSD":"HASE CASH$",
    "JDD":"enJoy$"
}

sign_list = ["M","S","C","F","W","A","B"]

dccCurCodeDict = {
    "036" : "AUD",
    "124" : "CAD",
    "156" : "CNY",
    "196" : "CPY",
    "208" : "DKK",
    "344" : "HKD",
    "352" : "ISK",
    "356" : "INR",
    "360" : "IDR",
    "392" : "JPY",
    "410" : "KRW",
    "446" : "MOP",
    "458" : "MYR",
    "470" : "MTL",
    "554" : "NZD",
    "578" : "NOK",
    "608" : "PHP",
    "702" : "SGD",
    "710" : "ZAR",
    "752" : "SEK",
    "756" : "CHF",
    "764" : "THB",
    "826" : "GBP",
    "840" : "USD",
    "901" : "TWD",
    "978" : "EUR"
}

responseCodeMsgDict = {
    '400':"請聯絡易辦事",
    '401':"請聯絡易辦事",
    '402':"請聯絡易辦事",
    '403':"請聯絡易辦事",
    '404':"請聯絡易辦事",
    '410':"請聯絡易辦事",
    '413':"請聯絡易辦事",
    '414':"請聯絡易辦事",
    '427':"請聯絡易辦事",
    '428':"請聯絡易辦事",
    '405':"請重新操作",
    '409':"請重新操作",
    '411':"請重新操作",
    '412':"請重新操作",
    '415':"請與銀行聯絡",
    '420':"請與銀行聯絡",
    '416':"銀行系統故障",
    '421':"銀行系統故障",
    '417':"戶口已被取消",
    '418':"戶口選擇錯誤",
    '419':"此卡已失效",
    '422':"請查詢銀行",
    '423':"轉賬超過限額",
    '424':"密碼重按過限額",
    '425':"私人密碼錯誤",
    '426':"請重新操作",
    '444':"不接納此卡",
    '500':"請重新操作",
    '504':"請重新操作",
    '506':"請重新操作",
    '509':"請重新操作",
    '512':"請重新操作",
    '514':"請重新操作",
    '515':"請重新操作",
    '520':"請重新操作",
    '522':"請重新操作",
    '523':"請重新操作",
    '530':"請重新操作",
    '532':"請重新操作",
    '533':"請重新操作",
    '538':"請重新操作",
    '505':"請聯絡易辦事",
    '528':"請聯絡易辦事",
    '529':"請聯絡易辦事",
    '507':"其他原因",
    '508':"其他原因",
    '516':"其他原因",
    '517':"核對錯誤",
    '519':"其他原因",
    '535':"卡上資料錯誤",
    '536':"請重新操作",
    '537':"不接納此卡",
    '539':"其他原因",
    '541':"請重新操作",
    '542':"轉賬超過限額",
    '543':"其他原因",
    '550':"請結算 / 核賬",
    '557':"取款金額不符",
    '575':"請聯絡易辦事",
    '612':"其他原因",
    '613':"其他原因",
    '614':"其他原因",
    '645':"請聯絡易辦事",
    '646':"請聯絡易辦事",
    '900':"請重新操作",
    '902':"請重新操作",
    '901':"請重新操作",
    '909':"MAC錯誤"
}

def __packEPSResponseCodeMsg(respCode,transData,printOut):
    #in the table 
    if respCode in responseCodeMsgDict:
        printOut.append(print_at_middle(responseCodeMsgDict[transData["RESP"]],False))
        printOut.append(print_at_middle(transData["RESPMSG"],True))
        #Chinese + nextline + English
        transData["RESPMSG"] = responseCodeMsgDict[transData["RESP"]] + "\n" + transData["RESPMSG"]
        #matched the resp code, return 
        return
    try:
        int_respCode = int(respCode)
        #check range
        if int_respCode >= 918 and int_respCode <= 959:
            printOut.append(print_at_middle("請聯絡卡中心",False))
            printOut.append(print_at_middle(transData["RESPMSG"],True))
            #Chinese + nextline + English
            transData["RESPMSG"] = "請聯絡卡中心" + "\n" + transData["RESPMSG"]

        elif int_respCode >= 960 and int_respCode <= 999:
            printOut.append(print_at_middle("請聯絡銀行",False))
            printOut.append(print_at_middle(transData["RESPMSG"],True))
            #Chinese + nextline + English
            transData["RESPMSG"] = "請聯絡銀行" + "\n" + transData["RESPMSG"]
        else:
            printOut.append(print_at_middle("其他原因",False))
            printOut.append(print_at_middle(transData["RESPMSG"],True))
            #Chinese + nextline + English
            transData["RESPMSG"] = "其他原因" + "\n" + transData["RESPMSG"]
    except:
        printOut.append(print_at_middle("其他原因",False))
        printOut.append(print_at_middle(transData["RESPMSG"],True))
        #Chinese + nextline + English
        transData["RESPMSG"] = "其他原因" + "\n" + transData["RESPMSG"]

def __add_minus(cmd):
    if cmd == "VOID" or cmd == "REFUND":
        return "-"
    else:
        return ""

#Pack transData
def formatTransDataTerminal(rawData,transData,modelType):
    if modelType == PAX_S60:
        #CMD and TYPE
        if rawData[0:1] == "0":
            transData["CMD"] = "SALE"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "2":
            transData["CMD"] = "REFUND"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "3":
            transData["CMD"] = "VOID"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "4":
            transData["CMD"] = "RETRIEVAL"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "5":
            transData["CMD"] = "SALE"
            transData["TYPE"] = "EPS"
        elif rawData[0:1] == "6":
            transData["CMD"] = "RETRIEVAL"
            transData["TYPE"] = "EPS"
        elif rawData[0:1] == "@":
            transData["CMD"] = "SALE"
            transData["TYPE"] = "UPI"
        elif rawData[0:1] == "A":
            transData["CMD"] = "VOID"
            transData["TYPE"] = "UPI"
        elif rawData[0:1] == "D":
            transData["CMD"] = "RETRIEVAL"
            transData["TYPE"] = "UPI"
        elif rawData[0:1] == "I" or rawData[0:1] == "J" or rawData[0:1] == "K":
            transData["CMD"] = "MEMBER"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "P":
            transData["CMD"] = "MEMBER"
            transData["TYPE"] = "VAC"
        elif rawData[0:1] == "Q":
            transData["CMD"] = "VOID"
            transData["TYPE"] = "VAC"

        
        #discard the MessageType
        rawData = rawData[1:]
        if transData["TYPE"] == "EDC":
            if transData["CMD"] != "MEMBER":
                transData["RESP"] = rawData[0:3]
                rawData = rawData[3:]
                transData["RESPMSG"] = rawData[0:20]
                rawData = rawData[20:]
                #ignore 1 byte original trans type
                rawData = rawData[1:]
                transData["ECRREF"] = rawData[0:16]
                rawData = rawData[16:]
                try:
                    transData["AMT"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                    transData["TIPS"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                except:
                    transData["AMT"] = 0.00
                    transData["TIPS"] = 0.00
                    rawData = rawData[12:]
                    rawData = rawData[12:]

                transData["DATE"] = rawData[0:8]
                rawData = rawData[8:]
                transData["TIME"] = rawData[0:6]
                rawData = rawData[6:]
                transData["CARD"] = rawData[0:10]
                rawData = rawData[10:]
                transData["PAN"] = rawData[0:19]
                rawData = rawData[19:]
                transData["EXPDATE"] = rawData[0:4]
                rawData = rawData[4:]
                transData["TERMINALID"] = rawData[0:8]
                rawData = rawData[8:]
                transData["MERCHANTID"] = rawData[0:15]
                rawData = rawData[15:]
                transData["TRACE"] = rawData[0:6]
                transData["INVOICE"] = rawData[0:6]
                rawData = rawData[6:]
                transData["BATCHNO"] = rawData[0:6]
                rawData = rawData[6:]
                transData["APPCODE"] = rawData[0:6]
                rawData = rawData[6:]
                transData["REFNUM"] = rawData[0:12]
                rawData = rawData[12:]

                #DCC
                if rawData[0:3] != "   ":
                    transData["CURRCODE"] = rawData[0:3]
                    rawData = rawData[3:]
                    transData["FXRATE"] = float(rawData[1:8])/(10 ** int(rawData[0:1]))
                    rawData = rawData[8:]
                    transData["FOREIGNAMT"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                else:
                    rawData = rawData[3:]
                    rawData = rawData[8:]
                    rawData = rawData[12:]

                #Entry Mode
                transData["ENTRYMODE"] = rawData[0:1]
                rawData = rawData[1:]

                if transData["ENTRYMODE"] in sign_list:
                    transData["SIGNBLOCK"] = "N"
                else:
                    transData["SIGNBLOCK"] = "Y"

                #Loyalty
                #if the HASE is completely new. It may treat as normal card also. 
                if rawData[0:60] != "{:060d}".format(0) and rawData[0:60] != "".ljust(60):

                    #Cash Dollar
                    hsd_dict = {}

                    #enjoy Dollar
                    enjoy_dict = {}

                    enjoy_dict["REDEEMED"] = float(rawData[0:12])
                    rawData = rawData[12:]
                    hsd_dict["REDEEMED"] = float(rawData[0:12])
                    rawData = rawData[12:]

                    transData["NETAMT"] = float(rawData[0:12])
                    rawData = rawData[12:]
                    
                    enjoy_dict["BAL"] = float(rawData[0:12])
                    rawData = rawData[12:]
                    hsd_dict["BAL"] = float(rawData[0:12])
                    rawData = rawData[12:]

                    full_loy_dict = {
                        "HSD":hsd_dict,
                        "JDD":enjoy_dict
                    }
                    transData["LOYALTY"] = full_loy_dict
            else:
                #Membership function
                transData["RESP"] = rawData[0:3]
                rawData = rawData[3:]
                transData["RESPMSG"] = rawData[0:20]
                rawData = rawData[20:]
                transData["ECRREF"] = rawData[0:16]
                rawData = rawData[16:]
                transData["DATE"] = rawData[0:8]
                rawData = rawData[8:]
                transData["TIME"] = rawData[0:6]
                rawData = rawData[6:]
                transData["CARD"] = rawData[0:10]
                rawData = rawData[10:]
                transData["PAN"] = rawData[0:19]
                rawData = rawData[19:]
                transData["EXPDATE"] = rawData[0:4]
                rawData = rawData[4:]
                transData["TERMINALID"] = rawData[0:8]
                rawData = rawData[8:]
                transData["MERCHANTID"] = rawData[0:15]
                rawData = rawData[15:]
                transData["ENTRYMODE"] = rawData[0:1]
                rawData = rawData[1:]
                transData["CIAMID"] = rawData[0:20]
                rawData = rawData[20:]
                transData["PROGRAMID"] = rawData[0:20]
                rawData = rawData[20:]
                #ignore rest

        elif transData["TYPE"] == "EPS":
            transData["RESP"] = rawData[0:3]
            rawData = rawData[3:]
            transData["RESPMSG"] = rawData[0:20]
            rawData = rawData[20:]
            transData["ECRREF"] = rawData[0:16]
            rawData = rawData[16:]
            #ignore 12-digit total amount and 12-digit other amount
            rawData = rawData[12:]
            rawData = rawData[12:]
            transData["DATE"] = rawData[0:8]
            rawData = rawData[8:]
            transData["TIME"] = rawData[0:6]
            rawData = rawData[6:]
            transData["PAN"] = rawData[0:19]
            rawData = rawData[19:]
            transData["TERMINALID"] = rawData[0:8]
            rawData = rawData[8:]
            transData["MERCHANTID"] = rawData[0:15]
            rawData = rawData[15:]
            transData["TRACE"] = rawData[0:6]
            transData["INVOICE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["BANKINVALUEDAY"] = rawData[0:4]
            rawData = rawData[4:]

            #Avoid 0x00 string
            if rawData[0:28] == '\x00'*28:
                transData["DEBITACCOUNTNO"] = ""
            else:
                transData["DEBITACCOUNTNO"] = rawData[0:28]
            rawData = rawData[28:]
            
            if rawData[0:20] == '\x00'*20:
                transData["BANKADDITIONALRESP"] = ""
            else:
                transData["BANKADDITIONALRESP"] = rawData[0:20]
            rawData = rawData[20:]

            transData["CARD"] = rawData[0:10]
            rawData = rawData[10:]
            #ignore 3-digit brand name
            rawData = rawData[3:]
            #ignore 6-digit billing currency
            rawData = rawData[6:]
            try:
                transData["AMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
                transData["CASHBACKAMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
            except:
                transData["AMT"] = 0.00
                transData["CASHBACKAMT"] = 0.00
                rawData = rawData[12:]
                rawData = rawData[12:]            
            transData["ACINDICATOR"] = rawData[0:3]
            rawData = rawData[3:]
            transData["REFNUM"] = rawData[0:6]
            rawData = rawData[6:]
            transData["SIGNBLOCK"] = "N"
            #ignore the Filler

        elif transData["TYPE"] == "UPI":
            transData["RESP"] = rawData[0:3]
            rawData = rawData[3:]
            transData["RESPMSG"] = rawData[0:20]
            rawData = rawData[20:]
            #ignore 1 byte original trans type
            rawData = rawData[1:]
            transData["ECRREF"] = rawData[0:16]
            rawData = rawData[16:]
            try:
                transData["AMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
                rawData = rawData[12:]
            except:
                transData["AMT"] = 0.00
                rawData = rawData[12:]
                rawData = rawData[12:]
            transData["DATE"] = rawData[0:8]
            rawData = rawData[8:]
            transData["TIME"] = rawData[0:6]
            rawData = rawData[6:]
            transData["CARD"] = rawData[0:10]
            rawData = rawData[10:]
            transData["PAN"] = rawData[0:19]
            rawData = rawData[19:]
            transData["EXPDATE"] = rawData[0:4]
            rawData = rawData[4:]
            transData["TERMINALID"] = rawData[0:8]
            rawData = rawData[8:]
            transData["MERCHANTID"] = rawData[0:15]
            rawData = rawData[15:]
            transData["TRACE"] = rawData[0:6]
            transData["INVOICE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["BATCHNO"] = rawData[0:6]
            rawData = rawData[6:]
            transData["APPCODE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["REFNUM"] = rawData[0:12]
            rawData = rawData[12:]
            transData["SIGNBLOCK"] = rawData[0:1]

            #"U" is default value, no meaning
            transData["ENTRYMODE"] = "U"

            #ignore the rest      
        elif transData["TYPE"] == "VAC":
            transData["RESP"] = rawData[0:3]
            rawData = rawData[3:]
            transData["RESPMSG"] = rawData[0:20]
            rawData = rawData[20:]
            #ignore 1 byte original trans type
            rawData = rawData[1:]
            transData["ECRREF"] = rawData[0:16]
            rawData = rawData[16:]
            try:
                transData["AMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
                rawData = rawData[12:]
            except:
                transData["AMT"] = 0.00
                rawData = rawData[12:]
                rawData = rawData[12:]

            transData["DATE"] = rawData[0:8]
            rawData = rawData[8:]
            transData["TIME"] = rawData[0:6]
            rawData = rawData[6:]
            transData["CARD"] = rawData[0:10]
            rawData = rawData[10:]
            transData["PAN"] = rawData[0:19]
            rawData = rawData[19:]
            transData["EXPDATE"] = rawData[0:4]
            rawData = rawData[4:]
            transData["TERMINALID"] = rawData[0:8]
            rawData = rawData[8:]
            transData["MERCHANTID"] = rawData[0:15]
            rawData = rawData[15:]
            transData["TRACE"] = rawData[0:6]
            transData["INVOICE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["BATCHNO"] = rawData[0:6]
            rawData = rawData[6:]
            transData["APPCODE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["REFNUM"] = rawData[0:12]
            rawData = rawData[12:]
            try:
                transData["VACBALANCE"] = float(rawData[0:12])/100
                rawData = rawData[12:]
            except:
                transData["VACBALANCE"] = 0.00
                rawData = rawData[12:]
            transData["VACEXPDATE"] = rawData[0:8]
            rawData = rawData[8:]
            #ignore the rest

#Pack receipt
def formatTransReceiptTerminal(transData,printOut,props):
    if transData["TYPE"] == "EDC" or transData["TYPE"] == "UPI" or transData["TYPE"] == "VAC":
        #Anfield should not has receipt
        if (transData["TYPE"] != "EDC" or transData["TYPE"] != "MEMBER"):
            printOut.append(bilingualDict[transData["CMD"]] +" "+ transData["CMD"])
            printOut.append("")
            printOut.append(mix_2_column_b(bilingualDict["DATE"],"DATE",formatDateTimeInReceipt(True,transData["DATE"]),bilingualDict["TIME"],"TIME",formatDateTimeInReceipt(False,transData["TIME"])))
            printOut.append(mix_2_column_b(bilingualDict["BATCH"],"BATCH",transData["BATCHNO"],bilingualDict["TRACE"],"TRACE",transData["TRACE"]))
            printOut.append(mix_1_column_b(bilingualDict["MID"],"MID",transData["MERCHANTID"]))
            printOut.append(mix_1_column_b(bilingualDict["TID"],"TID",transData["TERMINALID"]))
            printOut.append(mix_1_column_b(bilingualDict["PAN"],"PAN",transData["PAN"] + " " + transData["ENTRYMODE"]))
            printOut.append(mix_1_column_b(bilingualDict["EXPDATE"],"EXPDATE",transData["EXPDATE"][0:2] + "/"+ transData["EXPDATE"][2:4]))
            printOut.append(transData["CARD"][2:])
            printOut.append(mix_1_column_b(bilingualDict["APPCODE"],"APPCODE",transData["APPCODE"]))
            printOut.append(mix_1_column_b(bilingualDict["REFNUM"],"REFNUM",transData["REFNUM"]))
            printOut.append(mix_1_column("ECRREF",transData["ECRREF"]))
            printOut.append("")

            if "LOYALTY" in transData:
                printOut.append(mix_1_column_b(bilingualDict["TOTAL"],"TOTAL",props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % transData["AMT"]))
                loy = transData["LOYALTY"]
                for looping in loy:
                    dollar = loy[looping]
                    printOut.append(mix_1_column(haseLoyaltyDict[looping],props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % dollar["REDEEMED"]))
                printOut.append("-"*40)
                printOut.append(mix_1_column_b(bilingualDict["NET"],"NET",props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % transData["NETAMT"]))
                
                if transData["CMD"] == "SALE":
                    printOut.append("")
                    printOut.append("")

                    printOut.append(" "*34 + "BAL")
                    for looping in loy:
                        dollar = loy[looping]
                        printOut.append(mix_1_column(haseLoyaltyDict[looping],'%.2f' % dollar["BAL"]))
            elif "CURRCODE" in transData:
                #DCC section
                printOut.append("FX RATE: "+ str(transData["FXRATE"]))
                printOut.append(print_at_middle_b(bilingualDict["TOTAL"],"TOTAL"))
                printOut.append(print_at_both_end("HKD []",dccCurCodeDict[transData["CURRCODE"]]+" [X]"))
                printOut.append(print_at_both_end(str(transData["AMT"]),str(transData["FOREIGNAMT"])))
            else:
                #normal section
                printOut.append(mix_1_column_b(bilingualDict["TOTAL"],"TOTAL",props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % transData["AMT"]))
    elif transData["TYPE"] == "EPS":
        if transData["RESP"] == "000":
            #approve transaction
            printOut.append(bilingualDict[transData["CMD"]] +" "+ transData["CMD"])
            printOut.append("")
            printOut.append(mix_2_column_b(bilingualDict["DATE"],"DATE",formatDateTimeInReceipt(True,transData["DATE"]),bilingualDict["TIME"],"TIME",formatDateTimeInReceipt(False,transData["TIME"])))
            printOut.append(mix_1_column_b(bilingualDict["MID"],"MID",transData["MERCHANTID"]))
            printOut.append(mix_1_column_b(bilingualDict["TID"],"TID",transData["TERMINALID"]))
            printOut.append(mix_1_column_b(bilingualDict["PAN"],"PAN",transData["PAN"]))
            printOut.append(mix_1_column("ISN",transData["TRACE"]))
            printOut.append(mix_1_column("A/C",transData["DEBITACCOUNTNO"]))
            printOut.append(mix_1_column("A/C INDICATOR",transData["ACINDICATOR"]))

            printOut.append(mix_1_column("PURCHASE",props["region"]+" "+str(transData["AMT"])))
            printOut.append(mix_1_column("CASHBACK",props["region"]+" "+str(transData["CASHBACKAMT"])))
            printOut.append("-"*40)
            printOut.append(mix_1_column("TOTAL",props["region"]+" "+str(transData["AMT"]+transData["CASHBACKAMT"])))
            printOut.append("")
            #need to test pure chinese position
            printOut.append("*"*40)
            printOut.append("")
            printOut.append(print_at_middle(bilingualDict["ACCEPTED"],False))
            printOut.append(print_at_middle("ACCEPTED",True))
            printOut.append("")
            printOut.append("*"*40)

            if "BANKADDITIONALRESP" in transData and transData["BANKADDITIONALRESP"]:
                printOut.append("")
                printOut.append(print_at_middle(transData["BANKADDITIONALRESP"],True))

        elif "E" in transData["RESP"]:
            #internal reject
            print("Reject EPS")
        else:
            #online reject
            printOut.append("X"*40)
            printOut.append("X"*40)
            printOut.append(print_at_middle(bilingualDict["REJECTED"],False))
            printOut.append(print_at_middle("REJECTED",True))
            printOut.append("X"*40)
            printOut.append("X"*40)
            printOut.append(bilingualDict[transData["CMD"]] +" "+ transData["CMD"])
            printOut.append("")
            printOut.append(mix_2_column_b(bilingualDict["DATE"],"DATE",formatDateTimeInReceipt(True,transData["DATE"]),bilingualDict["TIME"],"TIME",formatDateTimeInReceipt(False,transData["TIME"])))
            printOut.append(mix_1_column_b(bilingualDict["MID"],"MID",transData["MERCHANTID"]))
            printOut.append(mix_1_column_b(bilingualDict["TID"],"TID",transData["TERMINALID"]))
            printOut.append(mix_1_column_b(bilingualDict["PAN"],"PAN",transData["PAN"]))
            printOut.append(mix_1_column("ISN",transData["TRACE"]))
            printOut.append(mix_1_column("A/C",transData["DEBITACCOUNTNO"]))
            printOut.append(mix_1_column("A/C INDICATOR",transData["ACINDICATOR"]))
            printOut.append(mix_1_column("TOTAL",props["region"]+" "+str(transData["AMT"]+transData["CASHBACKAMT"])))

            printOut.append("")
            #Print the Reason
            __packEPSResponseCodeMsg(transData["RESP"],transData,printOut)

            if "BANKADDITIONALRESP" in transData and transData["BANKADDITIONALRESP"]:
                printOut.append("")
                printOut.append(print_at_middle(transData["BANKADDITIONALRESP"],True))
            







