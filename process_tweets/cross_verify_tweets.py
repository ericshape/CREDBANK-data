# created by Ji Wang ericshape @ 4/5/16 11:47 AM

import numpy as np
import json
import sys
import re

idRegEx = re.compile(r".*ID=")
endElRegEx = re.compile(r"'.*")

ratingsFile = "cred_event_TurkRatings.data"
tweetsFile = "cred_event_SearchTweets.data"
merge_outputFile = "merge_timeline.output"

inputFile = "cred_event_SearchTweets.data"
topic_outputFile = "topic_timeline.output"

class Cross_Verify_Tweets():
    def __init__(self):
        pass


    def topic_timeline(self):
        output = open(outputFile, "w")

        with open(inputFile, "r") as f:
            header = f.next()

            for line in f:
                topicData = line.split("\t")

                topicKey = topicData[0]
                topicTerms = topicData[1]
                topicTweetCount = topicData[2]
                tweetIdList = topicData[3]

                print topicKey

                realTweetIds = []

                # Need to read: [('ID=522759240817971202', 'AUTHOR=i_Celeb_Gossips', 'CreatedAt=2014-10-16 14:41:30'),...]
                idElements = tweetIdList.split("),")
                for element in idElements:
                    elArr = element.split(",")
                    idEl = filter(lambda x: "ID" in x, elArr)[0]
                    idEl = idRegEx.sub("", idEl)
                    idEl = endElRegEx.sub("", idEl)

                    realTweetIds.append(long(idEl))

                realTweetIds = list(set(realTweetIds))

                topicMap = {
                    "key": topicKey,
                    "terms": topicTerms.split(","),
                    "count": topicTweetCount,
                    "tweets": realTweetIds
                }

                json.dump(topicMap, output, sort_keys=True)
                output.write("\n")

        output.close()

    def merge_timeline(self):
        tweetsMap = {}
        with open(tweetsFile, "r") as f:

            for line in f:
                tweetData = json.loads(line)
                tweetsMap[tweetData["key"]] = tweetData

        output = open(outputFile, "w")

        with open(ratingsFile, "r") as f:
            header = f.next()

            for line in f:
                topicData = line.split("\t")

                topicKey = topicData[0]
                topicTerms = topicData[1]
                ratings = topicData[2]
                reasons = topicData[3]

                ratings = map(lambda x: int(x.strip().replace("'", "")),
                              ratings.replace("[", "").replace("]", "").split(","))
                ratings = np.array(ratings)

                tweetsMap[topicKey]["ratings"] = ratings.tolist()
                tweetsMap[topicKey]["mean"] = ratings.mean()

                topicMap = tweetsMap[topicKey]

                print topicMap["key"], topicMap["mean"]

                json.dump(topicMap, output, sort_keys=True)
                output.write("\n")

        output.close()


if __name__ == '__main__':
    cross_verify_tweets = Cross_Verify_Tweets()
