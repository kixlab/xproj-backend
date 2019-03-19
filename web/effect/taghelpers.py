from effect.models import Effect
from taggit.models import Tag
from json import JSONEncoder

class TagTreeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, TagNode):
            return o.__dict__
        elif isinstance(o, TagTree):
            return self.default(TagTree.root)
        elif isinstance(o, list):
            return JSONEncoder.default(self, [self.default(p) for p in o])
        else:
            return JSONEncoder.default(self, o)

class TagNode:
    tag = ''
    pos_count = 0
    neg_count = 0
    total_count = 0
    children = []
    def __repr__(self):
        return self.tag

    def __init__(self, tag, pos_count = 0, neg_count = 0):
        self.tag = tag
        self.pos_count = pos_count
        self.neg_count = neg_count
        self.total_count = pos_count + neg_count
        self.children = []
        self.pc = 0

    def add_child(self, node):
        if node.tag not in [t.tag for t in self.children]:
            self.children.append(node)

    def add_child_name(self, name, pos_count, neg_count):
        if name not in [t.tag for t in self.children]:
            self.children.append(TagNode(name, pos_count, neg_count))


    def remove_child(self, tag):
        targetIdx = None
        for idx, node in enumerate(self.children):
            if node.tag == tag:
                targetIdx = idx
                break
        if targetIdx is not None:
            self.children.pop(targetIdx)
        
class TagTree:
    root = None
    included_tags = []
    cooccur = None

    def __init__(self):
        self.root = TagNode('root')
        self.included_tags = []
        self.cooccur = None

    def isEmpty(self):
        return len(self.included_tags) <= 0

    def construct_tag_tree(self, tag_list, policy):
        sorted_tags = sorted(tag_list, key = lambda x: x[1], reverse = True)
        tag_txt = [t[0] for t in sorted_tags]
        self.cooccur = TagCoOccur(tag_txt, policy)

        for i in range(len(sorted_tags)):
            level1_node = TagNode(sorted_tags[i][0], sorted_tags[i][2], sorted_tags[i][3])

            for j in range(len(sorted_tags)):
                if self.cooccur[i][j][0] + self.cooccur.cooccur[i][j][1] > 0:
                    level1_node.add_child_name(sorted_tags[j][0], self.cooccur.cooccur[i][j][0], self.cooccur.cooccur[i][j][1])

            self.root.add_child(level1_node)

    # def compute_cooccur(self, taglist, policy):
    #     if self.cooccur is not None:
    #         return

    #     self.cooccur = [[[0,0] for t in taglist] for t in taglist]

    #     queryset = Effect.objects.filter(is_guess = False).filter(policy = policy)

    #     for e in queryset:
    #         tags = e.tags.names()
    #         for i in range(len(tags)):
    #             for j in range(i):
    #                 t1_idx = taglist.index(tags[i])
    #                 t2_idx = taglist.index(tags[j])

    #                 if e.isBenefit:
    #                     self.cooccur[t1_idx][t2_idx][0] += 1
    #                     self.cooccur[t2_idx][t1_idx][0] += 1
    #                 else:
    #                     self.cooccur[t1_idx][t2_idx][1] += 1
    #                     self.cooccur[t2_idx][t1_idx][1] += 1

class TagCoOccur:
    cooccur = None
    taglist = None
    tag_txt = None
    policy = None

    def __init__(self, taglist, policy):
        self.taglist = sorted(taglist, key = lambda x: x[1], reverse = True)
        self.tag_txt = [t[0] for t in self.taglist]

        self.policy = policy

        self.cooccur = [[[0, 0, 0] for t in taglist] for u in taglist]

        queryset = Effect.objects.filter(is_guess = False).filter(policy = policy)

        for e in queryset:
            tags = e.tags.names()
            for i in range(len(tags)):
                for j in range(i):
                    t1_idx = self.tag_txt.index(tags[i])
                    t2_idx = self.tag_txt.index(tags[j])

                    if e.isBenefit:
                        self.cooccur[t1_idx][t2_idx][1] += 1
                        self.cooccur[t2_idx][t1_idx][1] += 1
                    else:
                        self.cooccur[t1_idx][t2_idx][2] += 1
                        self.cooccur[t2_idx][t1_idx][2] += 1

                    
        for i in range(len(taglist)):
            for j in range(i):
                self.cooccur[i][j][0] = self.cooccur[i][j][1] + self.cooccur[i][j][2]
                self.cooccur[j][i][0] = self.cooccur[i][j][0]

    def closest(self, tag): # fetch the tag with highest co-occurence
        tagidx = self.tag_txt.index(tag)

        target = (0, 0, 0) # target tag index, co-occurence, total count

        for i in range(len(self.taglist)):
            if self.cooccur[tagidx][i][0] > target[1]: # larger co-occurence 
                target = (i, self.cooccur[tagidx][i][0], self.taglist[i][1])
            elif (self.cooccur[tagidx][i][0] == target[1]) and (self.taglist[i][1] > target[2]): # equal co-occur but larger group
                target = (i, self.cooccur[tagidx][i][0], self.taglist[i][1])
        
        return self.tag_txt[target[0]]

    def farthest(self, tag): # fetch the tag with the most different opinion distribution
        tagidx = self.tag_txt.index(tag)
        tag_ratio = self.taglist[tagidx][2] / self.taglist[tagidx][1] * 100 # pos / total
        target = (0, -1, 0) # target tag index, pos/total, total count

        for i in range(len(self.taglist)):
            if (self.taglist[i][1] >= 3) and (abs(tag_ratio - (self.taglist[i][2]/ self.taglist[i][1] * 100)) > target[1]): # total_count > 3 and the largest ratio difference 
                target = (i, abs(tag_ratio - (self.taglist[i][2]/ self.taglist[i][1] * 100)),  self.taglist[i][1])

        return self.tag_txt[target[0]]

    def most_different(self, tag): # fetch the tag with the most different co-occurence distribution
        tagidx = self.tag_txt.index(tag)
        tag_ratio = self.taglist[tagidx][2] / self.taglist[tagidx][1] * 100 # pos / total
        target = (0, -1, 0) # target tag index, co-occured pos/total, total count

        for i in range(len(self.taglist)):

            if (self.taglist[i][1] >= 3) and (self.cooccur[tagidx][i][0] > 0) and (abs(tag_ratio - (self.cooccur[tagidx][i][1]/ self.cooccur[tagidx][i][0] * 100)) > target[1]): # total_count > 3 and the largest ratio difference 
                target = (i, abs(tag_ratio - (self.cooccur[tagidx][i][1]/ self.cooccur[tagidx][i][0] * 100)),  self.taglist[i][1])

        return self.tag_txt[target[0]]

    def most_positive(self, tag): # tag that contributes positive effects the most 
        tagidx = self.tag_txt.index(tag)
        target = (0, 1, 0.5) # tag idx, # of positive effects, ratio of positive effects

        for i in range(len(self.taglist)):
            if self.cooccur[tagidx][i][1] > target[1] and (self.cooccur[tagidx][i][1] / self.cooccur[tagidx][i][0]) >= 0.5:
                target = (i, self.cooccur[tagidx][i][1], (self.cooccur[tagidx][i][1] / self.cooccur[tagidx][i][0]))
            elif self.cooccur[tagidx][i][1] == target[1] and (self.cooccur[tagidx][i][1] / self.cooccur[tagidx][i][0]) > target[2]:
                target = (i, self.cooccur[tagidx][i][1], (self.cooccur[tagidx][i][1] / self.cooccur[tagidx][i][0]))


        return self.tag_txt[target[0]]

    def most_negative(self, tag): # tag that contributes negative effects the most 
        tagidx = self.tag_txt.index(tag)
        target = (0, 1, 0.5) # tag idx, # of negative effects, ratio of negative effects

        for i in range(len(self.taglist)):
            if self.cooccur[tagidx][i][2] > target[1] and (self.cooccur[tagidx][i][2] / self.cooccur[tagidx][i][0]) >= 0.5:
                target = (i, self.cooccur[tagidx][i][2], (self.cooccur[tagidx][i][2] / self.cooccur[tagidx][i][0]))
            elif self.cooccur[tagidx][i][2] == target[1] and (self.cooccur[tagidx][i][2] / self.cooccur[tagidx][i][0]) > target[2]:
                target = (i, self.cooccur[tagidx][i][2], (self.cooccur[tagidx][i][2] / self.cooccur[tagidx][i][0]))

        return self.tag_txt[target[0]]

    def farthest_subgroup(self, tag_high, tag_low):
        tag_high_idx = self.tag_txt.index(tag_high)
        tag_low_idx = self.tag_txt.index(tag_low)
        tag_ratio = self.cooccur[tag_high_idx][tag_low_idx][1] / self.cooccur[tag_high_idx][tag_low_idx][0] * 100 # pos / total
        target = (0, -1, 0) # target tag index, pos/total, total count

        for i in range(len(self.taglist)):
            if self.cooccur[tag_high_idx][i][0] >= 3 and (abs(tag_ratio - (self.cooccur[tag_high_idx][i][1] / self.cooccur[tag_high_idx][i][0] * 100)) > target[1]): # the largest ratio difference 
                target = (i, abs(tag_ratio - (self.cooccur[tag_high_idx][i][1] / self.cooccur[tag_high_idx][i][0] * 100)),  self.cooccur[tag_high_idx][i][0])

        return (tag_high, self.tag_txt[target[0]])

    def farthest_group(self, tag_high, tag_low):
        tag_high_idx = self.tag_txt.index(tag_high)
        tag_low_idx = self.tag_txt.index(tag_low)
        tag_ratio = self.cooccur[tag_high_idx][tag_low_idx][1] / self.cooccur[tag_high_idx][tag_low_idx][0] * 100 # pos / total
        target = (0, -1, 0) # target tag index, pos/total, total count

        for i in range(len(self.taglist)):
            if (self.taglist[i][1] >= 3) and (abs(tag_ratio - (self.taglist[i][2]/ self.taglist[i][1] * 100)) > target[1]): # total_count > 3 and the largest ratio difference 
                target = (i, abs(tag_ratio - (self.taglist[i][2]/ self.taglist[i][1] * 100)),  self.taglist[i][1])

        return (self.tag_txt[target[0]])
        

    # def construct_tag_tree(self, tag_list, policy):
    #     sorted_tags = sorted(tag_list, key = lambda x: x[1], reverse = True)
    #     while len(sorted_tags) > 0:
    #         tags_list = [x[0] for x in sorted_tags]
    #         ele = sorted_tags.pop(0) # pick the most referenced one
    #         queryset_level1 = Effect.objects.filter(tags__name__in=[ele[0]]).filter(is_guess = False)
    #         level1_node = TagNode(ele[0], ele[2], ele[3])
    #         self.included_tags.append(ele[0])
    #         # self.root.add_child(level1_node)

    #         # possible_children = list(queryset_level1.values('tags__name')) # extract possible childs
    #         # possible_children_text = list(set([tag for tag in possible_children['tags__name']]))
    #         # level1_node.pc = possible_children
    #         for t in tags_list:
    #             if t in self.included_tags:
    #                 continue
                
    #             t12 = queryset_level1.filter(tags__name__in=[t])
    #             t12_count = t12.count()
    #             # t12_pos_count = t12.filter(isBenefit = True).count()
    #             # t12_neg_count = t12.filter(isBenefit = False).count()

    #             # if (t12_neg_count + t12_pos_count) > 0:
    #             #     level1_node.add_child_name(t, t12_pos_count, t12_neg_count)
    #             t2 = None
    #             t2idx = None
    #             for idx, tag in enumerate(sorted_tags):
    #                 if tag[0] == t:
    #                     t2idx = idx
    #                     t2 = tag 
    #             if t2 is None:
    #                 continue

    #             t2_count = t2[1]
    #             if t12_count >= 0.85 * t2_count:
    #                 level1_node.add_child_name(t2[0], t2[2], t2[3])
    #                 sorted_tags.pop(t2idx)

    #         self.root.add_child(level1_node)

def decide_inclusion(tag1, tag2):
    queryset = Effect.objects.all()
    tag1_count = queryset.filter(tags__name__in=[tag1]).count()
    tag2_count = queryset.filter(tags__name__in=[tag2]).count()
    tag12_count = queryset.filter(tags__name__in=[tag1, tag2]).count()
