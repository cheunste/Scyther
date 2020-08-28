import re
import logging
import sys
import argparse
from datetime import datetime


def get_variable_name(varexp_line):
	regex = r"(?<=\d)\,(.*?)\,\,"
	matches = re.search(regex,varexp_line)
	tag_name = matches.group(1).replace(',','.')
	return tag_name


def create_varexp_dictionary(varexp_file):
	with open(varexp_file) as f:
		new_dict = {get_variable_name(line):line for line in f}
	sorted_dict = dict(sorted(new_dict.items(), key=lambda item: item[0]))
	return sorted_dict


def get_extraction_tags(user_tag_regex, varexp_dictionary):
	logging.debug(f"Finding all tags with regex {user_tag_regex}")
	list_of_keys = varexp_dictionary.keys()
	extracted_keys = [key for key in list_of_keys if re.search(user_tag_regex,key)]
	return extracted_keys


def separate_tags_from_varexp(removal_tags,varexp_dict):
	time_now = datetime.now().strftime("%Y%m%d-%H%M%S")
	get_site_prefix = removal_tags[0][:5]
	with open(f"{get_site_prefix}-Varexp-{time_now}.txt",'w') as varexp_file, \
			open(f"{get_site_prefix}-Extracted-Tags{time_now}.txt",'w') as separated_tags:
		for tag_name,varexp_line in varexp_dict.items():
			if tag_name in removal_tags:
				logging.debug(f"Removing {tag_name} from varexp")
				separated_tags.write(varexp_line)
			else:
				varexp_file.write(varexp_line)


def main():
	parser = argparse.ArgumentParser(description="This script extracts a PcVue tag from a varexp file given a regex")
	parser.add_argument("-filePath",default="./Varexp.txt", metavar="fp", type=str,
	                    help="The file path to the varexp file. Can be on a remote UCC")
	parser.add_argument("-regex", help="The regex of the varexp tag you want to filter out")
	args = parser.parse_args()

	user_regex = args.regex
	varexp_file_path = args.filePath
	print(f"user regex {user_regex}")
	print(f"varexp path {varexp_file_path}")
	logging.debug(f"Using the varexp in path {varexp_file_path}")
	logging.debug(f"User regex: {user_regex}")

	varexp_dictionary = create_varexp_dictionary(varexp_file_path)
	tags_to_extract = get_extraction_tags(user_regex,varexp_dictionary)
	separate_tags_from_varexp(tags_to_extract,varexp_dictionary)


if __name__ == "__main__":
	main()
