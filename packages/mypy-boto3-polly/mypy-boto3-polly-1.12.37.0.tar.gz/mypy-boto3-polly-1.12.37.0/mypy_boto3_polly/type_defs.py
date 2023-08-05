"""
Main interface for polly service type definitions.

Usage::

    from mypy_boto3.polly.type_defs import VoiceTypeDef

    data: VoiceTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "VoiceTypeDef",
    "DescribeVoicesOutputTypeDef",
    "LexiconAttributesTypeDef",
    "LexiconTypeDef",
    "GetLexiconOutputTypeDef",
    "SynthesisTaskTypeDef",
    "GetSpeechSynthesisTaskOutputTypeDef",
    "LexiconDescriptionTypeDef",
    "ListLexiconsOutputTypeDef",
    "ListSpeechSynthesisTasksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "StartSpeechSynthesisTaskOutputTypeDef",
    "SynthesizeSpeechOutputTypeDef",
)

VoiceTypeDef = TypedDict(
    "VoiceTypeDef",
    {
        "Gender": Literal["Female", "Male"],
        "Id": Literal[
            "Aditi",
            "Amy",
            "Astrid",
            "Bianca",
            "Brian",
            "Camila",
            "Carla",
            "Carmen",
            "Celine",
            "Chantal",
            "Conchita",
            "Cristiano",
            "Dora",
            "Emma",
            "Enrique",
            "Ewa",
            "Filiz",
            "Geraint",
            "Giorgio",
            "Gwyneth",
            "Hans",
            "Ines",
            "Ivy",
            "Jacek",
            "Jan",
            "Joanna",
            "Joey",
            "Justin",
            "Karl",
            "Kendra",
            "Kimberly",
            "Lea",
            "Liv",
            "Lotte",
            "Lucia",
            "Lupe",
            "Mads",
            "Maja",
            "Marlene",
            "Mathieu",
            "Matthew",
            "Maxim",
            "Mia",
            "Miguel",
            "Mizuki",
            "Naja",
            "Nicole",
            "Penelope",
            "Raveena",
            "Ricardo",
            "Ruben",
            "Russell",
            "Salli",
            "Seoyeon",
            "Takumi",
            "Tatyana",
            "Vicki",
            "Vitoria",
            "Zeina",
            "Zhiyu",
        ],
        "LanguageCode": Literal[
            "arb",
            "cmn-CN",
            "cy-GB",
            "da-DK",
            "de-DE",
            "en-AU",
            "en-GB",
            "en-GB-WLS",
            "en-IN",
            "en-US",
            "es-ES",
            "es-MX",
            "es-US",
            "fr-CA",
            "fr-FR",
            "is-IS",
            "it-IT",
            "ja-JP",
            "hi-IN",
            "ko-KR",
            "nb-NO",
            "nl-NL",
            "pl-PL",
            "pt-BR",
            "pt-PT",
            "ro-RO",
            "ru-RU",
            "sv-SE",
            "tr-TR",
        ],
        "LanguageName": str,
        "Name": str,
        "AdditionalLanguageCodes": List[
            Literal[
                "arb",
                "cmn-CN",
                "cy-GB",
                "da-DK",
                "de-DE",
                "en-AU",
                "en-GB",
                "en-GB-WLS",
                "en-IN",
                "en-US",
                "es-ES",
                "es-MX",
                "es-US",
                "fr-CA",
                "fr-FR",
                "is-IS",
                "it-IT",
                "ja-JP",
                "hi-IN",
                "ko-KR",
                "nb-NO",
                "nl-NL",
                "pl-PL",
                "pt-BR",
                "pt-PT",
                "ro-RO",
                "ru-RU",
                "sv-SE",
                "tr-TR",
            ]
        ],
        "SupportedEngines": List[Literal["standard", "neural"]],
    },
    total=False,
)

DescribeVoicesOutputTypeDef = TypedDict(
    "DescribeVoicesOutputTypeDef", {"Voices": List[VoiceTypeDef], "NextToken": str}, total=False
)

LexiconAttributesTypeDef = TypedDict(
    "LexiconAttributesTypeDef",
    {
        "Alphabet": str,
        "LanguageCode": Literal[
            "arb",
            "cmn-CN",
            "cy-GB",
            "da-DK",
            "de-DE",
            "en-AU",
            "en-GB",
            "en-GB-WLS",
            "en-IN",
            "en-US",
            "es-ES",
            "es-MX",
            "es-US",
            "fr-CA",
            "fr-FR",
            "is-IS",
            "it-IT",
            "ja-JP",
            "hi-IN",
            "ko-KR",
            "nb-NO",
            "nl-NL",
            "pl-PL",
            "pt-BR",
            "pt-PT",
            "ro-RO",
            "ru-RU",
            "sv-SE",
            "tr-TR",
        ],
        "LastModified": datetime,
        "LexiconArn": str,
        "LexemesCount": int,
        "Size": int,
    },
    total=False,
)

LexiconTypeDef = TypedDict("LexiconTypeDef", {"Content": str, "Name": str}, total=False)

GetLexiconOutputTypeDef = TypedDict(
    "GetLexiconOutputTypeDef",
    {"Lexicon": LexiconTypeDef, "LexiconAttributes": LexiconAttributesTypeDef},
    total=False,
)

SynthesisTaskTypeDef = TypedDict(
    "SynthesisTaskTypeDef",
    {
        "Engine": Literal["standard", "neural"],
        "TaskId": str,
        "TaskStatus": Literal["scheduled", "inProgress", "completed", "failed"],
        "TaskStatusReason": str,
        "OutputUri": str,
        "CreationTime": datetime,
        "RequestCharacters": int,
        "SnsTopicArn": str,
        "LexiconNames": List[str],
        "OutputFormat": Literal["json", "mp3", "ogg_vorbis", "pcm"],
        "SampleRate": str,
        "SpeechMarkTypes": List[Literal["sentence", "ssml", "viseme", "word"]],
        "TextType": Literal["ssml", "text"],
        "VoiceId": Literal[
            "Aditi",
            "Amy",
            "Astrid",
            "Bianca",
            "Brian",
            "Camila",
            "Carla",
            "Carmen",
            "Celine",
            "Chantal",
            "Conchita",
            "Cristiano",
            "Dora",
            "Emma",
            "Enrique",
            "Ewa",
            "Filiz",
            "Geraint",
            "Giorgio",
            "Gwyneth",
            "Hans",
            "Ines",
            "Ivy",
            "Jacek",
            "Jan",
            "Joanna",
            "Joey",
            "Justin",
            "Karl",
            "Kendra",
            "Kimberly",
            "Lea",
            "Liv",
            "Lotte",
            "Lucia",
            "Lupe",
            "Mads",
            "Maja",
            "Marlene",
            "Mathieu",
            "Matthew",
            "Maxim",
            "Mia",
            "Miguel",
            "Mizuki",
            "Naja",
            "Nicole",
            "Penelope",
            "Raveena",
            "Ricardo",
            "Ruben",
            "Russell",
            "Salli",
            "Seoyeon",
            "Takumi",
            "Tatyana",
            "Vicki",
            "Vitoria",
            "Zeina",
            "Zhiyu",
        ],
        "LanguageCode": Literal[
            "arb",
            "cmn-CN",
            "cy-GB",
            "da-DK",
            "de-DE",
            "en-AU",
            "en-GB",
            "en-GB-WLS",
            "en-IN",
            "en-US",
            "es-ES",
            "es-MX",
            "es-US",
            "fr-CA",
            "fr-FR",
            "is-IS",
            "it-IT",
            "ja-JP",
            "hi-IN",
            "ko-KR",
            "nb-NO",
            "nl-NL",
            "pl-PL",
            "pt-BR",
            "pt-PT",
            "ro-RO",
            "ru-RU",
            "sv-SE",
            "tr-TR",
        ],
    },
    total=False,
)

GetSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "GetSpeechSynthesisTaskOutputTypeDef", {"SynthesisTask": SynthesisTaskTypeDef}, total=False
)

LexiconDescriptionTypeDef = TypedDict(
    "LexiconDescriptionTypeDef", {"Name": str, "Attributes": LexiconAttributesTypeDef}, total=False
)

ListLexiconsOutputTypeDef = TypedDict(
    "ListLexiconsOutputTypeDef",
    {"Lexicons": List[LexiconDescriptionTypeDef], "NextToken": str},
    total=False,
)

ListSpeechSynthesisTasksOutputTypeDef = TypedDict(
    "ListSpeechSynthesisTasksOutputTypeDef",
    {"NextToken": str, "SynthesisTasks": List[SynthesisTaskTypeDef]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

StartSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "StartSpeechSynthesisTaskOutputTypeDef", {"SynthesisTask": SynthesisTaskTypeDef}, total=False
)

SynthesizeSpeechOutputTypeDef = TypedDict(
    "SynthesizeSpeechOutputTypeDef",
    {"AudioStream": Union[bytes, IO], "ContentType": str, "RequestCharacters": int},
    total=False,
)
