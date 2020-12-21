#!/usr/bin/env python
import sys
import getopt
import requests
import json

version = "v0.2"
github_url = "https://github.com/y-ates/version_fetcher"
repo_list_file = "json_repo_list.json"

def fetch_repo(json_repo_list, needle, tag="name"):
    with open(json_repo_list) as f:
        data = json.load(f)

        if needle in data:
            if tag == "name":
                return str(data[needle]["name"])
            elif tag == "url":
                return str(data[needle]["url"])
        else:
            return 0

        f.close()

def fetch_git(repo, name):
    if repo != 0:
        r = requests.get("https://api.github.com/repos/" + repo + "/releases/latest")
        json_response = json.loads(r.text)
        
        """
        FALLBACK
        There is no "latest release" flag on this repository.
        Trying to get the latest by parsing all releases.
        """
        try:
            if "Not Found" in json_response["message"]:
                r = requests.get("https://api.github.com/repos/" + repo + "/tags")
                json_response = json.loads(r.text)
                return json_response[0]["name"]
            elif "message" in json_response:
                print("[#] Github API message:")
                print("[#] " + json_response["message"])
                print()
        except:
            try:
                return json_response["tag_name"]
            except:
                print("[-] Could not fetch latest release number")
                print("[#] Give it a manual try on: " + fetch_repo(repo_list_file, name, "url"))
                sys.exit()
    else:
        print("[-] Error: Repository is not listed")
        print("[#] Check for typo's or create an issue on Github: " + github_url)
        sys.exit()

def usage():
    print("Version Fetcher " + version + " by Yakup Ates")
    print()
    print("Example Usage:")
    print("[1] " + str(sys.argv[0]) + " -n jquery")
    print("[2] " + str(sys.argv[0]) + " --name jquery")
    
def main(argv):
   try:
       opts, args = getopt.getopt(argv[1:], "hn:", ["help", "name="])
   except getopt.GetoptError as e:
       print(e)
       print(str(sys.argv[0]) + " -n <name_of_software>")
       sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
          usage()
          sys.exit()
      elif opt in ("-n", "--name"):
          toSearch = str(arg).lower()
          repo_name = fetch_repo(repo_list_file, toSearch)
          latest_version = fetch_git(repo_name, toSearch)
          
          print("Latest version of " + str(toSearch) + " is: " + str(latest_version))
          
if __name__ == "__main__":
    main(sys.argv)
