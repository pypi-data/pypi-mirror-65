import clr
import json
clr.AddReference("System.Collections")
clr.AddReference(r"EFTECRCOMDLL")

from .EFTECRCOMDLL import ComPortController
from .terminalUtils import *
from .generalUtils import *
from .logUtils import *

comPort = None

modelType = 0
def openPortTerminal(EdcCom,logPath,EdcType):

    global comPort
    global modelType
    modelType = EdcType

    if comPort is None:
        comPort = ComPortController(True,logPath,EdcType)
    else:
        return "PF"
    Result = comPort.portOpen(EdcCom,0)

    writeLogString("TERMINAL","OPEN COM:"+str(Result))

    return Result

def closePortTerminal():
    Result = comPort.portClose()

    writeLogString("TERMINAL","CLOSE COM:"+str(Result))

    return Result

def saleTerminal(payment_type,ecr_ref,amount,additional_amount,payment_option,transData,printOut):
    request_cmd = ""
    if modelType == PAX_S60:
        if payment_type == "EDC":
            request_cmd += "0"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(amount)
            #6-digit VOID trace and 6-digit instal
            request_cmd += "000000000000"
            if payment_option == "NORMAL_REDEEM":
                request_cmd += "03"
            else:
                request_cmd += "00"
        elif payment_type == "EPS":
            total = amount + additional_amount
            request_cmd += "5"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(total)
            request_cmd += "000000000000"
            request_cmd += "000000"
            request_cmd += "EE"
            request_cmd += "{:012d}".format(amount)
            request_cmd += "{:012d}".format(additional_amount)
        elif payment_type == "UPI":
            request_cmd += "@"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(amount)
            request_cmd += "CU"
            request_cmd += "000000"

        comPort.SerialClearBuffer()

        writeLogString("TERMINAL","REQUEST CMD:"+request_cmd)

        result = comPort.SerialWrite(request_cmd)

        writeLogString("TERMINAL","REQUEST SENT:"+str(result))

        if result:
            result = comPort.SerialRead(120)
            if result != None:
                formatTransDataTerminal(result,transData,modelType)

                writeLogString("TERMINAL","RESPONSE:"+result)

                return transData["RESP"]
            else:
                writeLogString("TERMINAL","RESPONSE: ECR TIMEOUT")
                transData["RESP"] = "E10"
                transData["RESPMSG"] = "終端機沒有回應\nTERMINAL NO RESPONSE"
                return "E10"
        else:
            writeLogString("TERMINAL","REQUEST TERMINAL FAILURE")
            transData["RESP"] = "E11"
            transData["RESPMSG"] = "不能連接終端機\nREQUEST TERMINAL FAILURE"
            return "E11"
    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "E13"
        transData["RESPMSG"] = "設定值錯誤\nPROPERTIES SETTING ERROR"
        return "E13"

def refundTerminal(payment_type,ecr_ref,amount,transData,printOut):
    request_cmd = ""
    if modelType == PAX_S60:
        #PAX only EDC refund
        request_cmd += "2"
        if len(ecr_ref) > 16:
            request_cmd += ecr_ref[:16]
        else:
            request_cmd += ecr_ref.ljust(16)
        request_cmd += "{:012d}".format(amount)
        #6-digit VOID trace and 6-digit instal, 2-digit redeem
        request_cmd += "000000000000"
        request_cmd += "00"
        
        comPort.SerialClearBuffer()

        writeLogString("TERMINAL","REQUEST CMD:"+request_cmd)

        result = comPort.SerialWrite(request_cmd)
        
        writeLogString("TERMINAL","REQUEST SENT:"+str(result))

        if result:
            result = comPort.SerialRead(120)
            if result != None:
                formatTransDataTerminal(result,transData,modelType)

                writeLogString("TERMINAL","RESPONSE:"+result)

                return transData["RESP"]
            else:
                writeLogString("TERMINAL","RESPONSE: ECR TIMEOUT")
                transData["RESP"] = "E10"
                transData["RESPMSG"] = "終端機沒有回應\nTERMINAL NO RESPONSE"
                return "E10"
        else:
            writeLogString("TERMINAL","REQUEST TERMINAL FAILURE")
            transData["RESP"] = "E11"
            transData["RESPMSG"] = "不能連接終端機\nREQUEST TERMINAL FAILURE"
            return "E11"

    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "E13"
        transData["RESPMSG"] = "設定值錯誤\nPROPERTIES SETTING ERROR"
        return "E13"

def voidSaleTerminal(payment_type,invoice,originalECRREF,transData,printOut):
    request_cmd = ""
    if modelType == PAX_S60:
        if payment_type == "EDC":
            request_cmd += "3"

            #ECRREF is the search key
            if len(originalECRREF) > 16:
                request_cmd += originalECRREF[:16]
            else:
                request_cmd += originalECRREF.ljust(16)

            #Invoice and amount are dont-care
            request_cmd += "{:012d}".format(0)
            request_cmd += "{:06d}".format(int(invoice))

            #6-digit instal and redeem
            request_cmd += "000000"
            request_cmd += "00"

        elif payment_type == "UPI":
            request_cmd += "A"

            #ECRREF is the search key
            if len(originalECRREF) > 16:
                request_cmd += originalECRREF[:16]
            else:
                request_cmd += originalECRREF.ljust(16)

            # VOID amount cannot use $0.00
            request_cmd += "{:012d}".format(1)
            request_cmd += "CU"
            request_cmd += "{:06d}".format(int(invoice))
        elif payment_type == "VAC":
            request_cmd += "Q"
            #ECRREF is the search key
            if len(originalECRREF) > 16:
                request_cmd += originalECRREF[:16]
            else:
                request_cmd += originalECRREF.ljust(16)
            #Invoice and amount are dont-care
            request_cmd += "{:012d}".format(0)
            request_cmd += "{:06d}".format(int(invoice))
        comPort.SerialClearBuffer()

        writeLogString("TERMINAL","REQUEST CMD:"+request_cmd)

        result = comPort.SerialWrite(request_cmd)

        writeLogString("TERMINAL","REQUEST SENT:"+str(result))

        if result:
            result = comPort.SerialRead(120)
            if result != None:
                formatTransDataTerminal(result,transData,modelType)

                writeLogString("TERMINAL","RESPONSE:"+result)

                return transData["RESP"]
            else:
                writeLogString("TERMINAL","RESPONSE: ECR TIMEOUT")
                transData["RESP"] = "E10"
                transData["RESPMSG"] = "終端機沒有回應\nTERMINAL NO RESPONSE"
                return "E10"
        else:
            writeLogString("TERMINAL","REQUEST TERMINAL FAILURE")
            transData["RESP"] = "E11"
            transData["RESPMSG"] = "不能連接終端機\nREQUEST TERMINAL FAILURE"
            return "E11"

    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "E13"
        transData["RESPMSG"] = "設定值錯誤\nPROPERTIES SETTING ERROR"
        return "E13"

def retrievalTerminal(payment_type,invoice,transData,printOut):
    request_cmd = ""
    invoice_2_retrieve = 0
    try:
        invoice_2_retrieve = "{:06d}".format(int(invoice))
    except:
        invoice_2_retrieve = "******"

    if modelType == PAX_S60:
        if payment_type == "EDC":
            request_cmd += "4"
            request_cmd += invoice_2_retrieve
        elif payment_type == "UPI":
            request_cmd += "D"
            request_cmd += invoice_2_retrieve
        elif payment_type == "EPS":
            request_cmd += "6"
            request_cmd += invoice_2_retrieve

        comPort.SerialClearBuffer()

        writeLogString("TERMINAL","REQUEST CMD:"+request_cmd)

        result = comPort.SerialWrite(request_cmd)

        writeLogString("TERMINAL","REQUEST SENT:"+str(result))

        if result:
            result = comPort.SerialRead(120)
            if result != None:
                formatTransDataTerminal(result,transData,modelType)

                writeLogString("TERMINAL","RESPONSE:"+result)

                return transData["RESP"]
            else:
                writeLogString("TERMINAL","RESPONSE: ECR TIMEOUT")
                transData["RESP"] = "E10"
                transData["RESPMSG"] = "終端機沒有回應\nTERMINAL NO RESPONSE"
                return "E10"
        else:
            writeLogString("TERMINAL","REQUEST TERMINAL FAILURE")
            transData["RESP"] = "E11"
            transData["RESPMSG"] = "不能連接終端機\nREQUEST TERMINAL FAILURE"
            return "E11"

    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "E13"
        transData["RESPMSG"] = "設定值錯誤\nPROPERTIES SETTING ERROR"
        return "E13"

def membershipTerminal(payment_type,ecr_ref,option,amount,ciamID,transData,printOut):
    request_cmd = ""
    invoice_2_retrieve = 0
    try:
        invoice_2_retrieve = "{:06d}".format(int(ecr_ref))
    except:
        invoice_2_retrieve = "******"

    if modelType == PAX_S60:
        if payment_type == "EDC":
            if option == "MEMRET":
                request_cmd += "J"
                request_cmd +=invoice_2_retrieve
            else:
                if option == "MEMLINK":
                    request_cmd += "I"
                elif option == "MEMENQ":
                    request_cmd += "J"
                    
                if len(ecr_ref) > 16:
                    request_cmd += ecr_ref[:16]
                else:
                    request_cmd += ecr_ref.ljust(16)

                if len(ciamID) > 20:
                    request_cmd += ciamID[:20]
                else:
                    request_cmd += ciamID.ljust(20)
        elif payment_type == "VAC":
            request_cmd += "P"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(amount)
            request_cmd += "000000"

        comPort.SerialClearBuffer()

        writeLogString("TERMINAL","REQUEST CMD:"+request_cmd)

        result = comPort.SerialWrite(request_cmd)

        writeLogString("TERMINAL","REQUEST SENT:"+str(result))


        if result:
            result = comPort.SerialRead(120)
            if result != None:
                formatTransDataTerminal(result,transData,modelType)

                writeLogString("TERMINAL","RESPONSE:"+result)

                return transData["RESP"]
            else:
                writeLogString("TERMINAL","RESPONSE: ECR TIMEOUT")
                transData["RESP"] = "E10"
                transData["RESPMSG"] = "終端機沒有回應\nTERMINAL NO RESPONSE"
                return "E10"
        else:
            writeLogString("TERMINAL","REQUEST TERMINAL FAILURE")
            transData["RESP"] = "E11"
            transData["RESPMSG"] = "不能連接終端機\nREQUEST TERMINAL FAILURE"
            return "E11"

    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "E13"
        transData["RESPMSG"] = "設定值錯誤\nPROPERTIES SETTING ERROR"
        return "E13"


    
