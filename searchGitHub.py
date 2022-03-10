from github import Github
from github import RateLimitExceededException
import calendar
import logging
import time
g = Github('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')
Github.AccessToken = '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'


def searchgithub():
    count = 0
    logger = logging
    keyword = "bpmn"
    issues = g.search_code(query=keyword)
    while True:
        try:
            for pr in issues:
                with open('approvedlicense.txt', 'a') as file:
                    try:
                        print(count)
                        file.write("https://github.com/" + pr.repository.full_name + "/blob/master/" + pr.path + "\n")
                    except:
                        print("Whoops")
            count += 1
            logger.info(count)
        except StopIteration:
            break  # loop end
        except RateLimitExceededException:
            search_rate_limit = g.get_rate_limit().search
            logger.info('search remaining: {}'.format(search_rate_limit.remaining))
            reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 10
            print(sleep_time)
            time.sleep(sleep_time)
            continue


searchgithub()

