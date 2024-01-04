# Modify from https://github.com/LexsionLee/tencent-translate-for-goldendict
# Use with `python .py YourInput` for translate multi-language to Chinese, supported languages list on https://cloud.tencent.com/document/api/551/15620. And translate Chinese to English.
# Write by GPT-3.5 🧙, scillidan 🤡. See
# https://sharegpt.com/c/t8Fb0HC
# https://sharegpt.com/c/e7cmAFb
# https://sharegpt.com/c/wXz7J6u

import json
import unicodedata
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import argparse
import textwrap
import langid

# Add your api-key here.
SecretId = "" 
SecretKey = ""

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            '''))
    parser.add_argument('qText', metavar='Text', type=str, default='', help='Original text for query.')
    return parser.parse_args()

def get_language_code(text):
    try:
        detected_lang = langid.classify(text)
        return detected_lang[0]
    except:
        return None

def translate_text(source_text, source_lang, target_lang):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

        req = models.TextTranslateRequest()
        params = {
            "SourceText": source_text,
            "Source": source_lang,
            "Target": target_lang,
            "ProjectId": 0
        }

        req.from_json_string(json.dumps(params))

        resp = client.TextTranslate(req)

        dictResp = json.loads(resp.to_json_string())

        return dictResp['TargetText'], target_lang

    except TencentCloudSDKException as err:
        print(err)
        return None, None

args = get_args()
source_text = args.qText

source_lang = get_language_code(source_text)

if source_lang == 'zh':
    # Input is Chinese
    translated_text, target_lang = translate_text(source_text, "zh", "en")
else:
    # Input is not Chinese
    translated_text, target_lang = translate_text(source_text, source_lang, "zh")

if translated_text is not None:
    print("")
    print(translated_text)
    print("")

print("")
print(source_text)
