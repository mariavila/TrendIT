import string

class SubredditProbability:
    def __init__(self):
        self.dic_appearances = {}
        self.dic_probability = {}

    def get_data_appearance(self,data):
        #call data from reddit
        #data = ["a", "b", "a", "c", "a", "a", "b", "a", "c", "a", "a", "b", "a", "c", "a", "a", "b", "a", "c", "a","a", "b", "a", "c", "a","a", "b", "a", "c", "a", "d"]
        for i in data:
            if i in self.dic_appearances.keys():
                self.dic_appearances[i] += 1
            else:
                self.dic_appearances[i] = 1

    def get_probabilities(self,data):
        self.get_data_appearance(data)
        sum = 0.0
        for i in self.dic_appearances.keys():
            sum += self.dic_appearances[i];

        for i in self.dic_appearances.keys():
            self.dic_probability[i] = float(self.dic_appearances[i]) / sum

    def is_outlier(self, subreddit):
        if subreddit in self.dic_appearances.keys():
            if self.dic_probability[subreddit] > 0.05:
                return False    
        return True
