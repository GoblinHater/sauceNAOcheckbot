import requests
from bs4 import BeautifulSoup
from Replies import *

# Below are different test cases I used:-

# img = "https://i0.wp.com/nekyou.mangadex.com/wp-content/uploads/sites/83/2019/08/00202.jpg?fit=713%2C1024&ssl=1"
# img = "https://i.imgur.com/chYG9bU.png"
# pixiv img:
# img = "https://i.pinimg.com/originals/61/2f/63/612f63b9efa09cdf65ae3576ca3504b3.jpg"
# result of interst:
# img = "https://i.redd.it/jw7vzsuu2nq51.jpg"
# saucenao doesnt have result
# img = "https://i.imgur.com/81OEeM8.jpg"


def GetSauce(url,isSubreddit = False):
    search = "https://saucenao.com/search.php"
    try:
        r = requests.post(search, data={'url': url}, timeout=5)
        soup = BeautifulSoup(r.content, 'html.parser')
    # Get all titles that sauceNAO displays
        all_titles = soup.find_all('div', class_='result')
        if all_titles:
            first_title = all_titles[0]
            first_match = first_title.find('div', class_='resultcontent')
            # print(first_match)
            # If there are no resuls
            if first_match is None:
                if not isSubreddit:
                    replyNeg = Negative_reply + footer
                    return replyNeg
                else:
                    print("No results found")
                    return ""

            title = first_match.find('div', class_='resulttitle')
            titletp = str(title.get_text(separator=" ").strip())
            titletp.replace("  ", " ")
            titletp += "\n\n"
            # print("titletp: "+titletp)

            content = first_match.find('div', class_='resultcontentcolumn')
            fullcontnt = content.get_text(separator=" ").strip()
            # print("full contnt: ", end="")
            fullcontnt.replace("  ", " ")
            fullcontnt += "\n\n"
            # print(fullcontnt)

            similar = soup.find('div', class_="resultsimilarityinfo")
    # Now 60% requirement for mentions is also 60%
            similarity_i = float(similar.text[0:-1])
            if similarity_i < 60 and isSubreddit:
                print("Similarity of the result was less than 60")
                return ""

            print("similarity of first result:", similarity_i)

            saucelink = ""
            # Loop through all the results
            for post in all_titles:
                subpost_similarity = post.find('div', class_='resultsimilarityinfo')
                if subpost_similarity:
                    subpost_similarity = float(subpost_similarity.text[0:-1])
                    # Quality check for 2nd result onwards
                    if subpost_similarity > 65 and abs(subpost_similarity - similarity_i) < 25:
                        # print(subpost_similarity)
                        content_check = post.find('div', class_='resultcontentcolumn')
                        if content_check is not None:
                            if "pixiv" in content_check.text.lower() or "da" in content_check.text.lower() or "seiga" in content_check.text.lower() or "nijie" in content_check.text.lower():
                                if content_check.find('a'):
                                    for link in content_check.find_all('a'):
                                        print(link.get('href'))
                                        saucelink = link.get('href')
                                        break
                        if saucelink != "":
                            similarity_i = subpost_similarity
                            break

                        misc_check = post.find('div', class_='resultmiscinfo')
                        # For GelBooru/DanBooru etc. type of links
                        if misc_check is not None:
                            if misc_check.find('a'):
                                for link in misc_check.find_all('a'):
                                    print(link.get('href'))
                                    saucelink = link.get('href')
                                    break

                        if saucelink != "":
                            similarity_i = subpost_similarity
                            break

            print("sauce: " + str(saucelink))
            if len(saucelink) > 0 and float(similarity_i) > 65:
                replyPos = "**Sauce:** " + titletp + "[Sauce link]" + "(" + saucelink + ")\n\n" + "Similarity = " + str(similarity_i) + "\n\n" + footer
                return replyPos
            elif len(saucelink) == 0 and float(similarity_i) > 65 and isSubreddit:
                replyPos = "**Sauce:** " + titletp + fullcontnt + "Similarity = " + str(similarity_i) + "\n\n" + footer
                return replyPos
            elif not isSubreddit:
                replyPos = "**Sauce:** " + titletp + fullcontnt + "Similarity = " + str(similarity_i) + "\n\n" + footer
                return replyPos
            return ""
        else:
            if not isSubreddit:
                replyNeg = Wrong_file + footer
                return replyNeg
            else:
                print("No result")
                return ""
    except Exception as e:
        print(e)
