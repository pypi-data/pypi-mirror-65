import clr
import json
clr.AddReference("System.Collections")
clr.AddReference(r"paymentQR")

from System.Collections import ArrayList
from System import String
from .paymentQR import TransRecord
from .paymentQR import paymentQRAPI

qrAPI=paymentQRAPI()
testdata = TransRecord()
arraylist = ArrayList()
result = -1

qrTypeList = ["DUMMY","ALIPAY","WECHAT","UPIQR"]

responseCodeDictionary = {
    -2  : "無效金額\nInvalid amount",
    -3  : "無效支付碼\nInvalid barcode",
    -4  : "無效收銀機參考編號\nInvalid ECR reference number",
    -5  : "沒有記錄\nNo such record",
    -11 : "沖正待處理\nReversal Pending",
    -12 : "連線錯誤\nConnection problem",
    -13 : "交易已撤消\nTransaction already voided",
    -14 : "交易超時或通訊錯誤\nTimeout",
    -16 : "回覆信息錯誤\nError Response Message",
    -99 : "不知名錯誤\nUnknown error",
    0  : "交易成功\nTransaction Approved",
    1  :"查詢支付方\nEnquire Payment Processor",
    2  :"查詢服務商\nEnquire Service Providers",
    3  :"商戶代號錯誤\nInvalid Merchant ID",
    4  :"未做實名認証\nA/C Not Authenticated",
    5  :"拒絕\nDeclined",
    6  :"錯誤\nError",
    9  :"未開通無網絡支付\nNo Network Payment Not Authorized",
    12 :"交易無效\nInvalid Transaction",
    13 :"金額錯誤\nInvalid Amount",
    14 :"無效支付碼\nInvalid Payment Code",
    19 :"超時-重做交易\nTimeout – Retry Again",
    20 :"無效交易\nInvalid Transaction",
    21 :"不作任何處理\nNo Processing",
    22 :"懷疑操作有誤\nOperation Issues",
    23 :"不可接受的交易費\nUnacceptable Trans",
    25 :"找不到原交易\nRecord Not Found",
    26 :"買家操作未完成\nBuyer Operation Not Completed",
    28 :"不要重試\nError – Do No Retry",
    29 :"交易修改失敗\nModification Failure",
    30 :"傳輸格式錯誤\nTransmission Format",
    31 :"網絡中斷\nNetwork Interruption",
    34 :"作弊嫌疑\nFraud Suspected",
    36 :"受限制的帳戶\nRestricted Account",
    39 :"無此帳戶\nInvalid Account",
    41 :"帳戶已凍結\nAccount Frozen",
	42 :"無此帳戶\nInvalid Account",
	43 :"非法支付碼\nInvalid Payment Code",
	51 :"餘額不足\nInsufficient Fund",
	54 :"支付碼已過期\nPayment Code Expired",
	55 :"支付密碼錯\nIncorrect Payment Password",
	57 :"服務不支持\nUnsupported Service",
	58 :"交易不允許\nTransaction Not Allowed",
	59 :"有作弊嫌疑\nFraud Suspected",
	60 :"產品限額校驗未通過\nExceed of The Payment Threshold of Product",
	61 :"超限額\nExceed Limit",
	62 :"服務代碼錯誤\nServer Code Error",
	63 :"支付碼校驗錯誤\nPayment Code Verification Failed",
	64 :"原始金額不正確\nIncorrect Original Amount",
	65 :"限制使用\nRestricted",
	66 :"超當日限額\nExceed Daily Limit",
	67 :"超當月限額\nExceed Monthly Limit",
	68 :"主機應答超時\nHost Response Timeout",
	69 :"超外匯兌換限額\nOver Currency Exchange Limitation",
	75 :"支付密碼錯超限\nPayment Password retrial",
	76 :"產品代碼錯誤\nnvalid Product Code",
	77 :"結帳錯誤\nSettlement Error",
	78 :"追蹤碼錯誤\nTracking Code Error",
	79 :"無效帳戶\nInvalid Account",
	80 :"數據錯誤\nEncryption Error",
	81 :"加密錯誤\nPassword Unauthorized",
	83 :"密碼不能檢驗\nCannot Connect to Payment",
	84 :"未能連接支付方\nProcessor",
	85 :"正常帳戶\nNormal Account",
	87 :"支付密碼處理錯\nIncorrect Payment PW Processing",
	88 :"網絡故障\nNetwork Failure",
	89 :"終端代碼錯誤\nInvalid Terminal Code",
	90 :"系統備份\nSystem Backup",
	91 :"支付方網絡錯誤\nPayment Processor Network Issue",
	92 :"通訊錯誤\nCommunication Error",
	93 :"交易不能完成\nTrans Not Completed",
	94 :"序號重複\nDuplicated Number",
	95 :"日切中請等待\nDaily Cut－Off – Please",
	96 :"系統故障\nSystems Error",
	97 :"無此終端號\nInvalid Terminal ID",
	98 :"收不到支付方應答\nResponse from Payment Processor",
	99 :"密碼加密格式錯\nInvalid PW Encryption"
}

def __packRespMsg(result, transData):
    if result in responseCodeDictionary:
        transData["RESPMSG"] = responseCodeDictionary[result]
    else:
        transData["RESPMSG"] = "UNKNOWN ERROR"


def saleQR(code, ecrRef, amount, transData, stringList):
    result = qrAPI.SaleQR(code,ecrRef,amount,testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)
    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    __packRespMsg(result,transData)
    return result


def voidSaleQR(invoice,transData,stringList):
    result = qrAPI.Void(invoice,"",testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)

    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    __packRespMsg(result,transData)
    return result

def refundQR(EcrRef,Amount,originalData,transData,stringList):
    if "QRTYPE" in originalData and "APPV" in originalData and "REFNUM" in originalData:
        oriDataString = originalData["QRTYPE"]+originalData["APPV"]+originalData["REFNUM"]
    else:
        transData["RESP"] = "E12"
        transData["RESPMSG"] = "輸入參數錯誤\nINPUT PARAMETER ERROR"
        return "E12"
    result = qrAPI.Refund(EcrRef,Amount,oriDataString,testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)
    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    
    __packRespMsg(result,transData)
    return result

def retrievalQR(invoice,ecrRef,transData,stringList):
    result = qrAPI.Retrieval(invoice,ecrRef,testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)
    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    __packRespMsg(result,transData)
    return result
	

def checkTypeQR(qr_code,transData):
    result = qrAPI.GetQRType(qr_code)

    transData["CMD"] = "ENQ"
    transData["TYPE"] = "QR"
    transData["PAN"] = qr_code
    transData["RESP"] = result
    if result < 0:
        transData["RESPMSG"] = "INVALID CODE"
        transData['STATUS'] = "ERROR"
    else:
        transData["RESPMSG"] = "APPROVED"
        transData["STATUS"] = "APPROVED"
        transData["CARD"] = qrTypeList[result]

    return result
        
