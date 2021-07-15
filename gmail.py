# https://developers.google.com/gmail/api/quickstart/python

import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import base64
import email
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.message import EmailMessage
from email.utils import make_msgid

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.labels', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']


def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8")
  }


def create_draft(service, user_id, message_body):
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()

    print("Draft id: %s\nDraft message: %s" % (draft['id'], draft['message']))

    return draft
  except Exception as e:
    print('An error occurred: %s' % e)
    return None

def send_message(service, user_id, message):
  try:
    message = service.users().messages().send(userId=user_id, body=message).execute()
    return message
  except Exception as e:
    print('An error occurred: %s' % e)
    return None


def create_message_with_attachment(sender, to, subject, message_text, file):
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'

  main_type, sub_type = content_type.split('/', 1)
  print(main_type)

  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read().decode("utf-8"), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {'raw': raw_message.decode("utf-8")}


def create_html_message(sender, to, image1_path, image2_path):
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = "[힙서비콘 선물] 티켓이 배송되었습니다."
    msgRoot['From'] = sender
    msgRoot['To'] = to

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <style></style>
  <body>
    <div style="display: table-cell; vertical-align: middle">
      <div
        class="content-container"
        style="
          background-color: #f2f2f2;
          width: 100%;
          max-width: 590px;
          box-sizing: border-box;
          position: relative;
          text-align: center;
        "
      >
        <div style="width: 100%; background-color: black">
          <img
            style="width: 335px"
            src="https://github.com/Jesscha/hipName/blob/master/%E1%84%89%E1%85%A1%E1%86%BC%E1%84%83%E1%85%A1%E1%86%AB%E1%84%87%E1%85%A2%E1%84%82%E1%85%A5-05@3x.png?raw=true"
          />
        </div>
        <p
          class="hip-text"
          style="
            font-size: 14px;
            font-weight: normal;
            font-stretch: normal;
            font-style: normal;
            line-height: 1.71;
            letter-spacing: -0.34px;
            text-align: left;
            color: #000000;
            padding-left: 15px;
            padding-right: 15px;
            padding-bottom: 15px;
          "
        >
          <strong
            >Hoxy…⁉ <br />
            당신의 이름은.. '이커' 성은.. '메'..? <br />
            프로덕트 '메이커' 😆 <br /> </strong
          ><br />
          우리 오프라인 이벤트 같은 거 갈 때.. 티켓 있으면 괜히 설레고 인증샷
          찍고 싶고 그렇잖아요?! <br />
          📸 힙서비콘 티켓을 2개 준비했어요!!<br />
          아래 티켓을 다운로드해서 인스타그램에 인증 가즈아~ <br />
          <br />
          [핵중요] 3,289개의 서비스 사례에서 뽑아낸
          <strong>27가지 UX 원칙 가이드</strong>를 GET하는 방법!
          <br />
          - 인스타에 티켓을 피드나 스토리에 올리면서!<br />
          - <strong>#힙서비콘</strong> 해시태그와<br />
          - 힙서비콘 내용이 도움이 될 <strong>지인 딱 2명</strong>만 같이 태그</strong
          >해주세요! <br />
          <br />
          ※ 주의 <strong>@hip.servie</strong> 인스타 태그 안 하면 드리고 싶어도
          못 드려요!! 😭
        </p>
      </div>
      <div
        class="ticket1"
        style="
          justify-content: center;
          background-color: #f2f2f2;
          width: 100%;
          max-width: 590px;
          padding-top: 10px;
          padding-bottom: 10px;
          box-sizing: border-box;
          margin-top: 20px;
          text-align: center;
        "
      >
        <img
          style="width: 100%; max-width: 336px"
          src="cid:image1"
          alt="힙서비콘 초대장1"
        />
      </div>
      <div
        class="ticket2"
        style="
          justify-content: center;
          background-color: #f2f2f2;
          width: 100%;
          max-width: 590px;
          padding-top: 10px;
          padding-bottom: 10px;
          box-sizing: border-box;
          margin-top: 20px;
          text-align: center;
        "
      >
        <img
          style="width: 100%; max-width: 336px"
          src="cid:image2"
          alt="힙서비콘 초대장2"
        />
      </div>

      <div
        class="under-content"
        style="
          padding: 15px;

          justify-content: center;
          background-color: #f2f2f2;
          width: 100%;
          max-width: 590px;
          box-sizing: border-box;
          margin-top: 20px;
        "
      >
        <p
          style="
            font-size: 14px;
            font-weight: normal;
            font-stretch: normal;
            font-style: normal;
            line-height: 1.71;
            letter-spacing: -0.34px;
            text-align: left;
            color: #000000;
          "
        >
          전 정말 힙서비콘 시즌4를 듣고 나면 더 성장한Product Maker가 되어있을
          거라 장담해요!<br />
          다양한 세션을 준비했으니! 꼭 놓치지 않았으면 좋겠어요 ㅠㅠ 여러분이
          기대하는 것의 2배를 얻어 가실 수 있도록 최선을 다해 준비했답니다! 🥰
          <br />
          <br />
          이미 어떤 세션 있는지 보고 느낌 오셨죠…?ㅎ<br />
          아주 뽕뽑을 그 각 나옵니다!!<br />
          그리고 우리 각자 서비스에 다 적용해서 200% 좋은 유저 경험
          만들어보자규요!!<br />
          <br />

          그럼 이제, To be better Product Maker가 될 준비되셨나요?!<br />
          <strong>7월 29일 밤 9시 30분!</strong> 알람 설정! 꼭! 해놓으세요!!<br />
          <br />
          <br />

          BYE (비 와 이이~~~!)👋👋👋
        </p>
      </div>
    </div>
  </body>
</html>
""", 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    with open(image1_path, 'rb') as f:
        msgImage = MIMEImage(f.read(), _subtype="jpeg")

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    with open(image2_path, 'rb') as f:
        msgImage = MIMEImage(f.read(), _subtype="jpeg")

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage)

    raw_message = base64.urlsafe_b64encode(msgRoot.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


def get_messages(service, user_id):
  try:
    return service.users().messages().list(userId=user_id).execute()
  except Exception as error:
    print('An error occurred: %s' % error)


def get_mime_message(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()
    print('Message snippet: %s' % message['snippet'])
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except Exception as error:
    print('An error occurred: %s' % error)

def get_attachments(service, user_id, msg_id, store_dir):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    for part in message['payload']['parts']:
      if(part['filename'] and part['body'] and part['body']['attachmentId']):
        attachment = service.users().messages().attachments().get(id=part['body']['attachmentId'], userId=user_id, messageId=msg_id).execute()

        file_data = base64.urlsafe_b64decode(attachment['data'].encode('utf-8'))
        path = ''.join([store_dir, part['filename']])

        f = open(path, 'wb')
        f.write(file_data)
        f.close()
  except Exception as error:
    print('An error occurred: %s' % error)



class Gmail:
    def __init__(self):
        """Shows basic usage of the Gmail API.
            Lists the user's Gmail labels.
            """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token_gmail.json'):
            creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token_gmail.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)

    def send_email(self, sender, to, image1_path, image2_path):
        message = create_html_message(sender, to, image1_path, image2_path)
        result = send_message(self.service, sender, message)
        print(result)
        if result['labelIds'][0] != 'SENT':
            return False

        return True
