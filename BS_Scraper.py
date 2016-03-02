import urllib2
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import csv
import httplib
import requests_cache
import time

linkSet = ['http://gsa.gov']
outputFile= open('scraperOutput.csv', 'w+')
output_writer=csv.writer(outputFile, lineterminator='\n')
output_writer.writerow(['url'])
requests_cache.install_cache('test_cache', backend='sqlite')


def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimited(2)
def crawlPages(linkSet):
    for link in linkSet:
        request = rq.get(link, verify = False)
        try:
            response = request.text
            soup = BeautifulSoup(response)
            for a in soup.findAll('a'):
                try:
                    if '.gov' in a['href'] and not a['href'].startswith('/'):
                        if a['href'] not in linkSet:
                            if not str(a['href']).startswith("mailto"):
                                linkSet.append(a['href'])
                                outputLink = str(a['href'])
                                output_writer.writerow([outputLink])
                            else:
                                continue
                except KeyError:
                    continue
        except requests.exceptions.ConnectionError as e:
            continue
        except requests.exceptions.MissingSchema, e:
            continue
        except urllib2.HTTPError, e:
            continue
        except urllib2.URLError, e:
            continue
        except ValueError:
            continue
        except httplib.BadStatusLine, e:
            continue

if __name__ == "__main__":
    crawlPages(linkSet)
