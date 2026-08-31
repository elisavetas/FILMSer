# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for the config module."""

import pytest
import re

from src.filmser.config import (
    NGRAM_NAMES, ENCHANT2PROVIDER2TAG,
    SIZE2SPACY, SPACY_LANG, LANG2SPACYLANG,
    NON_WORD_BOUND, NON_WORD_BOUND_IN_ICU, ICU_LANG2POSTFIX,
    ISO2FULL, FULL2ISO, ISO2WIKT
)


class TestNgramNames:
	"""Tests for NGRAM_NAMES mapping."""

	def test_ngram_names_structure(self):
		"""NGRAM_NAMES should be a dict mapping integers to strings."""
		assert isinstance(NGRAM_NAMES, dict), "NGRAM_NAMES should be a dict"
		for key in NGRAM_NAMES.keys():
			assert isinstance(key, int), f"NGRAM_NAMES key {key!r} should be int"
		for value in NGRAM_NAMES.values():
			assert isinstance(value, str), f"NGRAM_NAMES value {value!r} should be str"

	def test_ngram_names_not_empty(self):
		"""NGRAM_NAMES should not be empty."""
		assert len(NGRAM_NAMES) > 0, "NGRAM_NAMES should not be empty"


class TestEnchant2Provider2Tag:
	"""Tests for ENCHANT2PROVIDER2TAG mapping."""

	def test_enchant2provider2tag_structure(self):
		"""ENCHANT2PROVIDER2TAG should be a dict mapping strings to (str, list) tuples."""
		assert isinstance(ENCHANT2PROVIDER2TAG, dict), "ENCHANT2PROVIDER2TAG should be a dict"

	def test_enchant2provider2tag_contains_strings(self):
		"""All keys in ENCHANT2PROVIDER2TAG should be strings and values should be (str, list)."""
		for lang, (provider, tags) in ENCHANT2PROVIDER2TAG.items():
			assert isinstance(lang, str), f"ENCHANT2PROVIDER2TAG key {lang!r} should be str"
			assert isinstance(provider, str), f"ENCHANT2PROVIDER2TAG provider {provider!r} should be str"
			assert isinstance(tags, list), f"ENCHANT2PROVIDER2TAG tags {tags!r} should be a list"
			for tag in tags:
				assert isinstance(tag, str), f"ENCHANT2PROVIDER2TAG tag {tag!r} should be str"

	def test_enchant2provider2tag_not_empty(self):
		"""ENCHANT2PROVIDER2TAG should not be empty."""
		assert len(ENCHANT2PROVIDER2TAG) > 0, "ENCHANT2PROVIDER2TAG should not be empty"


class TestSize2Spacy:
	"""Tests for SIZE2SPACY mapping."""

	def test_size2spacy_structure(self):
		"""SIZE2SPACY should be a dict mapping strings to strings."""
		assert isinstance(SIZE2SPACY, dict), "SIZE2SPACY should be a dict"
		for key in SIZE2SPACY.keys():
			assert isinstance(key, str), f"SIZE2SPACY key {key!r} should be str"
		for value in SIZE2SPACY.values():
			assert isinstance(value, str), f"SIZE2SPACY value {value!r} should be str"

	def test_size2spacy_valid_values(self):
		"""All SIZE2SPACY values should be valid spacy size codes."""
		valid_sizes = {'sm', 'md', 'lg', 'trf'}
		for value in SIZE2SPACY.values():
			assert value in valid_sizes, f"SIZE2SPACY value {value!r} should be in {valid_sizes}"


class TestSpacyLang:
	"""Tests for SPACY_LANG set."""

	def test_spacy_lang_is_set(self):
		"""SPACY_LANG should be a set."""
		assert isinstance(SPACY_LANG, set), "SPACY_LANG should be a set"

	def test_spacy_lang_contains_strings(self):
		"""All entries in SPACY_LANG should be strings."""
		for lang in SPACY_LANG:
			assert isinstance(lang, str), f"SPACY_LANG entry {lang!r} should be str"

	def test_spacy_lang_not_empty(self):
		"""SPACY_LANG should not be empty."""
		assert len(SPACY_LANG) > 0, "SPACY_LANG should not be empty"


class TestLang2SpacyLang:
	"""Tests for LANG2SPACYLANG mapping."""

	def test_lang2spacylang_structure(self):
		"""LANG2SPACYLANG should be a dict mapping strings to strings."""
		assert isinstance(LANG2SPACYLANG, dict), "LANG2SPACYLANG should be a dict"
		for key in LANG2SPACYLANG.keys():
			assert isinstance(key, str), f"LANG2SPACYLANG key {key!r} should be str"
		for value in LANG2SPACYLANG.values():
			assert isinstance(value, str), f"LANG2SPACYLANG value {value!r} should be str"

	def test_lang2spacylang_targets_in_spacy_lang(self):
		"""All target values in LANG2SPACYLANG should be in SPACY_LANG."""
		for target_lang in LANG2SPACYLANG.values():
			assert target_lang in SPACY_LANG, f"{target_lang} should be in SPACY_LANG"


class TestNonWordBound:
	"""Tests for NON_WORD_BOUND set."""

	def test_non_word_bound_is_set(self):
		"""NON_WORD_BOUND should be a set."""
		assert isinstance(NON_WORD_BOUND, set), "NON_WORD_BOUND should be a set"

	def test_non_word_bound_contains_strings(self):
		"""All entries in NON_WORD_BOUND should be strings."""
		for lang in NON_WORD_BOUND:
			assert isinstance(lang, str), f"NON_WORD_BOUND entry {lang!r} should be str"

	def test_non_word_bound_not_empty(self):
		"""NON_WORD_BOUND should not be empty."""
		assert len(NON_WORD_BOUND) > 0, "NON_WORD_BOUND should not be empty"


class TestNonWordBoundInICU:
	"""Tests for NON_WORD_BOUND_IN_ICU set."""

	def test_non_word_bound_in_icu_is_set(self):
		"""NON_WORD_BOUND_IN_ICU should be a set."""
		assert isinstance(NON_WORD_BOUND_IN_ICU, set), "NON_WORD_BOUND_IN_ICU should be a set"

	def test_non_word_bound_in_icu_contains_strings(self):
		"""All entries in NON_WORD_BOUND_IN_ICU should be strings."""
		for lang in NON_WORD_BOUND_IN_ICU:
			assert isinstance(lang, str), f"NON_WORD_BOUND_IN_ICU entry {lang!r} should be str"

	def test_non_word_bound_in_icu_not_empty(self):
		"""NON_WORD_BOUND_IN_ICU should not be empty."""
		assert len(NON_WORD_BOUND_IN_ICU) > 0, "NON_WORD_BOUND_IN_ICU should not be empty"

	def test_non_word_bound_in_icu_subset(self):
		"""NON_WORD_BOUND_IN_ICU should be a intersection of NON_WORD_BOUND and ICU_LANG2POSTFIX keys."""
		assert NON_WORD_BOUND_IN_ICU <= NON_WORD_BOUND, "NON_WORD_BOUND_IN_ICU should be subset of NON_WORD_BOUND"
		assert NON_WORD_BOUND_IN_ICU <= set(ICU_LANG2POSTFIX.keys()), "NON_WORD_BOUND_IN_ICU should be subset of ICU_LANG2POSTFIX keys"
		assert NON_WORD_BOUND_IN_ICU == NON_WORD_BOUND & set(ICU_LANG2POSTFIX.keys()), "NON_WORD_BOUND_IN_ICU should equal intersection of NON_WORD_BOUND and ICU_LANG2POSTFIX keys"


class TestICULang2Postfix:
	"""Tests for ICU_LANG2POSTFIX mapping."""

	def test_icu_lang2postfix_structure(self):
		"""ICU_LANG2POSTFIX should be a dict mapping strings to lists."""
		assert isinstance(ICU_LANG2POSTFIX, dict), "ICU_LANG2POSTFIX should be a dict"
		for key in ICU_LANG2POSTFIX.keys():
			assert isinstance(key, str), f"ICU_LANG2POSTFIX key {key!r} should be str"
		for value in ICU_LANG2POSTFIX.values():
			assert isinstance(value, list), f"ICU_LANG2POSTFIX value for {value!r} should be list"

	def test_icu_lang2postfix_not_empty(self):
		"""ICU_LANG2POSTFIX should not be empty."""
		assert len(ICU_LANG2POSTFIX) > 0, "ICU_LANG2POSTFIX should not be empty"

	def test_icu_lang2postfix_list_values_are_strings(self):
		"""All list values in ICU_LANG2POSTFIX should contain strings."""
		for lang, postfixes in ICU_LANG2POSTFIX.items():
			for postfix in postfixes:
				assert isinstance(postfix, str), f"Non-string postfix {postfix!r} found for {lang}"


class TestFull2ISO2Full:
	"""Tests for FULL2ISO and ISO2FULLmapping."""

	def test_full2iso2full_structure(self):
		"""FULL2ISO should be a dict mapping strings to strings."""
		for d in [FULL2ISO, ISO2FULL]:
			assert isinstance(d, dict), "FULL2ISO/ISO2FULL should be dicts"
			for key in d.keys():
				assert isinstance(key, str), f"FULL2ISO/ISO2FULL key {key!r} should be str"
			for value in d.values():
				assert isinstance(value, str), f"FULL2ISO/ISO2FULL value {value!r} should be str"

	def test_full2iso2full_not_empty(self):
		"""FULL2ISO should not be empty."""
		assert len(FULL2ISO) > 0, "FULL2ISO should not be empty"
		assert len(ISO2FULL) > 0, "ISO2FULL should not be empty"

	def test_full2iso_lowercase_nonspace_keys(self):
		"""All keys in FULL2ISO should be lowercase and have underscores instead of spaces."""
		for key in FULL2ISO.keys():
			assert key == key.lower(), f"FULL2ISO key {key!r} should be lowercase"
			assert " " not in key, f"FULL2ISO key {key!r} should not contain spaces"
	
	def test_iso2full_capitalized_values(self):
		"""All values in ISO2FULL should be capitalized."""
		all_values = [list(filter(None, re.split(r"[\s\-()']+", v))) for v in ISO2FULL.values()]
		for all_v in all_values:
			for part in all_v:
				assert part == part.capitalize(), f"ISO2FULL value part {part!r} should be capitalized"

	def test_iso_length(self):
		"""All ISO codes in FULL2ISO should be 2 or 3 characters long."""
		for items in [FULL2ISO.values(), ISO2FULL.keys()]:
			for iso_code in items:
				assert len(iso_code.split('_')[0]) in {2, 3}, f"ISO code '{iso_code.split('_')[0]}' is not 2 or 3 characters long."

	def test_iso_postfix_uppercase(self):
		"""All ISO code postfixes in FULL2ISO should be uppercase if present."""
		for items in [FULL2ISO.values(), ISO2FULL.keys()]:
			for iso_code in items:
				if "_" in iso_code:
					_, postfix = iso_code.split('_', 1)
					if not postfix.isnumeric():  # Allow numeric postfixes (e.g., 'es_419')
						assert postfix.isupper(), f"ISO code postfix '{postfix}' in '{iso_code}' is not uppercase."

	def test_reverse_mapping_consistency(self):
		"""ISO2FULL and FULL2ISO should be consistent reverse mappings (where applicable)."""
		for iso_code, full_name in ISO2FULL.items():
			normalized_name = full_name.lower().replace(' ', '_')
			if normalized_name in FULL2ISO:
				assert FULL2ISO[normalized_name] == iso_code, \
					f"Inconsistent mapping: ISO2FULL[{iso_code}]={full_name}, but FULL2ISO[{normalized_name}]={FULL2ISO[normalized_name]}"
	
	def test_iso_in_both_mappings(self):
		"""All ISO codes in FULL2ISO should be present in ISO2FULL and vice versa."""
		full2iso_codes = set(FULL2ISO.values())
		iso2full_codes = set(ISO2FULL.keys())
		assert full2iso_codes <= iso2full_codes, f"Some ISO codes in FULL2ISO are missing in ISO2FULL: {full2iso_codes - iso2full_codes}"
		assert iso2full_codes <= full2iso_codes, f"Some ISO codes in ISO2FULL are missing in FULL2ISO: {iso2full_codes - full2iso_codes}"


class TestISO2Wikt:
	"""Tests for ISO2WIKT mapping."""

	def test_iso2wikt_structure(self):
		"""ISO2WIKT should be a dict mapping strings to strings."""
		assert isinstance(ISO2WIKT, dict), "ISO2WIKT should be a dict"
		for key in ISO2WIKT.keys():
			assert isinstance(key, str), f"ISO2WIKT key {key!r} should be str"
		for value in ISO2WIKT.values():
			assert isinstance(value, str), f"ISO2WIKT value {value!r} should be str"

	def test_iso2wikt_not_empty(self):
		"""ISO2WIKT should not be empty."""
		assert len(ISO2WIKT) > 0, "ISO2WIKT should not be empty"

	def test_iso2wikt_2_elements(self):
		"""All Wiktionary file prefixes in ISO2WIKT should contain exactly one dot for splitting into two elements:
			Full language name and ISO code."""
		for wikt_prefix in ISO2WIKT.values():
			assert wikt_prefix.count(".") == 1, f"Wiktionary file prefix '{wikt_prefix}' does not contain exactly one dot."


class TestLanguageSetIntersections:
	"""Tests for relationships between different language sets."""

	def test_enchant_lang_in_iso2full(self):
		"""All ENCHANT_LANG codes should be in ISO2FULL."""
		assert set(ENCHANT2PROVIDER2TAG.keys()) <= set(ISO2FULL.keys()), \
		f"ENCHANT2PROVIDER2TAG keys should be subset of ISO2FULL keys, missing: {set(ENCHANT2PROVIDER2TAG.keys()) - set(ISO2FULL.keys())}"

	def test_spacy_lang_in_iso2full(self):
		"""All SPACY_LANG and LANG2SPACYLANG codes should be in ISO2FULL."""
		assert SPACY_LANG <= set(ISO2FULL.keys()), f"SPACY_LANG should be subset of ISO2FULL keys, missing: {SPACY_LANG - set(ISO2FULL.keys())}"
		assert set(LANG2SPACYLANG.keys()) <= set(ISO2FULL.keys()), f"LANG2SPACYLANG keys should be subset of ISO2FULL keys, missing: {set(LANG2SPACYLANG.keys()) - set(ISO2FULL.keys())}"
	
	def test_non_word_bound_in_iso2full(self):
		"""All NON_WORD_BOUND codes should be in ISO2FULL."""
		assert NON_WORD_BOUND <= set(ISO2FULL.keys()), f"NON_WORD_BOUND should be subset of ISO2FULL keys, missing: {NON_WORD_BOUND - set(ISO2FULL.keys())}"

	def test_icu_in_iso2full(self):
		"""All NON_WORD_BOUND_IN_ICU and ICU_LANG2POSTFIX codes should be in ISO2FULL."""
		assert NON_WORD_BOUND_IN_ICU <= set(ISO2FULL.keys()), f"NON_WORD_BOUND_IN_ICU should be subset of ISO2FULL keys, missing: {NON_WORD_BOUND_IN_ICU - set(ISO2FULL.keys())}"
		assert set(ICU_LANG2POSTFIX.keys()) <= set(ISO2FULL.keys()), f"ICU_LANG2POSTFIX keys should be subset of ISO2FULL keys, missing: {set(ICU_LANG2POSTFIX.keys()) - set(ISO2FULL.keys())}"

	def test_iso2wikt_in_iso2full(self):
		"""All ISO codes in ISO2WIKT should be in ISO2FULL."""
		assert set(ISO2WIKT.keys()) <= set(ISO2FULL.keys()), f"ISO2WIKT keys should be subset of ISO2FULL keys, missing: {set(ISO2WIKT.keys()) - set(ISO2FULL.keys())}"