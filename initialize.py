import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tsc_helper.tsc_helper import create_webhook


def main():
	create_webhook(os.environ.get('TABLEAU_TOKEN'), os.environ.get('TABLEAU_EVENT_NAME'))


if __name__ == "__main__":
	main()
