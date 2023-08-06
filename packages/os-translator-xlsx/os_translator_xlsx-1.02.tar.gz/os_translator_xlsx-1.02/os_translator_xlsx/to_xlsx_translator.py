import xlsxwriter
import os_translator.Translator as translator


###########################################################################
# this module aim is to translate a string to a desired languages and save
# the output in a nice excel file
#
# Side note:
# You can use this Google Play initials bank:
# ['en-GB', 'af', 'am', 'ar', 'hy-AM', 'az-AZ', 'bn-BD', 'eu-ES', 'be', 'bg', 'my-MM', 'ca', 'zh-HK', 'zh-CN', 'zh-TW', 'hr', 'cs-CZ', 'da-DK', 'nl-NL', 'en-AU', 'en-IN', 'en-SG', 'en-ZA', 'en-CA', 'en-US', 'et', 'fil', 'fi-FI', 'fr-FR', 'fr-CA', 'gl-ES', 'ka-GE', 'de-DE', 'el-GR', 'hi-IN', 'hu-HU', 'is-IS', 'id', 'it-IT', 'ja-JP', 'kn-IN', 'km-KH', 'ko-KR', 'ky-KG', 'lo-LA', 'lv', 'lt', 'mk-MK', 'ms', 'ml-IN', 'mr-IN', 'mn-MN', 'ne-NP', 'no-NO', 'fa', 'pl-PL', 'pt-BR',
#                       'pt-PT', 'ro', 'ro', 'ru-RU', 'sr', 'si-LK', 'sk', 'sl', 'es-419', 'es-ES', 'es-US', 'sw', 'sv-SE', 'ta-IN', 'te-IN', 'th', 'tr-TR', 'uk', 'vi', 'zu']
###########################################################################


def translate_to_excel(excel_file_path,
                       service_account_json_path,
                       project_id,
                       language_initials_src,
                       text_list,
                       language_initials_list):
    """Will translate a text to a given languages and save the results in a nice excel file.

    Parameters:
    :param excel_file_path: the path to the excel file with all of the translations
    :param service_account_json_path: the path to your google translate api json key. Download from your firebase's project's settings
    :param project_id: your project id (fetch from your api console project's name: https://console.cloud.google.com/?_ga=2.55756075.1423406147.1582784765-1154152733.1582784765)
    :param language_initials_src: the source language
    :param text_list: a list containing all of the texts to translate
    :param language_initials_list: the initials of the languages you want to translate to

    NOTICE:
        If there are substrings you don't want to translate, write KEEP before them. Example: "The boy looks KEEPWord".
        Also, you can use this bank of languages:
        ['en-GB', 'af', 'am', 'ar', 'hy-AM', 'az-AZ', 'bn-BD', 'eu-ES', 'be', 'bg', 'my-MM', 'ca', 'zh-HK', 'zh-CN', 'zh-TW', 'hr', 'cs-CZ', 'da-DK', 'nl-NL', 'en-AU', 'en-IN', 'en-SG', 'en-ZA', 'en-CA', 'en-US', 'et', 'fil', 'fi-FI', 'fr-FR', 'fr-CA', 'gl-ES', 'ka-GE', 'de-DE', 'el-GR', 'hi-IN', 'hu-HU', 'is-IS', 'id', 'it-IT', 'ja-JP', 'kn-IN', 'km-KH', 'ko-KR', 'ky-KG', 'lo-LA', 'lv', 'lt', 'mk-MK', 'ms', 'ml-IN', 'mr-IN', 'mn-MN', 'ne-NP', 'no-NO', 'fa', 'pl-PL', 'pt-BR',
                       'pt-PT', 'ro', 'ro', 'ru-RU', 'sr', 'si-LK', 'sk', 'sl', 'es-419', 'es-ES', 'es-US', 'sw', 'sv-SE', 'ta-IN', 'te-IN', 'th', 'tr-TR', 'uk', 'vi', 'zu']
    """

    # open excel file
    workbook = xlsxwriter.Workbook(excel_file_path)
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 20)

    # Write some simple text.
    worksheet.write('A1', language_initials_src)

    # run on all of the sentences
    for sentenceIdx in range(len(text_list)):
        worksheet.write('A' + str((sentenceIdx + 2)), text_list[sentenceIdx])
        curr_letter = 66
        times = 1

        # run on all of the languages
        for langIdx in range(len(language_initials_list)):

            # if letter overlapped
            if curr_letter == 91:
                curr_letter = 66
                times += 1

            worksheet.write((chr(curr_letter) * times) + '1', language_initials_list[langIdx])
            translation = translator.translate_text(text_list[sentenceIdx],
                                                    service_account_json_path,
                                                    project_id,
                                                    language_initials_list[langIdx],
                                                    language_initials_src)

            if isinstance(translation, Exception):
                curr_letter += 1
                print('Error with ' + language_initials_list[langIdx] + ": " + str(translation))
                print("skipping!")
                continue
            else:
                worksheet.write(chr(curr_letter) + str(sentenceIdx + 2), translation)
                curr_letter += 1

    workbook.close()
