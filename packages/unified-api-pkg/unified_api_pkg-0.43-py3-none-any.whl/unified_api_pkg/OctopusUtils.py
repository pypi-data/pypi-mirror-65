from datetime import datetime
from .generalUtils import *

OCT_BASCI_TIMESTAMP = 946684800

bilingualDict = {
	"SALE":"八達通付款",
    "TOPUP":"八達通增值服務",
    "REFUND":"退款",
    "MID":"商戶號",
    "TID":"機號",
    "OUTLET":"店號",
    "DATE":"日期",
    "TIME":"時間",
    "PAN":"八達通號碼",
    "TOTAL":"扣除金額",
    "NET":"扣除淨額",
    "ACCEPTED":"接受",
    "REJECTED":"不接受",
    "TOPUPVALUE":"增值金額",
    "REMINBAL":"餘額",
    "ENQ":" 查詢",
    "CASH":"現金增值",
    "AAVS":"自動增值",
    "ONLINE":"網上增值",
    "OTHER":"其他",
    "REDEEMED":"兌換日日賞$",
    "EARN":"賺取日日賞$",
    "R_BAL":"日日賞$餘額",
    "R_TITLE":"八達通日日賞",
    "SUB_AMT":"公共交通費用補貼金額",
    "SUBSIDY":"公共交通費用補貼",
    "ECRREF":"收據號碼",

    "NO_SUB1":"沒有未領取的公共交通費用補貼，",
    "NO_SUB2":"詳情可到ptfss.gov.hk 查詢。",

    "MAX_SUB1":"你的八達通儲值額已達上限，",
    "MAX_SUB2":"尚有未領取的公共交通費用補貼",
    "MAX_SUB3":"請稍後再試。如需協助請致電",
    "MAX_SUB4":"公共交通費用補貼計劃熱線",
    "MAX_SUB5":"2969-5500。",

    "REMAIN_SUB1":"尚有未領取的公共交通費用補貼 ",
    "REMAIN_SUB2":"請稍後再試。如需協助請致電",
    "REMAIN_SUB3":"公共交通費用補貼計劃熱線2969-5500。",

    "REG_R":"請即上網登記八達通日日賞"
}


octDict = {
    "TOPUP":"Octopus Add Value Service",
    "SALE":"Octopus payment",
    "ENQ":"Eligible Reward$",
    "TOTAL":"Amount deducted",
    "SUB_AMT":"Public Transport Fare Subsidy Amount",
    "SUBSIDY":"Public Transport Fare Subsidy",

    "NO_SUB1":"No uncollected public transport fare",
    "NO_SUB2":"subsidy. Please visit ptfss.gov.hk for",
    "NO_SUB3":"more details",

    "MAX_SUB1":"Your Octopus has reached the maximum",
    "MAX_SUB2":"stored value. There is uncollected public",
    "MAX_SUB3":"transport fare subsidy of",
    "MAX_SUB4":", please try again later. Should you",
    "MAX_SUB5":"require assistance, please call Public",
    "MAX_SUB6":"Transport Fare Subsidy Scheme hotline",
    "MAX_SUB7":"2969-5500.",

    "REMAIN_SUB1":"There is uncollected public transport fare",
    "REMAIN_SUB2":"subsidy of ",
    "REMAIN_SUB3":"please try again later. Should you require",
    "REMAIN_SUB4":"assistance, please call Public Transport",
    "REMAIN_SUB5":"Fare Subsidy Scheme hotline 2969-5500",

    "REG_R":"Register now for Octopus Rewards at"
}

responseCodeDict = {
    100001:"未能接駁八達通收費器\nMOP connection failure",
    100005:"未能接駁八達通收費器\nMOP connection failure",
    100016:"讀卡錯誤，請重試\nRead card error, retry please",
    100017:"讀卡錯誤，請重試\nRead card error, retry please",
    100019:"此卡失效\nInvalid card",
    100020:"請再拍卡\nPresent card again",
    100021:"此八達通卡或產品已失效，請聯絡港鐵客務中心\nInvalid Octopus, please contact MTR Customer Service Centre",
    100022:"+++ 請勿取消交易 +++\n交易未能完成\n請通知顧客用同一張卡再次拍卡，以確保交易無誤\n+++ DO NOT CANCEL THE TXN +++\nTransaction Incomplete\nPlease request customer to present the same card again to complete the transaction",
    100024:"此卡失效\nInvalid card",
    100025:"交易未完成，請重試\nIncomplete transaction, retry please",
    100032:"請再拍卡\nPresent card again",
    100034:"讀卡錯誤，請重試\nRead card error, retry please",
    100048:"餘額不足\nInsufficient value",
    100049:"儲值額超出上限\nStored value exceed limit",
    100051:"控制台識別號碼不正確\nInvalid POS controller ID",
    101002:"超出日日賞$ 批額上限\nR$ issued exceed quota",
    101003:"日日賞$ 餘額不足\nnsufficient R$ value",
    101004:"日日賞$ 參數設定錯誤\nInvalid R$ parameter",
    101005:"錯卡，請重試(八達通號碼88888888)\nIncorrect card, retry please (Octopus no. 88888888)",
    101006:"計算錯誤\nCalculation Error",
    101007:"參數設定錯誤\nInvalid Parameter",
    101008:"計算錯誤\nCalculation Error",
    101009:"系統失效\nRMS System Error",
    101010:"日日賞$ 功能未啟動\nR$ not activated",
    101011:"日日賞$ 功能未啟動\nR$ not activated",
    101012:"日日賞$ 功能失效\nR$ Invalid",
    101013:"超出日日賞$ 累積上限\nR$ earned exceed limit",
    101014:"兌換日日賞$ 設定失效\nR$ system block to redeem",
    101015:"系统檔案無效\nInvalid RMS File",
    101016:"日日賞$ 有效期屆滿\nR$ expired",
    101018:"此卡之日日賞功能經已啟動\nRewards function on Octopus already activated",
    101101:"參數設定錯誤\nInvalid parameter",
    101102:"參數設定錯誤\nInvalid parameter",
    101103:"交易額超出上限\nBPA value exceed limits",
    101104:"超出日日賞$ 批額上限\nIssued R$ exceed limits",
    101201:"電子印花寫入錯誤",
    101202:"電子印花讀取錯誤",
    101203:"電子印花號碼失效",
    101204:"電子印花超出上限",
    101205:"超出電子印花批額上限",
    101206:"電子印花校驗錯誤",
    101207:"電子印花功能尚未啓動",
    101208:"電子印花參數設定錯誤",
    101209:"電子印花系统未能使用",
    1000222:"請重試(八達通號碼88888888)\nRetry please (Octopus no. 88888888)",
    100068:"商戶專有設定檔不存在\nNo Required List",
    100072:"未能支援有關功能\nFeature Not Supported",
}

list_last_topup_eng = [
    "","CASH","ONLINE","REFUND","AAVS","OTHERS"
]

list_last_topup_chinese = [
    "","現金增值","線上增值","退款","自動增值","其他"
]

def ecrRefToBCDByte(input, ecrRef, isSale):

    #Standard checking

    length = len(ecrRef)
    #Spec required at least 4 digit ecr ref. add "0" if not enough
    if length < 4:
        ecrRef = ecrRef + "0000"
    
    last_4 = ecrRef[(length-4):]


    if isSale:
        #Do Sale format
        #c_int buffer
        input[22] = int(last_4[2:3],16)<<12|int(last_4[3:4],16)<<8|int(last_4[0:1],16)<<4|int(last_4[1:2],16)
        input[23] = int(last_4[2:3],16)<<16|int(last_4[3:4],16)<<20|int(last_4[0:1],16)<<12|int(last_4[1:2],16)<<8

        
    else:
        #TopUp format

        #c_char buffer
        #1st byte of AI must be 0
        input[0] = 0

        input[1] = int(last_4[0:1],16)<<4|int(last_4[1:2],16)
        input[2] = int(last_4[2:3],16)<<4|int(last_4[3:4],16)
        

def packResponseCode(resp,transData):
    if resp in responseCodeDict:
        transData["RESP"]=resp
        transData["RESPMSG"] = responseCodeDict[resp]
    elif resp > 100000:
        transData["RESP"]=resp
        transData["RESPMSG"] = "發生錯誤(編號999999)\nError 999999"
    else:
        transData["RESP"]=resp
        transData["RESPMSG"] = "交易成功\nTransaction Approved"

def __add_minus(cmd):
    if cmd == "TOPUP":
        return ""
    else:
        return "-"

def formatTransDataOctopus(UD_list,transData):
    idx = 0
    
    if len(UD_list) <= 0:
        return

    idx = 1
    for x in range(0,int(UD_list[0])):

        #Normal UD
        if int(UD_list[idx]) == 0:
            idx = idx + 1
            transData["CARD"] = "OCTOPUS"
            if "UDSN" not in transData:
                transData["UDSN"] = str(UD_list[idx])
            else:
                transData["UDSN"] = transData["UDSN"] + "|" + str(UD_list[idx])
            txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(UD_list[idx+1]))
            transData["DATE"] = txn_datetime.strftime("%Y%m%d")
            transData["TIME"] = txn_datetime.strftime("%H%M%S")
            transData["TXNSEQ"] = str(UD_list[idx+5])
            
            if "AMT" not in transData:
                transData["AMT"] = float(UD_list[idx+6])/10
            else:
                if transData["AMT"] < float(UD_list[idx+6])/10:
                    transData["AMT"] = float(UD_list[idx+6])/10


            transData["REMINBAL"] = float(UD_list[idx+7])/10
            transData["RESP"] = str(UD_list[idx+7])
            #Go though normal UD.
            idx = idx + 7

            #Next UD type
            idx = idx + 1
        
        #RMS UD
        elif int(UD_list[idx]) == 1:
            idx = idx + 1
            #the UD contain RMS information
            transData["CARD"] = "OCTOPUS"

            if "RDSN" not in transData:
                transData["RDSN"] = str(UD_list[idx])
            else:
                transData["RDSN"] = transData["RDSN"] + "|" + str(UD_list[idx])
            
            txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(UD_list[idx+1]))
            transData["DATE"] = txn_datetime.strftime("%Y%m%d")
            transData["TIME"] = txn_datetime.strftime("%H%M%S")

            if "RMSTXNSEQ" not in transData:
                transData["RMSTXNSEQ"] = str(UD_list[idx+6])
            else:
                transData["RMSTXNSEQ"] = transData["RMSTXNSEQ"] + "|" + str(UD_list[idx+6])

            if "AMT" not in transData:
                transData["AMT"] = float(UD_list[idx+8])/10
            else:
                if transData["AMT"] < float(UD_list[idx+8])/10:
                    transData["AMT"] = float(UD_list[idx+8])/10
            #Go though RMS UD
            idx = idx + 10

            #Next UD type
            idx = idx + 1

        #Subsidy UD
        elif int(UD_list[idx]) == 2:
            idx = idx + 1
            transData["CARD"] = "OCTOPUS"
            if "UDSN" not in transData:
                transData["UDSN"] = str(UD_list[idx])
            else:
                transData["UDSN"] = transData["UDSN"] + "|" + str(UD_list[idx])
            txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(UD_list[idx+1]))
            transData["DATE"] = txn_datetime.strftime("%Y%m%d")
            transData["TIME"] = txn_datetime.strftime("%H%M%S")

            transData["TXNSEQ"] = str(UD_list[idx+5])

            #Next UD type
            idx = idx + 1

def formatTransReceiptOctopus(transData,printOut,props,receiptType):

    if receiptType == "REDEEM_COMP" or receiptType == "ISSUE":
        #Partial Receipt
        printOut.append("")
        if props["language"] == "C":
            printOut.append(print_at_middle(bilingualDict["R_TITLE"],False))
        else:
            printOut.append(print_at_middle("Octopus Rewards",True))

        printOut.append(mix_1_column_b(bilingualDict["TID"],"Device no.",props["OCTTID"]))
        printOut.append(mix_1_column_b(bilingualDict["OUTLET"],"Shop no.",props["OctOutletID"]))

       #printOut.append(mix_2_column_b(bilingualDict["TID"],"Device no.",props["OCTTID"],bilingualDict["OUTLET"],"Shop no.",props["OUTLET"]))

        printOut.append(mix_1_column_b(bilingualDict["PAN"],"Octopus no.",transData["PAN"]))
        printOut.append(mix_1_column_b(bilingualDict["ECRREF"],"Receipt no.",transData["ECRREF"]))

        if "R_REDEEMED" in transData:
            if props["language"] == "C":
                printOut.append(mix_1_column_c(bilingualDict["REDEEMED"],"R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"])))
            else:
                printOut.append(mix_1_column("Redeem Reward$","R$"+__add_minus(transData["CMD"])+'%.1f' % transData["R_REDEEMED"]))
        
        if "R_EARN" in transData:
            if props["language"] == "C":
                printOut.append(mix_1_column_c(bilingualDict["EARN"],"R$"+'%.1f' % transData["R_EARN"]))
            else:
                printOut.append(mix_1_column("Earn Reward$","R$"+'%.1f' % transData["R_EARN"]))

        if "R_BALANCE" in transData:
            if props["language"] == "C":
                printOut.append(mix_1_column_c(bilingualDict["R_BAL"],"R$"+'%.1f' % transData["R_BALANCE"]))
            else:
                printOut.append(mix_1_column("Reward$ Balance","R$"+'%.1f' % transData["R_BALANCE"]))
        
    else:
        #Normal receipt

        if receiptType == "" or receiptType == None:
            #Treat as normal sale, remove RMS info
            if "R_REDEEMED" in transData:
                transData.pop("R_REDEEMED")
            if "R_EARN" in transData:
                transData.pop("R_EARN")
            if "R_BALANCE" in transData:
                transData.pop("R_BALANCE")
            if "NETAMT" in transData:
                transData.pop("NETAMT")
            
        printOut.append(bilingualDict[transData["CMD"]])
        printOut.append(octDict[transData["CMD"]])
        printOut.append("")
        printOut.append(mix_2_column_b(bilingualDict["DATE"],"DATE",formatDateTimeInReceipt(True,transData["DATE"]),bilingualDict["TIME"],"TIME",formatDateTimeInReceipt(False,transData["TIME"])))
        #printOut.append(mix_1_column_b(bilingualDict["MID"],"MID",props["OCTMID"]))
        printOut.append(mix_1_column_b(bilingualDict["TID"],"Device no.",props["OCTTID"]))
        printOut.append(mix_1_column_b(bilingualDict["OUTLET"],"Shop no.",props["OctOutletID"]))
        #printOut.append(mix_2_column_b(bilingualDict["TID"],"Device no.",props["OCTTID"],bilingualDict["OUTLET"],"Shop no.",props["OUTLET"]))
        printOut.append(mix_1_column_b(bilingualDict["PAN"],"Octopus no.",transData["PAN"]))
        printOut.append(mix_1_column_b(bilingualDict["ECRREF"],"Receipt no.",transData["ECRREF"]))
        #printOut.append(transData["CARD"])
        printOut.append("")

        if transData["CMD"] == "TOPUP" and transData["AMT"] != 0:
            #normal add value
            printOut.append(mix_1_column_b(bilingualDict["TOPUPVALUE"],"Add value amount",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["AMT"]))
            if transData["OCTTYPE"] != str(1):
                printOut.append(mix_1_column_b(bilingualDict["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))
        elif transData["CMD"] == "SUBSIDY" and transData["AMT"] == 0:
            #transport subsidy
            #pass in CMD is SUBSIDY, change back to TOPUP after print receipt
            transData["CMD"] = "TOPUP"
            if props["language"] == "C":
                printOut.append(mix_1_column_c2(bilingualDict["SUB_AMT"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["Sub_TotalCollect"]))
            else:
                printOut.append(mix_1_column(octDict["SUB_AMT"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["Sub_TotalCollect"]))

            if transData["OCTTYPE"] != str(1):
                printOut.append(mix_1_column_b(bilingualDict["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))

            if props["language"] == "C":
                #No subsidy collected
                if transData["Sub_TotalCollect"] == 0:
                    printOut.append("")
                    printOut.append(bilingualDict["NO_SUB1"])
                    printOut.append(bilingualDict["NO_SUB2"])
                else:
                    if transData["Sub_reason"] == 1:
                        printOut.append("")
                        printOut.append(bilingualDict["MAX_SUB1"])
                        printOut.append(bilingualDict["MAX_SUB2"]+"$"+str(transData["Sub_Outstand"]))
                        printOut.append(bilingualDict["MAX_SUB3"])
                        printOut.append(bilingualDict["MAX_SUB4"])
                        printOut.append(bilingualDict["MAX_SUB5"])
                    elif transData["Sub_reason"] > 1:
                        printOut.append("")
                        printOut.append(bilingualDict["REMAIN_SUB1"]+"$"+str(transData["Sub_Outstand"]))
                        printOut.append(bilingualDict["REMAIN_SUB2"])
                        printOut.append(bilingualDict["REMAIN_SUB3"])


            else:
                if transData["Sub_TotalCollect"] == 0:
                    printOut.append("")
                    printOut.append(octDict["NO_SUB1"])
                    printOut.append(octDict["NO_SUB2"])
                    printOut.append(octDict["NO_SUB3"])
                else:
                    if transData["Sub_reason"] == 1:
                        printOut.append("")
                        printOut.append(octDict["MAX_SUB1"])
                        printOut.append(octDict["MAX_SUB2"])
                        printOut.append(octDict["MAX_SUB3"]+"$"+str(transData["Sub_Outstand"]))
                        printOut.append(octDict["MAX_SUB4"])
                        printOut.append(octDict["MAX_SUB5"])
                        printOut.append(octDict["MAX_SUB6"])
                        printOut.append(octDict["MAX_SUB7"])  
                    elif transData["Sub_reason"] > 1:
                        printOut.append("")
                        printOut.append(octDict["REMAIN_SUB1"])
                        printOut.append(octDict["REMAIN_SUB2"]+"$"+str(transData["Sub_Outstand"]))
                        printOut.append(octDict["REMAIN_SUB3"])
                        printOut.append(octDict["REMAIN_SUB4"])
                        printOut.append(octDict["REMAIN_SUB5"])
            
            #after all printing, remove the subsidy information
            print("Sub_Total:"+str(transData["Sub_Total"]))
            print("Sub_TotalCollect:"+str(transData["Sub_TotalCollect"]))
            print("Sub_Outstand:"+str(transData["Sub_Outstand"]))
            print("Sub_reason:"+str(transData["Sub_reason"]))
            transData.pop("Sub_Total")
            transData.pop("Sub_TotalCollect")
            transData.pop("Sub_Outstand")
            transData.pop("Sub_reason")
                        
        elif transData["CMD"] == "SALE":
            printOut.append(mix_1_column_b(bilingualDict["TOTAL"],octDict["TOTAL"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["AMT"]))
            if "R_REDEEMED" in transData:
                if props["language"] == "C":
                    printOut.append(mix_1_column_c(bilingualDict["REDEEMED"],"R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"])))
                else:
                    printOut.append(mix_1_column("Redeem Reward$","R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"])))
                printOut.append("-"*40)

                #Not required
                transData.pop("R_REDEEMED")

            if "NETAMT" in transData:
                printOut.append(mix_1_column_b(bilingualDict["NET"],"NET",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["NETAMT"]))
            

            if transData["OCTTYPE"] != str(1):
                printOut.append(mix_1_column_b(bilingualDict["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))
            
            printOut.append("")

            if "LAST_ADD" in transData:
                list_last_topup = transData["LAST_ADD"].split(",")
                transData.pop("LAST_ADD")
                if int(list_last_topup[1]) < 4:
                    if props["language"] == "C":
                        printOut.append("上一次於 "+ list_last_topup[0] +" "+ list_last_topup_chinese[int(list_last_topup[1])])
                    else:
                        printOut.append("LAST ADD VALUE BY " + list_last_topup_eng[int(list_last_topup[1])]+ " ON "+list_last_topup[0])
                    printOut.append("")

            if "R_EARN" in transData:
                if props["language"] == "C":
                    printOut.append(print_at_middle(bilingualDict["R_TITLE"],False))
                    printOut.append(mix_1_column_c(bilingualDict["EARN"],"R$"+'%.1f' % transData["R_EARN"]))
                else:
                    printOut.append(mix_1_column("Earn Reward$","R$"+'%.1f' % transData["R_EARN"]))

            if "R_BALANCE" in transData:
                if props["language"] == "C":
                    printOut.append(mix_1_column_c(bilingualDict["R_BAL"],"R$"+'%.1f' % transData["R_BALANCE"]))
                else:
                    printOut.append(mix_1_column("Reward$ Balance","R$"+'%.1f' % transData["R_BALANCE"]))
            
            if "NON_REWARDS" in transData:
                transData.pop("NON_REWARDS")
                if props["language"] == "C":
                    printOut.append(print_at_middle(bilingualDict["REG_R"],False))
                    printOut.append(print_at_middle("www.octopusrewards.com.hk",True))
                else:
                    printOut.append(print_at_middle(bilingualDict["REG_R"],True))
                    printOut.append(print_at_middle("www.octopusrewards.com.hk",True))
