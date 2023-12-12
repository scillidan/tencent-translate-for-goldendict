# Modify from https://github.com/LexsionLee/tencent-translate-for-goldendict. See https://sharegpt.com/c/t8Fb0HC and https://sharegpt.com/c/e7cmAFb.

import json
import unicodedata
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

import argparse
import textwrap

SecretId = "" # Add your api-key here.
SecretKey = ""

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            '''))
    parser.add_argument('qText',metavar='Text', type=str, default='', help='Original text for query.')
    return parser.parse_args()

def contains_chinese(text):
    for char in text:
        if 'CJK' in unicodedata.name(char):
            return True
    return False

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

        return dictResp['TargetText']

    except TencentCloudSDKException as err:
        print(err)
        return None

args = get_args()
source_text = args.qText

if contains_chinese(source_text):
    # Input is Chinese
    translated_text_zh_to_en = translate_text(source_text, "zh", "en")
    if translated_text_zh_to_en is not None:
        print("")
        print(translated_text_zh_to_en)
        print()
else:
    # Input is English
    translated_text_en_to_zh = translate_text(source_text, "en", "zh")
    if translated_text_en_to_zh is not None:
        print("")
        print(translated_text_en_to_zh)
        print()

print("")
print(source_text)