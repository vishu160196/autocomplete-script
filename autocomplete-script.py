import requests
import argparse
import pandas as pd
import tqdm


def get_ranks_for_letter(lang, n, df):
    ranks = []
    suggestionUrl = 'URL'

    for kw in tqdm.tqdm(df[list(df)[0]]):
        query = kw[:n]
        res = requests.get(suggestionUrl + 'language=' + lang + '&query=' + query).json()

        suggestions = res['responseObject']
        rank = '-'
        for i, s in enumerate(suggestions):
            try:
                if s['displayName'].lower() == kw.lower():
                    rank = i + 1
                    break
            except KeyError:
                print("\nNo display name found for one suggestion in:\nquery: " + query + "\nkeyword: " + kw + "\n")
        ranks.append(rank)

    return ranks


def get_ranks(domain, letters_list, df):
    language = domain

    columns = {}
    for n in letters_list:
        print("\tprocessing for " + str(n) + " letter queries")
        columns[language + '_' + str(n)] = get_ranks_for_letter(language, int(n), df)
        print("\tfinsihed")

    df_domain = pd.DataFrame(columns)
    return df_domain


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='csv file containing keywords')
    parser.add_argument('--letters', help='comma separated list of numbers')
    parser.add_argument('--languages', help='domains to get suggestion - en, nl')

    args = parser.parse_args()
    if not args.file or not args.languages or not args.letters:
        print("One or more arguments missing, use -h to display the required arguments")
        return

    df = pd.read_csv(args.file)
    if len(list(df)) != 1:
        print("Invalid format of keywords file, only one column must be present")
        return

    letters_list = args.letters.split(',')

    try:
        ind = letters_list.index('1')
        print("Autocomplete does not work for 1 letter")
        return
    except ValueError:
        pass

    domains_list = args.languages.split(',')

    for domain in domains_list:
        print("now processing language:" + domain + "\n")
        df = pd.concat((df, get_ranks(domain, letters_list, df)), axis=1)
        print("language " + domain + " finished")

    df.to_csv("./autocomplete-rankings.csv")


if __name__ == "__main__":
    main()
