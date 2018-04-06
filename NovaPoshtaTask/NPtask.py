from datetime import date

import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import requests as requests

from urllib import request

url="https://api.novaposhta.ua/v2.0/json/"
apiKey="1c66e119bf1b7b178e34d7ea1a5bc89f"
senderCounterpartyRef= "bbf4d097-cdb8-11e6-8ba8-005056881c6b"
counterpartyPropertySender="Sender"
counterpartyPropertyRecipient="Recipient"
sender={}
pathForPDF="/home/raccoon/PycharmProjects/NovaPoshtaTask"


deliveryInformation=[
{
    "PayerType": "Sender",
    "PaymentMethod": "Cash",
    "CargoType": "Cargo",
    "VolumeGeneral": "0.1",
    "Weight": "10",
    "ServiceType": "WarehouseDoors",
    "SeatsAmount": "1",
    "Description": "абажур",
    "Cost": "500",
    "RecipientCityName": "київ",
    "RecipientArea": "",
    "RecipientAreaRegions": "",
    "RecipientAddressName": "Столичне шосе",
    "RecipientHouse": "20",
    "RecipientFlat": "37",
    "RecipientName": "Брюс Уэйн",
    "RecipientType": "PrivatePerson",
    "RecipientsPhone": "380991234567"
},
{
    "PayerType": "Sender",
    "PaymentMethod": "Cash",
    "CargoType": "Cargo",
    "VolumeGeneral": "0.1",
    "Weight": "10",
    "ServiceType": "WarehouseDoors",
    "SeatsAmount": "1",
    "Description": "револьвер",
    "Cost": "300",
    "RecipientCityName": "київ",
    "RecipientArea": "",
    "RecipientAreaRegions": "",
    "RecipientAddressName": "Борщагівська",
    "RecipientHouse": "148",
    "RecipientFlat": "",
    "RecipientName": "Брюс Уиллис",
    "RecipientType": "PrivatePerson",
    "RecipientsPhone": "380991254567"
}


]
def getcounterpartyRef(apiKey,counterpartyProperty):
    data={
    "apiKey": apiKey,
     "modelName": "Counterparty",
     "calledMethod": "getCounterparties",
     "methodProperties": {
         "CounterpartyProperty": counterpartyProperty,
         "Page": "1"
     }
    }
    r = requests.get(url, json=data)
    return r.json().get("data")[0].get("Ref")
def updateSender(apiKey, counterpartyRef):
    data={
        "apiKey": apiKey,
        "modelName": "Counterparty",
        "calledMethod": "getCounterpartyAddresses",
        "methodProperties": {
            "Ref": counterpartyRef,
            "CounterpartyProperty": "Sender"
        }
    }
    r = requests.get(url, json=data)
    sender.update({"SenderAddress":r.json().get("data")[0].get("Ref")})
    sender.update({"CitySender":r.json().get("data")[0].get("CityRef")})
    sender.update({"Sender": getcounterpartyRef(apiKey, counterpartyPropertySender)})
    data={
     "apiKey": apiKey,
     "modelName": "Counterparty",
     "calledMethod": "getCounterpartyContactPersons",
     "methodProperties": {
             "Ref": counterpartyRef,
             "Page": "1"
                         }
        }
    r = requests.get(url, json=data)
    sender.update({ "ContactSender": r.json().get("data")[0].get("Ref")})
    sender.update({"SendersPhone": r.json().get("data")[0].get("Phones")})



def makeElDoc(sender,deliveriInfo):
    docNumbers = []
    for j,value  in enumerate(deliveriInfo):
        data={  "apiKey": apiKey,
                "modelName": "InternetDocument",
                "calledMethod": "save",
                "methodProperties": {
                    "NewAddress": "1",
                "DateTime": str(date.today().day)+"."+str(date.today().month)+"."+str(date.today().year)}
                }
        for i in sender:
            data.get( "methodProperties").update({i:sender.get(i)})
        for i in deliveriInfo[j]:
            data.get("methodProperties").update({i:deliveriInfo[j].get(i)})
        r = requests.get(url, json=data)
        docNumbers.append(r.json().get("data")[0].get("IntDocNumber"))

        print(r.json())
        print(docNumbers)
    return  docNumbers
def getMarking(docNumbers,apiKey):
    for i in docNumbers:
        print("https://my.novaposhta.ua/orders/printMarkings/orders[]/"+i+"/type/pdf/apiKey/"+apiKey)
        pdf = request.urlopen("https://my.novaposhta.ua/orders/printMarkings/orders[]/"+i+"/type/pdf/apiKey/"+apiKey).read()
        f = open("document_"+i+".pdf", "wb")
        f.write(pdf)
        f.close()
def mergePDFs(docNumbers):
    merger = PdfFileMerger()
    for i in docNumbers:
        merger.append(open("document_"+i+".pdf", 'rb'))
    with open('markings.pdf', 'wb') as fout:
        merger.write(fout)
    for i in docNumbers:
        os.remove("/home/raccoon/PycharmProjects/NovaPoshtaTask/document_"+i+".pdf")


updateSender(apiKey,getcounterpartyRef(apiKey,"Sender"))
docNumbers=makeElDoc(sender, deliveryInformation)
getMarking(docNumbers,apiKey)
mergePDFs(docNumbers)
