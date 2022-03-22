from github import Github
from github import RateLimitExceededException
import calendar
import logging
import time
import config

g = Github(config.GHAC)
Github.AccessToken = config.GHAC

def searchgithub(x,y):
    z = True
    count = 0
    tc = 0
    logger = logging
    keyword = f"{config.Keyword}  size:{x}..{y}"
    issues = g.search_code(query=keyword)
    totalcount = issues.totalCount
    print(totalcount)
    while z == True:
        try:
            for pr in issues:
                with open('foundfiles.txt', 'a') as file:
                    try:
                        file.write("https://github.com/" + pr.repository.full_name + "/blob/master/" + pr.path + "\n")
                        count += 1
                        tc += 1
                        if tc >= totalcount:
                            search_rate_limit = g.get_rate_limit().search
                            logger.info('search remaining: {}'.format(search_rate_limit.remaining))
                            reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
                            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 10
                            print(f"Sleep Time: + {sleep_time}")
                            time.sleep(sleep_time)
                            z = False
                            break
                    except:
                        print("Whoops")
            logger.info(count)
        except StopIteration:
            break  # loop end
        except RateLimitExceededException:
            search_rate_limit = g.get_rate_limit().search
            logger.info('search remaining: {}'.format(search_rate_limit.remaining))
            reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 10
            print(f"Sleep Time: + {sleep_time}")
            time.sleep(sleep_time)
            continue
            
intervall = config.intervall
smallestfilesize = config.smallestfilesize
largestfilesize = config.largestfilesize
n = smallestfilesize + intervall

while smallestfilesize <= largestfilesize:
    print(str(smallestfilesize) + " bis " + str(n))
    searchgithub(smallestfilesize, n)
    smallestfilesize= smallestfilesize + intervall
    n = n + intervall

