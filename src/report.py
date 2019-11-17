import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from util import FlowName, BuildNumber, getVar, fetchCredential

SmtpAddr = getVar('FLOWCI_EMAIL_SMTP')
IsSSL = getVar('FLOWCI_EMAIL_SSL')
FromAddr = getVar('FLOWCI_EMAIL_FROM')
ToAddr = getVar('FLOWCI_EMAIL_TO')
Credential = getVar('FLOWCI_EMAIL_CREDENTIAL', required=False)

def createServer():
    if IsSSL in ['true', 'yes']:
        return smtplib.SMTP_SSL(SmtpAddr, 465)
        
    return smtplib.SMTP(SmtpAddr)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def createHtml():
    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('flow.ci <%s>' % FromAddr)
    msg['To'] = ToAddr

    subject = "job {} - #{}".format(FlowName, BuildNumber)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg

def fetchFlowUsers():
    global ToAddr
    # TODO: fetch flow userlist from api
    pass

def send():
    server = createServer()
    server.set_debuglevel(1)

    if ToAddr == 'FLOW_USERS':
        fetchFlowUsers()

    if Credential != None:
        c = fetchCredential(Credential)
        server.login(c['pair']['username'], c['pair']['password'])

    msg = createHtml()
    server.sendmail(from_addr=FromAddr, to_addrs=ToAddr.split(','), msg=msg.as_string())
    server.quit()

send()
