# -*- coding: utf-8 -*-

from nwae.lang.config.Config import Config
from nwae.lang.LangFeatures import LangFeatures
from nwae.lang.LangHelper import LangHelper
from nwae.lang.nlp.WordList import WordList
from nwae.lang.nlp.SpellingCorrection import SpellingCorrection
import nwae.utils.UnitTest as ut
from nwae.utils.Log import Log


#
# Test NLP stuff
#
class UnitTestSpellingCorrection:

    def __init__(
            self,
            ut_params
    ):
        self.ut_params = ut_params
        if self.ut_params is None:
            # We only do this for convenience, so that we have access to the Class methods in UI
            self.ut_params = ut.UnitTestParams()

        self.word_segmenter = {}
        self.synonymlist = {}
        self.wordlist = {}
        self.spell_corr = {}

        for lang in [LangFeatures.LANG_TH]:
            ret_obj = LangHelper.get_word_segmenter(
                lang                 = lang,
                dirpath_wordlist     = ut_params.dirpath_wordlist,
                postfix_wordlist     = ut_params.postfix_wordlist,
                dirpath_app_wordlist = ut_params.dirpath_app_wordlist,
                postfix_app_wordlist = ut_params.postfix_app_wordlist,
                dirpath_synonymlist  = ut_params.dirpath_synonymlist,
                postfix_synonymlist  = ut_params.postfix_synonymlist,
                # We can only allow root words to be words from the model features
                allowed_root_words   = None,
                do_profiling         = False
            )
            self.word_segmenter[lang] = ret_obj.wseg
            self.synonymlist[lang] = ret_obj.snnlist

            self.wordlist[lang] = WordList(
                lang             = lang,
                dirpath_wordlist = ut_params.dirpath_wordlist,
                postfix_wordlist = ut_params.postfix_wordlist
            )
            words = self.wordlist[lang].wordlist[WordList.COL_WORD].tolist()

            self.spell_corr[lang] = SpellingCorrection(
                lang              = lang,
                words_list        = words,
                dir_path_model    = ut_params.dirpath_sample_data,
                identifier_string = str(lang) + '_sample',
                do_profiling      = True
            )

        return

    def run_unit_test(
            self
    ):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)

        lang = LangFeatures.LANG_TH
        test_sent = [
            # Case words segmented correctly to ['มี', 'เงน', 'ที่', 'ไหน'] and 'เงน' corrected to 'เงิน'
            ['มีเงนที่ไหน',
             ['มี', 'เงิน', 'ที่', 'ไหน']],
            #['สำนักงนตำรวจแห่งชาติ',
            # ['สำนัก', 'งาน', 'ตำรวจ', 'แห่ง', 'ชาติ']]
            # 'มีโปรไหนใช้ได้กัลยุสนี้',
        ]

        for obj in test_sent:
            s = obj[0]
            arr_expected = obj[1]

            seg = self.word_segmenter[lang].segment_words(
                text = s,
                return_array_of_split_words = True
            )
            Log.debug(
                '"' + s + '" segmented to ' + str(seg)
            )

            arr_cor = self.spell_corr[lang].do_spelling_correction(
                text_segmented_arr=seg
            )
            Log.debug('Corrections array: ' + str(arr_cor))
            res_final.update_bool(res_bool=ut.UnitTest.assert_true(
                observed = arr_cor,
                expected = arr_expected,
                test_comment = 'Test "' + str(s) + '" to ' + str(arr_cor)
            ))

        return res_final


if __name__ == '__main__':
    config = Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class       = Config,
        default_config_file = Config.CONFIG_FILE_PATH_DEFAULT
    )
    Log.LOGLEVEL = Log.LOG_LEVEL_DEBUG_1

    lang = LangFeatures.LANG_TH

    ut_params = ut.UnitTestParams(
        dirpath_wordlist     = config.get_config(param=Config.PARAM_NLP_DIR_WORDLIST),
        postfix_wordlist     = config.get_config(param=Config.PARAM_NLP_POSTFIX_WORDLIST),
        dirpath_app_wordlist = config.get_config(param=Config.PARAM_NLP_DIR_APP_WORDLIST),
        postfix_app_wordlist = config.get_config(param=Config.PARAM_NLP_POSTFIX_APP_WORDLIST),
        dirpath_synonymlist  = config.get_config(param=Config.PARAM_NLP_DIR_SYNONYMLIST),
        postfix_synonymlist  = config.get_config(param=Config.PARAM_NLP_POSTFIX_SYNONYMLIST),
        dirpath_model        = None,
        dirpath_sample_data  = config.get_config(param=Config.PARAM_NLP_DIR_SAMPLE_DATA)
    )

    res = UnitTestSpellingCorrection(ut_params=ut_params).run_unit_test()
    exit(res.count_fail)
