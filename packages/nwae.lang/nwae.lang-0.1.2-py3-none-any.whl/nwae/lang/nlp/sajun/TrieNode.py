# -*- coding: utf-8 -*-
# By Steve Hanov, 2011. Released to the public domain
# Code modified from http://stevehanov.ca/blog/?id=114

import nwae.utils.Log as lg
from inspect import currentframe, getframeinfo
import time
import nwae.lang.nlp.WordList as wl
from nwae.lang.LangFeatures import LangFeatures
import nwae.utils.UnitTest as ut
from nwae.lang.config.Config import Config


#
# The Trie data structure keeps a set of words, organized with one node (one TrieNode object)
# for each letter.
# Some nodes may have a word attribute, some may not.
#
class TrieNode:

    # Keep some interesting statistics
    NODE_COUNT = 0
    WORD_COUNT = 0

    @staticmethod
    def build_trie_node(
            words
    ):
        start = time.time()

        trie = TrieNode()
        # read dictionary file into a trie
        for word in words:
            TrieNode.WORD_COUNT += 1
            trie.insert(word)

        end = time.time()
        lg.Log.important(
            str(TrieNode.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Successfully build Trie Node of ' + str(TrieNode.NODE_COUNT)
            + ' nodes, and ' + str(TrieNode.WORD_COUNT) + ' total words. Took '
            + str(round((end - start), 5)) + ' secs.'
        )
        return trie

    def __init__(
            self
    ):
        # Some nodes are not words (e.g. "w", "wo", "wor" from "word"), so default to None
        self.word = None
        # Branch off here with more TrieNode class objects
        self.children = {}
        # Need to count using global variable as this is a linked set of TrieNode objects
        TrieNode.NODE_COUNT += 1
        return

    def insert(
            self,
            word
    ):
        node = self
        #
        # Create new nodes if needed, and at the end record the word
        #
        for letter in word:
            if letter not in node.children:
                # New branch
                node.children[letter] = TrieNode()
            # Where we are now
            node = node.children[letter]
        # At the final point, record the word
        node.word = word
        return

    # The search function returns a list of all words that are less than the given
    # maximum distance from the target word
    @staticmethod
    def search(
            trie,
            word,
            max_cost = 1
    ):
        # build first row. 0,1,2,3...,len(word)
        currentRow = list( range( len(word) + 1 ) )

        results = []

        # recursively search each branch of the trie
        for letter in trie.children:
            TrieNode.searchRecursive(
                node        = trie.children[letter],
                letter      = letter,
                word        = word,
                previousRow = currentRow,
                results     = results,
                max_cost    = max_cost
            )

        return results

    #
    # The most general among the <edit distance> family of algorithm is
    # the Damerau–Levenshtein distance, that allows all below
    #   1. Insertion
    #   2. Deletion
    #   3. Substitution
    #   4. TODO Transposition of 2 adjacent characters
    #
    # This recursive helper is used by the search function above. It assumes that
    # the previousRow has been filled in already.
    #
    @staticmethod
    def searchRecursive(
            node,
            letter,
            word,
            previousRow,
            results,
            max_cost
    ):
        columns = len( word ) + 1
        # West, north-west don't exist, so take only north
        currentRow = [ previousRow[0] + 1 ]

        # Build one row for the letter, with a column for each letter in the target
        # word, plus one for the empty string at column 0
        for column in range( 1, columns ):
            # west
            insertCost = currentRow[column - 1] + 1
            # north
            deleteCost = previousRow[column] + 1

            # north-west
            if word[column - 1] != letter:
                replaceCost = previousRow[ column - 1 ] + 1
            else:
                replaceCost = previousRow[ column - 1 ]

            # TODO Transposition of 2 adjacent characters
            #   We will need also the previous 2 rows
            # transpositionCost =

            currentRow.append( min( insertCost, deleteCost, replaceCost ) )

        # if the last entry in the row indicates the optimal cost is less than the
        # maximum cost, and there is a word in this trie node, then add it.
        if currentRow[-1] <= max_cost:
            if node.word is not None:
                results.append( (node.word, currentRow[-1] ) )

        # if any entries in the row are less than the maximum cost, then
        # recursively search each branch of the trie
        if min( currentRow ) <= max_cost:
            for letter in node.children:
                TrieNode.searchRecursive(
                    node        = node.children[letter],
                    letter      = letter,
                    word        = word,
                    previousRow = currentRow,
                    results     = results,
                    max_cost    = max_cost
                )
        return


class TrieNodeUnitTest:

    def __init__(
            self,
            ut_params
    ):
        self.ut_params = ut_params
        if self.ut_params is None:
            # We only do this for convenience, so that we have access to the Class methods in UI
            self.ut_params = ut.UnitTestParams()

    def run_unit_test(self):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)

        lang = LangFeatures.LANG_TH
        # read dictionary file into a trie
        wl_obj = wl.WordList(
            lang             = lang,
            dirpath_wordlist = self.ut_params.dirpath_wordlist,
            postfix_wordlist = self.ut_params.postfix_wordlist
        )
        words = wl_obj.wordlist[wl.WordList.COL_WORD].tolist()

        trie = TrieNode.build_trie_node(
            words = words
        )
        lg.Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ": Read %d words into %d nodes" % (TrieNode.WORD_COUNT, TrieNode.NODE_COUNT)
        )

        test_data = [
            ('เงน', (
                ('เกน', 1), ('เขน', 1), ('เคน', 1), ('เงก', 1), ('เงย', 1), ('เงา', 1), ('เงิน', 1), ('เง็น', 1),
                ('เง้', 1), ('เจน', 1), ('เชน', 1), ('เซน', 1), ('เดน', 1), ('เถน', 1), ('เบน', 1), ('เมน', 1),
                ('เลน', 1), ('เวน', 1), ('เสน', 1), ('เอน', 1), ('โงน', 1), ('ฉงน', 1)
            )),
        ]

        for i in range(len(test_data)):
            word_corrections_tuple = test_data[i]
            word = word_corrections_tuple[0]
            corrections = word_corrections_tuple[1]

            start = time.time()
            results = TrieNode.search(
                trie = trie,
                word = word
            )
            end = time.time()
            lg.Log.debug("Search took " + str(end - start) + 's.')

            for word_dist_tuple in results:
                res_final.update_bool(res_bool=ut.UnitTest.assert_true(
                    observed = word_dist_tuple in corrections,
                    expected = True,
                    test_comment = 'test word ' + str(i) + ' "' + str(word)
                                   + '" tuple (word, edit-distance) ' + str(word_dist_tuple)
                ))

        return res_final


if __name__ == '__main__':
    config = Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class       = Config,
        default_config_file = Config.CONFIG_FILE_PATH_DEFAULT
    )
    lg.Log.LOGLEVEL = lg.Log.LOG_LEVEL_DEBUG_1

    ut_params = ut.UnitTestParams(
        dirpath_wordlist     = config.get_config(param=Config.PARAM_NLP_DIR_WORDLIST),
        postfix_wordlist     = config.get_config(param=Config.PARAM_NLP_POSTFIX_WORDLIST),
        dirpath_app_wordlist = config.get_config(param=Config.PARAM_NLP_DIR_APP_WORDLIST),
        postfix_app_wordlist = config.get_config(param=Config.PARAM_NLP_POSTFIX_APP_WORDLIST),
        dirpath_synonymlist  = config.get_config(param=Config.PARAM_NLP_DIR_SYNONYMLIST),
        postfix_synonymlist  = config.get_config(param=Config.PARAM_NLP_POSTFIX_SYNONYMLIST),
        dirpath_model        = None,
        dirpath_sample_data  = config.get_config(param=Config.PARAM_NLP_DIR_SAMPLE_DATA),
    )

    res = TrieNodeUnitTest(ut_params=ut_params).run_unit_test()
    exit(res.count_fail)


