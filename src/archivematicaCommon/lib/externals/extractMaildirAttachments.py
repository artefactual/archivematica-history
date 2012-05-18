#!/usr/bin/python -OO
# vim:fileencoding=utf8

#Author Ian Lewis
#http://www.ianlewis.org/en/parsing-email-attachments-python

import mailbox
from email.Header import decode_header
import email
from base64 import b64decode
import sys
from email.Parser import Parser as EmailParser
from email.utils import parseaddr
# cStringIOはダメ
from StringIO import StringIO
import os

class NotSupportedMailFormat(Exception):
    pass

def parse_attachment(message_part):
    content_disposition = message_part.get("Content-Disposition", None)
    if content_disposition:
        dispositions = content_disposition.strip().split(";")
        if bool(content_disposition and dispositions[0].lower() == "attachment"):

            file_data = message_part.get_payload(decode=True)
            attachment = StringIO(file_data)
            attachment.content_type = message_part.get_content_type()
            attachment.size = len(file_data)
            attachment.name = None
            attachment.create_date = None
            attachment.mod_date = None
            attachment.read_date = None

            for param in dispositions[1:]:
                name,value = param.split("=")
                name = name.lower().strip() 
                if name == "filename":
                    attachment.name = value
                elif name == "create-date":
                    attachment.create_date = value  #TODO: datetime
                elif name == "modification-date":
                    attachment.mod_date = value #TODO: datetime
                elif name == "read-date":
                    attachment.read_date = value #TODO: datetime
            return attachment

    return None

def parse(content):
    """
    Eメールのコンテンツを受け取りparse,encodeして返す
    """
    p = EmailParser()
    msgobj = p.parse(content)
    if msgobj['Subject'] is not None:
        decodefrag = decode_header(msgobj['Subject'])
        subj_fragments = []
        for s , enc in decodefrag:
            if enc:
                s = unicode(s , enc).encode('utf8','replace')
            subj_fragments.append(s)
        subject = ''.join(subj_fragments)
    else:
        subject = None

    attachments = []
    body = None
    html = None
    for part in msgobj.walk():
        attachment = parse_attachment(part)
        if attachment:
            attachments.append(attachment)
        elif part.get_content_type() == "text/plain":
            if body is None:
                body = ""
            body += unicode(
                part.get_payload(decode=True),
                part.get_content_charset(),
                'replace'
            ).encode('utf8','replace')
        elif part.get_content_type() == "text/html":
            if html is None:
                html = ""
            html += unicode(
                part.get_payload(decode=True),
                part.get_content_charset(),
                'replace'
            ).encode('utf8','replace')
    return {
        'subject' : subject,
        'body' : body,
        'html' : html,
        'from' : parseaddr(msgobj.get('From'))[1], # 名前は除いてメールアドレスのみ抽出
        'to' : parseaddr(msgobj.get('To'))[1], # 名前は除いてメールアドレスのみ抽出
        'attachments': attachments,
        'msgobj' : msgobj,
    }
    
if __name__ == '__main__':
    #http://www.doughellmann.com/PyMOTW/mailbox/
    maildir = sys.argv[1]
    import lxml.etree as etree
    #print "Extracting attachments from: " + maildir
    root = etree.Element("ArchivematicaMaildirAttachmentExtractionRecord")
    root.set("directory", maildir) 
    for maildirsub2 in os.listdir(maildir):
        maildirsub = os.path.join(maildir, maildirsub2)
        #print "Extracting attachments from: " + maildirsub
        md = mailbox.Maildir(maildirsub)
        directory = etree.SubElement(root, "subDir")
        directory.set("dir", maildirsub2)
        for item in md.iterkeys():
            #print maildirsub2, item
            fil = md.get_file(item)
            out = parse(fil)
            #for i in out.iterkeys():
                #print i
            if len(out['attachments']):
                msg = etree.SubElement(directory, "msg")
                etree.SubElement(msg, "Subject").text = out["subject"] 
                etree.SubElement(msg, "Date").text = out['msgobj']['date']
                etree.SubElement(msg, "To").text = out["to"]
                etree.SubElement(msg, "From").text = out["from"]
                for i in range(len(out['attachments'])):
                    attachment = out['attachments'][i]
                    #attachment = StringIO(file_data) TODO LOG TO FILE
                    attch = etree.SubElement(msg, "attachment")
                    etree.SubElement(attch, "name").text = attachment.name
                    etree.SubElement(attch, "content_type").text = attachment.content_type
                    etree.SubElement(attch, "size").text = str(attachment.size)
                    etree.SubElement(attch, "create_date").text = attachment.create_date
                    etree.SubElement(attch, "mod_date").text = attachment.mod_date
                    etree.SubElement(attch, "read_date").text = attachment.read_date
    print etree.tostring(root, pretty_print=True)

                    
