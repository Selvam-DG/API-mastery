import requests

def send_soap(xml):
    headers = {"Content-Type": "text/xml"}
    resp = requests.post("http://localhost:8000", data=xml, headers=headers)
    print(resp.text)

# Example usage:
xml_request = """ 
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:stu="student.soap.api">
   <soapenv:Header/>
   <soapenv:Body>
      <stu:get_all_students/>
   </stu:Body>
</soapenv:Envelope>
"""
send_soap(xml_request)
